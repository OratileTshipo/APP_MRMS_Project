#!/usr/bin/env python3
"""
normalize_activities.py
=======================
Normalize the single-source-of-truth CSVs in the project root:

1. Activities.csv
   - DirectorateLabel: rewritten from the authoritative `Directorate` short-code
     column -> canonical DirectorateName in Directorates.csv (blank-code rows are
     resolved from the ActivityCode prefix / label fuzzy match).
   - ProgrammeLabel: every variant ('Pragramme 1', 'Programme ', 'FINANCE ' …)
     mapped to the canonical Programmes.csv Title. The one swapped row (id 241)
     is fixed: its label held the programme and its programme held the directorate.
   - Only the two label columns change; all other bytes (incl. multi-line quoted
     ActivityDescription fields and the ListSchema blob) are preserved exactly.
2. Directorates.csv
   - 'RISK MANAGEMENT '  -> 'Risk Management'
   - 'INTERNAL CONTROL'  -> 'Internal Control'
   - RIC (Risk and Internal Control) retired: Active -> False (per product
     decision — RIC is no longer in use; RISK and IC are the live directorates).
3. APP_Users.csv
   - Oratile Tshipo moved from 'Risk and Internal Control'/RIC to
     'Internal Control'/IC (product decision).
4. Emits a mapping report (reference/data-normalization-report.md).

Usage:  python3 tools/normalize_activities.py
"""
import csv
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT = os.path.dirname(ROOT)          # project root holding the CSVs
ACT_CSV = os.path.join(PARENT, "Activities.csv")
DIR_CSV = os.path.join(PARENT, "Directorates.csv")
USR_CSV = os.path.join(PARENT, "APP_Users.csv")
REPORT = os.path.join(ROOT, "reference", "data-normalization-report.md")

# ----------------------------------------------------------------------------
# 1. Canonical references
# ----------------------------------------------------------------------------
DIRECT_CANON = {
    "ICT": "Information Communications & Technology Management",
    "HRM": "Human Resources Management",
    "HRD": "Human Resource Development",
    "LEGAL SERVICES": "Legal Services",
    "FINANCE": "Finance",
    "SCM": "Supply Chain Management",
    "CFO": "Chief Financial Officer",
    "RIC": "Risk and Internal Control",          # retired (Active=False)
    "SPECIAL PROGRAMMES": "Special Programmes",
    "SECURITY SERVICES": "Security Services",
    "SPME": "Strategic Planning Monitoring and Evaluations",
    "CMMUNICATIONS": "Communications",
    "IAM": "Immovable Asset Management",
    "ICMTS": "Infrastructure Coordination, Maintenance and Technical Support",
    "IIPIME": "Integrated Infrastructure Planning, Innovation, Monitoring and Evaluation",
    "CBP": "Community Based Programme",
    "RISK": "Risk Management",                    # cleaned from 'RISK MANAGEMENT '
    "IC": "Internal Control",                     # cleaned from 'INTERNAL CONTROL'
}
PREFIX_TO_CODE = {
    "ICTM": "ICT", "SPME": "SPME", "HRM": "HRM", "HRD": "HRD",
    "COMM": "CMMUNICATIONS", "IC": "IC", "LEGAL": "LEGAL SERVICES",
    "SPECIAL": "SPECIAL PROGRAMMES", "FINANCE": "FINANCE", "SCM": "SCM",
    "CFO": "CFO", "RISK": "RISK", "IAM": "IAM", "CMMUNICATIONS": "CMMUNICATIONS",
    "SECURITY": "SECURITY SERVICES",
}
PROG_MAP = {
    "Programme 1": "Programme 1",
    "Programme 1 ": "Programme 1",
    "PRogramme 1": "Programme 1",
    "Pragramme 1": "Programme 1",
    "Programmes 1": "Programme 1",
    "programme 1": "Programme 1",
    "Programme": "Programme 1",
    "Programme ": "Programme 1",
    "FINANCE ": "Programme 1",      # id 241 swapped column
    "": "Programme 1",              # id 428 (code IC) — default programme
    "Programme 2A": "Programme 2A",
    "Programme 3": "Programme 3",
}

