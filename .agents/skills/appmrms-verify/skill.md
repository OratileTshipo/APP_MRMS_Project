# APP-MRMS Source Verification Skill

## Purpose
Run the complete verification suite on APP-MRMS Power Apps source to catch errors before importing into Power Apps Studio.

## When to Use
- Before importing the msapp into Studio
- After editing any `src/Src/*.pa.yaml` file
- When debugging import failures
- As part of CI/CD pipeline

## Verification Steps

### Step 1: Screen Registry Check
```bash
python3 tools/check_screen_registry.py
```
**Expected:** 0 problems, every screen file has a matching _EditorState entry.

**If fails:** A screen file exists without _EditorState registration, or vice versa. Fix by adding/removing the screen from `_EditorState.pa.yaml` ScreensOrder.

### Step 2: Control Property Schema Check
```bash
python3 tools/check_control_props.py
```
**Expected:** 0 errors. Warnings for TypedDataCard/Toggle/ModernTextInput are expected (not in legacy manifest).

**If fails with PA2108 errors:** A control has a property that doesn't exist on that control type. Remove the invalid property from the pa.yaml file.

### Step 3: Power Fx Static Verification
```bash
python3 tools/verify_powerfx.py --strict
```
**Expected:** 0 errors, 0 warnings under --strict mode.

**Common failures:**
- Unbalanced parentheses/brackets → fix the formula
- Navigate target not found → add screen to _EditorState
- Patch key not in CSV schema → verify column name
- Delegation warning → pre-collect into local collection

### Step 4: YAML Parse Gate
```bash
python3 -c "import yaml,glob; [yaml.compose(open(f,encoding='utf-8')) for f in glob.glob('APP_MRMS/src/Src/*.pa.yaml')]"
```
**Expected:** No output (clean exit).

**If fails:** YAML syntax error in one of the pa.yaml files. Check for missing colons, wrong indentation, or special characters.

### Step 5: Pack Round-Trip (Optional)
```bash
pac canvas pack --sources APP_MRMS/src --msapp /tmp/roundtrip.msapp --layout SourceCode --overwrite
pac canvas unpack --msapp /tmp/roundtrip.msapp --sources /tmp/roundtrip_out --layout SourceCode --overwrite
diff -r APP_MRMS/src/Src /tmp/roundtrip_out/Src
```
**Expected:** No diff output (byte-identical).

## Quick Check (All Steps)
```bash
cd APP_MRMS && \
python3 tools/check_screen_registry.py && \
python3 tools/check_control_props.py && \
python3 tools/verify_powerfx.py --strict && \
echo "✅ All checks passed"
```

## Troubleshooting

### "Screen file exists but is MISSING from _EditorState"
Add the screen name to `_EditorState.pa.yaml` ScreensOrder list.

### "ScreensOrder entry with NO matching screen file"
Remove the entry from `_EditorState.pa.yaml` or create the missing screen file.

### "PA2108: Unknown property 'X' for control type 'Y'"
Remove property X from the control's Properties block in the pa.yaml file.

### "Navigate target 'X' is not a known screen"
Add the screen to `_EditorState.pa.yaml` ScreensOrder, or fix the Navigate() call.

### "Patch(X) keys not in the CSV header"
Verify the column name exists in the CSV file. Check for typos and trailing spaces.

### "DELEGATION: CountRows() over 'X' is not delegable"
Pre-collect the data source into a local collection with ClearCollect(), then count the collection.
