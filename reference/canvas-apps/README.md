# Canvas Apps — Reference Material

Permanent reference artifacts for working on the APP-MRMS canvas app outside
Power Apps Studio. Everything here was extracted once (from the original
`.msapp`, the unpacked `SourceCode` layout, the Word docs, or the official
Microsoft Learn Power Apps maker documentation PDF) and is kept so that any
future agent or model can work on the app **without re-running the expensive
extractions**.

## Layout

```
reference/
├── canvas-apps/
│   ├── README.md                     ← this manifest
│   ├── msapp-internals/              ← original .msapp internals, unzipped flat
│   │   ├── Controls/*.json           ← every control definition in the app
│   │   ├── References/               ← DataSources.json, Themes.json, Templates.json, ModernThemes.json, Resources.json
│   │   ├── Header.json / Properties.json
│   │   ├── Resources/PublishInfo.json
│   │   ├── Assets/Images/*.png       ← embedded images
│   │   ├── Src/*.pa.yaml             ← same source as src/Src (kept for self-containment)
│   │   └── AppCheckerResult.sarif    ← static-analysis results from the original app
│   ├── msapr-metadata/               ← metadata extracted from the .msapr resources archive
│   │   ├── msapr-header.json
│   │   └── msapp/                    ← Header.json, Properties.json, References/*.json, Resources/PublishInfo.json
│   ├── official-docs/                ← curated page-range text extractions of power-apps-maker.pdf
│   │   ├── pdf-toc.txt               ← document table of contents (first pages)
│   │   ├── pdf-p3500-source-file-format.txt    ← canvas apps source file format (.pa.yaml, SourceCode layout)
│   │   ├── pdf-p3600-coding-guidelines.txt     ← coding guidelines / best practices
│   │   ├── pdf-p3800-coding-guidelines-2.txt   ← more guidelines (naming, delegation, variables)
│   │   └── pdf-p4000-coding-guidelines-3.txt   ← more guidelines (collections, App.Formulas)
│   ├── troubleshooting/              ← full-text markdown extraction of troubleshoot-power-platform-power-apps.pdf
│   │   └── troubleshooting-guide.md  ← all 28 articles, TOC + page breaks (regenerate via tools/gen_troubleshoot_md.py)
│   ├── pdf-scan/                     ← all other page-range probes of the PDF (45 files, named by start page)
│   └── round-trip/                   ← pack → unpack verification output (byte-identical Src tree)
├── docs-extracted/                    ← plain-text extractions of the Word docs
│   ├── brd.txt / brd2.txt             ← BRD/FDS/TDS (pre- and post-schema-update)
│   ├── arch.txt / arch2.txt           ← Architecture Pack (pre- and post-update)
│   ├── phase1.txt / phase2.txt        ← Phase 1 Execution Guide (pre- and post-update)
│   └── urs.txt                        ← URS Stakeholder Validation
└── docs-original/                     ← pre-update .docx originals (backup of the docs before schema alignment)
```

## What each artifact is for

### msapp-internals/ (flat copy of the original app package)

The original `APP-MRMS_Project_app.msapp` is a zip. `pac canvas unpack` splits
it into `src/Src/*.pa.yaml` (editable source) + `src/APP-MRMS_Project_app.msapr`
(resources archive, itself a zip of the classic `msapp/` layout). This folder is
the **same `msapp/` content unzipped flat**, so it can be grepped directly
without unzipping. It is byte-identical to what is inside
`src/APP-MRMS_Project_app.msapr`.

Use it to answer: what controls exist, what is each control's full property
set, which data sources are referenced, what themes/templates are used.

### msapr-metadata/ (extracted from the .msapr)

The small JSON metadata files extracted from the `.msapr` resources archive:
app header, properties (incl. `DocumentAppType`/`DocumentLayoutVersion`), the
data-source connections (`References/DataSources.json` — all 11 SharePoint
lists + samples), and publish info.

### official-docs/ + pdf-scan/ (extracted from power-apps-maker.pdf)

`power-apps-maker.pdf` is the complete Microsoft Learn "Power Apps maker"
documentation (6,765 pages, ~404 MB) — too large to keep in the repo or
extract wholesale (full `pdftotext` times out). Instead, page ranges were
extracted with Ghostscript:

```bash
gs -q -dNOPAUSE -dBATCH -sDEVICE=txtwrite -sOutputFile=out.txt -f <start> -l <end> power-apps-maker.pdf
```

- `official-docs/` holds the curated, canvas-apps-relevant sections (see table
  below); the filenames encode the starting page.
- `pdf-scan/` holds every other probe (45 files, 61–6,600) so the full scan
  coverage is preserved even if the PDF is not available.

| File | Topic |
|---|---|
| `pdf-p3500-source-file-format.txt` | Work with canvas apps source file format (`.pa.yaml`, `SourceCode` layout, `Control:`/`Variant:` keywords, only non-default properties serialized) |
| `pdf-p3600-coding-guidelines.txt` | Canvas apps coding guidelines, best-practices guidance |
| `pdf-p3800-coding-guidelines-2.txt` | Naming conventions, delegation, variables best practices |
| `pdf-p4000-coding-guidelines-3.txt` | Collections, `App.Formulas`, more guidelines |

Note: the extracted text files contain the raw page text (including unrelated
adjacent pages in each range). The distilled, actionable guidance is in
`BEST_PRACTICES.md` at the repo root.

### troubleshooting/ (extracted from troubleshoot-power-platform-power-apps.pdf)

Full-text markdown extraction of the **Microsoft Learn Power Apps
troubleshooting** guide (296 pages, 21.7 MB — `troubleshoot-power-platform-
power-apps.pdf` in the project root). `troubleshooting-guide.md` contains all
28 articles with a clickable TOC; page breaks are `---` separators. Regenerate
with `python3 tools/gen_troubleshoot_md.py ../troubleshoot-power-platform-power-apps.pdf`.
Relevant to this app: *Troubleshoot Power Apps canvas app* (startup/sign-in),
*Debug canvas apps by using/without Live monitor*, *Power Apps troubleshooting
strategies*, *Isolate issues in canvas apps*, *Common issues and resolutions*.

### round-trip/ (pack → unpack verification)

Output of unpacking the **repacked** msapp (`pac canvas pack` then unpack).
The `Src/` tree here is byte-identical to the original unpacked source —
proof that editing `.pa.yaml` and repacking round-trips losslessly.

### docs-extracted/ + docs-original/

- `docs-extracted/` — plain-text versions of the Word docs (grep-friendly).
  `*2.txt` files are the post-schema-update versions; bare names are the
  pre-update extractions.
- `docs-original/` — the pre-update `.docx` files themselves (backed up before
  `update_docs_schema.py` ran), in case the aligned versions need comparison.

## Source of truth

- CSV files in this repo are the **single source of truth** for SharePoint list
  schemas (see README.md at repo root).
- `src/Src/*.pa.yaml` is the editable canvas app source (`SourceCode` layout).
- Round-trip verified: packing `src/` → `.msapp` → unpacking again yields
  byte-identical Src YAML and internal JSON (see CHANGES.md).
- Pristine pre-change snapshots live in `backup/` at the repo root.
