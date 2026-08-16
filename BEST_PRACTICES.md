# APP-MRMS — Canvas App Best Practices & Compliance Review

Source: official Microsoft Learn **"Power Apps maker"** documentation
(`power-apps-maker.pdf`, 6,765 pages; relevant sections extracted and read).
Scope: canvas apps only — external editing of screen files, packing/import
workflow, and industry-standard app architecture. Written 2026-08-16.

---

## Part 1 — External editing of screen files + pack/import workflow (the rules)

### 1.1 Source file format (*.pa.yaml) — how it works
- The `.msapp` is a binary container (zip) holding `Header.json`, `Properties.json`,
  `Controls/*.json`, `References/*`, assets, and the source code.
- **Only the files in the `\Src` folder of the extracted msapp are source code and
  intended for use with source control.** The JSON files are explicitly **not**
  stable between save/load cycles — never hand-edit them.
- `Src/App.pa.yaml` represents the app; `Src/[screen].pa.yaml` one file per screen
  (plus components in `Src/Components/` if present).
- The `SourceCode` (*.pa.yaml) schema is the **only active** schema. `Experimental`
  (*.fx.yaml) and the early-preview formats are **retired**.
- Key schema facts:
  - Top-level nodes group screens (`Screens:`) and the app (`App:`).
  - `Control: Name@version` defines the control type (the `@version` pins the
    control version used to deserialize properties). `Variant:` identifies the
    control variant. Both are required for instantiation and do **not** accept
    Power Fx expressions.
  - **Only properties that differ from their default values are serialized.**
  - All controls use ascending ZIndex starting at 1 (CSS-2 style ordering).
- Editing YAML externally is supported only through the CLI path
  (`pac canvas pack/unpack`, preview) or **Power Platform Source Control
  Integration** (git). Studio treats generated YAML as read-only.

### 1.2 The pack/import cycle — verified and lossless
- **Unpack:** `pac canvas unpack --msapp app.msapp --sources src --layout SourceCode --overwrite`
- **Edit:** change only `src/Src/*.pa.yaml` (add screens as new `Screens:` blocks,
  register them in `Src/_EditorState.pa.yaml` `ScreensOrder`, edit formulas).
- **Pack:** `pac canvas pack --sources src --msapp app.msapp --layout SourceCode --overwrite`
- **Import:** import the msapp into Power Apps. **After import, the app MUST be
  opened once for edit in Power Apps Studio to validate** — the pack output warns:
  *"Canvas apps packed using yaml SourceCode must be validated first by opening the
  app for edit within the Power Apps studio."* The packed app contains `packed.json`
  with `LoadFromYaml: true`, so Studio loads from the embedded YAML on that first open.
- **Round-trip verification (done 2026-08-16):** packing the unpacked APP-MRMS
  source and unpacking again produced byte-identical artifacts for every file
  (Header, Properties, PublishInfo, all Controls JSON, References, SARIF, Assets,
  all Src YAML). The only addition is `packed.json` (pack metadata) — expected.
  → The edit → pack → import path is safe if you follow the rules below.

### 1.3 Import-safety rules (so the app never fails to import)
1. Edit **only** `Src/*.pa.yaml` and `_EditorState.pa.yaml`; never touch the JSON.
2. Keep the `.msapr` (resources) file that `unpack` produced — `pack` merges the
   YAML source over it. Deleting or hand-editing it breaks resources/data sources.
3. Keep YAML inside the supported schema: `Control:`/`Variant:` with `=`
   prefixed Power Fx for properties. Don't invent new top-level keywords.
4. When adding a screen: add its `Screens:` block **and** register it in
   `_EditorState.pa.yaml` `ScreensOrder` (missing registration can orphan the screen).
5. When renaming/removing screens or controls, update every `Navigate(...)` and
   cross-reference (the app already has dangling refs to `scr_ReportForm` /
   `scr_ReportView` — see Part 3).
6. After packing, always verify the round trip (unpack to a temp folder and diff
   `Src/`), then open in Studio once to validate before distributing.
