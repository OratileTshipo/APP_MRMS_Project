# Canvas Apps — Reference Material

Permanent reference artifacts for working on the APP-MRMS canvas app outside
Power Apps Studio. Everything here was extracted once (from the original
`.msapp`, the unpacked `SourceCode` layout, or the official Microsoft Learn
Power Apps maker documentation PDF) and is kept so that any future agent or
model can work on the app **without re-running the expensive extractions**.

## Layout

```
reference/canvas-apps/
├── README.md                     ← this manifest
├── msapp-internals/              ← original .msapp internals, unzipped flat
│   ├── Controls/*.json           ← every control definition in the app
│   ├── References/               ← DataSources.json, Themes.json, Templates.json, ModernThemes.json, Resources.json
│   ├── Header.json / Properties.json
│   ├── Resources/PublishInfo.json
│   ├── Assets/Images/*.png       ← embedded images
│   ├── Src/*.pa.yaml             ← same source as src/Src (kept for self-containment)
│   └── AppCheckerResult.sarif    ← static-analysis results from the original app
└── official-docs/                ← page-range text extractions of power-apps-maker.pdf
    ├── pdf-toc.txt               ← document table of contents (first pages)
    ├── pdf-p3500-source-file-format.txt    ← canvas apps source file format (.pa.yaml, SourceCode layout)
    ├── pdf-p3600-coding-guidelines.txt     ← coding guidelines / best practices
    ├── pdf-p3800-coding-guidelines-2.txt   ← more guidelines (naming, delegation, variables)
    └── pdf-p4000-coding-guidelines-3.txt   ← more guidelines (collections, App.Formulas)
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

### official-docs/ (extracted from power-apps-maker.pdf)

`power-apps-maker.pdf` is the complete Microsoft Learn "Power Apps maker"
documentation (6,765 pages, ~404 MB) — too large to keep in the repo or
extract wholesale (full `pdftotext` times out). Instead, only the canvas-apps
relevant page ranges were extracted with Ghostscript:

```bash
gs -q -dNOPAUSE -dBATCH -sDEVICE=txtwrite -sOutputFile=out.txt -f <start> -l <end> power-apps-maker.pdf
```

The filenames encode the starting page. These cover the topics read for this
project:

| File | Topic |
|---|---|
| `pdf-p3500-source-file-format.txt` | Work with canvas apps source file format (`.pa.yaml`, `SourceCode` layout, `Control:`/`Variant:` keywords, only non-default properties serialized) |
| `pdf-p3600-coding-guidelines.txt` | Canvas apps coding guidelines, best-practices guidance |
| `pdf-p3800-coding-guidelines-2.txt` | Naming conventions, delegation, variables best practices |
| `pdf-p4000-coding-guidelines-3.txt` | Collections, `App.Formulas`, more guidelines |

Note: the extracted text files contain the raw page text (including unrelated
adjacent pages in each range). The distilled, actionable guidance is in
`BEST_PRACTICES.md` at the repo root.

## Source of truth

- CSV files in this repo are the **single source of truth** for SharePoint list
  schemas (see README.md at repo root).
- `src/Src/*.pa.yaml` is the editable canvas app source (`SourceCode` layout).
- Round-trip verified: packing `src/` → `.msapp` → unpacking again yields
  byte-identical Src YAML and internal JSON (see CHANGES.md).
