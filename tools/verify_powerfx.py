#!/usr/bin/env python3
"""
verify_powerfx.py — static verification for the unpacked Power Apps (canvas)
source in Src/*.pa.yaml. pac validates YAML structure only; this script checks
the Power Fx formulas themselves as far as possible without Studio:

  1. Formula extraction from the pa.yaml (plain scalars, quoted scalars, block scalars)
  2. Balance check: (), [], {} and string/comment awareness
  3. Defined vs referenced var*/col* identifiers
  4. Navigate()/scr_* targets exist
  5. Control names: uniqueness per screen, referenced controls exist (Reset/Select)
  6. Patch() record keys checked against the CSV schemas + DataSources.json
  7. _EditorState screens vs actual screen files

Exit code 0 = no errors (warnings are reported but tolerated).
Usage: python3 tools/verify_powerfx.py [--strict]
"""
import json
import os
import re
import sys
import glob
import csv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src", "Src")
CSV_DIR = ROOT
DS_PATH = os.path.join(ROOT, "reference", "canvas-apps", "msapp-internals", "References", "DataSources.json")

STRICT = "--strict" in sys.argv

# ---------------------------------------------------------------------------
# Power Fx built-in function / keyword vocabulary (common set)
# ---------------------------------------------------------------------------
BUILTINS = set("""
Abs Accent AddColumns And AnyValue App As Average Base64Decode Base64Encode Blank
Boolean Callback CDate Char Chooser Choices Clear ClearCollect ClearData
Coalesce Collect Color ColorFade ColorValue Column ColumnNames Columns
ComboData Concat Concurrent Confirm Connection Copy Count CountA CountIf
CountRows CountUnique Create DataSourceInfo Date DateAdd DateDiff DateValue
Day DecodeUrl Decimal Defaults Degrees Del Distribute Distinct Download Drop
DropColumns EditForm EncodedUrl EndsWith EncodeUrl EncodeHTML Error Errors
Exit Exp Filter Find First FirstN ForAll Form Format Gain Percent
GroupBy GUID HashTags Host If IfError Index Int IsBlank IsBlankOrError IsError
IsMatch IsNumeric IsType ISOWeekNum IsToday IsUTCToday IsType Join JSON
Last LastN Launch Left Len ln LoadData Local Lock LookUp Lower Match
MatchAll Max MaxDate Mid Min MinDate Minute Mod Month Name Navigate Not
Notify Now NumberValue Or Param Parse Patch PDF Pi Power Proper Radio
Rand RandBetween ReadNFCFile ReadNFCFileBinary Refresh Remove RemoveIf
Rename Replace Reset ResetForm RGBA Right Round RoundDown RoundUp SaveData
Search Second Select SelectButton Self Sequence Set ShareColumns ShowColumns
Shuffle Sign Sin Sort SortByColumns Sqrt StartsWith StdevP Stdev Sum Switch
Table Tan Tanh Text TextInput Today Trace Trim TrimEnds Trunc Type Ungroup
Unicode Unlock Upper URLEncode User Validate Value VarP Var WeekNum Weekday
With Year
""".split())

# Data source names available in the app
DATA_SOURCES = set("""
Programmes Projects Activities MonthlyReports APP_Users Directorates
KPIDefinitions Notifications AuditLog ReportComments EvidenceLibrary
Office365Users CustomGallerySample ComboBoxSample
""".split())

SCREENS = set()
FORMULA_FILES = []          # (path, name)
ERRORS = []
WARNINGS = []
INFOS = []


