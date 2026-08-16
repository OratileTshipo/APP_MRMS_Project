# APP-MRMS — Session Change Log

Date: 2026-08-16
Repo: `APP_MRMS/` (git, branch `main`)
Single source of truth for SharePoint list schemas: the CSV files in this folder.

---

## 1. Tooling setup

- Installed **Microsoft Power Platform CLI (`pac`)** v2.11.2 as a .NET global tool
  (`dotnet tool install --global Microsoft.PowerApps.CLI.Tool`).
- `dotnet` (SDK 8.0.423 / 10.0.302) was already present under `~/.dotnet` but not on
  PATH. Required env for `pac` to run:
  ```bash
  export PATH="$HOME/.dotnet:$PATH:$HOME/.dotnet/tools"
  export DOTNET_ROOT="$HOME/.dotnet"
  ```
- Installed `python-docx` 1.2.0 (used to update the Word documents).

## 2. msapp unpack (pac CLI)

- Unpacked `APP-MRMS_Project_app.msapp` with the current supported command:
  ```bash
  pac canvas unpack --msapp APP-MRMS_Project_app.msapp --sources APP_MRMS_Unpacked --layout SourceCode --overwrite
  ```
- `SourceCode` layout is the only active schema; `Experimental` (*.fx.yaml) is retired.
- Output: `APP_MRMS_Unpacked/APP-MRMS_Project_app.msapr` (zip holding the original
  `msapp/` JSON: Header, Properties, `Controls/*.json`, `References/*`, SARIF, Assets)
  plus `Src/` with `App.pa.yaml`, `_EditorState.pa.yaml` and one `.pa.yaml` per screen.

## 3. Pack round-trip verification (import safety)

- Packed the unpacked source back to an msapp:
  ```bash
  pac canvas pack --sources APP_MRMS_Unpacked --msapp APP-MRMS_Repacked.msapp --layout SourceCode --overwrite
  ```
- Unpacked the repacked file and compared **every** internal artifact against the
  original. Result: **all files byte-identical** —
  `Header.json`, `Properties.json`, `Resources/PublishInfo.json`, all
  `Controls/*.json`, all `References/*.json`, `AppCheckerResult.sarif`, all
  `Assets/Images/*.png`, and all `Src/*.pa.yaml`.
- The only addition is `packed.json` (pack metadata:
  `LoadFromYaml: true`, client = Pac CLI 2.11.2) — expected and harmless.
- **Conclusion:** the pack/unpack cycle is lossless. Apps built from this source will
  import without failure. Note from Microsoft docs + pac warning: an app packed from
  YAML SourceCode must be opened once for edit in Power Apps Studio after import to
  validate (it loads from the embedded YAML).

## 4. Official documentation reviewed (power-apps-maker.pdf)

- Read the Microsoft Learn "Power Apps maker" PDF (6,765 pages, 404 MB — extracted
  targeted sections with Ghostscript txtwrite):
  - *Work with canvas apps source file format (YAML)* — schema, structure,
    `Control:`/`Variant:` keywords, only non-default properties serialized,
    `\Src` is the only source-control surface.
  - *View source code files for canvas apps* / *Use code view* — Studio YAML is
    read-only; external editing only via Power Platform Git Integration.
  - *Disconnect Git version control* — PASopa retired; pac canvas pack/unpack (preview)
    is the supported CLI path for building msapp files.
- `pac canvas` CLI syntax verified directly from the installed CLI (v2.11.2), since the
  CLI reference lives in the separate Power Platform CLI doc set.

## 5. Code-base review (no changes made to the app source)

- **App (`Src/App.pa.yaml`)** — `OnStart` defines theme colours, filter defaults,
  reference collections (`colProgrammes/colProjects/colActivities/colDirectorates`),
  current-user role resolution (`APP_Users` lookup by `UserAccount.Email`), notifications,
  current FY/month/quarter.
- **9 screens**: `scr_Splash` → `scr_Home` → `scr_Users` → `scr_MyActivities` →
  `scr_Projects` → `scr_Activities` → `scr_Reports` → `scr_Reports_1` → `MainScreen1`.
- **11 connected data sources**: Programmes, Projects, Activities, MonthlyReports,
  APP_Users, Directorates, KPIDefinitions, Notifications, AuditLog, ReportComments,
  EvidenceLibrary (plus static samples CustomGallerySample, ComboBoxSample).
