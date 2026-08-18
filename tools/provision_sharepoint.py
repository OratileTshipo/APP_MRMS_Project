#!/usr/bin/env python3
"""
provision_sharepoint.py — Generate PnP PowerShell script to provision
SharePoint lists for APP-MRMS from the CSV schema files.

The CSV files in APP_MRMS/ are the single source of truth for list schemas.
This script parses the ListSchema XML embedded in each CSV and generates:
1. A PnP PowerShell script to create all lists with correct columns
2. Adds SupervisorApproved to MonthlyReports.Status (required for 2-stage approval)
3. Handles lookup columns (Projects → Directorates, Activities → Projects)
4. Optional: seed data import commands

Usage:
    python3 tools/provision_sharepoint.py --site-url "https://tenant.sharepoint.com/sites/APP-MRMS"
    python3 tools/provision_sharepoint.py --site-url "https://tenant.sharepoint.com/sites/APP-MRMS" --import-data
    python3 tools/provision_sharepoint.py --site-url "https://tenant.sharepoint.com/sites/APP-MRMS" --summary

Prerequisites:
    Install PnP PowerShell: Install-Module -Name PnP.PowerShell
    Connect: Connect-PnPOnline -Url <site-url> -Interactive
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

# CSV files that define SharePoint lists (order matters for lookups)
LIST_ORDER = [
    "Directorates",
    "Programmes",
    "Projects",
    "Activities",
    "MonthlyReports",
    "APP_Users",
]

# Additional lists needed by the app (not in CSVs)
EXTRA_LISTS = {
    "Notifications": {
        "Title": "Text",
        "RecipientUser": "User",
        "RelatedEntity": "Text",
        "Message": "MultiLineText",
        "IsRead": "Boolean",
        "CreatedDate": "DateTime",
    },
    "AuditLog": {
        "Title": "Text",
        "EntityType": "Text",
        "EntityId": "Text",
        "Action": "Text",
        "ActionBy": "User",
        "ActionDate": "DateTime",
        "Reason": "MultiLineText",
    },
    "ReportComments": {
        "Title": "Text",
        "Report": "Lookup:MonthlyReports",
        "Comment": "MultiLineText",
        "CommentBy": "User",
        "CommentDate": "DateTime",
    },
    "KPIDefinitions": {
        "Title": "Text",
        "KPIName": "Text",
        "Description": "MultiLineText",
        "TargetValue": "Number",
        "Formula": "MultiLineText",
    },
}

# Critical choices that must be added after list creation
CRITICAL_CHOICES = {
    "MonthlyReports": {
        "Status": [
            "Draft",
            "Submitted",
            "SupervisorApproved",  # Required for 2-stage approval flow
            "Approved",
            "Rejected",
            "Escalated",
        ],
    },
}

# CSV data files for seed import
CSV_DATA_FILES = {
    "Directorates": "Directorates.csv",
    "Programmes": "Programmes.csv",
    "Projects": "Projects.csv",
    "Activities": "Activities.csv",
    "MonthlyReports": "MonthlyReports.csv",
    "APP_Users": "APP_Users.csv",
}


def parse_csv_schema(csv_path):
    """Parse a CSV file and extract list schema from ListSchema XML."""
    with open(csv_path, encoding="utf-8-sig") as f:
        content = f.read()

    lines = content.split("\n")
    if not lines or "ListSchema=" not in lines[0]:
        return None, None

    # Parse ListSchema JSON
    schema_json = lines[0].replace("ListSchema=", "")
    try:
        schema = json.loads(schema_json)
    except json.JSONDecodeError:
        return None, None

    xml_list = schema.get("schemaXmlList", [])

    # Parse each field XML
    fields = []
    for xml_field in xml_list:
        field = parse_field_xml(xml_field)
        if field:
            fields.append(field)

    # Parse data rows (skip header which is the ListSchema line)
    data_rows = []
    if len(lines) > 1:
        reader = csv.reader(lines[1:])
        headers = next(reader, None)
        if headers:
            for row in reader:
                if row and any(cell.strip() for cell in row):
                    data_rows.append(dict(zip(headers, row)))

    return fields, data_rows


def parse_field_xml(xml_str):
    """Parse a SharePoint field XML string into a field definition."""
    try:
        # Extract attributes using regex
        attrs = {}
        for match in re.finditer(r'(\w+)="([^"]*)"', xml_str):
            attrs[match.group(1)] = match.group(2)

        name = attrs.get("Name", "")
        display_name = attrs.get("DisplayName", "")
        field_type = attrs.get("Type", "")
        required = attrs.get("Required", "FALSE").upper() == "TRUE"
        max_length = attrs.get("MaxLength", "")
        format_type = attrs.get("Format", "")

        # Extract choices
        choices = []
        choices_match = re.search(r"<CHOICES>(.*?)</CHOICES>", xml_str, re.DOTALL)
        if choices_match:
            choices = re.findall(r"<CHOICE>(.*?)</CHOICE>", choices_match.group(1))

        # Extract default value
        default_match = re.search(r"<Default>(.*?)</Default>", xml_str)
        default_value = default_match.group(1) if default_match else None

        # Extract lookup list
        lookup_list = attrs.get("List", "")

        # Extract user selection mode
        user_selection_mode = attrs.get("UserSelectionMode", "")

        return {
            "Name": name,
            "DisplayName": display_name or name,
            "Type": field_type,
            "Required": required,
            "MaxLength": max_length,
            "Format": format_type,
            "Choices": choices,
            "DefaultValue": default_value,
            "LookupList": lookup_list,
            "UserSelectionMode": user_selection_mode,
        }
    except Exception as e:
        print(f"  Warning: Could not parse field XML: {e}")
        return None


def generate_pnp_script(site_url, csv_dir, include_data=False):
    """Generate PnP PowerShell script for SharePoint provisioning."""
    script_lines = [
        "#" * 80,
        "# APP-MRMS SharePoint Provisioning Script",
        f"# Site URL: {site_url}",
        "# Generated by tools/provision_sharepoint.py",
        "#",
        "# Prerequisites:",
        "#   Install-Module -Name PnP.PowerShell -Scope CurrentUser",
        f"#   Connect-PnPOnline -Url '{site_url}' -Interactive",
        "#",
        "# Usage:",
        "#   .\\provision_sharepoint.ps1",
        "#",
        "# This script creates all SharePoint lists required by APP-MRMS",
        "# with the correct column schemas from the CSV source-of-truth files.",
        "#",
        "# CRITICAL: MonthlyReports.Status includes 'SupervisorApproved' for",
        "# the 2-stage approval workflow (Flow 2).",
        "#" * 80,
        "",
        "# ===========================================================",
        "# Configuration",
        "# ===========================================================",
        f'$SiteUrl = "{site_url}"',
        "",
        "# Verify connection",
        "try {",
        "    $context = Get-PnPContext",
        '    Write-Host "Connected to $SiteUrl" -ForegroundColor Green',
        "} catch {",
        '    Write-Host "Not connected. Run: Connect-PnPOnline -Url $SiteUrl -Interactive" -ForegroundColor Red',
        "    exit 1",
        "}",
        "",
        "# ===========================================================",
        "# Helper: Create field if it doesn't exist",
        "# ===========================================================",
        "function Add-FieldIfMissing {",
        "    param(",
        "        [string]$ListName,",
        "        [string]$FieldName,",
        "        [string]$DisplayName,",
        "        [string]$Type,",
        "        [bool]$Required = $false,",
        "        [string]$Choices = '',",
        "        [string]$LookupList = '',",
        "        [string]$UserSelectionMode = 'PeopleOnly'",
        "    )",
        "",
        "    try {",
        "        $field = Get-PnPField -List $ListName -Identity $FieldName -ErrorAction Stop",
        '        Write-Host "  [SKIP] $FieldName already exists" -ForegroundColor DarkGray',
        "        return",
        "    } catch {",
        "        # Field doesn't exist, create it",
        "    }",
        "",
        "    try {",
        "        $xml = ''",
        "        $req = if($Required){'TRUE'}else{'FALSE'}",
        "",
        "        switch ($Type) {",
        '            \'Text\'          { $xml = \'<Field Type="Text" DisplayName="\'+$DisplayName+\'" Name="\'+$FieldName+\'" Required="\'+$req+\'" MaxLength="255" />\' }',
        '            \'MultiLineText\' { $xml = \'<Field Type="Note" DisplayName="\'+$DisplayName+\'" Name="\'+$FieldName+\'" Required="\'+$req+\'" RichText="TRUE" RichTextMode="Compatible" />\' }',
        '            \'Number\'        { $xml = \'<Field Type="Number" DisplayName="\'+$DisplayName+\'" Name="\'+$FieldName+\'" Required="\'+$req+\'" />\' }',
        '            \'Boolean\'       { $xml = \'<Field Type="Boolean" DisplayName="\'+$DisplayName+\'" Name="\'+$FieldName+\'"><Default>1</Default></Field>\' }',
        '            \'DateTime\'      { $xml = \'<Field Type="DateTime" DisplayName="\'+$DisplayName+\'" Name="\'+$FieldName+\'" Format="DateOnly" />\' }',
        '            \'User\'          { $xml = \'<Field Type="User" DisplayName="\'+$DisplayName+\'" Name="\'+$FieldName+\'" UserSelectionMode="\'+$UserSelectionMode+\'" />\' }',
        '            \'Choice\'        { $xml = \'<Field Type="Choice" DisplayName="\'+$DisplayName+\'" Name="\'+$FieldName+\'" Format="Dropdown"><CHOICES>\'+$Choices+\'</CHOICES></Field>\' }',
        '            \'Lookup\'        { $xml = \'<Field Type="Lookup" DisplayName="\'+$DisplayName+\'" Name="\'+$FieldName+\'" List="\'+$LookupList+\'" ShowField="Title" />\' }',
        "        }",
        "",
        "        if ($xml) {",
        "            Add-PnPField -List $ListName -Field $xml",
        '            Write-Host "  [OK] $FieldName ($Type)" -ForegroundColor Green',
        "        }",
        "    } catch {",
        '        Write-Host "  [FAIL] $FieldName : $_" -ForegroundColor Red',
        "    }",
        "}",
        "",
        "# ===========================================================",
        "# Helper: Create list if it doesn't exist",
        "# ===========================================================",
        "function New-ListIfMissing {",
        "    param(",
        "        [string]$ListName",
        "    )",
        "",
        "    try {",
        "        $list = Get-PnPList -Identity $ListName -ErrorAction Stop",
        '        Write-Host "[SKIP] $ListName already exists" -ForegroundColor DarkGray',
        "        return $list",
        "    } catch {",
        "        # List doesn't exist, create it",
        "    }",
        "",
        "    try {",
        "        New-PnPList -Title $ListName -Template GenericList -EnableVersioning",
        '        Write-Host "[OK] Created $ListName" -ForegroundColor Green',
        "        return Get-PnPList -Identity $ListName",
        "    } catch {",
        '        Write-Host "[FAIL] $ListName : $_" -ForegroundColor Red',
        "        return $null",
        "    }",
        "}",
        "",
    ]

    # Process each CSV schema
    for list_name in LIST_ORDER:
        csv_file = CSV_DATA_FILES.get(list_name)
        if not csv_file:
            continue

        csv_path = os.path.join(csv_dir, csv_file)
        if not os.path.exists(csv_path):
            print(f"  Warning: {csv_path} not found, skipping {list_name}")
            continue

        fields, data_rows = parse_csv_schema(csv_path)
        if not fields:
            print(f"  Warning: No schema found in {csv_file}")
            continue

        script_lines.append("")
        script_lines.append("# ===========================================================")
        script_lines.append(f"# {list_name}")
        script_lines.append("# ===========================================================")
        script_lines.append(f'Write-Host "`n--- {list_name} ---" -ForegroundColor Cyan')
        script_lines.append(f'$list = New-ListIfMissing -ListName "{list_name}"')
        script_lines.append("if ($list) {")

        # Rename Title field if needed
        title_field = next((f for f in fields if f["Name"] == "Title"), None)
        if title_field and title_field["DisplayName"] != "Title":
            script_lines.append(f'    # Rename Title to "{title_field["DisplayName"]}"')
            script_lines.append(f'    Set-PnPField -List "{list_name}" -Identity "Title" -Values {{ Title = "{title_field["DisplayName"]}" }}')

        # Add each field
        for field in fields:
            if field["Name"] == "Title" or field["Type"] == "Computed":
                continue

            field_type = field["Type"]
            if field_type == "Note":
                field_type = "MultiLineText"

            # Build choices string
            choices_str = ",".join(field["Choices"]) if field["Choices"] else ""

            # Handle lookup columns
            if field["Type"] == "Lookup" and field["LookupList"]:
                script_lines.append(f'    Add-FieldIfMissing -ListName "{list_name}" -FieldName "{field["Name"]}" -DisplayName "{field["DisplayName"]}" -Type "Lookup" -LookupList "{field["LookupList"]}"')
            elif field_type == "Choice" and field["Choices"]:
                script_lines.append(f'    Add-FieldIfMissing -ListName "{list_name}" -FieldName "{field["Name"]}" -DisplayName "{field["DisplayName"]}" -Type "Choice" -Choices "{choices_str}"')
            elif field_type == "User":
                script_lines.append(f'    Add-FieldIfMissing -ListName "{list_name}" -FieldName "{field["Name"]}" -DisplayName "{field["DisplayName"]}" -Type "User"')
            else:
                script_lines.append(f'    Add-FieldIfMissing -ListName "{list_name}" -FieldName "{field["Name"]}" -DisplayName "{field["DisplayName"]}" -Type "{field_type}"')

        script_lines.append("}")

        # Add critical choices after list creation
        if list_name in CRITICAL_CHOICES:
            for field_name, choices in CRITICAL_CHOICES[list_name].items():
                choices_str = ",".join(choices)
                script_lines.append("")
                script_lines.append(f'    # CRITICAL: Add SupervisorApproved to {field_name} choices')
                script_lines.append(f'    Write-Host "  Adding SupervisorApproved to {field_name}..." -ForegroundColor Yellow')
                script_lines.append(f'    $field = Get-PnPField -List "{list_name}" -Identity "{field_name}"')
                script_lines.append(f'    $choices = $field.Choices')
                script_lines.append(f'    if ($choices -notcontains "SupervisorApproved") {{')
                script_lines.append(f'        $newChoices = $choices + "SupervisorApproved"')
                script_lines.append(f'        Set-PnPField -List "{list_name}" -Identity "{field_name}" -Values @{{ Choices = $newChoices }}')
                script_lines.append(f'        Write-Host "  [OK] Added SupervisorApproved" -ForegroundColor Green')
                script_lines.append(f'    }} else {{')
                script_lines.append(f'        Write-Host "  [SKIP] SupervisorApproved already exists" -ForegroundColor DarkGray')
                script_lines.append(f'    }}')

        # Add seed data import if requested
        if include_data and data_rows:
            script_lines.append("")
            script_lines.append(f"    # Import {len(data_rows)} seed data rows")
            script_lines.append(f'    $existingItems = Get-PnPListItem -List "{list_name}" -PageSize 100')
            script_lines.append(f'    if ($existingItems.Count -eq 0) {{')
            script_lines.append(f'        Write-Host "  Importing {len(data_rows)} rows..." -ForegroundColor Yellow')

            for row in data_rows[:50]:  # Limit for safety
                items = []
                for key, value in row.items():
                    if value and value.strip() and key not in ("LinkTitle", "LinkTitleNoMenu", "LinkTitle2"):
                        safe_value = value.replace("'", "''")
                        items.append(f'"{key}" = "{safe_value}"')

                if items:
                    item_dict = "; ".join(items)
                    script_lines.append(f'        Add-PnPListItem -List "{list_name}" -Values @{{{item_dict}}}')

            script_lines.append(f'        Write-Host "  [OK] Imported {len(data_rows)} rows" -ForegroundColor Green')
            script_lines.append(f'    }} else {{')
            script_lines.append(f'        Write-Host "  [SKIP] List has data" -ForegroundColor DarkGray')
            script_lines.append(f'    }}')

    # Add extra lists
    script_lines.append("")
    script_lines.append("# ===========================================================")
    script_lines.append("# Additional Lists (not in CSV schemas)")
    script_lines.append("# ===========================================================")

    for list_name, columns in EXTRA_LISTS.items():
        script_lines.append(f'Write-Host "`n--- {list_name} ---" -ForegroundColor Cyan')
        script_lines.append(f'$list = New-ListIfMissing -ListName "{list_name}"')
        script_lines.append("if ($list) {")

        for col_name, col_type in columns.items():
            if col_name == "Title":
                continue
            if col_type.startswith("Lookup:"):
                target = col_type.split(":")[1]
                script_lines.append(f'    Add-FieldIfMissing -ListName "{list_name}" -FieldName "{col_name}" -DisplayName "{col_name}" -Type "Lookup" -LookupList "{target}"')
            else:
                script_lines.append(f'    Add-FieldIfMissing -ListName "{list_name}" -FieldName "{col_name}" -DisplayName "{col_name}" -Type "{col_type}"')

        script_lines.append("}")

    # Add completion message
    script_lines.extend([
        "",
        "# ===========================================================",
        "# Summary",
        "# ===========================================================",
        'Write-Host "`n=== Provisioning Complete ===" -ForegroundColor Green',
        "",
        'Write-Host "Lists created:" -ForegroundColor Cyan',
    ])

    for list_name in LIST_ORDER:
        script_lines.append(f'Write-Host "  - {list_name}"')

    for list_name in EXTRA_LISTS:
        script_lines.append(f'Write-Host "  - {list_name}"')

    script_lines.extend([
        "",
        'Write-Host "`nCritical configuration:" -ForegroundColor Yellow',
        'Write-Host "  - MonthlyReports.Status includes SupervisorApproved (2-stage approval)"',
        "",
        'Write-Host "Next steps:" -ForegroundColor Yellow',
        'Write-Host "  1. Verify lists in Site Contents"',
        'Write-Host "  2. Seed APP_Users with real M365 accounts (1 per role)"',
        'Write-Host "  3. Import Power Apps: APP-MRMS_Project_app_v6.msapp"',
        'Write-Host "  4. Import Power Automate flows: flows/APP-MRMS-Approval.zip"',
    ])

    return "\n".join(script_lines)


def generate_column_summary(csv_dir):
    """Generate a summary of all columns for verification."""
    summary = []

    for list_name in LIST_ORDER:
        csv_file = CSV_DATA_FILES.get(list_name)
        if not csv_file:
            continue

        csv_path = os.path.join(csv_dir, csv_file)
        if not os.path.exists(csv_path):
            continue

        fields, data_rows = parse_csv_schema(csv_path)
        if not fields:
            continue

        summary.append(f"\n{'='*60}")
        summary.append(f"{list_name} ({len(fields)} fields, {len(data_rows)} data rows)")
        summary.append(f"{'='*60}")

        for field in fields:
            if field["Type"] == "Computed":
                continue
            choices_str = f" [{', '.join(field['Choices'])}]" if field["Choices"] else ""
            required_str = " (required)" if field["Required"] else ""
            summary.append(f"  {field['Name']:30s} {field['Type']:15s} {field['DisplayName']}{choices_str}{required_str}")

    # Add critical choices note
    summary.append(f"\n{'='*60}")
    summary.append("CRITICAL: Choices to add after provisioning")
    summary.append(f"{'='*60}")
    summary.append("  MonthlyReports.Status: Add 'SupervisorApproved' (for 2-stage approval)")

    return "\n".join(summary)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--site-url",
        required=True,
        help="SharePoint site URL, e.g. https://tenant.sharepoint.com/sites/APP-MRMS",
    )
    parser.add_argument(
        "--csv-dir",
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "APP_MRMS"),
        help="Directory containing CSV schema files (default: APP_MRMS/)",
    )
    parser.add_argument(
        "--output",
        default="provision_sharepoint.ps1",
        help="Output PowerShell script file (default: provision_sharepoint.ps1)",
    )
    parser.add_argument(
        "--import-data",
        action="store_true",
        help="Include seed data import commands in the script",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print column summary and exit",
    )
    args = parser.parse_args()

    csv_dir = os.path.abspath(args.csv_dir)

    if args.summary:
        print(generate_column_summary(csv_dir))
        return

    # Generate the provisioning script
    script = generate_pnp_script(args.site_url, csv_dir, args.import_data)

    # Write to file
    output_path = args.output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(script)

    print(f"Provisioning script generated: {output_path}")
    print(f"  Site URL: {args.site_url}")
    print(f"  CSV source: {csv_dir}")
    print(f"  Include data: {args.import_data}")
    print()
    print("To run:")
    print(f"  1. Connect-PnPOnline -Url '{args.site_url}' -Interactive")
    print(f"  2. .\\{output_path}")


if __name__ == "__main__":
    main()