# ---------------------------------------------------------------------------
# Formula extraction
# ---------------------------------------------------------------------------
def extract_formulas(path):
    """Return list of (control_path, prop, formula_text)."""
    with open(path, encoding="utf-8-sig") as f:
        lines = f.read().split("\n")
    formulas = []
    control_path = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        # track control nesting: lines like "  - Name:" inside Children
        m = re.match(r"^(\s*)- ([A-Za-z_][A-Za-z0-9_]*):\s*$", line)
        if m:
            indent = len(m.group(1))
            # pop controls deeper than this indent
            while control_path and control_path[-1][1] >= indent:
                control_path.pop()
            control_path.append((m.group(2), indent))
            i += 1
            continue
        # property line: indent, key, colon, value
        m = re.match(r"^(\s*)([A-Za-z0-9_\.\ ]+?):(?:\s*(.*))?$", line)
        if m and not line.lstrip().startswith("#"):
            key_indent = len(m.group(1))
            key = m.group(2).strip()
            rest = (m.group(3) or "").strip()
            # plain scalar formula (may continue on more-indented lines)
            if rest.startswith("="):
                # YAML plain scalars fold continuation lines that are more indented
                j = i + 1
                cont = []
                while j < n:
                    bl = lines[j]
                    if bl.strip() == "":
                        cont.append(bl)
                        j += 1
                    elif len(bl) - len(bl.lstrip()) > key_indent:
                        cont.append(bl)
                        j += 1
                    elif len(bl) - len(bl.lstrip()) == key_indent and bl.strip()[:1] in ")}]":
                        cont.append(bl)  # closing-token line folds back into the scalar
                        j += 1
                    else:
                        break
                if cont:
                    first = next((b for b in cont if b.strip() != ""), "")
                    dedent = len(first) - len(first.lstrip())
                    folded = "\n".join(b[dedent:] if b.strip() else "" for b in cont).strip("\n")
                    text = rest + ("\n" + folded if folded else "")
                    formulas.append((list(control_path), key, text))
                    i = j - 1
                else:
                    formulas.append((list(control_path), key, rest))
            # quoted formula  "=..." or '=...'
            elif (rest.startswith('"') and rest.endswith('"') and rest[1:2] == "=") or \
                 (rest.startswith("'") and rest.endswith("'") and rest[1:2] == "="):
                body = rest[2:-1].replace('""', '"')
                formulas.append((list(control_path), key, "=" + body))
            # block scalar
            elif re.match(r"^\|[-+]?\d*$", rest):
                j = i + 1
                block = []
                while j < n:
                    bl = lines[j]
                    if bl.strip() == "" or len(bl) - len(bl.lstrip()) > key_indent:
                        block.append(bl)
                        j += 1
                    else:
                        break
                if block:
                    # dedent by the first content line's indent
                    first = next((b for b in block if b.strip() != ""), "")
                    dedent = len(first) - len(first.lstrip())
                    text = "\n".join(b[dedent:] if b.strip() else "" for b in block)
                    text = text.strip("\n")
                    if text.startswith("="):
                        formulas.append((list(control_path), key, text))
                i = j - 1
        i += 1
    return formulas


# ---------------------------------------------------------------------------
# Balance / quote / comment checker
# ---------------------------------------------------------------------------
def scan_formula(formula):
    """Return (ok, msg). Checks (), [], {} balance and unterminated strings."""
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    i = 0
    n = len(formula)
    in_dq = in_sq = False
    in_block = False
    depth = 0
    while i < n:
        c = formula[i]
        nxt = formula[i + 1] if i + 1 < n else ""
        if in_block:
            if c == "*" and nxt == "/":
                in_block = False
                i += 2
                continue
            i += 1
            continue
        if in_dq:
            if c == '"':
                if nxt == '"':  # escaped quote ""
                    i += 2
                    continue
                in_dq = False
            i += 1
            continue
        if in_sq:
            if c == "'":
                if nxt == "'":  # escaped ''
                    i += 2
                    continue
                in_sq = False
            i += 1
            continue
        if c == "/" and nxt == "*":
            in_block = True
            i += 2
            continue
        if c == "/" and nxt == "/":
            while i < n and formula[i] != "\n":  # rest of line is comment
                i += 1
            continue
        if c == '"':
            in_dq = True
            i += 1
            continue
        if c == "'":
            in_sq = True
            i += 1
            continue
        if c in "([{":
            stack.append((c, i))
            depth += 1
            i += 1
            continue
        if c in ")]}":
            if not stack or stack[-1][0] != pairs[c]:
                return False, f"unbalanced '{c}' at char {i} (stack top: {stack[-1][0] if stack else 'empty'})"
            stack.pop()
            depth -= 1
            i += 1
            continue
        i += 1
    if in_dq:
        return False, "unterminated double-quoted string"
    if in_sq:
        return False, "unterminated single-quoted string"
    if in_block:
        return False, "unterminated /* comment"
    if stack:
        return False, f"unclosed '{stack[-1][0]}' at char {stack[-1][1]}"
    return True, ""


