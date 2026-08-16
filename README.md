# APP-MRMS — Annual Performance Plan Monthly Reporting Management System

[![CI status](https://github.com/OratileTshipo/APP_MRMS_Project/actions/workflows/ci.yml/badge.svg)](https://github.com/OratileTshipo/APP_MRMS_Project/actions/workflows/ci.yml)

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
| `tools/check_screen_registry.py` | CI guard: fails if any screen file in `src/Src/` has no matching `_EditorState` entry (or vice versa) |
| `.github/workflows/ci.yml` | GitHub Actions CI: runs the screen-registry check + `tools/verify_powerfx.py` on every push/PR |
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

## Importing the repacked app into Power Apps Studio (checklist)

> Note: `pac` has **no import command** and no auth profile is required for the
> browser flow — importing a canvas app is done in make.powerapps.com. The
> checklist below is the reproducible path.

1. **Repack the latest source** (if you just edited `src/`):
   ```bash
   pac canvas pack --sources src --msapp APP-MRMS_Project_app.msapp --layout SourceCode --overwrite
   ```
2. **Sanity-check the pack locally first** (catches breakage before Studio):
   ```bash
   python3 tools/check_screen_registry.py   # screen files ↔ _EditorState
   python3 tools/verify_powerfx.py          # formula balance, nav targets, patch keys
   python3 -c "import yaml,glob; [yaml.compose(open(f,encoding='utf-8')) for f in glob.glob('src/Src/*.pa.yaml')]"  # YAML parse gate
   ```
   (See CHANGES.md §24 for the full import-failure root causes — named formulas
   can't live in pa.yaml, single-line formulas can't contain `:` or `#`, control
   names are app-global, and `--sources src` (with the `.msapr`) is required for
   `pac canvas pack` in 2.11.2. For round-trip verification, `pac canvas unpack`
   in 2.11.2 also requires the explicit `--layout SourceCode` flag — without it
   the unpack crashes with an NRE, even on the pristine backup.)
3. **Open [make.powerapps.com](https://make.powerapps.com)** and sign in with an
   account that can create apps in the target environment (the one holding the
   SharePoint lists).
4. **Apps → Import canvas app** (top toolbar) → upload `APP-MRMS_Project_app.msapp`
   from the repo root.
5. **Re-link the data sources if prompted** — the pack references SharePoint
   lists by name (Programmes, Projects, Activities, MonthlyReports, APP_Users,
   Directorates, KPIDefinitions, Notifications, AuditLog, ReportComments,
   EvidenceLibrary). Confirm each connection resolves in the target environment.
6. **Open the imported app once for edit** (it loads from embedded YAML) and let
   it finish parsing — this is the real Studio-side validation step.
7. **Spot-check the screens that changed most recently:**
   - `scr_Reports` → resize the preview window; on small/phone width the sidebar
     should collapse and the back button should appear (uses `App.Size`).
   - `scr_ReportActivities` → select an activity and confirm an existing report
     for the current FY/month loads in the detail pane (Edit mode), or a fresh
     form opens (New mode) when none exists.
   - `scr_ApprovedReports` → drill into a report and confirm the back button
     returns to the dashboard.
   - Sidebar rail on any screen → every icon should navigate (Home, Projects,
     Activities, My Activities, Monthly Reports, Users).
8. **Save once in Studio** (File → Save / Save as) so the app is persisted in the
   environment, not just imported from the file.

**If the import fails:** the msapp was likely packed from an inconsistent source
state — re-run step 2, fix any reported errors, repack (step 1), and retry.
Keep the pristine original in `backup/` untouched as the fallback.

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
`scr_Reports` → `scr_ApprovedReports`

**Reusable components** (`src/Src/Component/`): every screen uses
`cmp_AppHeader` (navy header — PageTitle / ShowBack / ShowSearch / Subtitle inputs,
`SearchText` output) and `cmp_NavRail` (left nav rail — `ActiveScreen` input drives the
active-icon highlight). Canonical shell: root horizontal → `[NavRail, column
(Width = App.Width − NavRail.Width) → [AppHeader, body]]`. See BEST_PRACTICES.md row 8
and CHANGES.md §26.

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
  Activities list) — see CHANGES.md §12. Navigation audit (CHANGES.md §22): the
  "Activities" rail icon now points to scr_Activities on every screen, and all
  sidebar rail icons + Home KPI arrows are wired.
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
