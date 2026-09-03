#!/usr/bin/env python3
"""
sanitize_data.py — Remove sensitive and POPIA-restricted data from CSV/XLSX files.

Strips SharePoint ListSchema rows, detects personal/sensitive columns, and outputs
sanitized files safe for committing to any repository. Three modes:

  schema   — Column names, types, sensitivity flags, safe sample values only.
  redact   — Full dataset with sensitive columns replaced by [REDACTED].
  headers  — Column header names only (absolute minimum).

Usage:
    python3 tools/sanitize_data.py --input Activities.csv
    python3 tools/sanitize_data.py --input data.xlsx --mode redact
    python3 tools/sanitize_data.py --input *.csv --mode headers
    python3 tools/sanitize_data.py --input data.csv --config custom_config.json

Run locally on your machine before adding any file to a repo.
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Optional XLSX support
# ---------------------------------------------------------------------------
try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = SCRIPT_DIR / "sanitize_config.json"
OUTPUT_DIR = Path("sanitized_output")

# BOM for UTF-8
UTF8_BOM = "\ufeff"


# ---------------------------------------------------------------------------
# Config loader
# ---------------------------------------------------------------------------
def load_config(config_path: Path) -> dict:
    """Load sensitive/safe column patterns from config JSON."""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_sensitive_set(config: dict) -> tuple[set[str], list[str], set[str]]:
    """
    Return (exact_name_set, substring_patterns, exclusions) for sensitive columns.
    """
    exact = set()
    substrings = []
    exclusions = set()
    for category in config.get("sensitive_patterns", {}).values():
        for name in category.get("column_names", []):
            exact.add(name.lower().strip())
        for pat in category.get("contains_patterns", []):
            substrings.append(pat.lower())
        for pat in category.get("contains_patterns_exclusions", []):
            exclusions.add(pat.lower().strip())
    return exact, substrings, exclusions


def build_safe_set(config: dict) -> set[str]:
    """Return set of column names that are always safe."""
    safe = set()
    for name in config.get("safe_patterns", {}).get("column_names", []):
        safe.add(name.lower().strip())
    return safe


# ---------------------------------------------------------------------------
# Column sensitivity detection
# ---------------------------------------------------------------------------
def is_sensitive(col_name: str, exact_set: set[str], substrings: list[str],
                 safe_set: set[str], exclusions: set[str] = None) -> bool:
    """Determine if a column name is sensitive."""
    normalized = col_name.lower().strip()
    exclusions = exclusions or set()

    # If explicitly safe, not sensitive
    if normalized in safe_set:
        return False

    # Exact match on sensitive names
    if normalized in exact_set:
        return True

    # Substring match (but not if excluded)
    for pat in substrings:
        if pat in normalized:
            # Check if column is in exclusion list (e.g. "Directorate" contains "Director" but is safe)
            if normalized in exclusions or any(ex in normalized for ex in exclusions):
                continue
            return True

    return False


def detect_type(values: list[str]) -> str:
    """Detect the data type of a column from its sample values."""
    non_empty = [v.strip() for v in values if v.strip()]
    if not non_empty:
        return "empty"

    # Check for dates (ISO format or common patterns)
    date_patterns = [
        r"^\d{4}-\d{2}-\d{2}",       # 2026-08-27
        r"^\d{2}/\d{2}/\d{4}",       # 27/08/2026
        r"^\d{2}-\d{2}-\d{4}",       # 27-08-2026
    ]
    date_count = sum(1 for v in non_empty
                     if any(re.match(p, v) for p in date_patterns))
    if date_count > len(non_empty) * 0.7:
        return "datetime"

    # Check for numbers
    num_count = 0
    for v in non_empty:
        try:
            float(v.replace(",", ""))
            num_count += 1
        except ValueError:
            pass
    if num_count > len(non_empty) * 0.7:
        return "number"

    # Check for booleans
    bool_values = {"true", "false", "yes", "no", "1", "0"}
    if all(v.lower() in bool_values for v in non_empty):
        return "boolean"

    # Check for emails
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    email_count = sum(1 for v in non_empty if re.match(email_pattern, v))
    if email_count > len(non_empty) * 0.5:
        return "email"

    # Check for choice/enum (few unique values)
    unique = set(v.lower() for v in non_empty)
    if len(unique) <= 10 and len(non_empty) > 3:
        return f"choice ({len(unique)} values)"

    return "text"


# ---------------------------------------------------------------------------
# CSV handling
# ---------------------------------------------------------------------------
def parse_csv(filepath: Path) -> tuple[list[str], list[dict]]:
    """
    Parse a SharePoint-style CSV, skipping the ListSchema row.
    Returns (headers, list_of_row_dicts).
    """
    with open(filepath, "r", encoding="utf-8-sig") as f:
        raw_lines = f.readlines()

    # Find where actual data starts (skip ListSchema line)
    data_start = 0
    for i, line in enumerate(raw_lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("ListSchema="):
            data_start = i
            break

    # Parse from data_start
    reader = csv.DictReader(raw_lines[data_start:])
    headers = reader.fieldnames or []
    rows = list(reader)

    return [h for h in headers if h is not None], rows


def write_csv_schema(filepath: Path, headers: list[str], rows: list[dict],
                     exact_set: set, substrings: list, safe_set: set,
                     exclusions: set = None, sample_count: int = 3):
    """Write a schema-only CSV with column names and detected types only."""
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Column", "DetectedType", "Sensitive"])

        for col in headers:
            sensitive = is_sensitive(col, exact_set, substrings, safe_set, exclusions)
            dtype = detect_type([row.get(col, "") for row in rows])
            writer.writerow([col, dtype, "YES" if sensitive else "no"])


def write_csv_redacted(filepath: Path, headers: list[str], rows: list[dict],
                       exact_set: set, substrings: list, safe_set: set,
                       exclusions: set = None):
    """Write a redacted CSV with sensitive columns replaced by [REDACTED]."""
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for row in rows:
            redacted = {}
            for col in headers:
                if is_sensitive(col, exact_set, substrings, safe_set, exclusions):
                    redacted[col] = "[REDACTED]"
                else:
                    redacted[col] = row.get(col, "")
            writer.writerow(redacted)


def write_csv_headers(filepath: Path, headers: list[str]):
    """Write a headers-only CSV."""
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)


# ---------------------------------------------------------------------------
# XLSX handling
# ---------------------------------------------------------------------------
def parse_xlsx(filepath: Path) -> tuple[list[str], list[dict], list[list]]:
    """
    Parse an XLSX file.
    Returns (headers, list_of_row_dicts, raw_sheets_data).
    """
    wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
    all_rows = []
    all_headers = []

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        rows_iter = ws.iter_rows(values_only=True)

        # Find header row (first non-empty row)
        headers = []
        for row in rows_iter:
            if row and any(cell is not None for cell in row):
                headers = [str(c) if c is not None else "" for c in row]
                break

        if not headers:
            continue

        if not all_headers:
            all_headers = headers

        # Read data rows
        for row in rows_iter:
            if row and any(cell is not None for cell in row):
                row_dict = {}
                for i, h in enumerate(headers):
                    val = row[i] if i < len(row) else None
                    row_dict[h] = str(val) if val is not None else ""
                all_rows.append(row_dict)

    wb.close()
    return all_headers, all_rows, []


def write_xlsx_schema(filepath: Path, headers: list[str], rows: list[dict],
                      exact_set: set, substrings: list, safe_set: set,
                      exclusions: set = None, sample_count: int = 3):
    """Write a schema-only XLSX with column names and detected types only."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Schema"

    ws.append(["Column", "DetectedType", "Sensitive"])

    for col in headers:
        sensitive = is_sensitive(col, exact_set, substrings, safe_set, exclusions)
        dtype = detect_type([row.get(col, "") for row in rows])
        ws.append([col, dtype, "YES" if sensitive else "no"])

    # Auto-width columns
    for col_cells in ws.columns:
        max_len = 0
        col_letter = col_cells[0].column_letter
        for cell in col_cells:
            if cell.value:
                max_len = max(max_len, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = min(max_len + 2, 60)

    wb.save(filepath)


def write_xlsx_redacted(filepath: Path, headers: list[str], rows: list[dict],
                        exact_set: set, substrings: list, safe_set: set,
                        exclusions: set = None):
    """Write a redacted XLSX."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Redacted"

    ws.append(headers)

    for row in rows:
        redacted_row = []
        for col in headers:
            if is_sensitive(col, exact_set, substrings, safe_set, exclusions):
                redacted_row.append("[REDACTED]")
            else:
                redacted_row.append(row.get(col, ""))
        ws.append(redacted_row)

    # Auto-width
    for col_cells in ws.columns:
        max_len = 0
        col_letter = col_cells[0].column_letter
        for cell in col_cells:
            if cell.value:
                max_len = max(max_len, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = min(max_len + 2, 60)

    wb.save(filepath)


def write_xlsx_headers(filepath: Path, headers: list[str]):
    """Write a headers-only XLSX."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Headers"
    ws.append(headers)
    ws.column_dimensions["A"].width = 40
    wb.save(filepath)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def process_file(input_path: Path, mode: str, config: dict,
                 output_dir: Path, sample_count: int = 3):
    """Process a single CSV or XLSX file."""
    suffix = input_path.suffix.lower()
    if suffix not in (".csv", ".xlsx"):
        print(f"  SKIP (unsupported format): {input_path.name}")
        return False

    exact_set, substrings, exclusions = build_sensitive_set(config)
    safe_set = build_safe_set(config)

    # Determine output path
    out_stem = input_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n  Processing: {input_path.name}")

    if suffix == ".csv":
        headers, rows = parse_csv(input_path)
        print(f"    Columns: {len(headers)}, Rows: {len(rows)}")

        # Count sensitive
        sens_count = sum(1 for h in headers
                         if is_sensitive(h, exact_set, substrings, safe_set, exclusions))
        print(f"    Sensitive columns: {sens_count}/{len(headers)}")

        if mode == "schema":
            out_path = output_dir / f"{out_stem}_schema.csv"
            write_csv_schema(out_path, headers, rows, exact_set, substrings,
                             safe_set, exclusions, sample_count)
        elif mode == "redact":
            out_path = output_dir / f"{out_stem}_redacted.csv"
            write_csv_redacted(out_path, headers, rows, exact_set, substrings,
                               safe_set, exclusions)
        elif mode == "headers":
            out_path = output_dir / f"{out_stem}_headers.csv"
            write_csv_headers(out_path, headers)
        else:
            print(f"    Unknown mode: {mode}")
            return False

        print(f"    Output: {out_path}")
        return True

    elif suffix == ".xlsx":
        if not HAS_OPENPYXL:
            print("    ERROR: openpyxl not installed. Run: pip install openpyxl")
            return False

        headers, rows, _ = parse_xlsx(input_path)
        print(f"    Columns: {len(headers)}, Rows: {len(rows)}")

        sens_count = sum(1 for h in headers
                         if is_sensitive(h, exact_set, substrings, safe_set, exclusions))
        print(f"    Sensitive columns: {sens_count}/{len(headers)}")

        if mode == "schema":
            out_path = output_dir / f"{out_stem}_schema.xlsx"
            write_xlsx_schema(out_path, headers, rows, exact_set, substrings,
                              safe_set, exclusions, sample_count)
        elif mode == "redact":
            out_path = output_dir / f"{out_stem}_redacted.xlsx"
            write_xlsx_redacted(out_path, headers, rows, exact_set, substrings,
                                safe_set, exclusions)
        elif mode == "headers":
            out_path = output_dir / f"{out_stem}_headers.xlsx"
            write_xlsx_headers(out_path, headers)
        else:
            print(f"    Unknown mode: {mode}")
            return False

        print(f"    Output: {out_path}")
        return True

    return False


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--input", "-i", nargs="+", required=True,
        help="One or more CSV/XLSX files (or glob patterns) to sanitize"
    )
    parser.add_argument(
        "--mode", "-m", default="schema",
        choices=["schema", "redact", "headers"],
        help=(
            "schema  = column names + types + safe samples (default)\n"
            "redact  = full data with sensitive columns replaced\n"
            "headers = column names only"
        )
    )
    parser.add_argument(
        "--config", "-c", default=str(DEFAULT_CONFIG),
        help="Path to sensitive column config JSON"
    )
    parser.add_argument(
        "--output-dir", "-o", default=str(OUTPUT_DIR),
        help="Output directory for sanitized files"
    )
    parser.add_argument(
        "--samples", "-n", type=int, default=3,
        help="Number of sample values per non-sensitive column (schema mode)"
    )

    args = parser.parse_args()

    # Load config
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"ERROR: Config not found: {config_path}")
        sys.exit(1)
    config = load_config(config_path)

    output_dir = Path(args.output_dir)

    # Expand input paths
    input_files = []
    for pattern in args.input:
        p = Path(pattern)
        if p.exists():
            input_files.append(p)
        else:
            # Try glob
            import glob
            matches = glob.glob(pattern)
            for m in matches:
                mp = Path(m)
                if mp.suffix.lower() in (".csv", ".xlsx"):
                    input_files.append(mp)

    if not input_files:
        print("ERROR: No CSV or XLSX files found matching the input patterns.")
        sys.exit(1)

    print(f"=" * 60)
    print(f"  DATA SANITIZATION — Mode: {args.mode.upper()}")
    print(f"  Config: {config_path.name}")
    print(f"  Files:  {len(input_files)}")
    print(f"  Output: {output_dir}/")
    print(f"=" * 60)

    # Summarize sensitive patterns
    exact_set, substrings, exclusions = build_sensitive_set(config)
    safe_set = build_safe_set(config)
    print(f"\n  Sensitive patterns loaded:")
    for category, details in config.get("sensitive_patterns", {}).items():
        print(f"    - {category}: {len(details.get('column_names', []))} exact + "
              f"{len(details.get('contains_patterns', []))} substring patterns")

    # Process files
    processed = 0
    for filepath in sorted(input_files):
        if process_file(filepath, args.mode, config, output_dir, args.samples):
            processed += 1

    print(f"\n{'=' * 60}")
    print(f"  DONE — {processed}/{len(input_files)} files processed")
    print(f"  Output: {output_dir}/")
    print(f"{'=' * 60}")

    # Safety reminder
    print(f"\n  ⚠️  REMINDER: Review the output files before committing!")
    print(f"  Check that no personal information remains visible.")
    print(f"  When in doubt, use --mode headers for the safest output.\n")


if __name__ == "__main__":
    main()
