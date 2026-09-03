# PA1001 Import Error Catalog — Lessons Learned

**Purpose:** Every error Power Apps Studio rejected on import, its root cause, the
fix applied, and the rule that prevents it from being built again. Read this
before editing `src/Src/*.pa.yaml`, and run `tools/check_pa_yaml_structure.py`
before every `pac canvas pack`.

**Last updated:** 2026-09-03 (builds v7 → v10)

---

## How errors surface

`pac canvas pack` only validates that YAML *parses*. Power Apps Studio performs
a much stricter PaYaml validation **at import time** (`PA1001`), and it reports
errors one file at a time. That means:

1. **Fix errors iteratively**: Studio reports a few errors per attempt — fix,
   repack, re-import, repeat until import succeeds.
2. **Never trust a successful pack**: `Packing succeeded.` ≠ importable.
3. The pack must be **opened once for edit in Studio and saved** after import
   before external changes become visible.

---

## Error catalog

### E1. Block scalar (`|-`) swallowing sibling properties

**Files/lines:** `scr_Activities.pa.yaml:777`, `scr_Home.pa.yaml:2160`
**Error:** `PA1001 ... Reason: Power Fx expressions must start with '='.`

**Root cause:** A property value declared as a YAML block scalar consumed lines
that were meant to be *separate properties*:

```yaml
# BROKEN — everything at deeper indent is part of Y's value
Y: |-
AccessibleLabel: ="Activity Row Due"          # same indent as Y: → sibling (OK)
  =//ActivityRowMeta_lbl.Y + ActivityRowMeta_lbl.Height   # comment line
  ActivityItems_gal.TemplateHeight - 30                   # ← no '=' prefix → ERROR
```

The block scalar contains a `//` comment line followed by an expression line
that does not start with `=`. PaYaml requires every effective expression line
inside a formula block scalar to start with `=`.

**Fix:**
```yaml
Y: =ActivityItems_gal.TemplateHeight - 30
AccessibleLabel: ="Activity Row Due"
```

**Rule:**
- A block scalar is only needed for *multi-line formulas*. A single-line
  expression must be a plain scalar: `Y: =expr`.
- The **first content line** of a block-scalar formula must start with `=`.
  Deeper-indented continuation lines and `//` comment lines do NOT need `=`
  (Studio accepts `=// comment` preamble followed by `Filter(...)`).
- Never leave a `//`-commented-out old expression plus a live expression in the
  same block scalar — keep the live one only.
- Check that the block scalar does not swallow a following property line:
  a block scalar whose content lines are followed by a *less-indented*
  sibling property (`AccessibleLabel:` at the same indent as `Y:`) leaves the
  deeper lines dangling — they fold into the sibling's value and fail.

---

### E2. Duplicate property key inside one control

**Files/lines:** `scr_ApprovalQueue.pa.yaml:377`, `scr_Home.pa.yaml:2160`
**Error:** `PA1001 ... Reason: Duplicate name 'Width' used ... First use is located at ...`

**Root cause:** The same property (`Width:`, `AccessibleLabel:`) declared twice
at the same indentation inside one control block:

```yaml
Text: ="Drafts"
Width: =Parent.Width
Width: =Parent.Width     # ← duplicate → ERROR
```

A variant: an `AccessibleLabel` that had been *swallowed content* inside a
`Text: |-` block was incorrectly "restored" as a real property next to the
real `AccessibleLabel` of the same control.

**Fix:** Delete the duplicate line. When restoring swallowed lines, first
confirm the line was a genuine property (same indent as siblings) and that the
control does not already declare that property.

**Rule:**
- One property key per control block — no exceptions.
- When un-swallowing block-scalar content, verify against sibling properties
  before promoting a line to a real property.

---

### E3. Plain scalar formula containing `: ` (colon + space)

**Files/lines:** `scr_ReportActivities.pa.yaml:717, 911, 1216, 1448`,
`scr_Home.pa.yaml:2157`
**Error:** `PA1001 ... Reason: While scanning a plain scalar value, found invalid mapping.`

**Root cause:** A YAML plain scalar value (an unquoted `=...` expression) that
contains a colon followed by a space inside a string literal. YAML reads the
`: ` as a mapping separator and fails:

```yaml
AccessibleLabel: ="Status: " & ThisItem.Status.Value   # ← "Status: " has ': ' → ERROR
```

**Fix:** Quote the whole value as a double-quoted YAML scalar (Studio's own
style for complex expressions):

```yaml
AccessibleLabel: "=\"Status: \" & ThisItem.Status.Value"
```

**Rule:**
- Any plain-scalar `=...` value containing `: ` (colon + space) MUST be
  double-quoted: `Prop: "=...expr..."`
- This includes colon inside string literals (`"Status: "`, `"format: ..."`,
  `"(POE): ..."`).
- Detection: `grep -nE '^(\s*)([A-Za-z0-9_.]+): (=.*: .*)' src/Src/*.pa.yaml`

---