def fuzzy_dir_label(label):
    """Best-effort label -> canonical directorate name (blank-code rows)."""
    if not label:
        return None
    norm = re.sub(r"[^a-z0-9 ]", "", label.lower())
    norm = re.sub(r"\s+", " ", norm).strip()
    for canon in DIRECT_CANON.values():
        cnorm = re.sub(r"[^a-z0-9 ]", "", canon.lower())
        cnorm = re.sub(r"\s+", " ", cnorm).strip()
        if norm == cnorm:
            return canon
    fam = [
        ("strategic planning", "Strategic Planning Monitoring and Evaluations"),
        ("human resource management", "Human Resources Management"),
        ("human resource development", "Human Resource Development"),
        ("internal control", "Internal Control"),
        ("risk management", "Risk Management"),
        ("supply chain", "Supply Chain Management"),
        ("special programmes", "Special Programmes"),
        ("communications", "Communications"),
        ("legal services", "Legal Services"),
        ("finance", "Finance"),
        ("chief financial officer", "Chief Financial Officer"),
        ("immovable asset", "Immovable Asset Management"),
        ("information communications", "Information Communications & Technology Management"),
    ]
    for key, canon in fam:
        if key in norm:
            return canon
    return None

# ----------------------------------------------------------------------------
# 2. Activities.csv — offset-preserving rewrite
# ----------------------------------------------------------------------------
def scan_fields(text, start):
    """Yield lists of (start,end) field spans per row; handles quoted multi-line
    fields and CRLF/LF line endings."""
    i = start
    n = len(text)
    row = []
    while i < n:
        fs = i
        in_quotes = False
        while i < n:
            c = text[i]
            if in_quotes:
                if c == '"':
                    if i + 1 < n and text[i + 1] == '"':
                        i += 2
                        continue
                    in_quotes = False
                i += 1
                continue
            if c == '"':
                in_quotes = True
                i += 1
                continue
            if c == ',':
                row.append((fs, i))
                i += 1
                fs = i
                continue
            if c == '\r' or c == '\n':
                row.append((fs, i))
                yield row
                row = []
                if c == '\r' and i + 1 < n and text[i + 1] == '\n':
                    i += 2
                else:
                    i += 1
                fs = i
                break
            i += 1
        else:
            row.append((fs, n))
            yield row
            return

with open(ACT_CSV, encoding="utf-8-sig", newline="") as f:
    act_raw = f.read()

rows_info = []
for spans in scan_fields(act_raw, 0):
    vals = [act_raw[s:e] for (s, e) in spans]
    rows_info.append((spans, vals))

def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        return v[1:-1].replace('""', '"')
    return v

# row 0 = ListSchema blob, row 1 = header, rows 2+ = data
header = [unquote(h) for h in rows_info[1][1]]
d_idx = header.index("DirectorateLabel")
p_idx = header.index("ProgrammeLabel")
c_idx = header.index("Directorate")
code_idx = header.index("ActivityCode")

changes = {}       # row_index -> {col: (old, new)}
dir_map = {}       # (old,new) -> count
prog_map = {}      # (old,new) -> count

for ri in range(2, len(rows_info)):
    spans, vals = rows_info[ri]
    if not vals or not vals[0].strip():
        continue
    code = unquote(vals[c_idx])
    label = unquote(vals[d_idx])
    prog = unquote(vals[p_idx])
    row_ch = {}

    # ---- directorate ----
    new_dir = DIRECT_CANON.get(code) if code else None
    if new_dir is None:
        # prefix lives in ActivityCode; where that is blank, fall back to Title
        ac = unquote(vals[code_idx])
        if not ac and len(vals) > 1:
            ac = unquote(vals[1])
        m = re.match(r"^([A-Za-z ]+?)-", ac) if ac else None
        pcode = PREFIX_TO_CODE.get(m.group(1).strip().upper()) if m else None
        new_dir = DIRECT_CANON.get(pcode) if pcode else fuzzy_dir_label(label)
    if new_dir is None:
        new_dir = fuzzy_dir_label(label)
    if new_dir and new_dir != label:
        row_ch["DirectorateLabel"] = (label, new_dir)
        dir_map[(label, new_dir)] = dir_map.get((label, new_dir), 0) + 1

    # ---- programme ----
    new_prog = PROG_MAP.get(prog, prog)
    if new_prog != prog:
        row_ch["ProgrammeLabel"] = (prog, new_prog)
        prog_map[(prog, new_prog)] = prog_map.get((prog, new_prog), 0) + 1

    if row_ch:
        changes[ri] = row_ch

def quote_field(v):
    if not v:
        return '""'
    if any(ch in v for ch in ',"\r\n'):
        return '"' + v.replace('"', '""') + '"'
    return v

out = []
for ri, (spans, vals) in enumerate(rows_info):
    seg_start = spans[0][0]
    seg_end = spans[-1][1]
    term_end = seg_end
    if term_end < len(act_raw) and act_raw[term_end] == '\r':
        term_end += 1
    if term_end < len(act_raw) and act_raw[term_end] == '\n':
        term_end += 1
    row_ch = changes.get(ri)
    if not row_ch:
        out.append(act_raw[seg_start:term_end])
    else:
        new_fields = []
        for i, val in enumerate(vals):
            if i == d_idx and "DirectorateLabel" in row_ch:
                val = quote_field(row_ch["DirectorateLabel"][1])
            elif i == p_idx and "ProgrammeLabel" in row_ch:
                val = quote_field(row_ch["ProgrammeLabel"][1])
            new_fields.append(val)
        out.append(",".join(new_fields) + act_raw[seg_end:term_end])

