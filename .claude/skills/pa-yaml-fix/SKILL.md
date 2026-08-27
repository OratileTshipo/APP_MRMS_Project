---
name: pa-yaml-fix
description: Troubleshoot and fix PA1001 PaYaml import errors in Power Apps canvas app .pa.yaml files
invoked_by: /pa-yaml-fix
---

# PaYaml Import Error Troubleshooting

Fix PA1001 errors in Power Apps `.pa.yaml` source files before importing into Studio.

## Common PA1001 Error Patterns

### 1. "Power Fx expressions must start with '='"

**Cause:** A block scalar (`|-`/`|`/`|+`) property doesn't start with `=`, or a stray property is inside another's block scalar.

**Fix:**
```yaml
# WRONG
Visible: |-
  AccessibleLabel: ="Warning Text"
  =CountRows(colFlaggedItems) > 0

# CORRECT
Visible: |-
  =CountRows(colFlaggedItems) > 0
AccessibleLabel: ="Warning Text"
```

### 2. "duplicate key Control"

**Cause:** A control missing its `- ControlName:` prefix becomes a duplicate `Control:` key.

**Fix:** Add the missing name prefix:
```yaml
# WRONG
- RepActTitle_ico_field:
    Control: Classic/Icon@2.5.0
    Control: Classic/TextInput@2.3.2  # DUPLICATE

# CORRECT
- RepActTitle_ico_field:
    Control: Classic/Icon@2.5.0
- RepActTitle_txt:
    Control: Classic/TextInput@2.3.2
```

### 3. "did not find expected key" / "invalid mapping"

**Cause:** `: ` inside Power Fx double-quoted strings breaks YAML plain scalar.

**Fix:** Wrap in single quotes:
```yaml
# WRONG
OnSelect: =Set(x, "format: Programme-Activity")

# CORRECT
OnSelect: '=Set(x, "format: Programme-Activity")'
```

### 4. Wrong control name indentation

**Cause:** Control name indented too deep (inside sibling's properties).

**Fix:** Name indent = `Control:` indent - 4 spaces.

## Verification

```bash
python3 -c "import yaml,glob; [yaml.compose(open(f,encoding='utf-8')) for f in glob.glob('src/Src/*.pa.yaml')]"
python3 tools/check_control_props.py
python3 tools/check_screen_registry.py
```
