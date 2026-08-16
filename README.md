# APP-MRMS — Annual Performance Plan Monthly Reporting Management System

Power Apps Canvas app + SharePoint Online solution for the Department of Public Works
and Roads (DPWR), North West Province.

## Repository layout

| Path | Purpose |
|---|---|
| `*.csv` | **Single source of truth** for the SharePoint list schemas and seed data (Directorates, APP_Users, MonthlyReports, Activities, Projects, Programmes) |
| `APP-MRMS_Project_app.msapp` | Importable Power Apps package — **freshly repacked from `src/`** (the pristine original is in `backup/original-pack/`) |
| `src/` | Unpacked msapp source (`pac canvas unpack`, `SourceCode` layout): `App.pa.yaml`, `_EditorState.pa.yaml`, one `.pa.yaml` per screen, and the `.msapr` resources archive |
| `*.docx` | BRD/FDS/TDS, Architecture Pack, Phase 1 Execution Guide, URS Stakeholder Validation — **updated to match the CSV list schemas** (see CHANGES.md §4–5) |
| `Project Instructions` | Working brief for the solution build |
| `BEST_PRACTICES.md` | Distilled canvas-apps best practices + gap analysis of the current app (delegation, naming, collections, `App.Formulas`, source-format workflow) |
| `CHANGES.md` | Change log: tooling, unpack/pack verification, doc updates, findings |
| `update_docs_schema.py` | Script used to align the Word docs with the CSV schemas |
| `reference/` | Permanent reference material for future work (msapp internals, official-docs extractions, doc text, round-trip proof) — see `reference/canvas-apps/README.md` |
| `backup/` | Pristine pre-change snapshots of the original pack and unpacked source — see `backup/README.md` |

## Workflow (edit outside Studio → repack → import)

The `SourceCode` layout is the current supported layout for editing canvas apps
outside Power Apps Studio.

```bash
# Unpack
pac canvas unpack --msapp APP-MRMS_Project_app.msapp --sources src --layout SourceCode

# Edit screen .pa.yaml files under src/Src, then repack
pac canvas pack --sources src --msapp APP-MRMS_Project_app.msapp --layout SourceCode --overwrite
```

Round-trip is verified: pack → unpack yields byte-identical Src YAML and
internal JSON (the only addition is `packed.json` with `LoadFromYaml: true`,
which is expected). After importing a repacked app, open it once for edit in
Studio to validate (it loads from embedded YAML). See CHANGES.md §6 for the
full verification record.

**Before making changes:** `backup/` holds pristine copies of the original
`.msapp` and the unpacked source — restore from there if anything breaks.

## SharePoint list schemas (from CSV exports — source of truth)

### Directorates.csv
`DirectorateID` (text), `DirectorateName` (Title), `Programme` (text), `Director` (User),
`DeputyDirector` (User), `Deligate` (User), `Active` (Boolean, default true)

### APP_Users.csv
`Title`, `UserAccount` (User), `Role` (Choice: Administrator / ProgrammeManager /
Supervisor / Contributor / DeputyDirectorME), `Directorate`, `Directorate: DirectorateID`,
`Programme`, `Active` (Boolean)

### MonthlyReports.csv
`Title`, `Programme`, `Directorate`, `ProgrammeLabel`, `DirectorateLabel`, `Project`,
`ProjectOwnerLabel`, `Activity`, `ActivityOwnerLabel`, `Activity: ActivityShortDescription`,
`Activity: StartDate`, `Activity: EndDate`, `Activity: DueDate`, `ReportingMonth`
(April…March), `Quarter` (Q1–Q4, All), `FinancialYear` (2026/27, 2025/26, 2024/25, All),
`PlannedAct`, `PercentageComplete` (0–100), `Status` (Draft / Submitted / Approved /
Rejected / Escalated), `Version`, `SubmittedBy` (User), `SubmissionDate`, `ReviewedBy`
(User), `ReviewDate`, `RejectionReason`, `IsOverdue` (Boolean), `isFlagged` (Boolean),
`ReasonForDeviation`, `RemedialAction`, `Output`

### Activities.csv
`ID`, `Title` (e.g. ICTM-AC-0001), `ActivityCode`, `ActivityDescription`,
`ActivityShortDescription`, `Directorate`, `DirectorateLabel`, `ProgrammeLabel`, `Project`,
`Project: Reference`, `Frequency` (Monthly / Quarterly / Annual), `Owner` (User),
`ActivityOwner` (User), `Supervisor` (User), `StartDate`, `EndDate`, `DueDate`,
`Active` (Boolean), `Status` (Active / Completed / Not Started)