- **Known open items** (candidates for the screen-building task):
  - `scr_MyActivities` navigates to `scr_ReportForm` / `scr_ReportView`, which do not
    exist yet.
  - `scr_Splash` timer has no `OnTimerEnd` (no auto-navigation to Home).
  - `scr_Home` "New Monthly Report" / "View Reports Dashboard" buttons have no
    navigation wired.
  - `scr_Activities` is a copy of the Projects screen; its Save button still patches
    `Projects`.
  - `scr_Reports_1` duplicates `scr_Reports` (Form1_1, delete-confirm variant).

## 6. Word documents updated to the CSV schemas

Backups of the originals: `/tmp/docx_backup/`. Edit script: `update_docs_schema.py`.

### APP-MRMS_BRD_FDS_TDS_v2.docx (§3.2 SharePoint Data Model)
- **Projects**: added `ProjectCode`; `Budget` type corrected Currency → **Single line
  text**; `Directorate` corrected text → **Lookup (Directorates)** (+ `Directorate: Title`
  projection); `Programme` corrected Lookup → **Single line text** (matches
  Directorates.Programme); `FinancialYear` choices → 2026/27 … 2022/23; removed the
  stale "Projects_1 duplicate export" warning.
- **Activities**: added `ActivityCode`, `Directorate`, `ActivityOwner` (split from
  "Owner / ActivityOwner"), `Status` (Active/Completed/Not Started); `DueDayOfMonth`
  (Number) → **`DueDate` (Date only)**.
- **MonthlyReports**: `Activity` projections `DueDayOfMonth` → `DueDate`; `Quarter`
  choices → Q1–Q4 (+ All); removed non-existent `ProgressNarrative` → replaced with
  `ReasonForDeviation`, `RemedialAction`, `Output`; `Status` choices now include
  **Escalated**.
- Prose/flow/code references updated: `ProgressNarrative` → `Output`,
  `DueDayOfMonth` → `DueDate` throughout.

### APP_MRMS_Architecture_Pack.docx (§4 SharePoint Data Model)
- **Programmes**: example names corrected to live values (Programme 1, 2A, 2B, 3, 4).
- **Projects**: added `ProjectCode`, `ProjectGoalDescription`,
  `Directorate (+ Directorate: Title)` Lookup; `Budget` → Single line text;
  `Programme` → Single line text (⚠ not a Lookup); `FinancialYear` choices updated.
- **Activities**: added `ActivityCode`, `ActivityShortDescription`, `Directorate`,
  `DirectorateLabel`, `ProgrammeLabel`, `Project: Reference` projection,
  `ActivityOwner`, `Status`; `DueDayOfMonth` → `DueDate`.
- **MonthlyReports**: added Programme/Directorate/Project label rows, `Activity`
  projections row (incl. `DueDate`), `isFlagged`, `ReasonForDeviation`,
  `RemedialAction`, `Output`; `PlannedActivity` → `PlannedAct` (internal name noted);
  removed `ProgressNarrative`; `Quarter` → Q1–Q4 (+ All).
- **4.10 Users → APP_Users**: renamed section; `Title` → Single line text (display
  name); added `UserAccount` (Person); `Role` now includes **DeputyDirectorME**;
  `Programme` → Single line text; added `Directorate (+ Directorate: DirectorateID)`
  Lookup.
- ERD lookup chain corrected: `APP_Users (Directorate lookup) → Directorates`.

### APPMRMS_Phase1_ExecutionGuide.docx
- List inventory (§1) and Site Contents checklist (§5.1): `ReferenceData` →
  **Directorates** (Directorates is the verified list; ReferenceData has no CSV).
- Lookup chain description corrected to the actual Lookup columns.
- §5.2 spot-check table: column names corrected to live schema
  (`Active`, `Status`, `Supervisor`, `DueDate`, `isFlagged`, …) and a **Directorates**
  row added.
- §5.3 lookup verification text corrected (Projects.Directorate → Directorates;
  Programme is text, not a Lookup).
- §5.4 "ReferenceData seeded" → "Choice data": FinancialYear/Quarter are Choice
  columns per the CSV exports (MonthlyReports.FinancialYear = 2026/27, 2025/26,
  2024/25, All; Quarter = Q1–Q4, All; Projects.FinancialYear = 2026/27 … 2022/23).

### APP-MRMS_URS_Stakeholder_Validation_v1.docx
- No schema content to correct (requirements only; hierarchy note already accurate).
  Left unchanged.

## 7. Git repository

- Created `APP_MRMS/` git repo (branch `main`), initial commit `20dde2e` seeding:
  CSVs, docs, original `.msapp`, unpacked source under `src/`, README, `.gitignore`.
- This session's follow-up commit(s): updated Word docs (aligned to CSV schema),
  `update_docs_schema.py`, `CHANGES.md`.
