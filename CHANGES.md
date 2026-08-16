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
- **9 screens (original pack)**: `scr_Splash` → `scr_Home` → `scr_Users` →
  `scr_MyActivities` → `scr_Projects` → `scr_Activities` → `scr_Reports` →
  `scr_Reports_1` → `MainScreen1`. (Both `scr_Reports_1` and `MainScreen1` have
  since been retired — see §16 and §20.)
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

## 8. Reference material made permanent

- `reference/canvas-apps/msapp-internals/` — the original `.msapp` internals
  unzipped flat (Controls/*.json, References/*, Header.json, Properties.json,
  Resources/PublishInfo.json, Assets/Images, Src/*.pa.yaml, AppCheckerResult.sarif).
  Byte-identical to the content inside the committed `src/APP-MRMS_Project_app.msapr`;
  kept flat so it can be grepped without unzipping.
- `reference/canvas-apps/msapr-metadata/` — small JSON metadata extracted from the
  `.msapr` (header, properties, data-source connections, publish info).
- `reference/canvas-apps/official-docs/` — curated page-range text extractions of
  `power-apps-maker.pdf` (the full Microsoft Learn Power Apps maker docs,
  6,765 pp, ~404 MB, too large to keep/extract wholesale) covering the canvas-apps
  topics: source file format (p~3500), coding guidelines (p~3600–4000).
  Filenames encode the starting page; see `reference/canvas-apps/README.md`.
- `reference/canvas-apps/pdf-scan/` — all remaining page-range probes of the PDF
  (45 files, pages 61–6,600) so full scan coverage survives without the PDF.
- `reference/canvas-apps/round-trip/` — unpacked output of the **repacked** msapp;
  `Src/` is byte-identical to the original unpacked source (pack→unpack round-trip proof).
- `reference/docs-extracted/` — plain-text extractions of the Word docs
  (`*2.txt` = post-schema-update, bare names = pre-update).
- `reference/docs-original/` — pre-update `.docx` originals, backed up before
  `update_docs_schema.py` ran.
- `BEST_PRACTICES.md` added at repo root — distilled canvas-apps best practices
  and gap analysis of the current app (delegation, naming, collections,
  App.Formulas, source-format workflow).
- `backup/` — pristine pre-change snapshots: `original-pack/APP-MRMS_Project_app.msapp`
  (byte-identical to the top-level pack) and `unpacked/` (byte-identical to the
  original `pac canvas unpack` output). Restore points in case edits break the app.
- README.md refreshed to document all of the above and the current app state.

## 9. App source change — scr_Activities Save now writes to Activities

File: `src/Src/scr_Activities.pa.yaml` (editable source; unchanged elsewhere).

### Save_btn_1.OnSelect (active block)
- **Before:** `Patch(Projects, If(varMode = "New", Defaults(Projects), varSelectedProject), {...})`
  writing Projects-only columns (`PriorityChallenge`, `ProjectGoalDescription`,
  `KeyDeliverable`, `AnnualTarget`, `Budget`, `Responsibility`, `CompletionDate`,
  `FinancialYear`).
- **After:** `Patch(Activities, If(varMode = "New", Defaults(Activities), varSelectedProject), {...})`
  writing the **Activities.csv** columns:
  - `Title` ← `Reference_txt_1.Text` (free-text identifier, mirroring the Title pattern in Activities.csv)
  - `ActivityCode` ← `Reference_txt_1.Text`
  - `ActivityDescription` ← `ProjectGoalDescription_txt_1.Text`
  - `ActivityShortDescription` ← `PriorityChallenge_txt_1.Text`
  - `ProgrammeLabel` ← `ProjectProgramme_drp_1.Selected.Title` (text column per CSV)
  - `Directorate` ← `ProjectDirectorate_drp_1.Selected.DirectorateID` (text per CSV)
  - `DirectorateLabel` ← `ProjectDirectorate_drp_1.Selected.DirectorateName`
  - `ActivityOwner` ← `Responsibility_cmb_1.Selected.UserAccount` (User column per CSV)
  - `StartDate` / `EndDate` ← the two date pickers
  - `Active: true`
  - `Status` ← `ProjectStatus_drp_1.Selected.Value`
- Post-save refresh switched from `colProjectsInScope` (Projects) to
  `colActivitiesInScope` = `Filter(Activities, varCanViewAllReports || Directorate = varUserDirectorate)`.
- Notify message: "Activity saved successfully."

### ProjectStatus_drp_1 (form dropdown)
- `Items` rebound from `Choices(Projects.Status)` (Active/Closed/Cancelled) to
  **`Choices(Activities.Status)`** (Active/Completed/Not Started) and the New-mode
  default to `LookUp(Choices(Activities.Status), Value = "Active")`, so the value
  written by Save is a valid Activities choice.

### Notes / intentionally left
- The two commented-out legacy blocks (non-`_1` variants patching Projects) are dead
  code and were left as-is.
- Form control names/labels are still the Projects-copy ones (PriorityChallenge,
  Budget, FinancialYear…) — relabelling the form UI to the Activities schema is a
  separate task. Budget/FinancialYear/KeyDeliverable/AnnualTarget are still required
  by the Save validation but are no longer written (Activities has no such columns).
- `scr_Activities` gallery/filters still operate on `colProjectsInScope` (Projects) —
  wiring the list pane to `colActivitiesInScope` is a follow-up.

### Verification
- `pac canvas pack --sources src --msapp … --layout SourceCode` succeeds (YAML valid;
  pack emits only the standard "validate in Studio after import" notice).

## 10. App source change — new report screens + fixed navigation & splash

Files: `src/Src/scr_ReportForm.pa.yaml`, `src/Src/scr_ReportView.pa.yaml` (new),
`src/Src/scr_MyActivities.pa.yaml`, `src/Src/scr_Splash.pa.yaml`,
`src/Src/_EditorState.pa.yaml`.

### New screen: scr_ReportForm
- MonthlyReports create/edit form (plain controls + `Patch`, consistent with the
  app's other forms). Consumes context params from navigation:
  `selectedActivityID` (Activities.ID) and optional `editReportID`
  (MonthlyReports.ID).
- OnVisible sets `varReportMode` (New/Edit), `varReportActivity`
  (LookUp colActivities), `varEditReport` (LookUp MonthlyReports).
- Editable fields per MonthlyReports.csv: Title, ReportingMonth, Quarter,
  FinancialYear, PlannedActivity, PercentageComplete, Status, ReasonForDeviation,
  RemedialAction, Output. Read-only context card shows activity title/description
  and programme · directorate labels.
- Save: validates required fields, `Patch(MonthlyReports, If(New, Defaults,
  varEditReport), {...})` writing the CSV-schema columns (Activity lookup,
  ActivityOwnerLabel/ProgrammeLabel/DirectorateLabel denormalised from the
  activity; Version 1 on new), then navigates back to scr_MyActivities.

### New screen: scr_ReportView
- Read-only report detail screen. Consumes `viewReportID` (MonthlyReports.ID),
  sets `varViewReport` on OnVisible. Displays status/period/percentage cards plus
  title, planned activity, output, deviation/remedial, owner, submitted/reviewed
  by, rejection reason. Back button → scr_MyActivities.

### scr_MyActivities fixes
- Gallery `ActItems_gal.Items` was bound to raw `colActivities`; the action button
  read `ThisItem.ActivityID`/`ReportID`/`Status.Value` which only exist on the
  joined `colMyActivityStatus` collection built in OnVisible. Bound the gallery to
  `Filter(colMyActivityStatus, …)` (status filter only; FY/month are fixed to the
  current period in OnVisible) and updated the row field references
  (ActivityName, DueDay, ReportStatus, ActionLabel).
- Action button now navigates on **ReportStatus**: Not Started → scr_ReportForm
  (new), Draft/Rejected → scr_ReportForm (edit with editReportID), Approved →
  scr_ReportView, else informational notify. Labels use ActionLabel.

### scr_Splash fix
- `Timer_Splash` had no `OnTimerEnd` (timer started but never navigated). Added
  `OnTimerEnd: =Navigate(scr_Home, ScreenTransition.Fade)`; app now proceeds from
  the splash after the 1.8 s duration.

### Screen registration
- `_EditorState.pa.yaml` ScreensOrder now includes scr_ReportForm and
  scr_ReportView (inserted after scr_MyActivities).

### Verification
- `pac canvas pack` succeeds; unpacking the packed msapp reproduces all 12 screens
  including the two new ones (round-trip intact).

## 11. App source change — best practices applied (App.Formulas, delegation, dead code)

Per BEST_PRACTICES.md, applied to the live screens (2026-08-16).

### App.pa.yaml — App.OnStart Set() → named formulas (App.Formulas)
- Converted the immutable `Set()` calls in OnStart to **named formulas** (lazy,
  immutable, re-evaluate on dependency change): theme colours (varNavy…varBgLight),
  responsive breakpoints (varIsMobile/varIsTablet), current-user identity and derived
  role/scope (varUserEmail, varUserFullName, varCurrentUserRecord, varUserRole,
  varUserDirectorate, varUserProgramme, varUserDirectorateID, varCanViewAllReports),
  and reporting-period defaults (varCurrentFY, varCurrentMonth, varCurrentQuarter,
  varTodaysDate). Serialised as `App.Properties` entries (`name: =formula`); verified
  they round-trip through `pac canvas pack/unpack` and are carried in the embedded
  YAML (`LoadFromYaml: true`).
- **OnStart keeps only genuinely mutable state**: filter defaults (mutated by screen
  controls), the reference collections (screens re-collect colProgrammes /
  colDirectorates on OnVisible), notifications, and UI-state flags.
- Deleted the large `/* … */` commented block (the previous OnStart draft) and the
  commented-out `colKPIDefinitions` load.
- Naming note: the `var` prefix was **kept** on the named formulas (convention would
  drop it) because renaming would touch every `=var…` reference across 12 screens;
  the substance of the practice — immutable values as formulas, small fast OnStart —
  is applied.

### scr_Home — delegation fixes + dead code removal
- **colReportsInScope**: base filter was a 4-way OR across columns
  (`varCanViewAllReports || DirectorateLabel = … || DirectorateLabel = … ||
  ProgrammeLabel = …`) — not delegable on SharePoint. Replaced with a **role-first
  Switch** (per the BRD design): Administrator/DeputyDirectorME → MonthlyReports;
  ProgrammeManager → `Filter(MonthlyReports, ProgrammeLabel = varUserProgramme)`;
  Supervisor → `Filter(MonthlyReports, DirectorateLabel = varUserDirectorateID)`
  (data stores the short code — see MonthlyReports.csv); Contributor →
  `Filter(MonthlyReports, SubmittedBy.Email = varUserEmail)`. Each branch is a simple
  delegable single-column filter.
- **Overdue KPI fix**: the `colOverdueItems` ClearCollect was commented out (`/* */`)
  even though the live KPI cards filter on it (`CountRows(Filter(colOverdueItems, …))`),
  so the overdue counts were always 0. Restored the collection build.
- **Accidental comment-out fixed by deletion**: a `/*/` … `/*` typo (line 114 `/*`
  was meant to be `*/`) had swallowed sections 8–10 of OnVisible — the flagged-items
  block, the whole `colProgrammeProgress` build, and the `colMonthlyTrend` build.
  Neither collection is referenced by live controls (the programme-progress and
  trend galleries carry their own inline formulas), so the entire dead region was
  deleted and the remaining sections renumbered.
- **Inline galleries now filter the collected `colActivities`** instead of raw
  `Activities`: `MonthlyTrend_gal.Items` (`dueThisMonth`) and
  `ProgrammeProgress_gal.Items` (Distinct + `progActivities`) — same data, local
  execution, no delegation row-limit exposure. `colActivities` is refreshed at the
  top of scr_Home.OnVisible so newly created activities still appear.

### scr_Projects & scr_Activities — delegation fix + dead code removal
- **colProjectsInScope** base filter was a 3-way OR
  (`varCanViewAllReports || Directorate.Value = … || Directorate.Value = …`).
  Replaced with a **role-first If**: `If(varCanViewAllReports, Projects,
  Filter(Projects, Directorate.Value = varUserDirectorate))`. (The
  `= varUserDirectorateID` clause never matched — a Lookup's `.Value` is the full
  name, matching varUserDirectorate.)
- Deleted the two large `/* … */` commented alternative OnVisible blocks in each screen.
- scr_Activities header comment corrected (was a stale copy of scr_Projects'; the
  list pane still operates on Projects — see §9).

### Verification
- `pac canvas pack` succeeds and unpack reproduces the source **byte-identical**
  (`diff -rq` clean) — the app remains safe to import.

## 12. App source change — scr_Activities rebuilt as a true Activities master-detail

scr_Activities was a copy of scr_Projects: only the Save button wrote to Activities;
 the list pane, filters, form fields and selection state still operated on Projects
 (colProjectsInScope / varSelectedProject / Projects columns). The screen has now
 been rebuilt (1669 lines) as a clean Activities master-detail:

### OnVisible
- Builds **colActivitiesInScope** = role-first, delegable scope:
  `If(varCanViewAllReports, Activities, Filter(Activities, DirectorateLabel = varUserDirectorate))`
  (Activities.DirectorateLabel is text = directorate full name, matching
  varUserDirectorate). No more Projects.
- `varSelectedActivity` (renamed from varSelectedProject) defaults to the first row.
- Rebuilds reference + filter collections: colProgrammes / colDirectorates for the
  form, colProgrammesFilter / colDirectoratesFilter / colStatusFilter
  (`Choices(Activities.Status)`) for the filter bar.

### List pane (master)
- Search (title/code/short description/description) + Programme / Directorate /
  Status filter dropdowns, then a gallery over the filtered colActivitiesInScope.
- Row shows Title, status colour chip (Active green / Completed grey / Not Started
  amber), Directorate · Programme, and Due date (falls back to Frequency).
- Result count = `CountRows(ActivityItems_gal.AllItems)`.

### Detail form
- Fields per Activities.csv (Power Apps field names verified against the
  DataSources.json schema): Title, ActivityCode, ActivityShortDescription,
  ActivityDescription (multiline), Frequency (Choice), ProgrammeLabel,
  DirectorateLabel (cascades off Programme), ActivityOwner + Supervisor
  (APP_Users comboboxes), StartDate / EndDate / DueDate (date pickers), Status
  (Choice, defaults to Active on New), Active (toggle).
- Save: validates required fields via `varActivityFormValid`, then
  `Patch(Activities, If(varMode = "New", Defaults(Activities), varSelectedActivity), {…})`
  writing Title, ActivityCode, ActivityDescription, ActivityShortDescription,
  Frequency, ProgrammeLabel, **Directorate (lookup, `{Id: …}`)**,
  DirectorateLabel, ActivityOwner, Supervisor, StartDate, EndDate, DueDate,
  Active, Status. Refreshes colActivitiesInScope and notifies success only on the
  valid path.
- New / Edit / Cancel / **Delete** (with an inline confirm banner → `RemoveIf`)
  complete the CRUD flow.
- Control names cleaned (no `_1`/`_6`/`_7` copy-paste suffixes); all dead
  commented Projects blocks from the copied screen were dropped.

### Verification
- `pac canvas pack` succeeds and unpack reproduces the source **byte-identical**
  (`diff -rq` clean). Note: pac validates YAML structure, not Power Fx semantics —
  open the app once in Studio after import to validate the formulas.

## 13. Verification pass — App Checker findings fixed + documentation comments

### Background
Requested a full verification of all prior work ("make sure nothing breaks"). Playwright
cannot test a canvas app from this environment (no Power Apps runtime/credentials), so the
strongest available checks were run instead:
1. Full `pac canvas pack` → `pac canvas unpack` round trip (byte-identical source).
2. New static verifier `tools/verify_powerfx.py` (paren/quote balance, control references,
   variable definitions, navigation targets, Patch column audit against the CSV schemas and
   DataSources.json) — **13,182 formulas, 0 errors, 0 warnings**.
3. **App Checker SARIF deep-dive** — the `AppCheckerResult.sarif` carried inside the original
   pack contains 797 findings; 45 are **High** (formula errors) and were triaged against the
   current source. The SARIF travels with the pack, so these errors would also surface in
   Studio on import.

### High-severity formula errors fixed (5 root causes → ~45 findings)

| Location | Error | Root cause | Fix |
|---|---|---|---|
| `scr_Users` cmb_RegEmail.Items | `app-ErrUnknownNamespaceFunction` + ~25 cascading `.Selected`/`.UserPrincipalName`/`.Mail`/`.JobTitle`/type errors | `Office365Users.SearchUser(...)` no longer exists (removed from the connector) | → `Office365Users.SearchUserV2(...)` |
| `scr_MyActivities` OnVisible | `app-ErrInvalidName`/`InvalidDot` ×5 | `ActivityOwner.Email` used to filter **MonthlyReports** (that list has only the text `ActivityOwnerLabel`); `Act.'Activity: ActivityShortDescription'` and `Act.DueDay` don't exist on **Activities** (`ActivityShortDescription` is plain text; the date column is `DueDate`) | removed the owner predicate (redundant — `Act` is already the user's own activity); → `Act.ActivityShortDescription`; → `Day(Act.DueDate)` |
| `scr_MyActivities` ActRowAction_btn.OnSelect | `app-ErrInvalidName` (Fade) | navigation used bare `Fade` instead of `ScreenTransition.Fade` (introduced in the earlier nav fix) | → `ScreenTransition.Fade` ×3 |
| `scr_MyActivities` ActHdrRAG_ico | `app-ErrInvalidName` (CircleFill) | `Icon.CircleFill` is not in the Icon control's enum | converted control to `Circle@2.3.0` shape (same as the row RAG dots) |
| `scr_Home` MonthlyReport_gal.Items | `app-ErrInvalidName` (ProgressNarrative) + `app-ErrInvalidArgs-Func` (Lower) | `ProgressNarrative` is not a MonthlyReports column; also a stray trailing `\|\| (varHomeFilter…)` block made the whole Filter predicate always-true (dropdowns/search silently disabled) | search term → `Output`; stray block removed |

Field names were verified against the authoritative `DataSources.json` embedded in the pack
(internal names, display names, and `ConnectedDataSourceInfoNameMapping`) plus the CSV
schema files. Findings that were already resolved by earlier work (e.g. `scr_ReportForm` /
`scr_ReportView` invalid-name flags from before those screens existed) were left as-is.

### Documentation comments
Added `//` block comments (Power Fx comments — the only kind that survive pack → import →
unpack; YAML `#` comments are discarded by pac) to the key logic blocks across the app:
App.pa.yaml (named formulas + OnStart sections, already documented), screen OnVisible
loaders, Save/Submit/Delete handlers, gallery Items formulas, filter dropdowns, search box,
and the user-search combobox. Comments explain intent/why per canvas-apps best practice;
the app already used section-header style, which was extended rather than replaced.

