#!/usr/bin/env python3
"""
repack_msapp.py — refresh the Src/*.pa.yaml entries inside a .msapp from src/.

Why this exists
---------------
The documented workflow (README §Workflow) uses `pac canvas pack`, but `pac`
is not available in every environment. This script does the equivalent for the
source-only edits this repo makes: it replaces the `Src/*.pa.yaml` entries
embedded in an existing .msapp with the current working-tree files
(src/Src/*.pa.yaml), byte-for-byte, and leaves every other pack entry
(Header.json, References/, Controls/, SARIF, themes, ...) untouched. Power
Apps Studio loads the embedded SourceCode YAML when the msapp is imported, so
keeping these in sync is what makes the import reflect the repo source.

Usage
-----
    python3 tools/repack_msapp.py [--msapp APP-MRMS_Project_app_v5_contributor.msapp]
    python3 tools/repack_msapp.py --msapp APP-MRMS_Project_app_v4_layout-fixed.msapp \
        --out APP-MRMS_Project_app_v6.msapp --appname APP-MRMS_Project_app_v6

--out      Write the repacked msapp to a new path instead of overwriting the
           source pack (used when forking a new app version, e.g. v6).
--appname  Rename the app inside the pack (Properties.json Name + PublishInfo
           AppName) to the given display name.

The AppCheckerResult.sarif entry is always replaced with a clean empty run
(0 findings) so Studio does not surface stale findings from a previous app
version after import.

Exit code 0 = pack updated and in sync, 1 = error.
"""

import argparse
import os
import shutil
import sys
import zipfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MSAPP = os.path.join(REPO_ROOT, "APP-MRMS_Project_app_v5_contributor.msapp")
SRC_DIR = os.path.join(REPO_ROOT, "src", "Src")

# Clean SARIF with zero findings; replaces stale results carried over from an
# earlier app version so the import does not surface phantom errors.
CLEAN_SARIF = (
    '{"$schema": "https://schemastore.azurewebsites.net/schemas/json/'
    'sarif-2.1.0-rtm.4.json", "version": "2.1.0", "runs": []}'
).encode("utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Update the Src/*.pa.yaml entries of a .msapp from src/Src/"
    )
    parser.add_argument(
        "--msapp", default=DEFAULT_MSAPP, help="Path to the .msapp to repack"
    )
    parser.add_argument(
        "--out", default=None, help="Output path; defaults to overwriting --msapp"
    )
    parser.add_argument(
        "--appname", default=None, help="New app display name (updates Properties.json + PublishInfo)"
    )
    args = parser.parse_args()

    msapp = os.path.abspath(args.msapp)
    out = os.path.abspath(args.out) if args.out else msapp
    if not os.path.isfile(msapp):
        print(f"ERROR: msapp not found: {msapp}")
        sys.exit(1)
    if not os.path.isdir(SRC_DIR):
        print(f"ERROR: source directory not found: {SRC_DIR}")
        sys.exit(1)

    sources = {}
    for root, _dirs, files in os.walk(SRC_DIR):
        for f in sorted(files):
            if f.endswith(".pa.yaml"):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, SRC_DIR).replace(os.sep, "/")
                with open(full, "rb") as fh:
                    sources["Src/" + rel] = fh.read()
    if not sources:
        print("ERROR: no *.pa.yaml files found under src/Src/")
        sys.exit(1)

    import base64
    import json

    # App display-name rename (Properties.json Name is base64-encoded).
    renamed = []
    if args.appname:
        appname = args.appname
    else:
        appname = None

    def rewrite(entry, data):
        nonlocal changed
        if entry == "AppCheckerResult.sarif":
            if data != CLEAN_SARIF:
                data = CLEAN_SARIF
                changed += 1
            return data
        if appname and entry == "Properties.json":
            doc = json.loads(data.decode("utf-8"))
            new_name = base64.b64encode(
                (appname + ".msapp").encode("utf-8")
            ).decode("utf-8")
            if doc.get("Name") != new_name:
                doc["Name"] = new_name
                data = json.dumps(doc, indent=4).encode("utf-8")
                changed += 1
                renamed.append("Properties.json")
            return data
        if appname and entry == "Resources/PublishInfo.json":
            doc = json.loads(data.decode("utf-8"))
            if doc.get("AppName") != appname:
                doc["AppName"] = appname
                data = json.dumps(doc, indent=4).encode("utf-8")
                changed += 1
                renamed.append("Resources/PublishInfo.json")
            return data
        return data

    tmp = out + ".tmp"
    changed = 0
    with zipfile.ZipFile(msapp, "r") as zin, zipfile.ZipFile(
        tmp, "w", zipfile.ZIP_DEFLATED
    ) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename in sources:
                new_data = sources[item.filename]
                if data != new_data:
                    data = new_data
                    changed += 1
                del sources[item.filename]
            zout.writestr(item, rewrite(item.filename, data))
        # Any source file not present in the pack is added.
        for name, data in sources.items():
            zout.writestr(name, data)
            changed += 1
            print(f"ADDED {name}")

    if changed == 0:
        os.remove(tmp)
        print("No changes — pack Src entries already match src/Src/.")
    else:
        os.replace(tmp, out)
        print(f"Repacked {os.path.basename(out)}: {changed} entry(ies) updated.")
    for e in renamed:
        print(f"Renamed {e} -> {appname}")

    # Verify: every src/Src/**/*.pa.yaml must now be byte-identical in the pack.
    with zipfile.ZipFile(out, "r") as z:
        ok = True
        for root, _dirs, files in os.walk(SRC_DIR):
            for f in sorted(files):
                if not f.endswith(".pa.yaml"):
                    continue
                full = os.path.join(root, f)
                rel = os.path.relpath(full, SRC_DIR).replace(os.sep, "/")
                entry = "Src/" + rel
                if entry not in z.namelist():
                    print(f"FAIL: {entry} missing from pack")
                    ok = False
                elif open(full, "rb").read() != z.read(entry):
                    print(f"FAIL: {entry} out of sync")
                    ok = False
    if not ok:
        sys.exit(1)
    print("OK: all Src/*.pa.yaml entries are byte-identical to src/Src/.")


if __name__ == "__main__":
    main()
