#!/usr/bin/env python3
"""Generate reference/data-normalization-report.md from the git diff
HEAD vs working tree for Activities.csv, Directorates.csv, APP_Users.csv."""
import subprocess
import csv
import io
import collections
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(ROOT, "reference", "data-normalization-report.md")


def old_content(path):
    out = subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, text=True, cwd=ROOT)
    return out.stdout


def parse(path, text):
    lines = text.split("\n")
    reader = csv.reader(io.StringIO("\n".join(lines[1:])))
    return list(reader)


def unq(v):
    return v.strip().strip('"')


def load(path):
    with open(os.path.join(ROOT, path), encoding="utf-8-sig", newline="") as f:
        return f.read()


# ---- Activities.csv ----
old = parse("Activities.csv", old_content("Activities.csv"))
new = parse("Activities.csv", load("Activities.csv"))
hdr = old[0]
di, pi = hdr.index("DirectorateLabel"), hdr.index("ProgrammeLabel")
dir_map = collections.Counter()
prog_map = collections.Counter()
for o, n in zip(old[1:], new[1:]):
    if not o or not n or len(o) <= max(di, pi) or len(n) <= max(di, pi):
        continue
    ov, nv = unq(o[di]), unq(n[di])
    if ov != nv:
        dir_map[(ov, nv)] += 1
    op, np = unq(o[pi]), unq(n[pi])
    if op != np:
        prog_map[(op, np)] += 1

# ---- Directorates.csv ----
od = parse("Directorates.csv", old_content("Directorates.csv"))
nd = parse("Directorates.csv", load("Directorates.csv"))
dh = od[0]
ni, ai = dh.index("DirectorateName"), dh.index("Active")
dchg = []
for o, n in zip(od[1:], nd[1:]):
    if not o or not n:
        continue
    if unq(o[ni]) != unq(n[ni]):
        dchg.append((o[0], unq(o[ni]), unq(n[ni])))
    if unq(o[ai]) != unq(n[ai]):
        dchg.append((o[0], "Active=" + unq(o[ai]), "Active=" + unq(n[ai])))

# ---- APP_Users.csv ----
ou = parse("APP_Users.csv", old_content("APP_Users.csv"))
nu = parse("APP_Users.csv", load("APP_Users.csv"))
uh = ou[0]
udi, udid = uh.index("Directorate"), uh.index("Directorate: DirectorateID")
uchg = []
for o, n in zip(ou[1:], nu[1:]):
    if not o or not n:
        continue
    if unq(o[udi]) != unq(n[udi]):
        uchg.append((o[0], unq(o[udi]), unq(n[udi])))
    if unq(o[udid]) != unq(n[udid]):
        uchg.append((o[0] + " ID", unq(o[udid]), unq(n[udid])))

# ---- report ----
L = [
    "# Activities.csv data-normalization report",
    "",
    "Date: 2026-08-16. Generated from the git diff (HEAD vs working tree).",
    "",
    "## Decisions (product)",
    "- RISK and IC are kept as **separate** directorates (cleaned names below).",
    "- **RIC (Risk and Internal Control) is retired**: Directorates.csv Active=False;",
    "  the only APP_Users row on RIC (Oratile Tshipo) was reassigned to **Internal Control** (IC).",
    "- DirectorateLabel is rewritten from the authoritative `Directorate` short-code column",
    "  (blank-code rows resolved from ActivityCode prefix / label). ProgrammeLabel is mapped",
    "  to the canonical Programmes.csv titles.",
    "- Only the two label columns changed in Activities.csv; all other bytes preserved.",
    "",
    "## DirectorateLabel changes (Activities.csv)",
    "",
    "| Old value | New value | Rows |",
    "|---|---|---|",
]
for (o, n), c in sorted(dir_map.items()):
    L.append("| `{}` | `{}` | {} |".format(o, n, c))
L += [
    "",
    "## ProgrammeLabel changes (Activities.csv)",
    "",
    "| Old value | New value | Rows |",
    "|---|---|---|",
]
for (o, n), c in sorted(prog_map.items()):
    L.append("| `{}` | `{}` | {} |".format(o, n, c))
L += ["", "## Directorates.csv changes", "", "| ID | Old | New |", "|---|---|---|"]
for i, o, n in dchg:
    L.append("| {} | `{}` | `{}` |".format(i, o, n))
L += ["", "## APP_Users.csv changes", "", "| User | Old | New |", "|---|---|---|"]
for u, o, n in uchg:
    L.append("| {} | `{}` | `{}` |".format(u, o, n))

os.makedirs(os.path.dirname(REPORT), exist_ok=True)
with open(REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("dir changes:", sum(dir_map.values()), "| prog changes:", sum(prog_map.values()))
print("dir file changes:", dchg)
print("user changes:", uchg)
print("report:", REPORT)
