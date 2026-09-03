#!/usr/bin/env python3
"""
check_pa_yaml_structure.py — CI guard: PaYaml structural errors that Studio
rejects at import (PA1001) but `pac canvas pack` does not catch.

Purpose
-------
`pac canvas pack` only validates that YAML parses. Power Apps Studio runs a
stricter PaYaml validation at import time and fails with PA1001 for structural
issues. All of the following were hit on real imports (see
docs/PA1001-import-error-catalog.md); this script fails (exit 1) on any of
them so the pack step never ships a file Studio will reject.

Checks
------
1. Duplicate property key inside one control block
   (e.g. two `Width:` lines)                    -> FAIL  (catalog E2)
2. Duplicate `Control:` key — a control block
   missing its `- Name:` header                 -> FAIL  (catalog E4)
3. Plain-scalar `=...` value containing ': '
   (colon + space) which YAML reads as a
   mapping separator                            -> FAIL  (catalog E3)
4. Block-scalar formula (|- / |+ / >-) whose
   non-comment content lines do not start with
   '='                                          -> FAIL  (catalog E1)
5. Broken control block indentation: a `- Name:`
   header and its `Control:` body at wildly
   inconsistent indents                          -> FAIL  (catalog E5)
6. A property-looking line (e.g. `AccessibleLabel:`)
   swallowed INSIDE a block-scalar formula — it is
   sibling property text that got absorbed into the
   formula block                            -> FAIL  (catalog E6)
7. Empty block scalar on a formula property
   (`Visible: |-` with no content — a sibling
   property terminates it immediately)       -> FAIL  (catalog E7)

The scanner is indentation based (like check_control_props.py) because the
source format uses plain scalars starting with '=' that PyYAML rejects. It is
block-scalar aware: content inside `|-`, `|+`, `>-` formula blocks is skipped,
so formula text is never misread as YAML structure.

Usage
-----
    python3 tools/check_pa_yaml_structure.py [path/to/src/Src]
    # exit code 0 = clean, 1 = issues found

Run it as part of the rebuild checklist:
    python3 tools/check_pa_yaml_structure.py && \
    python3 tools/check_screen_registry.py && \
    python3 tools/check_control_props.py && \
    python3 tools/verify_powerfx.py
"""

import re
import sys
from pathlib import Path

CTRL_PAT = re.compile(r'^(\s*)- (\S.*):$')
KEY_PAT = re.compile(r'^(\s*)([\w\.\'\- ]+?):\s*(.*)$')
BLOCK_PAT = re.compile(r'^(\s*)([\w\.\'\- ]+?):\s*(\|[+>-]|\>[\+\-]?)\s*$')