### Projects.csv
`ID`, `ProjectID` (Title, unique), `ProjectCode`, `PriorityChallenge`,
`ProjectGoalDescription`, `KeyDeliverable`, `AnnualTarget`, `Reference`, `Budget`,
`Directorate`, `Directorate: Title`, `Programme`, `Responsibility` (User), `StartDate`,
`CompletionDate`, `FinancialYear` (2026/27 … 2022/23), `Status` (Active / Closed / Cancelled)

### Programmes.csv
`Title`, `ProgrammeCode`, `ProgrammeManager` (User), `Description`, `Active` (Boolean)

## App structure (unpacked src/Src)

Screens (in `_EditorState.pa.yaml` order):
`scr_Splash` → `scr_Home` → `scr_Users` → `scr_MyActivities` → `scr_ReportForm` →
`scr_ReportView` → `scr_Projects` → `scr_Activities` → `scr_ReportActivities` →
`scr_Reports` → `scr_ApprovedReports` → `MainScreen1`

Connected data sources: Programmes, Projects, Activities, MonthlyReports, APP_Users,
Directorates, KPIDefinitions, Notifications, AuditLog, ReportComments, EvidenceLibrary
(plus static samples CustomGallerySample, ComboBoxSample).

## Known open items (from code review)

- `scr_ReportForm` / `scr_ReportView` now exist (built per the MonthlyReports.csv schema) and
  `scr_MyActivities` navigates to them correctly; `scr_Splash` timer now navigates to Home on
  `OnTimerEnd`. (See CHANGES.md §10.)
- `scr_Home` action buttons are wired (CHANGES.md §14): "New Monthly Report" → scr_ReportForm
  (with the user's first own activity as context; Save guards against a missing activity),
  "View Reports Dashboard" → scr_Reports.
- `scr_Reports_1` (a duplicate of scr_Reports) has been **retired and repurposed** as
  `scr_ApprovedReports`, a read-only Approved Reports dashboard (KPI cards + filters +
  gallery → scr_ReportView, with context-aware back). Home's "APPROVED" KPI card links
  to it. See CHANGES.md §16.
- **`scr_ReportActivities`** (new, CHANGES.md §17) is the Activities → Report
  master-detail: role-scoped activities list on the left (all for admins/DDME, own
  only otherwise), inline MonthlyReports form in the detail pane. The "Monthly
  Reports" sidebar icon on every screen and Home's "New Monthly Report" button both
  open it. Since CHANGES.md §19, selecting an activity **loads its existing report
  for the current FY + month into the form (Edit mode)** via the
  `fnReportForCurrentPeriod` named formula — a new report is only started when none
  exists for that period.
- **CSV data normalized** (CHANGES.md §18): Activities.csv DirectorateLabel/
  ProgrammeLabel now use the canonical Directorates.csv/Programmes.csv names;
  RISK/IC kept separate (`Risk Management`/`Internal Control`); **RIC retired**
  (`Active=False`) and Oratile Tshipo reassigned to Internal Control. See
  `reference/data-normalization-report.md`.
- `scr_Activities` is now a full Activities master-detail (list + form CRUD over the
  Activities list) — see CHANGES.md §12. The only leftover is that nothing in the nav
  sidebar of other screens points at it yet (pre-existing).
- Best-practices pass applied (CHANGES.md §11): immutable OnStart `Set`s are now named
  formulas (App.Formulas), base scope filters are role-first & delegable (colReportsInScope,
  colProjectsInScope), dead/commented blocks were removed, and the two inline dashboard
  galleries now filter the collected `colActivities`. Naming convention (`var`/`col`/`scr`)
  kept as-is; `var` prefix retained on named formulas for minimal-diff safety.
- Verification pass (CHANGES.md §13): all 45 High-severity App Checker formula errors were
  triaged and their 5 root causes fixed (SearchUser→SearchUserV2, invalid Activities/
  MonthlyReports column refs in scr_MyActivities, bare `Fade`→`ScreenTransition.Fade`,
  `Icon.CircleFill`→Circle shape, `ProgressNarrative`→`Output` + stray-`||` filter removal in
  scr_Home). Key logic blocks now carry `//` documentation comments. `tools/verify_powerfx.py`
  (13182 formulas) is clean and the pack→unpack round trip is byte-identical.

See BEST_PRACTICES.md for how these should be addressed per canvas-apps best practice.
