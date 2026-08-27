---
name: pa-yaml-fix
version: 1.0.0
description: Troubleshoot and fix PA1001 PaYaml import errors in Power Apps canvas app source files. USE WHEN the user reports PA1001 errors, YAML parse failures, or "duplicate key" / "Power Fx expressions must start with '='" / "did not find expected key" / "invalid mapping" errors during msapp import.
author: Buffy
user-invocable: true
---

# PaYaml Import Error Troubleshooting

Fix PA1001 errors in Power Apps `.pa.yaml` source files before importing into Studio.

## Common PA1001 Error Patterns

### 1. "Power Fx expressions must start with '='"

**Cause:** A property value uses a YAML block scalar (`|-` or `|` or `|+`) but the first content line does not start with `=`.

**Also occurs when:** A stray property (like `AccessibleLabel`) is accidentally placed inside another property's block scalar content, making the block's first meaningful line not start with `=`.

**Fix:**
```yaml
# WRONG - block scalar content doesn't start with =
Visible: |-
  AccessibleLabel: ="Warning Text"
  =CountRows(colFlaggedItems) > 0

# CORRECT - AccessibleLabel moved to its own property, block starts with =
Visible: |-
  =CountRows(colFlaggedItems) > 0
AccessibleLabel: ="Warning Text"
```

**Key rules for block scalars (`|-`):**
- Block scalar content MUST start with `=` on the first content line
- Only use `|-` for multi-line formulas (OnSelect, OnChange, OnVisible, OnHover, Text, Default, Height, Color, Visible, Fill, Items, etc.)
- Never place a property definition (e.g., `AccessibleLabel: =...`) inside another property's block scalar

### 2. "duplicate key Control"

**Cause:** A control is missing its `- ControlName:` prefix, causing its `Control:` line to be treated as a duplicate key inside the previous control's mapping.

**Fix:**
```yaml
# WRONG - TextInput has no control name, becomes duplicate Control key
- RepActTitle_ico_field:
    Control: Classic/Icon@2.5.0
    Properties: ...
    Control: Classic/TextInput@2.3.2    # ← DUPLICATE!

# CORRECT - TextInput gets its own name
- RepActTitle_ico_field:
    Control: Classic/Icon@2.5.0
    Properties: ...
- RepActTitle_txt:
    Control: Classic/TextInput@2.3.2
    Properties: ...
```

**Detection:** Search for `Control:` lines that don't have a matching `- Name:` line before them within the same parent Children block.

### 3. "did not find expected key" / "invalid mapping"

**Cause:** A colon-space (`: `) inside a Power Fx double-quoted string breaks YAML plain scalar parsing.

**Fix:** Wrap the entire YAML value in single quotes:
```yaml
# WRONG - ": Programme" and ": ICTM" inside double-quoted strings break YAML
OnSelect: =Set(varTooltipText, If(varTooltipText = "Enter the format: Programme-Activity-SequentialNumber"))

# CORRECT - wrapped in single quotes
OnSelect: '=Set(varTooltipText, If(varTooltipText = "Enter the format: Programme-Activity-SequentialNumber"))'
```

**Detection:** Search for property lines where the Power Fx value contains `": "` or `": word"` inside double-quoted strings. Common patterns:
- `"format: Programme..."`
- `"status: Draft..."`
- `"Evidence (POE): progress..."`
- `"Status: " & ThisItem.Status.Value`

### 4. Wrong indentation on control names

**Cause:** A control name (`- Name:`) is indented too deep (inside a sibling's Properties block) while its `Control:` line is at the correct level.

**Fix:**
```yaml
# WRONG - name at indent 48 (inside RepActOutput_txt properties)
    Width: =Parent.Width
    - RepActAttachements_con:     # ← indent 48, WRONG
        Control: GroupContainer@1.5.0  # ← indent 34, correct level

# CORRECT - name at indent 34 (sibling level)
    Width: =Parent.Width
- RepActAttachements_con:         # ← indent 34, correct
    Control: GroupContainer@1.5.0  # ← indent 38 (name + 4)
```

**Rule:** The control name's indent must match its `Control:` line's indent minus 4 spaces. Use sibling controls as reference for correct indentation.

## Verification Before Import

After fixing pa.yaml files, always run:

```bash
# 1. YAML parse gate
python3 -c "import yaml,glob; [yaml.compose(open(f,encoding='utf-8')) for f in glob.glob('src/Src/*.pa.yaml')]"

# 2. Control properties check
python3 tools/check_control_props.py

# 3. Screen registry check
python3 tools/check_screen_registry.py
```

## PaYaml Structure Reference

```yaml
- ControlName:                    # indent N
    Control: ControlType@version  # indent N+4
    Variant: VariantName          # indent N+4 (optional)
    Properties:                   # indent N+4
      PropName: =PowerFxExpr     # indent N+8
      LongProp: |-               # indent N+8 (block scalar)
        =MultiLineFormula(       # indent N+12 (must start with =)
            arg1,
            arg2
        )
    Children:                     # indent N+4 (if has children)
      - ChildName:                # indent N+8
          Control: ChildType     # indent N+12
```

**Key indentation rules:**
- Control name: indent N
- Control/Variant/Properties/Children: indent N+4
- Property values: indent N+8
- Child controls: indent N+8 (same as properties)
- Child's Control/Properties: indent N+12
