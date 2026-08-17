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


def main():
    parser = argparse.ArgumentParser(
        description="Update the Src/*.pa.yaml entries of a .msapp from src/Src/"
    )
    parser.add_argument(
        "--msapp", default=DEFAULT_MSAPP, help="Path to the .msapp to repack"
    )
    args = parser.parse_args()

    msapp = os.path.abspath(args.msapp)
    if not os.path.isfile(msapp):
        print(f"ERROR: msapp not found: {msapp}")
        sys.exit(1)
    if not os.path.isdir(SRC_DIR):
        print(f"ERROR: source directory not found: {SRC_DIR}")
        sys.exit(1)

    sources = {}
    for f in sorted(os.listdir(SRC_DIR)):
        if f.endswith(".pa.yaml"):
            with open(os.path.join(SRC_DIR, f), "rb") as fh:
                sources["Src/" + f] = fh.read()
    if not sources:
        print("ERROR: no *.pa.yaml files found under src/Src/")
        sys.exit(1)

    tmp = msapp + ".tmp"
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
            zout.writestr(item, data)
        # Any source file not present in the pack is added.
        for name, data in sources.items():
            zout.writestr(name, data)
            changed += 1
            print(f"ADDED {name}")

    if changed == 0:
        os.remove(tmp)
        print("No changes — pack Src entries already match src/Src/.")
    else:
        os.replace(tmp, msapp)
        print(f"Repacked {os.path.basename(msapp)}: {changed} Src entry(ies) updated.")

    # Verify: every src/Src/*.pa.yaml must now be byte-identical in the pack.
    with zipfile.ZipFile(msapp, "r") as z:
        ok = True
        for f in sorted(os.listdir(SRC_DIR)):
            if not f.endswith(".pa.yaml"):
                continue
            entry = "Src/" + f
            if entry not in z.namelist():
                print(f"FAIL: {entry} missing from pack")
                ok = False
            elif z.read(entry) != sources.get(entry) and open(
                os.path.join(SRC_DIR, f), "rb"
            ).read() != z.read(entry):
                print(f"FAIL: {entry} out of sync")
                ok = False
    if not ok:
        sys.exit(1)
    print("OK: all Src/*.pa.yaml entries are byte-identical to src/Src/.")


if __name__ == "__main__":
    main()