act_new = "".join(out)
with open(ACT_CSV, "w", encoding="utf-8-sig", newline="") as f:
    f.write(act_new)

print(f"Activities.csv: {sum(len(c) for c in changes.values())} label changes "
      f"across {len(changes)} rows")

# ----------------------------------------------------------------------------
# 3. Directorates.csv
# ----------------------------------------------------------------------------
def read_simple_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        lines = f.read().split("\n")
    blob = lines[0]
    reader = csv.reader(io.StringIO("\n".join(lines[1:])))
    return blob, list(reader)

def write_simple_csv(path, blob, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        f.write(blob + "\n" + buf.getvalue())

blob, d_rows = read_simple_csv(DIR_CSV)
d_hdr = d_rows[0]
name_idx = d_hdr.index("DirectorateName")
active_idx = d_hdr.index("Active")
dir_file_changes = []
for r in d_rows[1:]:
    if len(r) <= max(name_idx, active_idx):
        continue
    rid = r[0]
    if rid == "RISK" and r[name_idx].strip() == "RISK MANAGEMENT":
        dir_file_changes.append(("RISK", r[name_idx], "Risk Management"))
        r[name_idx] = "Risk Management"
    elif rid == "IC" and r[name_idx].strip() == "INTERNAL CONTROL":
        dir_file_changes.append(("IC", r[name_idx], "Internal Control"))
        r[name_idx] = "Internal Control"
    elif rid == "RIC":
        dir_file_changes.append(("RIC", r[name_idx] + " / Active", "retired"))
        r[active_idx] = "False"
write_simple_csv(DIR_CSV, blob, d_rows)
print("Directorates.csv:", dir_file_changes)

# ----------------------------------------------------------------------------
# 4. APP_Users.csv
# ----------------------------------------------------------------------------
blob, u_rows = read_simple_csv(USR_CSV)
u_hdr = u_rows[0]
u_dir = u_hdr.index("Directorate")
u_dirid = u_hdr.index("Directorate: DirectorateID")
user_changes = []
for r in u_rows[1:]:
    if len(r) > max(u_dir, u_dirid) and r[u_dir].strip() == "Risk and Internal Control":
        user_changes.append((r[0], r[u_dir], "Internal Control"))
        r[u_dir] = "Internal Control"
        r[u_dirid] = "IC"
write_simple_csv(USR_CSV, blob, u_rows)
print("APP_Users.csv:", user_changes)

# ----------------------------------------------------------------------------
# 5. Mapping report
# ----------------------------------------------------------------------------
os.makedirs(os.path.dirname(REPORT), exist_ok=True)
lines = [
    "# Activities.csv data-normalization report",
    "",
    "Date: 2026-08-16. Run by `tools/normalize_activities.py`.",
    "",
    "## Decisions (product)",
    "- RISK and IC are kept as **separate** directorates (cleaned names below).",
    "- **RIC (Risk and Internal Control) is retired**: Directorates.csv Active=False;",
    "  the only APP_Users row on RIC (Oratile Tshipo) was reassigned to **Internal Control** (IC).",
    "- DirectorateLabel is rewritten from the authoritative `Directorate` short-code column",
    "  (blank-code rows resolved from ActivityCode prefix / label). ProgrammeLabel is mapped",
    "  to the canonical Programmes.csv titles.",
    "",
    "## DirectorateLabel changes",
    "",
    "| Old value | New value | Rows |",
    "|---|---|---|",
]
for (old, new), n in sorted(dir_map.items()):
    lines.append(f"| `{old}` | `{new}` | {n} |")
lines += ["", "## ProgrammeLabel changes", "", "| Old value | New value | Rows |", "|---|---|---|"]
for (old, new), n in sorted(prog_map.items()):
    lines.append(f"| `{old}` | `{new}` | {n} |")
lines += ["", "## Directorates.csv changes", "", "| ID | Old | New |", "|---|---|---|"]
for rid, old, new in dir_file_changes:
    lines.append(f"| {rid} | `{old}` | `{new}` |")
lines += ["", "## APP_Users.csv changes", "", "| User | Old | New |", "|---|---|---|"]
for usr, old, new in user_changes:
    lines.append(f"| {usr} | `{old}` | `{new}` |")
with open(REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("Report:", REPORT)