7. ALM note from Microsoft docs: canvas-app package import/export is for **basic
   transfer only**; the msapp format does **not** support full ALM. For governed
   environments use Dataverse solutions with environment variables; the pack/unpack
   path is the correct choice here because the app is SharePoint-backed (no Dataverse).

---

## Part 2 — Official canvas-app best practices (from the maker docs)

### 2.1 Delegation & small data payloads
- **Keep data payloads small** — the #1 enterprise pattern. Galleries bound directly
  to a data source page ~100 records automatically. Aim for 100–200 records per
  default query; scope data with views, default filters, or required search input.
- **Delegation:** prefer `Filter`/`Search`/`SortByColumns` (delegable operators) so
  the server does the work. **SharePoint does not delegate `CountRows`, `CountIf`,
  `GroupBy`, `AddColumns`, `FirstN`, `Distinct`, `ForAll`, `Sum`/`Average` over
  non-delegated results** — those run locally after downloading only 500–2,000 rows,
  which silently returns wrong results beyond that limit.
- **Optimized query pattern:** single table/view → prefiltered on the server →
  filter/sort columns indexed.
- **Explicit Column Selection** (Settings > Upcoming features > Preview) limits
  fetched columns — good to enable.
- Multi-condition `Filter` with `||` across columns is often **not** delegable on
  SharePoint — split into simple delegable filters or accept the row limit.

