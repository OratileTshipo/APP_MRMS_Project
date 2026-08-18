#!/usr/bin/env python3
"""
Build the APP-MRMS approval-flow Power Automate import package (.zip).

The flows reference the SharePoint site and five lists via {{TOKEN}} placeholders
in the template files under flows/templates/APP-MRMS-Approval. This script
substitutes your real values and packs the result in the exact layout the
Power Automate import wizard expects.

Usage:
    python3 tools/build_flow_zips.py \
        --site-url "https://yourorg.sharepoint.com/sites/APP-MRMS" \
        --monthlyreports "<MonthlyReports list GUID>" \
        --activities "<Activities list GUID>" \
        --notifications "<Notifications list GUID>" \
        --auditlog "<AuditLog list GUID>" \
        --users "<APP_Users list GUID>" \
        [--output flows/APP-MRMS-Approval.zip]

How to find list GUIDs:
    Open the list in SharePoint, go to List settings, look at the browser URL:
    .../Lists/AllItems.aspx?List=%7B<GUID>%7D
    (the %7B / %7D are literal braces around the GUID). Or run PnP:
    Connect-PnPOnline -Url <site> -Interactive
    Get-PnPList -Identity 'MonthlyReports' | Select Id
"""
import argparse
import json
import sys
import zipfile
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "flows" / "templates" / "APP-MRMS-Approval"

TOKENS = {
    "SITE_URL": None,
    "MR_GUID": None,
    "ACT_GUID": None,
    "NOTIF_GUID": None,
    "AUDIT_GUID": None,
    "USERS_GUID": None,
}

MANIFEST_LAST = ["Microsoft.Flow/flows/manifest.json"]

# Flow folders excluded from the import package. The template source is kept for
# later fixing, but the flow is not part of the shipped manifest (see
# flows/templates/APP-MRMS-Approval/manifest.json).
EXCLUDED_FLOW_DIRS = set()  # All flows now have unique action names and are included


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--site-url", required=True, help="SharePoint site URL, e.g. https://x.sharepoint.com/sites/APP-MRMS")
    p.add_argument("--monthlyreports", required=True, help="GUID of the MonthlyReports list")
    p.add_argument("--activities", required=True, help="GUID of the Activities list")
    p.add_argument("--notifications", required=True, help="GUID of the Notifications list")
    p.add_argument("--auditlog", required=True, help="GUID of the AuditLog list")
    p.add_argument("--users", required=True, help="GUID of the APP_Users list")
    p.add_argument("--output", default=str(Path(__file__).resolve().parent.parent / "flows" / "APP-MRMS-Approval.zip"))
    return p.parse_args()


def substitute(text: str, values: dict) -> str:
    missing = [tok for tok in values if values[tok] is None and ("{{" + tok + "}}") in text]
    if missing:
        raise SystemExit(
            f"Missing token value(s): {', '.join('{{' + t + '}}' for t in missing)}. "
            "Provide all --monthlyreports/--activities/--notifications/--auditlog/--users arguments."
        )
    for tok, val in values.items():
        text = text.replace("{{" + tok + "}}", val)
    return text


def main():
    args = parse_args()
    values = {
        "SITE_URL": args.site_url,
        "MR_GUID": args.monthlyreports,
        "ACT_GUID": args.activities,
        "NOTIF_GUID": args.notifications,
        "AUDIT_GUID": args.auditlog,
        "USERS_GUID": args.users,
    }

    if not TEMPLATE_DIR.is_dir():
        raise SystemExit(f"Template directory not found: {TEMPLATE_DIR}")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    for path in sorted(TEMPLATE_DIR.rglob("*")):
        if path.is_file():
            rel = path.relative_to(TEMPLATE_DIR).as_posix()
            if any(f"/{guid}/" in "/" + rel for guid in EXCLUDED_FLOW_DIRS):
                continue
            entries.append((rel, path))

    # Root manifest must come first in the archive, then the flow content.
    root_manifest = next((p for r, p in entries if r == "manifest.json"), None)
    if root_manifest is None:
        raise SystemExit("Root manifest.json missing in templates")

    def key(item):
        rel, _ = item
        if rel == "manifest.json":
            return (0, rel)
        return (1, rel)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel, path in sorted(entries, key=key):
            content = path.read_text(encoding="utf-8")
            content = substitute(content, values)
            # Validate JSON for all .json members so a bad edit fails here, not at import.
            if rel.endswith(".json"):
                try:
                    json.loads(content)
                except json.JSONDecodeError as e:
                    raise SystemExit(f"Invalid JSON in {rel}: {e}")
            zf.writestr(rel, content)

    print(f"Package written: {out}")
    print("Flows included:")
    with zipfile.ZipFile(out) as zf:
        for name in zf.namelist():
            print("  " + name)


if __name__ == "__main__":
    sys.exit(main())