### Verification
- `tools/verify_powerfx.py`: **13182 formulas, 0 errors, 0 warnings**.
- `pac canvas pack` succeeds; unpack reproduces the source **byte-identical** — safe to import.
- Reminder (as before): pac validates YAML structure, not Power Fx semantics — open once in
  Studio after import to confirm; the SARIF in the import will no longer carry the fixed errors.

## 14. App source change — scr_Home action buttons wired

- **New Monthly Report** (`Button2`) now navigates to `scr_ReportForm`, passing the
  user's first own activity (`colMyActivities`) as `selectedActivityID` — this is the
  context the form needs to patch `Activity: { Id: … }` and denormalise the
  owner/programme/directorate labels. Falls back to a blank ID when the user has no
  activities.
- **View Reports Dashboard** (`ViewReportsDashboard_lbl` + `ViewReportsDash_ico`) now
  navigate to `scr_Reports`.
- **scr_ReportForm Save guard**: added an `IsBlank(varReportActivity)` branch so a
  report cannot be saved without an activity (previously the Patch would have written a
  blank Activity ID when the form was opened without context).

Verified: `tools/verify_powerfx.py` (13,186 formulas, 0 errors) and pack→unpack round
trip byte-identical.

## 15. scr_Activities form fields — confirmed relabeled; top-level pack refreshed