# Property names whose values are always Power Fx formulas in PaYaml.
# Used only to avoid flagging plain-text block scalars (e.g. Tooltip: |-).
# A line inside a block scalar that looks like a sibling property
# (`Name: =...` or `Name: "..."`) — swallowed property text, not formula.
SWALLOWED_PAT = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*):\s*[="]')

FORMULA_PROPS = {
    'OnSelect', 'OnVisible', 'OnHidden', 'OnChange', 'OnHover', 'OnUnhover',
    'OnSelectAction', 'Text', 'Y', 'X', 'Width', 'Height', 'AccessibleLabel',
    'Visible', 'Items', 'Default', 'Fill', 'Color', 'BorderColor', 'Tooltip',
    'HintText', 'DisplayMode', 'ZIndex', 'FillPortions', 'LayoutAlignItems',
    'LayoutDirection', 'LayoutGap', 'LayoutMinHeight', 'LayoutMinWidth',
    'PaddingBottom', 'PaddingLeft', 'PaddingRight', 'PaddingTop',
    'RadiusBottomLeft', 'RadiusBottomRight', 'RadiusTopLeft', 'RadiusTopRight',
    'AutoHeight', 'Wrap', 'Align', 'AlignInContainer', 'Font', 'FontWeight',
    'Size', 'Mode', 'ItemDisplayText', 'ItemAccessibleLabel', 'Value',
    'FocusedBorderThickness', 'HoverColor', 'HoverFill', 'PressedColor',
    'PressedFill', 'DisabledColor', 'DisabledFill', 'DisabledBorderColor',
    'FocusedBorderColor', 'BorderThickness', 'BorderStyle', 'DropShadow',
    'Chevron', 'Overflow', 'VerticalOverflow', 'LeftPadding', 'RightPadding',
    'TopPadding', 'BottomPadding', 'MaxLength', 'MinLength', 'ErrorMessage',
    'Required', 'SelectionMaxCount', 'SelectionMinCount', 'SelectionMode',
    'ShowValue', 'ShowMaximum', 'Minimum', 'Maximum', 'Step', 'Format',
    'Language', 'Direction', 'Image', 'ImagePosition', 'LoadingSpinner',
    'LoadingSpinnerColor', 'PressedBorderColor', 'HoverBorderColor',
    'HoverImage', 'PressedImage', 'DisabledImage', 'ContentLanguage',
    'OverflowBehavior', 'ItemBackgroundFill', 'ItemBorderColor',
    'ItemBorderThickness', 'ItemHoverFill', 'ItemPressedFill',
    'ItemBorderStyle', 'ItemFontColor', 'ItemFontWeight', 'ItemSize',
    'ItemTextHAlign', 'ItemValueText', 'ItemPaddingLeft', 'ItemPaddingRight',
    'ItemGap', 'ItemHeight', 'SelectionColor', 'SelectionFill',
    'SelectionTextColor', 'Italic', 'Strikethrough', 'Underline', 'Base',
    'BasePaletteColor', 'Icon', 'DisabledImage', 'ReadOnly',
}


def scan_file(path: Path) -> list:
    """Return a list of (line_no, message) issues found in one pa.yaml file."""
    issues = []
    try:
        lines = path.read_text(encoding='utf-8-sig').splitlines()
    except (OSError, UnicodeDecodeError) as e:
        return [(0, f'cannot read file: {e}')]

    keys_at = {}          # indent -> {key: line_no} for current mapping scope
    block_indent = None   # content indent of the open block scalar, if any

    for i, raw in enumerate(lines, 1):
        s = raw.rstrip()

        # --- skip content inside an open block scalar ---------------------
        if block_indent is not None:
            if not s.strip():
                continue
            cur = len(s) - len(s.lstrip())
            if cur < block_indent:
                block_indent = None
            else:
                # E6: a property-looking line at exactly the block content
                # indent is a sibling property swallowed into the formula.
                # Legit formula continuation lines never start with a bare
                # identifier + ': ' + '='/"' (record literals start with '{').
                if cur == block_indent and SWALLOWED_PAT.match(s):
                    issues.append((i, "property-looking line swallowed inside "
                        f"block scalar — dedent or delete it: "
                        f"{s.strip()[:60]}"))
                continue

        # --- a block scalar opens here ------------------------------------
        m = BLOCK_PAT.match(s)
        if m:
            # find first non-empty content line to establish block indent
            j = i
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                block_indent = len(lines[j]) - len(lines[j].lstrip())
            continue

        # --- a new list item resets key tracking at its indent ------------
        m = CTRL_PAT.match(s)
        if m:
            il = len(m.group(1))
            for k in list(keys_at):
                if k >= il:
                    del keys_at[k]
            continue

        # --- a key: value line ---------------------------------------------
        m = KEY_PAT.match(s)
        if not m:
            continue
        indent, key, val = m.groups()
        il = len(indent)

        # E4/E5: duplicate Control key => missing '- Name:' header
        if key == 'Control' and il in keys_at and 'Control' in keys_at[il]:
            issues.append(
                (i, f"duplicate 'Control:' key — missing '- Name:' header "
                    f"(first 'Control:' at line {keys_at[il]['Control']})"))

        # E2: duplicate property key in the same block
        keys_at.setdefault(il, {})
        if key in keys_at[il]:
            issues.append(
                (i, f"duplicate key '{key}' in same control block "
                    f"(first at line {keys_at[il][key]})"))
        keys_at[il][key] = i

        # E3: plain-scalar formula containing ': ' (colon + space)
        if val.startswith('=') and not val.startswith(('|=', '>=')) \
                and re.search(r':\s', val):
            issues.append(
                (i, f"plain-scalar formula contains ': ' — quote the whole "
                    f"value: Prop: \"={val[1:].strip()[:60]}...\""))

    return issues


def scan_block_scalar_formulas(path: Path) -> list:
    """E1: block-scalar formulas whose first line lacks '='.

    PaYaml rule (matching Studio's PA1001 check): the FIRST content line of
    a block scalar that holds a formula must start with '='. Continuation
    lines (deeper-indented expression lines, '//' comments) are expression
    continuations and are NOT checked — e.g. this is valid:

        Items: |-
          =// comment explaining the filter
          Filter(colActivitiesInScope, ...)

    Only block scalars on formula properties are checked; plain-text values
    (e.g. Tooltip: |-) are skipped. A block whose first line is a '//' or
    '/*' comment is also skipped (comment-only preamble is allowed).
    """
    issues = []
    lines = path.read_text(encoding='utf-8-sig').splitlines()
    for i, raw in enumerate(lines, 1):
        m = BLOCK_PAT.match(raw.rstrip())
        if not m:
            continue
        indent, key, _ = m.groups()
        if key not in FORMULA_PROPS:
            continue  # plain-text block scalar (e.g. Tooltip) — fine
        base = len(indent)
        # the first non-empty content line of this block scalar
        j = i
        while j < len(lines):
            nxt = lines[j].rstrip()
            if not nxt.strip():
                j += 1
                continue
            nind = len(nxt) - len(nxt.lstrip())
            if nind <= base:
                # E7: empty block scalar on a formula property — a sibling
                # property at the same indent terminates it immediately,
                # leaving an empty formula Studio rejects.
                issues.append((i, f"empty block scalar for formula property "
                    f"'{key}' — remove the '|-' or restore the formula"))
                break
            content = nxt.strip()
            if content.startswith('//') or content.startswith('/*'):
                break  # comment-first block — allowed (Studio accepts)
            if not content.startswith('='):
                issues.append(
                    (j + 1, f"block-scalar formula for '{key}' first content "
                        f"line must start with '=': {content[:60]}"))
            break  # only the first content line is checked
    return issues


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('src/Src')
    files = sorted(root.glob('*.pa.yaml'))
    if not files:
        print(f'no pa.yaml files found under {root}')
        return 1

    total = 0
    for f in files:
        issues = scan_file(f) + scan_block_scalar_formulas(f)
        if issues:
            print(f'{f}:')
            for lineno, msg in issues:
                print(f'  line {lineno}: {msg}')
                total += 1

    if total:
        print(f'\n{total} structural issue(s) found — fix before packing '
              f'(see docs/PA1001-import-error-catalog.md)')
        return 1
    print(f'OK: {len(files)} files, 0 structural issues')
    return 0


if __name__ == '__main__':
    sys.exit(main())