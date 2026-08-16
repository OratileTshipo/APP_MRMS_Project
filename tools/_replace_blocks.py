#!/usr/bin/env python3
"""Replace a control block in a pa.yaml file with new YAML, preserving indentation.

Usage:
  python3 _replace_blocks.py <file> <control-name> <replacement-file> [--keep-refs]

The block starts at the line `- <control-name>:` and ends at the next line whose
indent is <= the block's own indent (i.e. a sibling or dedent). The replacement
text is re-indented to match the block's indent. Prints the line range replaced.
"""
import sys
from pathlib import Path

def find_block(lines, name):
    """Return (start_idx, end_idx, indent) of the `- name:` block."""
    pat = f"- {name}:"
    for i, line in enumerate(lines):
        if line.lstrip().startswith(pat) and line.strip() == pat:
            indent = len(line) - len(line.lstrip())
            j = i + 1
            while j < len(lines):
                l2 = lines[j]
                if l2.strip() == "":
                    j += 1
                    continue
                ind2 = len(l2) - len(l2.lstrip())
                if ind2 <= indent and l2.lstrip().startswith("- "):
                    break
                if ind2 <= indent:
                    # A dedented non-list line ends the block too (parent key)
                    # but only if it isn't a continuation (impossible at <= indent)
                    break
                j += 1
            return i, j, indent
    return None

def main():
    file, name, repl_file = sys.argv[1], sys.argv[2], sys.argv[3]
    lines = Path(file).read_text(encoding="utf-8").splitlines()
    res = find_block(lines, name)
    if not res:
        print(f"ERROR: block '- {name}:' not found in {file}")
        sys.exit(1)
    start, end, indent = res
    repl = Path(repl_file).read_text(encoding="utf-8").rstrip("\n").split("\n")
    # Re-indent the replacement to the block's indent (relative to its own first line)
    base = len(repl[0]) - len(repl[0].lstrip())
    out = []
    for rl in repl:
        rstrip = rl.rstrip()
        cur = len(rstrip) - len(rstrip.lstrip())
        pad = indent + max(0, cur - base)
        out.append(" " * pad + rstrip.lstrip())
    new_lines = lines[:start] + out + lines[end:]
    Path(file).write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(f"replaced lines {start+1}-{end} (indent {indent}) in {file}")

if __name__ == "__main__":
    main()
