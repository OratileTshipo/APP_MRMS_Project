---
name: troubleshoot
description: Troubleshoot common Power Apps canvas app issues and fixes
invoked_by: /troubleshoot
---

# Troubleshoot Power Apps Issues

Common issues and their fixes.

## Import Errors

### PA2108 - Unknown Control Property
**Error:** Control has a property not in the manifest
**Fix:**
```bash
python3 tools/check_control_props.py  # Find which controls have issues
```
Remove or rename the invalid property in the `.pa.yaml` file.

### Screen Registry Mismatch
**Error:** Screen file without `_EditorState` entry (or vice versa)
**Fix:**
```bash
python3 tools/check_screen_registry.py  # Find mismatches
```
Add the missing entry in `_EditorState.pa.yaml`.

### YAML Parse Error
**Error:** Invalid YAML syntax in `.pa.yaml` file
**Fix:**
```bash
python3 -c "import yaml,glob; [yaml.compose(open(f,encoding='utf-8')) for f in glob.glob('src/Src/*.pa.yaml')]"
```
Check the reported file for syntax issues (missing quotes, bad indentation).

## Formula Errors

### Unbalanced Brackets
**Fix:** Count opening/closing brackets, parens, braces in the formula.

### Invalid Column Reference
**Fix:** Check `CHANGES.md` for CSV schemas — column names must match exactly.

### Named Formula in Wrong Place
**Fix:** Move to `App.Formulas` in `App.pa.yaml`, not in screen `OnStart`.

## Common Patterns

### Role-Based Filtering
```yaml
# Good - delegable, role-first
Filter(Activities, Owner.Email = User().Email)

# Bad - complex Or() may not delegate
Filter(Activities, Owner.Email = User().Email || Supervisor.Email = User().Email)
```

### Navigation with Context
```yaml
# Pass context to screen
Navigate(scr_ReportForm, ScreenTransition.None, {ReportID: ThisItem.ID})
```

### Patch for Updates
```yaml
Patch(MonthlyReports, ThisItem, {Status: "Submitted", SubmittedBy: User()})
```

## Restoring from Backup

If source is broken beyond repair:
```bash
cp -r backup/original-pack/* src/
pac canvas unpack --msapp backup/original-pack/APP-MRMS_Project_app.msapp --sources src --layout SourceCode
```
