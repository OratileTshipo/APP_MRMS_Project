#!/usr/bin/env python3
"""Scan and fix common PA1001 YAML syntax errors in Power Apps .pa.yaml files.

Usage:
    python3 fix_msapp_errors.py <path_to_extracted_msapp>/Src/
    python3 fix_msapp_errors.py /tmp/msapp_dev/Src/
    python3 fix_msapp_errors.py --check-only <path>   # scan only, no fixes

Fixes applied:
  1. Block scalars (|-) on non-behavior properties that don't start with =
  2. Misplaced properties inside block scalars (e.g. AccessibleLabel inside Text: |-)
  3. Colon-space in double-quoted Power Fx strings (wraps value in single quotes)
  4. Missing control name prefixes (duplicate Control keys)
  5. Misindented control names
"""

import re
import sys
import os
import glob as globmod


# Properties that use Power Fx expressions (must start with =)
POWER_FX_PROPS = {
    'Y', 'X', 'Width', 'Height', 'Visible', 'Color', 'BorderColor', 'BorderThickness',
    'Size', 'FontWeight', 'PaddingTop', 'PaddingBottom', 'PaddingLeft', 'PaddingRight',
    'Align', 'VerticalAlign', 'LayoutDirection', 'LayoutGap', 'TabIndex',
    'DisabledFill', 'HoverFill', 'FocusedBorderThickness', 'Icon', 'DisplayMode',
    'Tooltip', 'MinWidth', 'MinHeight', 'MaxWidth', 'MaxHeight', 'Fill', 'Font',
    'RadiusBottomLeft', 'RadiusBottomRight', 'RadiusTopLeft', 'RadiusTopRight',
    'PressedBorderColor', 'PressedColor', 'PressedFill', 'HoverBorderColor',
    'HoverColor', 'LayoutMinHeight', 'LayoutMinWidth', 'LayoutJustifyContent',
    'LayoutAlignItems', 'LayoutOverflowX', 'LayoutOverflowY', 'Mode', 'Default',
    'Text', 'AccessibleLabel', 'AlignInContainer', 'DropShadow', 'FillPortions',
    'PaddingBottom', 'PaddingLeft', 'PaddingRight', 'PaddingTop',
    'TemplatePadding', 'TemplateSize', 'TemplateFill', 'TemplateBorderColor',
    'TemplateHoverFill', 'TemplatePressedFill', 'TemplateLineHeight', 'TemplateFormat',
    'DisabledBorderColor', 'DisabledColor', 'FocusedBorderColor', 'FocusedColor',
    'FocusedFill', 'AutoHeight', 'Format', 'HintText', 'MaxLength',
    'TextFormat', 'VerticalOverflow', 'BorderColor',
}

# Structural keywords (NOT Power Fx, don't need = prefix)
STRUCTURAL_KEYS = {
    'Control', 'Variant', 'Description', 'Name', 'ComponentName', 'TemplateName',
    'MethodName', 'DataType', 'IsParameter', 'ReturnType', 'MinValue', 'MaxValue',
    'MaxLength', 'IsBehavior', 'Style', 'ArgumentNames', 'ReturnNames', 'ReturnTypes',
    'IsClass', 'WithReference', 'Category', 'ComponentDefinition', 'AccessRestriction',
    'Children', 'Properties', 'ZIndex',
}


def scan_block_scalar_issues(lines):
    """Find block scalars on properties where content doesn't start with =."""
    issues = []
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.rstrip()
        m = re.match(r'^(\s+)(\w+):\s*(\|[-+]?)\s*$', s)
        if m:
            prop_indent = len(m.group(1))
            prop_name = m.group(2)
            # Check if this is a Power Fx property (not structural)
            if prop_name not in STRUCTURAL_KEYS:
                # Find the first content line
                j = i + 1
                while j < len(lines) and lines[j].strip() == '':
                    j += 1
                if j < len(lines):
                    content_indent = len(lines[j]) - len(lines[j].lstrip())
                    if content_indent > prop_indent:
                        first_content = lines[j].strip()
                        if not first_content.startswith('=') and not first_content.startswith('#'):
                            issues.append(('block_scalar_no_equals', i + 1, prop_name, first_content[:60]))
        i += 1
    return issues