- **Confirmed**: `scr_Activities` form fields were already relabeled to the
  Activities.csv schema in the §12 rebuild — the form now shows ACTIVITY TITLE,
  ACTIVITY CODE, SHORT DESCRIPTION, ACTIVITY DESCRIPTION, FREQUENCY, PROGRAMME,
  DIRECTORATE, ACTIVITY OWNER, SUPERVISOR, START DATE, END DATE, DUE DATE, STATUS,
  ACTIVE. No PriorityChallenge / Budget / FinancialYear remain anywhere in that
  screen (they now only exist in scr_Projects, where they belong).
- **Root cause of the confusion**: the top-level `APP-MRMS_Project_app.msapp` was
  still the *original* pack (byte-identical to `backup/original-pack/`, SHA
  74faade…), so importing it showed the old Projects-copy labels even though the
  source had been rebuilt.
- **Fix**: repacked `src/` → top-level `APP-MRMS_Project_app.msapp`
  (`pac canvas pack --overwrite`). Verified the packed file now contains the
  Activities-schema labels and zero PriorityChallenge references in scr_Activities;
  all 13 screens present. The pristine original remains in `backup/`.

## 16. scr_Reports_1 duplicate retired → repurposed as Approved Reports dashboard

- **Problem**: `scr_Reports_1` was a full duplicate of `scr_Reports` (same CRUD form,
  every control suffixed `_1`/`_6`/`_7`/`_8`, plus a delete-confirm dialog variant).
  Nothing in the app navigated to it — dead weight flagged in BEST_PRACTICES §3.
