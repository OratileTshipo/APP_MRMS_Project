---
name: rebuild-app
description: Repack the Power Apps canvas app from unpacked YAML source into an importable .msapp file
invoked_by: /rebuild-app
---

# Rebuild Power Apps Canvas App

Repack the current unpacked source into an importable `.msapp` file.

## Steps

1. **Verify source integrity:**
   ```bash
   python3 tools/check_pa_yaml_structure.py   # PA1001 structural guards (run FIRST)
   python3 tools/check_screen_registry.py
   python3 tools/check_control_props.py
   python3 tools/verify_powerfx.py
   ```
   If `check_pa_yaml_structure.py` reports issues, fix them before packing —
   Studio will reject the import with PA1001 otherwise (see
   docs/PA1001-import-error-catalog.md for each error class and its fix).

2. **Repack the app** (use next version number):
   ```bash
   pac canvas pack --sources src --msapp APP-MRMS_Project_app_v7.msapp --layout SourceCode --overwrite
   ```

3. **Verify the pack:**
   ```bash
   python3 tools/verify_powerfx.py
   python3 -c "import yaml,glob; [yaml.compose(open(f,encoding='utf-8')) for f in glob.glob('src/Src/*.pa.yaml')]"
   ```

4. **Update CHANGES.md** with the new version and what changed.

## Versioning Rule
Never overwrite an existing pack. Always create a new `_vN_` named file.

## Current Version
Check `README.md` for the latest versioned pack.