def strip_strings_and_comments(formula):
    """Return formula with string literals and comments blanked (same length)."""
    out = list(formula)
    i = 0
    n = len(formula)
    in_dq = in_sq = in_block = False
    while i < n:
        c = formula[i]
        nxt = formula[i + 1] if i + 1 < n else ""
        if in_block:
            if c == "*" and nxt == "/":
                in_block = False
                out[i] = out[i + 1] = " "
                i += 2
                continue
            out[i] = " "
            i += 1
            continue
        if in_dq:
            if c == '"':
                if nxt == '"':
                    out[i] = out[i + 1] = " "
                    i += 2
                    continue
                in_dq = False
            out[i] = " "
            i += 1
            continue
        if in_sq:
            if c == "'":
                if nxt == "'":
                    out[i] = out[i + 1] = " "
                    i += 2
                    continue
                in_sq = False
            out[i] = " "
            i += 1
            continue
        if c == "/" and nxt == "*":
            in_block = True
            out[i] = out[i + 1] = " "
            i += 2
            continue
        if c == "/" and nxt == "/":
            while i < n and formula[i] != "\n":
                out[i] = " "
                i += 1
            continue
        if c in "\"'":
            if c == '"':
                in_dq = True
            else:
                in_sq = True
            out[i] = " "
            i += 1
            continue
        i += 1
    return "".join(out)


# ---------------------------------------------------------------------------
# Control names per file
# ---------------------------------------------------------------------------
def extract_control_names(path):
    names = []
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            m = re.match(r"^(\s*)- ([A-Za-z_][A-Za-z0-9_]*):\s*$", line.rstrip("\n"))
            if m:
                names.append(m.group(2))
    return names


# ---------------------------------------------------------------------------
# CSV schemas
# ---------------------------------------------------------------------------
def csv_columns():
    cols = {}
    for f in os.listdir(CSV_DIR):
        if f.endswith(".csv"):
            with open(os.path.join(CSV_DIR, f), encoding="utf-8-sig") as fh:
                reader = csv.reader(fh)
                rows = list(reader)
            if len(rows) >= 2:
                cols[f] = [c.strip() for c in rows[1]]
    return cols