- **Decision**: repurpose, not delete — the Home "APPROVED" KPI had no drill-down, so
  a read-only **Approved Reports dashboard** adds real value.
- **What changed**:
  - `scr_Reports_1.pa.yaml` → **`scr_ApprovedReports.pa.yaml`** (screen key + file
    renamed; `_EditorState.pa.yaml` ScreensOrder updated).
  - Full rebuild (34 KB) as a read-only dashboard: navy header with back button,
    FY / Programme / Directorate / Quarter filter bar + Clear Filters,
    three KPI cards (TOTAL APPROVED, APPROVED THIS FY, APPROVED THIS MONTH), search
    box (title/output), and a gallery of approved reports. No edit form, no delete.
  - `OnVisible` builds **colApprovedReports** with the same role-first delegable
    scope as scr_Home's colReportsInScope (`Status.Value = "Approved"` + role filter;
    Supervisor matches on `DirectorateLabel = varUserDirectorateID`).
  - Gallery rows drill into `scr_ReportView` passing
    `{viewReportID: ThisItem.ID, returnTo: "Approved"}`.
  - **scr_ReportView back button is now context-aware**: OnVisible captures
    `varViewReturnTo = Coalesce(returnTo, "MyActivities")`; both back controls
    (header icon + bottom button) return to `scr_ApprovedReports` when entered from
    the dashboard, else to `scr_MyActivities` (unchanged behaviour for existing
    paths). Bottom button label switches accordingly.
  - **scr_Home entry point**: the APPROVED KPI card's subtitle (previously the dead
    text "placeholder") is now "View approved reports →" and navigates to
    `scr_ApprovedReports`.