### 2.2 Replace App.OnStart Set/Collect with named formulas (App.Formulas)
- A long `App.OnStart` with ordered `Set`/`ClearCollect` calls blocks the first
  screen and slows Studio (up to 80% Studio load-time reduction observed when
  switching). Named formulas are **immutable, independent, lazily evaluated**:
  - Theme colours, static filter defaults, derived role/scope values → named formulas.
  - Do **not** put named formulas inside `App.OnStart` (they're formulas, not statements).
  - Keep `Set` only for genuinely mutable state.
- Example pattern:
  ```
  varNavy = ColorValue("#122952");
  colProgrammes = Filter(Programmes, Active = true);
  varCanViewAllReports = varUserRole = "DeputyDirectorME" || varUserRole = "Administrator";
  ```

### 2.3 Split long formulas
- Formulas >256k characters are the top cause of Studio slowdown; split with named
  formulas, the `With()` function (nest + `As` for intermediate records), or canvas
  components with custom output properties.
- Imperative logic (Set/Collect/Notify/Patch/SubmitForm) can't be named formulas →
  split via a hidden button's `OnSelect` + `Select(hiddenButton)`, or a Toggle whose
  `OnCheck` runs the logic.

### 2.4 Naming & structure conventions (coding guidelines)
- Consistent prefixes: `var` for mutable variables, `col` for collections,
  semantic control names (e.g. `btnSubmit`, `lblTitle`), `scr` for screens.
  (Named-formula convention drops the `var` prefix since they're immutable.)
- No duplicated screens/controls (the app currently duplicates — see Part 3).
- Remove dead code and commented-out formula blocks before packing.
- Use `Concurrent()` for independent data calls; `With()` instead of nested
  `LookUp` chains; avoid `LookUp`-of-`LookUp` (denormalise label columns instead —
  this app already does this via `DirectorateLabel`/`ProgrammeLabel`).

### 2.5 Business logic: Power Fx vs Power Automate
- **Power Fx** for low-latency, in-app logic (Data + Power Fx is fastest).
- **Power Automate** for long-running / multi-connector / async work and audit
  trails (run history). Kick off flows and don't block the UI.
- Design UI around inherent latency: either pause with a progress indicator, or
  offload to a flow.

### 2.6 Partitioning & ALM
- Very large apps (thousands of controls) → separate canvas apps with `Launch()`
  (save state first — state is lost across Launch) or model-driven custom pages.
- Use canvas **components / component libraries** for shared UI (nav, headers,
  theming) — this app's repeated header/sidebar blocks are ideal component candidates.

---

## Part 3 — Gap analysis: how the current APP-MRMS app measures up

Verified against the unpacked source (`APP_MRMS_Unpacked/Src/*.pa.yaml`, no changes made).

| # | Practice | Current state | Action |
|---|---|---|---|
| 1 | Named formulas vs OnStart Set/Collect | `App.pa.yaml` OnStart is a long ordered sequence of `Set`/`ClearCollect` (plus a large commented block) — theme, filters, collections, role, notifications, FY/quarter all inline | Convert immutable values to `App.Formulas` (theme colours, derived role/scope, FY/month/quarter, reference collections) |
| 2 | Remove dead code | `App.pa.yaml` (commented block), `scr_Home` OnVisible (commented `colOverdueItems`/`colFlaggedItems`/`colMonthlyTrend`), `scr_Projects`/`scr_Activities` (`/* */` alternatives), `scr_MyActivities` (commented gallery Items) | Delete commented blocks before the next pack |
| 3 | No duplicated screens | `scr_Reports_1` duplicates `scr_Reports`; `scr_Activities` is a copy of `scr_Projects` whose Save button still patches `Projects`; `MainScreen1` is empty | Rework `scr_Activities` to patch `Activities`; retire `scr_Reports_1`/`MainScreen1` or repurpose |
| 4 | No dangling references | `scr_MyActivities` navigates to `scr_ReportForm` and `scr_ReportView`, which don't exist; `scr_Splash` timer has no `OnTimerEnd`; `scr_Home` "New Monthly Report" / "View Reports Dashboard" buttons have no OnSelect | Build the missing screens (planned task) and wire navigation |
| 5 | Delegation & payloads | Base scope `ClearCollect(colReportsInScope, Filter(MonthlyReports, ...OR...))` mixes roles/directorates in one filter; heavy `Distinct`/`ForAll`/`GroupBy` on collections; SharePoint OR filters likely non-delegable | Keep base filter simple & delegable (scope by role first), index filter columns, stay within 500–2,000-row collected set; avoid `CountRows` on raw SharePoint |
| 6 | Long formulas | `scr_Home` `MonthlyTrend_gal.Items` is a very long inline `ForAll(Sequence(12)...)`; several OnVisible blocks are long | Extract to named formulas / `With` blocks |
| 7 | Naming conventions | Uses `var`/`col` prefixes and `scr` screen names consistently — good | Align new screens with the same scheme; drop `var` prefix only for named-formula conversions |
| 8 | Components for repeated UI | Every screen hand-builds the same navy header + icon sidebar (with `_1`…`_8` suffix duplicates) | Extract header/sidebar into a component library (Phase 2) |
| 9 | Import-safety | Round trip verified lossless (Part 1.2); original msapp untouched | Follow Part 1.3 rules for every future edit → pack → import |
| 10 | ALM | msapp import/export is basic transfer only (no Dataverse) | Keep schemas in CSV (source of truth) + YAML in git; treat msapp as a build artifact |

### Recommended remediation order (for the upcoming screen-build + pack task)
1. Build `scr_ReportForm` + `scr_ReportView` (the referenced-but-missing screens),
   register both in `_EditorState.pa.yaml`.
2. Wire `scr_Splash` timer (`OnTimerEnd: Navigate(scr_Home)`) and the unwired
   `scr_Home` buttons.
3. Convert `App.OnStart` immutable `Set`s → `App.Formulas`; delete commented blocks.
4. Rework `scr_Activities` to CRUD the Activities list; retire `scr_Reports_1`.
5. Re-run the round-trip verification (unpack → diff → pack) and import once into
   Studio to validate.

---
### Application status (2026-08-16)
- **Done** (CHANGES.md §11): rows 1–2, 5–6, and part of 7 — OnStart immutable `Set`s →
  named formulas; dead commented blocks removed; base scope filters made role-first and
  delegable (`colReportsInScope`, `colProjectsInScope`); the two inline dashboard
  galleries (trend/progress) now filter the collected `colActivities`; `colOverdueItems`
  restored (was commented out but consumed by live KPI cards).
- **Open**: row 3 (`scr_Reports_1` duplicate, `MainScreen1` empty, scr_Activities list
  pane still on Projects), row 4 (unwired scr_Home buttons), row 8 (header/sidebar
  components), row 10 (ALM via git + CSV source of truth).

---
*Supporting artifacts: CHANGES.md (session change log), update_docs_schema.py,
APP_MRMS_Unpacked/ (working source), APP_MRMS/ repo (git-tracked copies).*
