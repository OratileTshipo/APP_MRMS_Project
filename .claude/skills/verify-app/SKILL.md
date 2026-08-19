---
name: verify-app
description: Run all verification checks on the Power Apps canvas app source and pack
invoked_by: /verify-app
---

# Verify Power Apps Canvas App

Run all verification checks to ensure the app is valid before import.

## Full Verification Suite

```bash
# 1. Screen registry check - ensures all screens have EditorState entries
python3 tools/check_screen_registry.py

# 2. Control properties check - validates against Templates.json (PA2108 class)
python3 tools/check_control_props.py

# 3. Formula verification - checks formula balance, nav targets, patch keys
python3 tools/verify_powerfx.py

# 4. YAML parse gate - ensures all .pa.yaml files are valid YAML
python3 -c "import yaml,glob; [yaml.compose(open(f,encoding='utf-8')) for f in glob.glob('src/Src/*.pa.yaml')]"
```

## Quick Checks (individual)

- **Screen registry only:** `python3 tools/check_screen_registry.py`
- **Control props only:** `python3 tools/check_control_props.py`
- **Formulas only:** `python3 tools/verify_powerfx.py`
- **YAML syntax only:** `python3 -c "import yaml,glob; [yaml.compose(open(f,encoding='utf-8')) for f in glob.glob('src/Src/*.pa.yaml')]"`

## What Each Check Catches

| Check | Catches |
|-------|---------|
| Screen registry | Missing `_EditorState` entries, orphaned screen files |
| Control props | Unknown properties (PA2108 class Studio errors) |
| Formula verify | Unbalanced formulas, broken nav targets, invalid Patch keys |
| YAML parse | Syntax errors in .pa.yaml files |