- **Tooling note**: this pac version (2.11.2) crashes with a NullReferenceException
  on the deprecated Experimental unpack layout — even on the pristine original pack.
  The supported `--layout SourceCode` works; all round-trips now use it explicitly.
- Verified: `tools/verify_powerfx.py` (9,995 formulas across 13 files, 0 errors),
  pack→unpack round trip byte-identical, embedded YAML in the packed msapp matches
  source byte-for-byte, `scr_Reports_1` absent from / `scr_ApprovedReports` present
  in the packed app. Top-level `APP-MRMS_Project_app.msapp` repacked with
  `--layout SourceCode`.

## 17. New screen — scr_ReportActivities (Activities → Report master-detail)

- **Purpose** (product decision): the reporting screen is an Activities
  master-detail — the left pane lists activities; clicking one opens the
  MonthlyReports **report form in the detail pane** so the user reports on the
  selected activity inline.
- **Master list scope** (role-based, per product decision):
  - `varCanViewAllReports` (Administrator / DeputyDirectorME) → **all** active
    activities (`colReportActivities = Filter(Activities, 'Active ' = true)`).
  - Everyone else → **only their own** activities
    (`Filter(Activities, ActivityOwner.Email = varUserEmail, 'Active ' = true)`).
  - Search (title/code/short description/description) + Programme / Status
    dropdowns filter the gallery over `colReportActivities`.
- **Detail pane**: inline report form (Title, Reporting Month, Quarter, Financial
  Year, Planned Activity, % Complete, Status, Reason for Deviation, Remedial
  Action, Output) defaulting month/quarter/FY to the current period. Gallery
  OnSelect sets `varReportActivity` + resets to New mode; **Save** validates
  required fields then `Patch(MonthlyReports, Defaults(MonthlyReports), {…})`
  with the same denormalised activity fields as scr_ReportForm
  (Activity lookup `{Id, Value}`, ActivityOwnerLabel, ProgrammeLabel,
  DirectorateLabel), notifies success and stays on screen for the next report.
  Cancel clears the selection.
- **Wiring**: registered in `_EditorState.pa.yaml`; the previously-dead
  "Monthly Reports" (CalendarBlank) sidebar icon now navigates here on ALL
  screens (scr_Home/scr_Projects/scr_Activities/scr_MyActivities/scr_Users/
  scr_Reports); scr_Home "New Monthly Report" now opens this screen
  (scr_ReportForm remains reachable from scr_MyActivities for per-activity edits).
- Verified: `tools/verify_powerfx.py` (10,543 formulas across 14 files, 0 errors),
  pack→unpack round trip byte-identical, all Navigate targets resolve.
  Top-level `APP-MRMS_Project_app.msapp` repacked with `--layout SourceCode`.

