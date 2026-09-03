#!/usr/bin/env python3
"""
check_control_props.py — CI guard: control properties vs the control manifest.

Purpose
-------
Power Apps Studio rejects a canvas app on import when a control has a property
that does not exist on that control type (import error PA2108, "Unknown
property '<prop>' for canvas control '<control>'"). `pac canvas pack` only
validates YAML structure, so hand-authored pa.yaml can pass the pack round
trip and still fail import. This script compares every property declared in
the pa.yaml source against the authoritative control template manifest
(References/Templates.json — the same widget definitions Studio validates
against) and fails (exit 1) on any unknown property.

The pa.yaml files are walked with a small indentation-based parser instead of
a full YAML parser: the source format uses plain scalars that start with `=`
(Power Fx formulas), which PyYAML rejects with "could not determine a
constructor for the tag 'tag:yaml.org,2002:value'". Only the structural keys
(control declarations and property names) matter here, so the parser reads
those and ignores scalar values entirely.

Checks
------
1. Every `Control: <Type>@<version>` node's `Properties:` keys must exist on
   the matching template in Templates.json  -> FAIL on unknown property
2. A small set of implicit common properties (LayoutMinHeight / LayoutMinWidth
   / AlignInContainer) that Studio writes on every control but that are not
   declared in the templates are always allowed.
3. A control type (base name + version) with no matching template in the
   manifest is reported as a WARNING (the manifest may simply predate a
   newer control version).

Usage
-----
    python3 tools/check_control_props.py [--src DIR] [--templates FILE]

Defaults to the repo layout (src/Src/ + the unpacked original manifest at
reference/canvas-apps/msapp-internals/References/Templates.json). If that
default manifest is missing (reference/ was dropped from the dev/main lines),
the copy embedded in a tracked root .msapp pack is used instead.
Exit code 0 = clean, 1 = unknown properties found.
"""

import argparse
import glob
import io
import json
import os
import re
import sys
import zipfile

# Repo-relative defaults (script lives in tools/, repo root is one level up)
DEFAULT_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Src")
DEFAULT_TEMPLATES = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "reference",
    "canvas-apps",
    "msapp-internals",
    "References",
    "Templates.json",
)

# Properties Studio writes on nearly every control but that are not declared
# in the control template XML (verified against the v4.2 source, which
# imported cleanly in Power Apps Studio, and against the pristine msapp's
# Controls/*.json). Anything here is always allowed.
#
# FillPortions: real AutoLayout container property (how much space a container
# takes inside its AutoLayout parent). The Templates.json manifest in this repo
# predates/omits it, but Studio writes it on every container and it imports
# cleanly (v5_import_errors shows no FillPortions failures).
IMPLICIT_COMMON_PROPERTIES = {
    "LayoutMinHeight",
    "LayoutMinWidth",
    "AlignInContainer",
    "FillPortions",
}

# YAML control names that do not match the manifest template name 1:1.
# (Classic/TextInput is declared in the manifest under the template name "text".)
CONTROL_ALIASES = {
    "textinput": "text",
}

# Root .msapp packs that embed the authoritative control manifest. Tried in
# order when the unpacked reference/ copy is missing; any other root *.msapp
# that ships References/Templates.json is used as a last resort.
MANIFEST_PACK_ORDER = ("APP-MRMS_Latest_dev_27Aug2026_InfoIcons.msapp",)

PROPERTY_TAG_RE = re.compile(r"<property\s+name=\"([^\"]+)\"")


def _msapp_templates_stream(pack_path):
    """Return an open text stream over the Templates.json inside a .msapp pack.

    A .msapp file is a zip archive whose References/Templates.json is the same
    authoritative widget manifest the unpacked reference/ copy is derived
    from. Returns None if the pack does not contain that member.
    """
    with zipfile.ZipFile(pack_path) as pack:
        try:
            raw = pack.read("References/Templates.json")
        except KeyError:
            return None
    return io.StringIO(raw.decode("utf-8"))


