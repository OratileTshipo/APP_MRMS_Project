# Data Sanitization — Instructions

Scripts to strip sensitive and POPIA-restricted data from CSV and XLSX exports before committing to any repository.

**Run locally on your machine.** These scripts do not touch the original files.

---

## Quick Start

```bash
# Install openpyxl (needed for XLSX support)
pip install openpyxl

# Schema mode (default) — column names + data types only, zero org data
python3 tools/sanitize_data.py --input *.csv

# Redact mode — full dataset with sensitive columns replaced by [REDACTED]
python3 tools/sanitize_data.py --input *.csv --mode redact

# Headers mode — column names only (safest option)
python3 tools/sanitize_data.py --input *.csv --mode headers
```

---

## Modes

| Mode | Output | Safe for AI? | Safe for public repo? |
|------|--------|-------------|----------------------|
| `schema` | Column name + detected type + YES/NO flag | ✅ Yes | ✅ Yes |
| `redact` | Full data, sensitive columns → `[REDACTED]` | ⚠️ Review first | ⚠️ Review first |
| `headers` | Column names only | ✅ Yes | ✅ Yes |

---

## Usage

### Process specific files
```bash
python3 tools/sanitize_data.py --input Activities.csv MonthlyReports.csv
```

### Process all CSVs in current directory
```bash
python3 tools/sanitize_data.py --input *.csv
```

### Process XLSX files
```bash
python3 tools/sanitize_data.py --input export.xlsx --mode schema
```

### Custom output directory
```bash
python3 tools/sanitize_data.py --input *.csv --output-dir safe_exports/
```

### Custom config file
```bash
python3 tools/sanitize_data.py --input *.csv --config tools/sanitize_config.json
```

---

## What Gets Flagged as Sensitive

| Category | Examples | Why |
|----------|----------|-----|
| **Person columns** | ActivityOwner, Supervisor, Director, ProgrammeManager, SubmittedBy | POPIA — personal information |
| **Email columns** | UserAccount, Email | POPIA — contact information |
| **Password columns** | AppPassword, Password, Secret | Credentials — never commit |
| **Org-identifying** | Directorate, Programme, Project, ActivityDescription, Title | Organization-specific data |
| **Comment text** | CommentText, RejectionReason, ReasonForDeviation | May contain personal opinions |
| **Financial** | Budget, Cost, FinancialYear | Commercially sensitive |
| **Internal IDs** | EntityId, Claims, PictureURL | Could expose infrastructure |

---

## What's Always Safe (Not Flagged)

| Type | Examples |
|------|----------|
| Numeric IDs | `ID`, `Version` |
| Booleans | `Active`, `IsOverdue`, `isFlagged`, `IsRead` |
| Status codes | `Status`, `ReportStatus`, `SubmissionStatus` |
| Period labels | `Quarter`, `ReportingMonth`, `Frequency` |
| Dates | `StartDate`, `EndDate`, `DueDate`, `SubmissionDate` |
| Percentages | `PercentageComplete` |
| KPI labels | `KPIName`, `KPITarget`, `KPIUnit` |
| Audit fields | `EntityType`, `Action`, `FieldChanged` |

---

## SharePoint CSV Handling

SharePoint exports prepend a `ListSchema=` metadata row containing XML. The script automatically detects and skips this row.

---

## Workflow

### Before committing CSV/XLSX exports

```bash
# 1. Run the script
python3 tools/sanitize_data.py --input *.csv --mode schema

# 2. Review the output
cat sanitized_output/*_schema.csv

# 3. Copy sanitized files over originals (or commit the sanitized versions)
cp sanitized_output/*_schema.csv .

# 4. Clean up
rm -rf sanitized_output/
```

### For sharing data with AI models

```bash
# Use redact mode — replaces sensitive columns with [REDACTED]
python3 tools/sanitize_data.py --input *.csv --mode redact

# Review the output before sharing
cat sanitized_output/*_redacted.csv
```

---

## Configuration

Edit `tools/sanitize_config.json` to customize:

- **Add sensitive patterns:** Add column names or substring patterns to `sensitive_patterns`
- **Add safe patterns:** Add columns that should never be flagged to `safe_patterns`
- **Add exclusions:** Use `contains_patterns_exclusions` to prevent false positives (e.g., "Directorate" contains "Director" but is not a person column)

---

## Testing

```bash
# Test schema mode — verify no org data in output
python3 tools/sanitize_data.py --input *.csv --mode schema --output-dir /tmp/test

# Verify no sensitive values leak
grep -r "nwpg\|gov.za\|@\|password\|Directorate.*ICTM" /tmp/test/

# Clean up
rm -rf /tmp/test
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `openpyxl not installed` | Run `pip install openpyxl` |
| Column not flagged as sensitive | Add it to `tools/sanitize_config.json` under the appropriate category |
| False positive (safe column flagged) | Add column name to `safe_patterns.column_names` |
| SharePoint ListSchema row showing up | Script handles this automatically — if it persists, check file encoding (should be UTF-8 with BOM) |

---

*Tool: `tools/sanitize_data.py` — Config: `tools/sanitize_config.json`*