## 18. CSV data normalization (Activities.csv + Directorates.csv + APP_Users.csv)

- **Problem** (found during the scr_Activities wiring audit): the role filter
  `DirectorateLabel = varUserDirectorate` matched almost nothing because
  Activities.csv labels were inconsistent (typos, case, trailing spaces,
  `&`/`,` variants), and the Risk/Internal Control family was split across
  RIC / RISK / IC with mismatched names. 349 of 516 rows matched no canonical
  directorate; the RIC user saw **zero** activities.
- **Product decisions** (user-confirmed):
  - RISK and IC stay **separate** directorates, with cleaned names
    (`Risk Management`, `Internal Control`).
  - **RIC (Risk and Internal Control) is retired**: `Active=False` in
    Directorates.csv; the only APP_Users row on RIC (Oratile Tshipo) was
    reassigned to **Internal Control** (IC).
- **What changed**:
  - `tools/normalize_activities.py` rewrites Activities.csv **DirectorateLabel**
    from the authoritative `Directorate` short-code column → canonical
    Directorates.csv name (blank-code rows resolved via ActivityCode/Title prefix
    or fuzzy label) and maps every **ProgrammeLabel** variant to the canonical
    Programmes.csv titles. Only the two label columns change — all other bytes
    (multi-line ActivityDescription fields, ListSchema blob) preserved exactly.
  - 242 directorate-label rows + 22 programme-label rows fixed; all 516 rows now
    canonical. The one swapped row (id 241) had label↔programme transposed — fixed.
  - Directorates.csv: `RISK MANAGEMENT ` → `Risk Management`,
    `INTERNAL CONTROL` → `Internal Control`, RIC retired (`Active=False`).
  - APP_Users.csv: Oratile Tshipo → `Internal Control` / `IC`.
- **Mapping report**: `reference/data-normalization-report.md` (generated from the
  git diff; regenerable with `tools/gen_normalization_report.py`).
- **Effect**: the RIC user now matches 60 activities; every directorate/programme
  filter dropdown value now matches the data exactly. Note: the live SharePoint
  lists need the same cleanup to match the CSVs.

## 19. scr_ReportActivities — load existing report for activity/period (Edit mode)

- **Request**: the detail pane should load an existing report for the selected
  activity + period instead of always starting a new one.
- **New named formula** `fnReportForCurrentPeriod` (App.Formulas):
  `First(Filter(MonthlyReports, Activity.Id = varReportActivity.ID,
  'FinancialYear '.Value = varCurrentFY, ReportingMonth.Value = varCurrentMonth))` —
  the existing report for the selected activity in the current FY + reporting month.
  Re-evaluates whenever `varReportActivity` changes.
- **Form behaviour** (OnVisible, gallery OnSelect, Save, Cancel): after setting
  `varReportActivity`/`varEditReport`, `varReportMode` is now `"Edit"` when a report
  exists for the activity + current period, else `"New"`. Because Power Apps only
  re-evaluates `Default` on `Reset()`, every form control (`RepActTitle_txt` …
  `RepActOutput_txt`, the three period dropdowns, `RepActFormStatus_drp`) is
  explicitly `Reset()` after the state changes so switching activities actually
  reloads the loaded record.
- **Save** now `Patch(MonthlyReports, If(varReportMode = "New", Defaults(MonthlyReports),
  varEditReport), …)` — inserts on New, updates the loaded record on Edit (Version kept
  via `Coalesce(varEditReport.Version, 1)`), then reloads the record so the form stays
  in Edit mode with the saved values. Notify text distinguishes "Report saved." vs
  "Report updated."; the Save button label switches to "Update Report" and the mode
  label shows "Editing existing report · …" in Edit mode.
- **Bug fixed**: Save's required-field validation checked `RepActStatus_drp` (the
  filter-bar dropdown, which always has a selection) instead of the form's
  `RepActFormStatus_drp` — the "Status required" check could never fire. Now checks
  `RepActFormStatus_drp.Selected`.
- **Verifier improvement**: `tools/verify_powerfx.py` var/collection reference checks
  are now a second pass after all files' definitions are collected, so cross-file
  references (e.g. App.pa.yaml named formulas referencing vars Set in screen files)
  no longer produce false positives.
- Verified: `tools/verify_powerfx.py` (10,544 formulas, 0 warnings, 0 errors), pack→
  unpack round trip byte-identical, packed app contains the formula + Edit logic.
  Top-level `APP-MRMS_Project_app.msapp` repacked with `--layout SourceCode`.

## 20. Retire the empty MainScreen1 (no-duplicate-screens cleanup complete)

- **Problem**: `MainScreen1` was a 13-line empty screen left over from the original
  template (only `Fill` + `LoadingSpinnerColor`, no children). Nothing navigated to it
  and it was never the start screen (`StartScreen: scr_Splash`), so it was dead weight
  in the app — the last item from the BEST_PRACTICES.md row-3 cleanup.
- **The one wrinkle**: `scr_Reports.pa.yaml` referenced `MainScreen1.Size` in 4
  responsive formulas (sidebar `FillPortions`/`Visible`, back-button `Visible`).
  `MainScreen1` was never displayed, so reading its `Size` was a fragile legacy
  template pattern.
