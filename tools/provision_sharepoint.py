#!/usr/bin/env python3
"""
provision_sharepoint.py — Generate PnP PowerShell script to provision
SharePoint lists for APP-MRMS from the CSV schema files.

The CSV files in APP_MRMS/ are the single source of truth for list schemas.
This script parses the ListSchema XML embedded in each CSV and generates:
1. A PnP PowerShell script to create all lists with correct columns
2. A CSV summary of all columns for verification
3. Optional: seed data import commands

Usage:
    python3 tools/provision_sharepoint.py --site-url "https://tenant.sharepoint.com/sites/APP-MRMS"
    python3 tools/provision_sharepoint.py --site-url "https://tenant.sharepoint.com/sites/APP-MRMS" --output provision.ps1
    python3 tools/provision_sharepoint.py --site-url "https://tenant.sharepoint.com/sites/APP-MRMS" --import-data

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
from xml.etree import ElementTree as ET

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

# SharePoint field type mapping
SP_FIELD_TYPES = {
    "Text": "Text",
    "Note": "MultiLineText",
    "Number": "Number",
    "Boolean": "Boolean",
    "DateTime": "DateTime",
    "User": "User",
    "Choice": "Choice",
    "Lookup": "Lookup",
    "Computed": "Computed",
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
        # Extract attributes using regex (simpler than full XML parsing for this format)
        attrs = {}
        for match in re.finditer(r'(\w+)="([^"]*)"', xml_str):
            attrs[match.group(1)] = match.group(2)

        name = attrs.get("Name", "")
        display_name = attrs.get("DisplayName", "")
        field_type = attrs.get("Type", "")
        required = attrs.get("Required", "FALSE").upper() == "TRUE"
        max_length = attrs.get("MaxLength", "")
        rich_text = attrs.get("RichText", "")
        rich_text_mode = attrs.get("RichTextMode", "")
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
            "RichText": rich_text,
            "RichTextMode": rich_text_mode,
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
        "#!" * 20,
        "# APP-MRMS SharePoint Provisioning Script",
        f"# Site URL: {site_url}",
        "# Generated by tools/provision_sharepoint.py",
        "#",
        "# Prerequisites:",
        "#   Install-Module -Name PnP.PowerShell -Scope CurrentUser",
        "#   Connect-PnPOnline -Url '" + site_url + "' -Interactive",
        "#",
        "# Usage:",
        "#   .\\provision_sharepoint.ps1",
        "#",
        "# This script creates all SharePoint lists required by APP-MRMS",
        "# with the correct column schemas from the CSV source-of-truth files.",
        "#",
        "# IMPORTANT: Run lists in order (Directorates first, then Programmes,",
        "# etc.) because some lists have Lookup columns referencing earlier lists.",
        "#" * 20,
        "",
        "# ===========================================================",
        "# Configuration",
        "# ===========================================================",
        f'$SiteUrl = "{site_url}"',
        "",
        "# Verify connection",
        "try {",
        "    $context = Get-PnPContext",
        '    Write-Host "✅ Connected to $SiteUrl" -ForegroundColor Green',
        "} catch {",
        '    Write-Host "❌ Not connected. Run: Connect-PnPOnline -Url $SiteUrl -Interactive" -ForegroundColor Red',
        "    exit 1",
        "}",
        "",
        "# ===========================================================",
        "# Helper function: Create field if it doesn't exist",
        "# ===========================================================",
        "function Add-PnPFieldIfMissing {",
        "    param(",
        "        [string]$ListName,",
        "        [string]$FieldName,",
        "        [string]$DisplayName,",
        "        [string]$Type,",
        "        [bool]$Required = $false,",
        "        [string]$Choices = '',",
        "        [int]$MaxLength = 255,",
        "        [string]$RichText = '',",
        "        [string]$LookupList = '',",
        "        [string]$UserSelectionMode = 'PeopleOnly'",
        "    )",
        "",
        "    try {",
        "        $field = Get-PnPField -List $ListName -Identity $FieldName -ErrorAction Stop",
        '        Write-Host "  ⏭️  Field \'$FieldName\' already exists" -ForegroundColor DarkGray',
        "    } catch {",
        "        try {",
        "            $fieldXml = ''",
        "            switch ($Type) {",
        '                "Text" { $fieldXml = "<Field Type=\'Text\' DisplayName=\'$DisplayName\' Name=\'$FieldName\' Required=\'$(if($Required){\'TRUE\'}else{\'FALSE\'})\' MaxLength=\'$MaxLength\' />" }',
        '                "MultiLineText" { $fieldXml = "<Field Type=\'Note\' DisplayName=\'$DisplayName\' Name=\'$FieldName\' Required=\'$(if($Required){\'TRUE\'}else{\'FALSE\'})\' RichText=\'TRUE\' RichTextMode=\'Compatible\' />" }',
        '                "Number" { $fieldXml = "<Field Type=\'Number\' DisplayName=\'$DisplayName\' Name=\'$FieldName\' Required=\'$(if($Required){\'TRUE\'}else{\'FALSE\'})\' />" }',
        '                "Boolean" { $fieldXml = "<Field Type=\'Boolean\' DisplayName=\'$DisplayName\' Name=\'$FieldName\'><Default>1</Default></Field>" }',
        '                "DateTime" { $fieldXml = "<Field Type=\'DateTime\' DisplayName=\'$DisplayName\' Name=\'$FieldName\' Format=\'DateOnly\' />" }',
        '                "User" { $fieldXml = "<Field Type=\'User\' DisplayName=\'$DisplayName\' Name=\'$FieldName\' UserSelectionMode=\'$UserSelectionMode\' />" }',
        '                "Choice" { $fieldXml = "<Field Type=\'Choice\' DisplayName=\'$DisplayName\' Name=\'$FieldName\' Format=\'Dropdown\'><CHOICES>$Choices</CHOICES></Field>" }',
        '                "Lookup" { $fieldXml = "<Field Type=\'Lookup\' DisplayName=\'$DisplayName\' Name=\'$FieldName\' List=\'$LookupList\' ShowField=\'Title\' />" }',
        "            }",
        "            if ($fieldXml) {",
        "                Add-PnPField -List $ListName -Field $fieldXml",
        '                Write-Host "  ✅ Created field \'$FieldName\' ($Type)" -ForegroundColor Green',
        "            }",
        "        } catch {",
        '            Write-Host "  ❌ Failed to create field \'$FieldName\': $_" -ForegroundColor Red',
        "        }",
        "    }",
        "}",
        "",
        "# ===========================================================",
        "# Helper function: Create list if it doesn't exist",
        "# ===========================================================",
        "function New-PnPListIfMissing {",
        "    param(",
        "        [string]$ListName,",
        "        [string]$Description = ''",
        "    )",
        "",
        "    try {",
        "        $list = Get-PnPList -Identity $ListName -ErrorAction Stop",
        '        Write-Host "⏭️  List \'$ListName\' already exists" -ForegroundColor DarkGray',
        "        return $list",
        "    } catch {",
        "        try {",
        "            New-PnPList -Title $ListName -Template GenericList -EnableVersioning",
        '            Write-Host "✅ Created list \'$ListName\'" -ForegroundColor Green',
        "            return Get-PnPList -Identity $ListName",
        "        } catch {",
        '            Write-Host "❌ Failed to create list \'$ListName\': $_" -ForegroundColor Red',
        "            return $null",
        "        }",
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
        script_lines.append(f'Write-Host "\\n📋 Creating list: {list_name}" -ForegroundColor Cyan')
        script_lines.append(f'$list = New-PnPListIfMissing -ListName "{list_name}"')
        script_lines.append("if ($list) {")

        # Remove default Title field if we're renaming it
        title_field = next((f for f in fields if f["Name"] == "Title"), None)
        if title_field and title_field["DisplayName"] != "Title":
            script_lines.append(f'    # Rename Title field to "{title_field["DisplayName"]}"')
            script_lines.append(f'    Set-PnPField -List "{list_name}" -Identity "Title" -Values {{ Title = "{title_field["DisplayName"]}" }}')

        # Remove default LinkTitle computed field
        script_lines.append('    # Remove default computed fields')
        script_lines.append(f'    try {{ Remove-PnPField -List "{list_name}" -Identity "LinkTitle" -Force -ErrorAction SilentlyContinue }} catch {{}}')
        script_lines.append(f'    try {{ Remove-PnPField -List "{list_name}" -Identity "LinkTitleNoMenu" -Force -ErrorAction SilentlyContinue }} catch {{}}')

        # Add each field
        for field in fields:
            if field["Name"] == "Title" or field["Type"] == "Computed":
                continue  # Skip Title (already handled) and Computed fields

            field_type = SP_FIELD_TYPES.get(field["Type"], "Text")
            required = "TRUE" if field["Required"] else "FALSE"

            # Build choices XML
            choices_xml = ""
            if field["Choices"]:
                choices_xml = "".join(f"<CHOICE>{c}</CHOICE>" for c in field["Choices"])

            # Determine lookup list name
            lookup_list = ""
            if field["Type"] == "Lookup" and field["LookupList"]:
                lookup_list = field["LookupList"]

            # User selection mode
            user_mode = "PeopleOnly"
            if field["UserSelectionMode"] == "0":
                user_mode = "PeopleOnly"
            elif field["UserSelectionMode"] == "1":
                user_mode = "PeopleAndGroups"

            # Generate PowerShell command
            if field_type == "Choice" and field["Choices"]:
                choices_ps = ",".join(field["Choices"])
                script_lines.append(f'    Add-PnPFieldIfMissing -ListName "{list_name}" -FieldName "{field["Name"]}" -DisplayName "{field["DisplayName"]}" -Type "Choice" -Choices "{choices_ps}"')
            elif field_type == "Lookup" and lookup_list:
                script_lines.append(f'    Add-PnPFieldIfMissing -ListName "{list_name}" -FieldName "{field["Name"]}" -DisplayName "{field["DisplayName"]}" -Type "Lookup" -LookupList "{lookup_list}"')
            elif field_type == "User":
                script_lines.append(f'    Add-PnPFieldIfMissing -ListName "{list_name}" -FieldName "{field["Name"]}" -DisplayName "{field["DisplayName"]}" -Type "User" -UserSelectionMode "{user_mode}"')
            elif field_type == "MultiLineText":
                script_lines.append(f'    Add-PnPFieldIfMissing -ListName "{list_name}" -FieldName "{field["Name"]}" -DisplayName "{field["DisplayName"]}" -Type "MultiLineText"')
            else:
                script_lines.append(f'    Add-PnPFieldIfMissing -ListName "{list_name}" -FieldName "{field["Name"]}" -DisplayName "{field["DisplayName"]}" -Type "{field_type}"')

        script_lines.append("}")

        # Add seed data import if requested
        if include_data and data_rows:
            script_lines.append("")
            script_lines.append(f"    # Import {len(data_rows)} seed data rows")
            script_lines.append(f'    $existingItems = Get-PnPListItem -List "{list_name}" -PageSize 100')
            script_lines.append(f'    if ($existingItems.Count -eq 0) {{')
            script_lines.append(f'        Write-Host "  📥 Importing {len(data_rows)} seed rows..." -ForegroundColor Yellow')

            for i, row in enumerate(data_rows[:50]):  # Limit to 50 rows for safety
                # Build item hashtable (only non-empty values)
                items = []
                for key, value in row.items():
                    if value and value.strip() and key not in ("LinkTitle", "LinkTitleNoMenu", "LinkTitle2"):
                        # Escape quotes
                        safe_value = value.replace("'", "''")
                        items.append(f'"{key}" = "{safe_value}"')

                if items:
                    item_dict = "; ".join(items)
                    script_lines.append(f'        Add-PnPListItem -List "{list_name}" -Values @{{{item_dict}}}')

            script_lines.append(f'        Write-Host "  ✅ Imported {len(data_rows)} rows" -ForegroundColor Green')
            script_lines.append(f'    }} else {{')
            script_lines.append(f'        Write-Host "  ⏭️  List already has data, skipping import" -ForegroundColor DarkGray')
            script_lines.append(f'    }}')

    # Add extra lists
    script_lines.append("")
    script_lines.append("# ===========================================================")
    script_lines.append("# Additional Lists (not in CSV schemas)")
    script_lines.append("# ===========================================================")

    for list_name, columns in EXTRA_LISTS.items():
        script_lines.append(f'Write-Host "\\n📋 Creating list: {list_name}" -ForegroundColor Cyan')
        script_lines.append(f'$list = New-PnPListIfMissing -ListName "{list_name}"')
        script_lines.append("if ($list) {")

        for col_name, col_type in columns.items():
            if col_name == "Title":
                continue
            if col_type.startswith("Lookup:"):
                target = col_type.split(":")[1]
                script_lines.append(f'    Add-PnPFieldIfMissing -ListName "{list_name}" -FieldName "{col_name}" -DisplayName "{col_name}" -Type "Lookup" -LookupList "{target}"')
            else:
                script_lines.append(f'    Add-PnPFieldIfMissing -ListName "{list_name}" -FieldName "{col_name}" -DisplayName "{col_name}" -Type "{col_type}"')

        script_lines.append("}")

    # Add completion message
    script_lines.extend([
        "",
        "# ===========================================================",
        "# Completion",
        "# ===========================================================",
        'Write-Host "\\n✅ SharePoint provisioning complete!" -ForegroundColor Green',
        'Write-Host "Lists created:" -ForegroundColor Cyan',
    ])

    for list_name in LIST_ORDER:
        script_lines.append(f'Write-Host "  • {list_name}"')

    for list_name in EXTRA_LISTS:
        script_lines.append(f'Write-Host "  • {list_name}"')

    script_lines.extend([
        "",
        'Write-Host "\\nNext steps:" -ForegroundColor Yellow',
        'Write-Host "  1. Verify all lists appear in Site Contents"',
        'Write-Host "  2. Import seed data: python3 tools/provision_sharepoint.py --site-url <url> --import-data"',
        'Write-Host "  3. Create APP_Users rows with real M365 accounts"',
        'Write-Host "  4. Add SupervisorApproved to MonthlyReports.Status choices"',
        'Write-Host "  5. Import the Power Apps package (APP-MRMS_Project_app_v6.msapp)"',
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

    print(f"✅ Provisioning script generated: {output_path}")
    print(f"   Site URL: {args.site_url}")
    print(f"   CSV source: {csv_dir}")
    print(f"   Include data: {args.import_data}")
    print()
    print("To run:")
    print(f"  1. Connect-PnPOnline -Url '{args.site_url}' -Interactive")
    print(f"  2. .\\{output_path}")


if __name__ == "__main__":
    main()