def resolve_manifest(templates_arg):
    """Resolve --templates to the manifest source the check validates against.

    Normally the given file path. But the canonical unpacked manifest
    (reference/canvas-apps/msapp-internals/References/Templates.json) was
    deleted from the dev/main lines during the 2026-08 repo cleanup while this
    guard still defaults to it, so every CI run hard-failed. When that default
    path is missing, fall back to the Templates.json embedded in a tracked root
    .msapp pack (the identical authoritative manifest) instead of exiting 1. A
    missing path that was supplied explicitly is returned as-is so main()
    reports it loudly — an explicit path is never silently substituted.
    """
    path = os.path.abspath(templates_arg)
    if os.path.exists(path) or path != os.path.abspath(DEFAULT_TEMPLATES):
        return path

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    packs = [
        os.path.join(repo_root, name)
        for name in MANIFEST_PACK_ORDER
        if os.path.exists(os.path.join(repo_root, name))
    ]
    if not packs:
        packs = sorted(glob.glob(os.path.join(repo_root, "*.msapp")))
    for pack_path in packs:
        stream = _msapp_templates_stream(pack_path)
        if stream is not None:
            print(
                "INFO: default manifest "
                f"{os.path.relpath(path)} not found — using Templates.json "
                f"embedded in {os.path.basename(pack_path)}"
            )
            return stream
    return path  # no usable pack either: main() will fail loudly below
INCLUDE_PROPERTY_TAG_RE = re.compile(r"<appMagic:includeProperty\s+name=\"([^\"]+)\"")

KEY_LINE_RE = re.compile(r"^(\s*)-?\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$")


def load_templates(source):
    """Return {template_name_lower: {"version": str, "properties": set}}.

    `source` is either a filesystem path or an open text stream (used when the
    canonical reference/ manifest is absent and Templates.json is read straight
    out of a tracked root .msapp pack instead).
    """
    f = open(source, encoding="utf-8") if isinstance(source, str) else source
    with f:
        data = json.load(f)
    used = data.get("UsedTemplates") if isinstance(data, dict) else data
    templates = {}
    for entry in used:
        name = entry["Name"]
        xml = entry["Template"]
        props = set(PROPERTY_TAG_RE.findall(xml)) | set(INCLUDE_PROPERTY_TAG_RE.findall(xml))
        templates[name.lower()] = {"version": entry["Version"], "properties": props}
    return templates


def control_key(control_value):
    """Split a `Control:` value into (normalised_type, version)."""
    base, _, version = control_value.partition("@")
    base = base.strip("'\"").split("/")[-1]  # drop e.g. "Classic/" prefix
    norm = CONTROL_ALIASES.get(base.lower(), base.lower())
    return norm, version.strip()