### E4. Missing `- Name:` header before a control

**Files/lines:** `scr_ReportActivities.pa.yaml:918, 986, 1044, 1103, 1171,
1228, 1285, 1343, 1400`
**Error:** `PA1001 ... Reason: Encountered duplicate key Control`

**Root cause:** A control's `Control:` / `Properties:` block directly follows
the previous control's properties **without its own `- ControlName:` list-item
header**, so the second `Control:` key duplicates the first at the same
indentation. Occurred for every input control (TextInput/Dropdown) placed after
its info-icon inside the report form:

```yaml
- RepActTitle_ico_field:
    Control: Classic/Icon@2.5.0
    Properties:
      ...
      TabIndex: =0
    Control: Classic/TextInput@2.3.2      # ← no "- RepActTitle_txt:" header → ERROR
    Properties:
      ...
```

**Fix:** Insert the missing header at the same indent as sibling list items,
using the control name referenced by formulas (`Reset(RepActTitle_txt)`,
`RepActMonth_drp.Selected`, …):

```yaml
- RepActTitle_ico_field:
    Control: Classic/Icon@2.5.0
    Properties:
      ...
      TabIndex: =0
- RepActTitle_txt:
    Control: Classic/TextInput@2.3.2
    Properties:
      ...
```

**Rule:**
- Every `Control:` key must be preceded by its own `- Name:` list item.
- The control name must match what formulas reference (`Reset(...)`,
  `.Selected`, `.Text`).
- When adding an icon next to an input control, ALWAYS add the input control
  as a *separate* list item — never let its `Control:` key land inside the
  icon's block.

---

### E5. Broken indentation of a control block

**File/line:** `scr_ReportActivities.pa.yaml:1415` (`RepActAttachements_con`)
**Error:** same as E4 (`duplicate key Control`), plus malformed hierarchy.