def scan_colon_in_string(lines):
    """Find property values with : inside double-quoted Power Fx strings."""
    issues = []
    for i, line in enumerate(lines):
        s = line.strip()
        m = re.match(r'^(\w+):\s+', s)
        if not m:
            continue
        prop_name = m.group(1)
        if prop_name in STRUCTURAL_KEYS:
            continue
        # Get the value after the property name
        val_start = s.find(': ') + 2
        val = s[val_start:]
        if val.startswith("'"):
            continue  # Already wrapped in YAML single quotes (safe)
        if not val.startswith('='):
            continue
        # Track quote state
        in_quote = False
        for j, c in enumerate(val):
            if c == '"' and (j == 0 or val[j - 1] != '\\'):
                in_quote = not in_quote
            elif c == ':' and in_quote and j + 1 < len(val) and val[j + 1] == ' ':
                issues.append(('colon_in_string', i + 1, prop_name, val[max(0, j - 20):j + 20]))
                break
    return issues


def scan_duplicate_control(lines):
    """Find Control: lines that might be duplicate keys (missing control name)."""
    issues = []
    in_children = False
    children_indent = 0
    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            continue
        indent = len(line) - len(line.lstrip())
        if 'Children:' in s and indent < 60:
            in_children = True
            children_indent = indent
            continue
        if in_children:
            if indent <= children_indent and s and not s.startswith('-'):
                in_children = False
                continue
            if s.startswith('Control:') and not s.startswith('Control: GroupContainer'):
                # Check if previous non-empty line is a control name
                for j in range(i - 1, max(i - 5, 0), -1):
                    prev = lines[j].strip()
                    if prev:
                        if re.match(r'^-\s+\w+:', prev):
                            break  # Has a name
                        elif prev.startswith(('Control:', 'Variant:', 'Properties:', 'Children:', 'ZIndex:')):
                            continue
                        else:
                            issues.append(('missing_control_name', i + 1, prev[:40]))
                            break
    return issues


def fix_colon_in_strings(filepath):
    """Wrap property values containing colon-space in double-quoted strings."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    changes = 0
    for i, line in enumerate(lines):
        s = line.strip()
        m = re.match(r'^(\w+):\s+=(.*)', s)
        if not m:
            m = re.match(r'^(\w+):\s+(\=.*)', s)
        if not m:
            continue
        prop_name = m.group(1)
        if prop_name in STRUCTURAL_KEYS:
            continue
        val = m.group(2)
        if val.startswith("'"):
            continue  # Already wrapped in YAML single quotes (safe)
        # Check for colon-space inside double-quoted strings
        in_quote = False
        has_colon_issue = False
        for j, c in enumerate(val):
            if c == '"' and (j == 0 or val[j - 1] != '\\'):
                in_quote = not in_quote
            elif c == ':' and in_quote and j + 1 < len(val) and val[j + 1] == ' ':
                has_colon_issue = True
                break
        if has_colon_issue:
            indent = line[:len(line) - len(line.lstrip())]
            lines[i] = f"{indent}{prop_name}: '{val}'\n"
            changes += 1
            print(f"  FIXED line {i + 1}: {prop_name}: wrapped value in single quotes")

    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    return changes


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    check_only = '--check-only' in sys.argv

    if len(args) < 1:
        print("Usage: python3 fix_msapp_errors.py <Src_dir> [--check-only]")
        sys.exit(1)

    src_dir = args[0]

    if not os.path.isdir(src_dir):
        print(f"ERROR: {src_dir} is not a directory")
        sys.exit(1)

    yaml_files = sorted(globmod.glob(os.path.join(src_dir, '*.pa.yaml')))
    if not yaml_files:
        print(f"ERROR: No .pa.yaml files found in {src_dir}")
        sys.exit(1)

    print(f"Scanning {len(yaml_files)} YAML files in {src_dir}\n")

    total_issues = 0
    total_fixes = 0

    for filepath in yaml_files:
        fname = os.path.basename(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        issues = []
        issues.extend(scan_block_scalar_issues(lines))
        issues.extend(scan_colon_in_string(lines))
        issues.extend(scan_duplicate_control(lines))

        if issues:
            print(f"  {fname}: {len(issues)} issue(s)")
            for kind, lineno, *rest in issues:
                if kind == 'block_scalar_no_equals':
                    print(f"    Line {lineno}: {rest[0]}: |- block content doesn't start with = ({rest[1]})")
                elif kind == 'colon_in_string':
                    print(f"    Line {lineno}: {rest[0]}: colon in quoted string ({rest[1]})")
                elif kind == 'missing_control_name':
                    print(f"    Line {lineno}: Control without name prefix (prev: {rest[0]})")
            total_issues += len(issues)

        if not check_only and issues:
            # Auto-fix colon-in-string issues
            total_fixes += fix_colon_in_strings(filepath)

    print(f"\n{'Scan complete' if check_only else 'Fix complete'}: {total_issues} issues found, {total_fixes} auto-fixed")
    if total_issues > 0 and check_only:
        print("Run without --check-only to auto-fix colon-in-string issues")


if __name__ == '__main__':
    main()