def scan_file(path):
    """
    Line-based scan of one pa.yaml file.

    Returns a list of (control_label, type@version, [property names]).

    The pa.yaml SourceCode layout nests controls like this (indent-relative):

        - MyLabel_lbl:          <- list item at indent X (label)
            Control: Label@2.5.1   <- Control: at X+4 (frame indent = X+4)
            Properties:            <- at X+4, opens the props block
              Text: ="hi"         <- property keys at X+6
            Children:              <- at X+4
              - MyChild:           <- child list item at X+6...

    We keep a stack of open control frames. A frame closes when a later line
    arrives at indent <= the frame's Control: indent (a sibling or ancestor),
    which is exactly how the old single-frame parser failed on deeply nested
    controls: it only tracked the innermost "current" control and silently
    dropped every child level, so unknown properties on nested controls (the
    PA2108 class Studio rejects on import) were never compared.
    """
    controls = []
    with open(path, encoding="utf-8-sig") as f:
        lines = f.read().splitlines()

    # Labels are declared on the "- Name:" line that sits 4 spaces above the
    # matching "Control:" line: pending_labels[control_indent] = name.
    pending_labels = {}
    stack = []  # frames: {indent, label, control_value, props_indent, props}

    # YAML block-scalar bodies (OnSelect: |- , Text: |-, Items: |-, ...) hold
    # multi-line Power Fx formulas whose inner text can contain "Key: value"
    # patterns (e.g. Patch(..., { Status: "Draft", ... })). Those lines must be
    # skipped, not parsed as control properties.
    BLOCK_SCALARS = {"|", "|-", "|+", ">", ">-", ">+"}
    block_scalar_indent = None  # property-line indent of the open block scalar

    for lineno, line in enumerate(lines, start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = KEY_LINE_RE.match(line)
        if not m:
            continue
        indent = len(m.group(1))
        is_list_item = line.lstrip().startswith("-")
        key = m.group(2)

        # While inside a block scalar, skip everything more indented than the
        # scalar's property line (the formula body).
        if block_scalar_indent is not None:
            if indent > block_scalar_indent:
                continue
            block_scalar_indent = None

        # Close any frames this line is at/below (sibling or ancestor).
        # Strict `<`: sibling "- Name:" lines sit 4 spaces below the open
        # frame's Control: indent, while "Properties:"/"Variant:"/"Children:"
        # sit exactly AT it and must stay open.
        while stack and indent < stack[-1]["indent"]:
            top = stack.pop()
            controls.append((top["label"], top["control_value"], top["props"]))

        if key == "Control":
            label = pending_labels.pop(indent, "unknown")
            stack.append(
                {
                    "indent": indent,
                    "label": label,
                    "control_value": m.group(3).strip(),
                    "props": [],
                    "props_indent": None,
                }
            )
            continue
        if key == "Properties":
            # The Properties: key sits at the same indent as its Control: line.
            if stack and indent == stack[-1]["indent"]:
                stack[-1]["props_indent"] = indent + 2
            continue

        # Property keys are plain (non-list) keys at props depth or deeper.
        if (
            stack
            and not is_list_item
            and stack[-1]["props_indent"] is not None
            and indent >= stack[-1]["props_indent"]
            and key != "Children"
        ):
            value = m.group(3).strip()
            if value in BLOCK_SCALARS:
                block_scalar_indent = indent
            stack[-1]["props"].append(key)
            continue

        # A plain key at the same indent as an open control's Control: line is a
        # non-property sibling key (e.g. a screen-level key); remember the label
        # of a control declaration for the Control: line that follows it.
        if is_list_item:
            pending_labels[indent + 4] = key

    while stack:
        top = stack.pop()
        controls.append((top["label"], top["control_value"], top["props"]))
    return controls


def main():
    parser = argparse.ArgumentParser(
        description="CI check: pa.yaml control properties vs the Templates.json manifest"
    )
    parser.add_argument("--src", default=DEFAULT_SRC, help="Directory containing *.pa.yaml files")
    parser.add_argument("--templates", default=DEFAULT_TEMPLATES, help="Path to Templates.json")
    args = parser.parse_args()

    src_dir = os.path.abspath(args.src)

    if not os.path.isdir(src_dir):
        print(f"ERROR: source directory not found: {src_dir}")
        sys.exit(1)

    # Either a file path (present, or an explicit path that must fail loudly)
    # or an in-memory stream when the missing default manifest was substituted
    # from a tracked root .msapp pack.
    manifest_source = resolve_manifest(args.templates)
    if isinstance(manifest_source, str) and not os.path.exists(manifest_source):
        print(f"ERROR: Templates.json not found: {manifest_source}")
        sys.exit(1)

    templates = load_templates(manifest_source)

    errors = []
    warnings = []
    checked = 0
    for path in sorted(glob.glob(os.path.join(src_dir, "*.pa.yaml"))):
        if os.path.basename(path) in ("App.pa.yaml", "_EditorState.pa.yaml"):
            continue
        for label, control_value, props in scan_file(path):
            norm, version = control_key(control_value)
            checked += 1
            template = templates.get(norm)
            if template is None:
                warnings.append(
                    f"{os.path.basename(path)}: no template in manifest for "
                    f"'{control_value}' (base '{norm}') — cannot validate properties"
                )
                continue
            if template["version"] != version:
                warnings.append(
                    f"{os.path.basename(path)}: '{control_value}' — manifest has "
                    f"version {template['version']}; version mismatch noted"
                )
            unknown = sorted(set(props) - template["properties"] - IMPLICIT_COMMON_PROPERTIES)
            for prop in unknown:
                errors.append(
                    f"{os.path.basename(path)}: {prop} is not a property of "
                    f"{label} ({control_value}) (PA2108 class — Studio import will fail)"
                )

    print("=" * 72)
    print("Control property schema check — src/Src/*.pa.yaml vs Templates.json")
    print("=" * 72)
    print(f"Control declarations checked: {checked}")
    for w in warnings:
        print("WARN:", w)
    for e in errors:
        print("FAIL:", e)
    if not errors and not warnings:
        print("OK: every control property exists on its template.")
    print("-" * 72)
    print(f"Errors: {len(errors)}   Warnings: {len(warnings)}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