**Root cause:** A control's list header and body had inconsistent indentation —
header at indent 48 (nested inside the previous control's properties) while its
body sat at indent 34 (as if it were a much shallower sibling):

```yaml
                                                - RepActAttachements_con:   # 48 spaces
                                  Control: GroupContainer@1.5.0            # 34 spaces
```

**Fix:** Re-indent the entire block to match its siblings (`RepActPOEAttachment_con`):
header at the same indent as sibling list items, body +4 from the header.

**Rule:**
- A control block's `- Name:` header, its `Control:`/`Properties:` keys, and
  property values must all use consistent, sibling-consistent indentation.
- After any structural edit, verify indent of header vs body.

---

### E6. Sibling property swallowed inside a block-scalar formula

**Files/lines:** `scr_Home.pa.yaml:673, 1038, 1143, 1251, 1361, 1469, 2159,
2245, 2332, 2739, 2766`, `scr_Activities.pa.yaml:774, 778, 860`,
`scr_Projects.pa.yaml:735, 939`, `scr_ReportView.pa.yaml:642`
**Error:** none by itself — it corrupts the formula it is stuck in (the line
becomes literal text after the closing `)`), and its *sibling* at the same
indent terminates the block, which then surfaces as E1/E7. Seen at import as:
`PA1001 ... Power Fx expressions must start with '='.`

**Root cause:** A property line ended up *inside* the previous `Text: |-`
block scalar instead of at sibling indent. It is absorbed as literal formula
text (renders in the label / breaks the expression), and it terminates the
block for the lines below it:

```yaml
Text: |-
  =If(
      IsBlank(ThisItem.DueDate),
      "Frequency: " & ThisItem.'Frequency '.Value,
      "Due " & Text(ThisItem.DueDate, "dd mmm yyyy")
  )
  AccessibleLabel: ="Activity"          # ← swallowed: literal text in formula
Width: =Parent.Width * .9               # ← terminates the block here
X: =10
Y: =ActivityItems_gal.TemplateHeight - 30
AccessibleLabel: ="Activity Row Due"    # ← real sibling property
```

**Fix — two cases:**
1. The control **already has** a real `AccessibleLabel` sibling (different
   value) → the swallowed line is garbage → **DELETE** it.
2. The control has **no** real `AccessibleLabel` → the swallowed line is the
   only trace of the property → **DEDENT** it to the same indent as `Text:`.

```yaml
# Case 1 (delete):
Text: |-
  =If(...)
Width: =Parent.Width * .9
AccessibleLabel: ="Activity Row Due"

# Case 2 (dedent):
Text: |-
  =If(...)
AccessibleLabel: ="Activity"           # now a real sibling property
```

**Rule:**
- `AccessibleLabel` (and any property) must sit at the *same indent* as its
  sibling properties — never one step deeper inside a `|-` formula block.
- When fixing, decide delete vs dedent by checking whether a real sibling
  property already exists in the same control.
- **PA2108 follow-up:** after dedenting, run `tools/check_control_props.py`.
  Two dedented `AccessibleLabel: ="Activity"` lines landed on classic
  `Label@2.5.1` controls (`lbl_RoleValue_Home`, `MonthlyPct_lbl`) — the
  reference manifest does not declare `AccessibleLabel` on that template, and
  the original Studio export never set it there. They were deleted (the
  generic `"Activity"` value was template-copy garbage anyway). Only dedent
  onto control types the manifest validates (ModernText, icons, …).

---

### E7. Empty block scalar on a formula property

**File/line:** `scr_Home.pa.yaml:2329` (`Visible: |-` on `WarningText_lbl`)
**Error:** `PA1001 ... Reason: Power Fx expressions must start with '='.`

**Root cause:** A property declared as a block scalar (`Visible: |-`) whose
content is immediately terminated by a sibling property at the same indent —
the block scalar ends up empty and PaYaml has no expression to validate:

```yaml
Visible: |-                    # ← empty: next line is at the same indent
AccessibleLabel: ="Warning Text"     # ← terminates the block scalar
  =true                        # ← dangles as AccessibleLabel's value → chaos
```

**Fix:** Either put the expression inline (`Visible: =true`) or remove the
empty `|-` marker:

```yaml
Visible: =true
AccessibleLabel: ="Warning Text"
```

**Rule:**
- A block scalar must have at least one content line deeper than the
  property indent. If the next non-blank line is at the same or shallower
  indent, the block is empty — convert to a plain `Prop: =expr` scalar.
- This is the same root cause family as E1/E6: a block scalar boundary that
  does not match where the properties actually are.

---

## Prevention — run before every pack

```bash
# 1. Structural PaYaml guards (catches E1–E7)
python3 tools/check_pa_yaml_structure.py

# 2. Existing checks
python3 tools/check_screen_registry.py
python3 tools/check_control_props.py
python3 tools/verify_powerfx.py
```

`check_pa_yaml_structure.py` scans all `src/Src/*.pa.yaml` and fails (exit 1)
on:
1. Duplicate property keys inside one control block (E2)
2. Duplicate `Control:` keys / missing `- Name:` headers (E4, E5)
3. Plain-scalar `=...` values containing `: ` (E3)
4. Block-scalar formulas whose **first content line** does not start with
   `=` (E1) — continuation and `//` comment lines are allowed
5. Property-looking lines swallowed inside block scalars (E6)
6. Empty block scalars on formula properties (E7)

It is block-scalar aware, so formula text inside `|-` / `|+` / `>-` is not
misread as YAML structure. Validation: current source reports 0 issues;
the pre-fix sources reported 102 (all real, zero false positives).

---

## Screen shell consistency rule (regression: v10)

**What happened:** the Approval Queue screen lost its sidebar and standard
header. Git history shows the `ApprQueueSidebar_con` (10 nav icons) and
`ApprQueueHeader_con` shell existed in commit `07c6943` and was **removed in
commit `b38b62e`** (role-scoping fix), leaving a bare `ApprQueueAppHeader_con`
and moving `ApprQueueBody_con` OUT of `ApprQueueDetails_con` to be a sibling.
The screen no longer matched Home / Projects / Activities / ReportActivities.

**The rule — every full screen follows this exact shell (from
`scr_ReportActivities.pa.yaml`, the canonical copy):**

```yaml
- <X>MainScreen_con:                      # horizontal, fills App
    Children:
      - <X>Sidebar_con:                   # ~5% width, vertical icon rail:
          # Home, Projects, Activities, MonthlyReports, MyActivities,
          # Trending, Users, <spacer>, Settings, Support  (9 icons + spacer)
      - <X>Details_con:                   # width = App.Width - Sidebar.Width
          Children:
            - <X>Header_con:              # navy bar, height ~13%:
                # Back_ico(Back()), HeaderLeft(Title+Subtitle), HeaderRight(User+Bell)
            - <X>Body_con:                # MUST be nested inside Details, sibling of Header
```

- The Body container is a **child of Details** (below the Header) — never a
  sibling of Details.
- Header width = `App.Width - <X>Sidebar_con.Width`; Body height =
  `Parent.Height - <X>Header_con.Height`.
- Restoring a screen shell: copy the sidebar + header blocks verbatim from
  `scr_ReportActivities.pa.yaml` (rename `RepAct*` → screen prefix), do NOT
  hand-retype them.

---

## Version history

| Build | Fixed | Result |
|---|---|---|
| v7 | — | ❌ 4 PA1001 errors at import |
| v8 | E1, E2, E3 (4 sites) | ❌ 2 more errors surfaced (E2 variant, E4) |
| v9 | E2 variant, E4 (9 headers), E5 | ❌ 1 more error surfaced (E7 at Home:2329) |
| v10 | E6 (5 more swallowed AccessibleLabels: Activities ×2, Projects ×2, ReportView ×1), E7, PA2108 (2 AccessibleLabels off Label@2.5.1) | ✅ **imported successfully** (2026-09-03) |
| v11 | Screen-shell regression: restored `ApprQueueSidebar_con` + standard header, Body re-nested inside Details | ✅ shell matches Home/ReportActivities |