- **Fix**: replaced all 4 references with the canonical **`App.Size = ScreenSize.Small`**
  (the documented App-object property returning the `ScreenSize` enum — same semantics,
  works regardless of which screen is active), then deleted `MainScreen1.pa.yaml` and
  removed it from `_EditorState.pa.yaml` ScreensOrder.
- **Result**: 11 screens remain (scr_Splash, scr_Home, scr_Users, scr_MyActivities,
  scr_ReportForm, scr_ReportView, scr_Projects, scr_Activities, scr_ReportActivities,
  scr_Reports, scr_ApprovedReports) — the no-duplicate-screens cleanup is now complete.
- Verified: `tools/verify_powerfx.py` (10,542 formulas across 13 files, 0 warnings,
  0 errors), pack→unpack round trip byte-identical, packed app has 13 YAML files with
  no `MainScreen1`. Top-level `APP-MRMS_Project_app.msapp` repacked with
  `--layout SourceCode`.

## 21. CI: screen-registry guard + GitHub Actions workflow

- **Request**: a CI check that fails if any screen file exists without a matching
  `_EditorState` entry (the drift that would silently drop a screen from the app).
- **New tool** `tools/check_screen_registry.py` — standalone, dependency-free check
  that scans `src/Src/*.pa.yaml` (excluding `App.pa.yaml` / `_EditorState.pa.yaml`)
  and the `ScreensOrder` list, failing (exit 1) on **both** directions:
  1. a screen file with no matching ScreensOrder entry, and
  2. a ScreensOrder entry with no matching screen file (stale registration).
  Screen names are read from the file's `Screens:` block (with a filename fallback)
  so renames stay in sync. Accepts `--src` / `--editor` overrides for testing.
- **New workflow** `.github/workflows/ci.yml` (GitHub Actions, ubuntu-latest,
  Python 3.11) — runs on every push/PR: the registry check plus the existing
  `tools/verify_powerfx.py` static verifier. No `pac`/.NET needed, so it runs
  anywhere.
- Verified: registry check passes on the current tree (11 files ↔ 11 entries) and
  fails with exit 1 on both mismatch directions (negative-tested with a scratch
  directory); workflow YAML parses; verifier still 0 errors.

## 22. Navigation audit (BEST_PRACTICES row 4) + header/sidebar duplication measure (row 8)

### Row 4 — no dangling references: audit result
Systematically scanned every Icon/Button across all 11 screens for missing `OnSelect`
and cross-checked the verifier (0 dangling Navigate targets). **Verified already wired**:
scr_Splash timer → Home (§8), scr_Home action buttons (§14), all CRUD buttons
(block-form `OnSelect`), scr_Users register submit, scr_Reports classic-form buttons.

**Found and fixed:**
1. **scr_Home sidebar rail was entirely unwired** — `Home_ico`, `MonthlyReports_ico`
   (CalendarBlank), `Activities_ico` (ListWatchlistRemind), `Icon1_4` (People) had no
   OnSelect, while the identical rail navigates on every other screen. Wired them to
   scr_Home / scr_ReportActivities / scr_MyActivities / scr_Users (same targets &
   transitions as sibling screens).
2. **scr_Home KPI arrows dead** — `AllProgrammes_ico` and `ViewAllReports_ico`
   (next to "All Programmes" / "View All Reports") had no OnSelect → now both
   `Navigate(scr_Reports, ScreenTransition.Fade)` (matching `ViewReportsDash_ico`).
3. **scr_MyActivities `Home_ico_2` dead** — no OnSelect → now `Navigate(scr_Home)`.
4. **RadarActivityMonitor inconsistency** — the "Activities" rail icon navigated to
   `scr_MyActivities` on 4 screens (self-navigation on scr_MyActivities itself) but
   to `scr_Activities` on scr_Activities. Fixed all 4 → `scr_Activities`; the
   separate `ListWatchlistRemind` icon remains the MyActivities link (→ scr_MyActivities).

**Deliberately left non-interactive** (decorative, not bugs): search-magnifier icons
paired with text boxes, bell/notification icons, and the Trending/Settings/Support
rail footer (dead on every screen — candidates for removal or wiring in Phase 2).

### Row 8 — components for repeated UI: duplication measured
- **~1,117 lines of near-identical rail YAML** across 6 screens: 9 icons × ~22 lines
  ≈ 197 lines each on scr_Activities / scr_MyActivities / scr_Projects / scr_Users /
  scr_Reports, plus a 6-icon ~132-line subset on scr_Home.