def datasource_columns():
    """Map list name -> set of Power Apps property names from DataSources.json."""
    result = {}
    if not os.path.exists(DS_PATH):
        return result
    with open(DS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    for d in data.get("DataSources", []):
        name = d.get("Name")
        meta = d.get("DataEntityMetadataJson")
        if not meta:
            continue
        try:
            inner = json.loads(list(meta.values())[0])
            props = inner["schema"]["items"]["properties"]
        except Exception:
            continue
        # accept both internal names and display titles (Power Fx resolves either)
        known = set(props.keys())
        for p in props.values():
            t = p.get("title", "").strip()
            if t:
                known.add(t)
        result[name] = known
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    files = sorted(glob.glob(os.path.join(SRC, "*.pa.yaml")))
    if not files:
        print("No Src/*.pa.yaml files found under", SRC)
        sys.exit(2)

    all_formulas = []   # (file, control_path, prop, formula)
    controls_per_file = {}
    defined_vars = set()
    defined_cols = set()
    defined_named = set()
    patch_keys = {}     # list -> set of patch keys
    screen_nav = set()
    screen_files = set()
    pending_var_refs = []   # (base, loc, prop, var) — checked after all files define vars
    pending_col_refs = []   # (base, loc, prop, col) — checked after all files define collections

    # Pre-register named formulas (App.Formulas) so var references resolve
    app_path = os.path.join(SRC, "App.pa.yaml")
    if os.path.exists(app_path):
        for cpath, prop, formula in extract_formulas(app_path):
            if prop not in ("OnStart", "StartScreen", "Theme"):
                defined_named.add(prop)

    for path in files:
        base = os.path.basename(path)
        screen_files.add(base)
        names = extract_control_names(path)
        dup = {x for x in names if names.count(x) > 1}
        if dup:
            ERRORS.append(f"[{base}] duplicate control names: {sorted(dup)}")
        controls_per_file[base] = names

        for cpath, prop, formula in extract_formulas(path):
            all_formulas.append((base, cpath, prop, formula))
            ok, msg = scan_formula(formula)
            loc = ".".join(c for c, _ in cpath) or base
            if not ok:
                ERRORS.append(f"[{base}] {loc}.{prop}: {msg}")
            else:
                clean = strip_strings_and_comments(formula)
                # definitions
                for m in re.finditer(r"\bSet\(\s*([A-Za-z_][A-Za-z0-9_]*)", clean):
                    defined_vars.add(m.group(1))
                for m in re.finditer(r"\b(?:ClearCollect|Collect)\(\s*([A-Za-z_][A-Za-z0-9_]*)", clean):
                    defined_cols.add(m.group(1))
                for m in re.finditer(r"\bNavigate\(\s*([A-Za-z_][A-Za-z0-9_]*)", clean):
                    screen_nav.add(m.group(1))
                # patch keys: find each Patch( call, then the record literal { ... }
                # that is the third argument (first { at paren-depth 1 after >=2 commas)
                for pm in re.finditer(r"\bPatch\(", clean):
                    i = pm.end()
                    depth = 0
                    commas = 0
                    rec_start = -1
                    while i < len(clean):
                        c = clean[i]
                        if c == "(":
                            depth += 1
                        elif c == ")":
                            if depth > 0:
                                depth -= 1
                        elif c == "," and depth == 0:
                            commas += 1
                        elif c == "{" and depth == 0 and commas >= 2:
                            rec_start = i
                            break
                        i += 1
                    if rec_start < 0:
                        continue
                    depth = 0
                    j = rec_start
                    while j < len(clean):
                        if clean[j] == "{":
                            depth += 1
                        elif clean[j] == "}":
                            depth -= 1
                            if depth == 0:
                                break
                        j += 1
                    body = clean[rec_start:j]
                    # data source is the first identifier after Patch(
                    m_ds = re.match(r"Patch\(\s*([A-Za-z_][A-Za-z0-9_]*)", clean[pm.start():])
                    if m_ds:
                        # top-level record keys only (skip nested { ... })
                        bdepth = 0
                        for km in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*:", body):
                            seg = body[:km.start()]
                            bdepth = seg.count("{") - seg.count("}")
                            if bdepth == 0:
                                patch_keys.setdefault(m_ds.group(1), set()).add(km.group(1))
                # record literals of the form { key: expr } used anywhere (named formulas etc.)
                # references — deferred to a second pass so cross-file definitions resolve
                for m in re.finditer(r"\b(var[A-Za-z0-9_]*)\b", clean):
                    pending_var_refs.append((base, loc, prop, m.group(1)))
                for m in re.finditer(r"\b(col[A-Za-z0-9_]*)\b", clean):
                    pending_col_refs.append((base, loc, prop, m.group(1)))
                # Reset/Select control references
                for m in re.finditer(r"\b(?:Reset|Select)\(\s*([A-Za-z_][A-Za-z0-9_]*)", clean):
                    target = m.group(1)
                    if target not in controls_per_file[base] and target not in SCREENS \
                            and target != "Parent" and target != "Self":
                        WARNINGS.append(f"[{base}] {loc}.{prop}: Reset/Select target '{target}' not found in {base}")

        # named formulas in App.pa.yaml
        if base == "App.pa.yaml":
            for cpath, prop, formula in extract_formulas(path):
                if prop not in ("OnStart", "StartScreen", "Theme"):
                    defined_named.add(prop)

    # screens from _EditorState
    es_path = os.path.join(SRC, "_EditorState.pa.yaml")
    if os.path.exists(es_path):
        with open(es_path, encoding="utf-8-sig") as f:
            es = f.read()
        for m in re.finditer(r"^\s*- ([A-Za-z0-9_]+)\s*$", es, re.M):
            SCREENS.add(m.group(1))
    # also screens from any Screens: block
    for path in files:
        with open(path, encoding="utf-8-sig") as f:
            head = f.read(2000)
        m = re.search(r"^Screens:\s*$", head, re.M)
        if m:
            sm = re.search(r"^Screens:\s*\n\s*([A-Za-z_][A-Za-z0-9_]*):", head, re.M)
            if sm:
                SCREENS.add(sm.group(1))

    # second pass: var/col references — all Set()/ClearCollect() definitions are now known
    for base, loc, prop, v in pending_var_refs:
        if v not in defined_vars and v not in defined_named:
            WARNINGS.append(f"[{base}] {loc}.{prop}: var '{v}' is never Set()/named-formula'd anywhere")
    for base, loc, prop, v in pending_col_refs:
        if v not in defined_cols:
            WARNINGS.append(f"[{base}] {loc}.{prop}: collection '{v}' is never ClearCollect/Collect'd anywhere")

    # navigation targets
    for t in sorted(screen_nav):
        if t not in SCREENS:
            ERRORS.append(f"Navigate target '{t}' is not a known screen ({sorted(SCREENS)})")

    # screens in _EditorState vs files
    expected = {f[:-8] for f in screen_files if f != "App.pa.yaml" and f != "_EditorState.pa.yaml"}
    missing_in_editor = expected - SCREENS
    if missing_in_editor:
        ERRORS.append(f"Screens missing from _EditorState: {sorted(missing_in_editor)}")

    # formula count + balance summary
    bad = [f for f in all_formulas if not scan_formula(f[3])[0]]
    INFOS.append(f"Formulas checked: {len(all_formulas)} across {len(files)} files; {len(bad)} unbalanced")

    # patch keys vs CSV/DataSources
    ds_cols = datasource_columns()
    csv_cols = csv_columns()
    for ds_name in sorted(patch_keys):
        keys = patch_keys[ds_name]
        known = ds_cols.get(ds_name, set())
        if known:
            unknown = keys - known
            if unknown:
                WARNINGS.append(f"Patch({ds_name}) keys not in the Power Apps schema: {sorted(unknown)}")
        # also check against CSV header (normalized)
        for csvf, cols in csv_cols.items():
            if csvf.replace(".csv", "").lower() == ds_name.lower():
                csv_known = {c for c in cols}
                unknown_csv = keys - csv_known
                if unknown_csv:
                    WARNINGS.append(f"Patch({ds_name}) keys not in {csvf} header: {sorted(unknown_csv)}")

    # ------------------------------------------------------------------
    print("=" * 78)
    print("Power Fx static verification — APP-MRMS unpacked source")
    print("=" * 78)
    for i in INFOS:
        print("INFO :", i)
    for w in sorted(set(WARNINGS)):
        print("WARN :", w)
    for e in sorted(set(ERRORS)):
        print("ERROR:", e)
    print("-" * 78)
    print(f"Infos: {len(INFOS)}  Warnings: {len(set(WARNINGS))}  Errors: {len(set(ERRORS))}")
    sys.exit(1 if ERRORS else 0)


if __name__ == "__main__":
    main()
