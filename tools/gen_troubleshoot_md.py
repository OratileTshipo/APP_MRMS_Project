#!/usr/bin/env python3
"""Build reference/canvas-apps/troubleshooting/troubleshooting-guide.md from the
pdftotext extraction of troubleshoot-power-platform-power-apps.pdf.

The PDF is Microsoft Learn's "Power Apps troubleshooting" guide (296 pages).
Top-level articles are detected from the document's own TOC (first pages);
page breaks (\f) become '---' separators inside articles.
"""
import re
import subprocess
import sys
from pathlib import Path

PDF = Path(sys.argv[1]) if len(sys.argv) > 1 else \
    Path("../troubleshoot-power-platform-power-apps.pdf")
OUT = Path("reference/canvas-apps/troubleshooting/troubleshooting-guide.md")

# Top-level article titles (from the PDF's TOC + major body sections).
# Matching is prefix-based (page-boundary titles are truncated).
ARTICLES = [
    "Troubleshoot broken connections",
    "Connection errors when running flows in Power Apps",
    "Troubleshoot HTTP 0 responses and other blocked calls",
    "Troubleshoot Power Query issues",
    "Troubleshoot Power Apps flow integration",
    "Common issues and resolutions for Power Apps",
    "Debug canvas apps by using Live monitor",
    "Debug canvas apps without Live monitor",
    "Power Apps troubleshooting strategies",
    "Isolate issues in canvas apps",
    "How to create a minimal repro canvas app",
    "Troubleshoot date and time issues in Power Apps canvas apps",
    "Troubleshoot canvas app performance issues",
    "Troubleshoot startup issues for Power Apps",
    "Troubleshoot common issues when using",
    "Azure key vault errors in wrap for Power",
    "Isolate issues in model-driven apps",
    "How to create a vanilla repro model-driven app",
    "Troubleshoot date and time issues in model-driven apps",
    "Troubleshoot Lookup control issues in",
    "Troubleshoot view issues in model",
    "Troubleshooting grid issues in Power",
    "Troubleshooting ribbon issues in Power",
    "Troubleshooting Word templates",
    "Known issues with document",
    "Troubleshooting server-based",
    "Troubleshooting conditional access",
    "Troubleshoot SharePoint integration",
    "Troubleshooting document",
    "Troubleshoot offline sync errors in the",
    "Troubleshooting startup or sign-in issues",
]

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()

def match_article(title: str, page_text: str):
    """Return the canonical article name if title and a list entry are prefixes of
    each other (page starts are often truncated), else None. Ambiguous short
    prefixes (e.g. date-and-time appears for both canvas and model-driven) are
    disambiguated by keywords in the rest of the page."""
    t = norm(title)
    cands = [art for art in ARTICLES if t.startswith(norm(art)) or norm(art).startswith(t)]
    if not cands:
        return None
    if len(cands) > 1:
        low = page_text.lower()
        has_canvas = "canvas" in low
        has_model = "model-driven" in low
        if has_canvas and not has_model:
            c = [a for a in cands if "canvas" in norm(a)]
            if c:
                return c[0]
        if has_model and not has_canvas:
            c = [a for a in cands if "model-driven" in norm(a)]
            if c:
                return c[0]
    return cands[0]

def main():
    # Extract full text with pdftotext (poppler) preserving layout
    raw = subprocess.run(
        ["pdftotext", "-layout", str(PDF), "-"],
        check=True, capture_output=True, text=True,
    ).stdout
    # Split into pages on form feeds (also drop leading \f on first line)
    pages = [p for p in raw.split("\f") if p.strip()]
    lines_out = []
    toc = []          # (anchor, title)
    seen = set()

    lines_out.append("# Power Apps troubleshooting — extracted text\n")
    lines_out.append(
        "> Extracted from `troubleshoot-power-platform-power-apps.pdf` "
        "(Microsoft Learn, 296 pages, 21.7 MB) with `pdftotext -layout`. "
        "Companion to the curated `official-docs/` extractions of "
        "`power-apps-maker.pdf`. Page breaks appear as `---`.\n"
    )
    lines_out.append("## Contents\n")

    body = []

    for page in pages:
        first = page.strip().split("\n", 1)[0].strip()
        art = match_article(first, page)
        if art and art not in seen:
            seen.add(art)
            anchor = re.sub(r"[^a-z0-9]+", "-", art.lower()).strip("-")
            toc.append((anchor, art))
            body.append(f"\n## {art}\n")
        body.append(page.rstrip() + "\n---\n")

    for anchor, title in toc:
        lines_out.append(f"- [{title}](#{anchor})")
    lines_out.append("\n---\n")
    lines_out.extend(body)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines_out), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes, {len(toc)} articles in TOC)")
    for _, t in toc:
        print("  -", t)

if __name__ == "__main__":
    main()