- The rail differs between screens **only** by control-name suffixes (`_1`…`_6`),
  the active-screen highlight, and one transition constant — classic component
  material. The §22 drift (Home's rail unwired) is exactly the failure mode a
  shared component prevents.
- **Recommendation (Phase 2)**: extract `cmp_NavRail` (params: active screen,
  optional back target) + `cmp_AppHeader` into a component library; screens then
  declare one component instead of ~200 lines each. This is a Studio-side
  refactor — keep the CSV source-of-truth and round-trip discipline (§3.5).

Verified: `tools/verify_powerfx.py` (10,549 formulas, 0 warnings, 0 errors),
registry check clean, pack→unpack round trip byte-identical, top-level
`APP-MRMS_Project_app.msapp` repacked with `--layout SourceCode`.

## 23. Studio import checklist (README)

- **Context**: importing the repacked msapp cannot be scripted from this machine —
  `pac` has no canvas import command (verbs are download/list/pack/unpack/validate/create,
  and `validate` is retired in 2.11.2), and no auth profile is set up. Canvas app
  import is a browser flow in make.powerapps.com.
- **Added** a reproducible **Studio import checklist** to README §Workflow: repack →
  local sanity checks (`check_screen_registry.py` + `verify_powerfx.py`) → import in
  make.powerapps.com → re-link SharePoint data sources → open once for edit →
  spot-check the recently changed screens (scr_Reports `App.Size` responsive
  behavior, scr_ReportActivities edit-mode reload, scr_ApprovedReports back,
  sidebar rail navigation) → save in Studio. Includes failure-recovery guidance
  (fix verifier errors, repack, retry; pristine `backup/` as fallback).

## 24. Import failure fixed (5 issue groups from the Studio import report)

**Background.** The user imported the repacked msapp into Power Apps Studio and it
failed. `import_errors` (in the project root) recorded the report. Root causes were
split across two categories: (a) genuine source-format violations introduced by
hand-editing, and (b) a schema misunderstanding about named formulas. All are fixed
and verified; the msapp was repacked and is ready to re-import.

### Issue 1 — PA2108 ×23: named formulas declared as App properties (App.pa.yaml)
- The pa.yaml **Source Code schema (v3.0 — the only version) defines the App node
  with `Properties` only; there is NO `Formulas` key**. Named formulas cannot be
  represented in the source format at all, so declaring `varNavy: =…` under
  `App.Properties` fails validation with “Unknown property for App”.
  (Verified against the official schema: `PowerApps-Tooling/schemas/pa-yaml/v3.0`.)
- **Fix:** reverted the named-formula refactor — all theme colours, breakpoints,
  user/role values, reporting-period defaults and the report lookup are now plain
  `Set()` calls in `App.OnStart`, exactly like the original Studio-authored app.
  `fnReportForCurrentPeriod` was inlined into the 3 call sites in
  `scr_ReportActivities` as `First(Filter(MonthlyReports, …))`.
- **Lesson (BEST_PRACTICES §2.2 updated):** App.Formulas is a Studio-only concept;
  hand-edited pa.yaml must use OnStart `Set()` for app-global values.

### Issue 2 — PA2110 ×20: duplicate control names across screens (scr_Activities)
- `scr_Activities` was rebuilt by copying scr_Projects/scr_Home, so 20 controls kept
  their source names (`Save_btn`, `FormHeader_con`, `Home_ico`, `Status_lbl`, …)
  and collided with the originals. Control names are **app-global** — every screen
  must use unique names.
- **Fix:** renamed all 20 in `scr_Activities` with the screen's existing `Act`
  prefix (`Save_btn` → `ActSave_btn`, `Home_ico` → `ActHome_ico`, …), updating the
  2 internal references (`ActivitiesSidebar_con.Width`, `ProgrammeFilter_drp`).
  A full cross-file scan confirms 0 remaining collisions.

### Issue 3 — PA2108: `PlaceholderText` on ModernTextInput (scr_ApprovedReports)
- The property is named **`Placeholder`** on `ModernTextInput`; `PlaceholderText`
  doesn't exist. Also bumped `ModernTextInput@1.0.0` → `@1.1.1` (clears the PA2105
  “older than current version” warning). Fixed both instances
  (scr_ApprovedReports, scr_ReportActivities — the latter's error was masked by its
  YAML parse failure).

### Issue 4 — PA2108: `HoverBorderColor`/`PressedBorderColor` on Circle (scr_MyActivities)
- `Circle@2.3.0` has `HoverFill`/`PressedFill` but no border-hover properties.
  Removed the two invalid lines (values duplicated the transparent `BorderColor`).

### Issue 5 — PA1001 ×2: YAML parse errors (scr_ReportActivities:456, scr_Reports:592)
- Per the Power Fx YAML grammar: **`:` and `#` are not allowed anywhere in
  single-line formulas**, even inside quoted strings. Two violations:
  - `scr_ReportActivities` `Text: =If(… "Reporting on: " …)` — the `: ` broke the
    plain scalar → converted to a `|-` block scalar.
  - `scr_Reports` `Items: =// comment` + continuation line — a comment embedded in
    a plain scalar → converted to a `|-` block scalar. The scan also caught a third,
    masked instance: `OnSelect: =// …` + `SubmitForm(Form1)` (line 792) → fixed.
- **Lesson:** any formula containing `:` or `#` must use the `|-` multiline form.

### Tooling & verification
- `pac canvas pack` with **`--sources src`** (the dir holding the `.msapr`
  reference + `Src/`) — packing bare `src/Src` triggers pac 2.11.2's
  “must be validated in Studio first” gate (and its FormatException crash).
- Verified: `yaml.compose` parses all 13 files (0 failures); new scan checks for
  `:`/`#` in single-line formulas (0 hits); **`tools/verify_powerfx.py` gained a
  cross-file duplicate-control-name check** (the PA2110 class — control names are
  app-global; confirmed it flags an injected dup in a scratch copy and reports 0
  on the real src); verifier now 10,524 formulas **0 warnings 0 errors**; registry
  check clean; pack→unpack round trip **byte-identical**; top-level
  `APP-MRMS_Project_app.msapp` repacked (13 pa.yaml files, no MainScreen1).
