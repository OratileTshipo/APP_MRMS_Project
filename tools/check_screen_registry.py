#!/usr/bin/env python3
"""
check_screen_registry.py — CI guard for the screen <-> _EditorState registry.

Purpose
-------
Every screen in a canvas app must be registered in the app's editor state
(_EditorState.pa.yaml, ScreensOrder list). A screen file that exists in
src/Src/ but is missing from _EditorState never gets loaded by the app; an
_EditorState entry with no matching file breaks the pack. This script fails
(exit code 1) on either mismatch so CI catches the drift immediately.

Checks (both directions)
------------------------
1. Screen file exists (src/Src/scr_*.pa.yaml) but has no matching
   ScreensOrder entry in _EditorState.pa.yaml  -> FAIL
2. ScreensOrder entry in _EditorState.pa.yaml with no matching screen file
   in src/Src/                                 -> FAIL

Usage
-----
    python3 tools/check_screen_registry.py [--src DIR] [--editor FILE]

Defaults to the repo layout (src/Src/ + src/Src/_EditorState.pa.yaml).
Exit code 0 = registry consistent, 1 = mismatches found.
"""

import argparse
import glob
import os
import re
import sys

# Repo-relative defaults (script lives in tools/, repo root is one level up)
DEFAULT_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Src")
DEFAULT_EDITOR = os.path.join(DEFAULT_SRC, "_EditorState.pa.yaml")


def screen_name_from_file(path):
    """
    Return the screen name declared inside the file's `Screens:` block.
    Prefer the declared key over the filename so renames stay in sync.
    """
    with open(path, encoding="utf-8-sig") as f:
        head = f.read(2000)
    # The file's first block is `Screens:` followed by `  <ScreenName>:`.
    m = re.search(r"^Screens:\s*\n\s*([A-Za-z_][A-Za-z0-9_]*):", head, re.M)
    if m:
        return m.group(1)
    # Fallback: infer from the filename (scr_Foo.pa.yaml -> scr_Foo).
    base = os.path.basename(path)
    if base.endswith(".pa.yaml"):
        return base[: -len(".pa.yaml")]
    return None


def editor_screens(path):
    """Return the ordered set of screen names listed under ScreensOrder."""
    screens = []
    if not os.path.exists(path):
        return screens
    with open(path, encoding="utf-8-sig") as f:
        content = f.read()
    in_order = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("ScreensOrder:"):
            in_order = True
            continue
        if in_order:
            # List items look like "- scr_Home"; stop at the next top-level key.
            m = re.match(r"^-\s*([A-Za-z_][A-Za-z0-9_]*)\s*$", stripped)
            if m:
                screens.append(m.group(1))
            elif stripped and not stripped.startswith("-"):
                in_order = False
    return screens


def main():
    parser = argparse.ArgumentParser(description="CI check: screen files <-> _EditorState registry")
    parser.add_argument("--src", default=DEFAULT_SRC, help="Directory containing *.pa.yaml screen files")
    parser.add_argument("--editor", default=DEFAULT_EDITOR, help="Path to _EditorState.pa.yaml")
    args = parser.parse_args()

    src_dir = os.path.abspath(args.src)
    editor_path = os.path.abspath(args.editor)

    if not os.path.isdir(src_dir):
        print(f"ERROR: screen source directory not found: {src_dir}")
        sys.exit(1)
    if not os.path.exists(editor_path):
        print(f"ERROR: _EditorState.pa.yaml not found: {editor_path}")
        sys.exit(1)

    # ---- collect screen files (exclude App.pa.yaml and _EditorState itself) ----
    screen_files = {}
    for path in sorted(glob.glob(os.path.join(src_dir, "*.pa.yaml"))):
        base = os.path.basename(path)
        if base in ("App.pa.yaml", "_EditorState.pa.yaml"):
            continue
        name = screen_name_from_file(path)
        screen_files[name] = base  # name -> filename

    registered = set(editor_screens(editor_path))

    # ---- direction 1: file exists but not registered ----
    unregistered = sorted(set(screen_files) - registered)
    # ---- direction 2: registered but no file ----
    orphaned = sorted(registered - set(screen_files))

    problems = []
    if unregistered:
        problems.append(
            "Screen file(s) exist but are MISSING from _EditorState ScreensOrder: "
            + ", ".join(f"{screen_files[n]} ({n})" for n in unregistered)
        )
    if orphaned:
        problems.append(
            "_EditorState ScreensOrder entry(ies) with NO matching screen file: "
            + ", ".join(orphaned)
        )

    # ---- report ----
    print("=" * 72)
    print("Screen registry check — src/Src/*.pa.yaml <-> _EditorState.pa.yaml")
    print("=" * 72)
    print(f"Screen files found : {len(screen_files)}")
    print(f"EditorState screens: {len(registered)}")
    for p in problems:
        print("FAIL:", p)
    if not problems:
        print("OK: every screen file is registered and every entry has a file.")
    print("-" * 72)
    print(f"Problems: {len(problems)}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
