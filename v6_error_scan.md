# v6 Error Scan — APP-MRMS_Project_app_v6.msapp

Date: 2026-08-17 · Branch: `dev` · Pack: `APP-MRMS_Project_app_v6.msapp` (commit `07c6943`, container shell, no components)

Scope: static analysis of the packed `.msapp` (Src/*.pa.yaml sources, pack manifests, compiled controls) plus the repo's own CI guards, to find errors Studio reports on import and in the formula checker.

---

## 1. Automated guards — ALL PASS

| Guard | Tool | Result |
|---|---|---|
| Screen registry (`src/Src` vs `_EditorState`) | `tools/check_screen_registry.py` | ✅ 12 screens, 0 problems |
| Control-property schema (PA2108 class, nested controls) | `tools/check_control_props.py` | ✅ Errors: 0 (36 warnings = templates not in repo manifest: TypedDataCard/Toggle — see §4) |
| Power Fx static verification (strict) | `tools/verify_powerfx.py --strict` | ✅ 12,687 formulas across 14 files, 0 unbalanced, 0 errors, 0 warnings (incl. delegation guard) |
| Pack ↔ source byte-identity | `tools/repack_msapp.py --prune` | ✅ all 14 `Src/*.pa.yaml` entries byte-identical to `src/Src/` |

## 2. Pack-level integrity — PASS

- Valid zip, no corrupt members.
- Component removal verified: **zero** `Control: CanvasComponent` / `ComponentName: cmp_*` in any screen; `Src/Component/*` pruned from the pack.
- App identity: `Properties.json` name and `PublishInfo` = `APP-MRMS_Project_app_v6`; `AppCheckerResult.sarif` = 0 findings.
- StartScreen = `scr_Splash`; all 12 screens registered; every `Navigate()` target resolves to an existing screen.
- All data sources referenced in formulas are declared in `References/DataSources.json`:
  `APP_Users, Activities, Directorates, MonthlyReports, Notifications, Programmes, Projects` (+ declared `AuditLog, EvidenceLibrary, KPIDefinitions, ReportComments`). `User()` is a built-in.
- Every control type used in Src resolves against the pack's `References/Templates.json` (import also proved this — the pack imports).

## 3. Suspects investigated and CLEARED (with evidence)

1. **`DefaultSelectedItems` on `ModernDropdown@1.0.2`** — the v5 import blocker (PA2108).
   All 15 occurrences are valid: 3 are on **ModernCombobox** controls (`ActivityOwner_cmb`, `Supervisor_cmb`, `Responsibility_cmb` — comboboxes do have this property) and 12 are `=Parent.Default` inside `TypedDataCard` children (Studio-written standard). No PA2108 risk. Import succeeded, confirming.
2. **Record-valued `Default:` on ModernDropdowns (13 controls)** — e.g. `ActProgrammeFilter_drp Default: =LookUp(colProgrammesFilter, Title = "All")`, form dropdowns `If(varMode = "New", Blank(), LookUp(colProgrammes, Title = varSelectedActivity.ProgrammeLabel))`.
   **Verified as the original Studio-authored pattern**: the pristine v1 app (`APP-MRMS_Project_app_v1_pristine.msapp`, `ProjectDirectorate_drp_1`) uses the identical record-`LookUp` style. ModernDropdown accepts a record default when `Items` is a record table, so this is the app's native behavior — NOT flagged as an error. (The v5 fix in commit `116371a` only targeted `Filter()` **tables**, which are genuinely invalid.)
3. **Dangling control references** — 112 candidates from a formula scan; every one cleared: `Status.Value` / `Programme.Value` / `Quarter.Value` etc. are implicit record-scope inside `Filter`/`LookUp`; `ImagePosition.Fill` is a global enum; the rest were inside `//` or `/* */` comments (`drp_ProgrammeFilter`, `lbl_ProgrammeName`, `DirectorateFilter_drp`, `Project_gal`, `Dropdown2`).
4. **Legacy references** — `scr_Reports_1` (scr_ApprovedReports:19) is inside a `//` comment; `App_Users` (scr_Projects:1474) is inside a commented-out `/*...*/` block (the live formula correctly uses `APP_Users`).
5. **Unknown vars/collections** — all `col*`/`var*` hits that appeared "unbuilt/unset" are multi-line `ClearCollect(...)` / `Set(...)` scan artifacts; nothing genuinely undefined.

## 4. Residual risks — CANNOT be verified statically; these need Studio/runtime confirmation

These are the most likely source of the errors you are seeing. None can be proven wrong from the pack alone.

| # | Risk | Where | What to check |
|---|---|---|---|
| R1 | **SharePoint column / list mismatch** — formulas reference specific columns (`'Active '`, `Status`, `SubmittedBy`, `DirectorateLabel`, `ProgrammeLabel`, `ReportingMonth`, `Quarter`, `FinancialYear `, `SubmissionDate`, `RejectionReason`, `ReviewedBy`, `ReviewDate`, `UserAccount.Email`, …). If any list was renamed/columns removed, every formula touching it shows errors. | all screens, esp. scr_Reports, scr_Home, scr_Activities, scr_ApprovalQueue | Studio error pane: "column 'X' does not exist" entries; compare against actual list columns |
| R2 | **Choice-value mismatches** — `Status.Value = "Submitted"/"Escalated"/"Approved"/"Rejected"`, `Quarter.Value`, role strings (`"Supervisor"`, `"ProgrammeManager"`, …) must match the SharePoint choice values exactly. | scr_ApprovalQueue, scr_Home, scr_Reports | Confirm choice values in the lists |
| R3 | **Environment/connector** — the app declares 13 data sources; if a connection isn't available on import, Studio shows source-level errors. | app-wide | Check connections after import; re-add if prompted |
| R4 | **Modern-control version skew** — pack uses ModernDropdown@1.0.2, ModernText@1.0.0, ModernCombobox@1.1.1, TypedDataCard@1.0.7. 4 types (TextInput, Toggle, ModernTextInput, TypedDataCard) are absent from the pack's Templates.json (import proved they still resolve, but a Studio-version mismatch can surface as control errors). | screens using modern controls (188 ModernText, 39 ModernDropdown, 30 TypedDataCard) | If "unknown control/version" errors appear, list them |
| R5 | **Splash timing differs from the v5 spec** — v6 splash `Duration: 1800` ms → `Navigate(scr_Home)` (v5 contributor spec was 10 s → My Activities). Confirm this is intended for v6. | scr_Splash | Confirm desired duration & destination |
| R6 | **Delegation at runtime** — strict check passed, but SharePoint delegation limits (2,000 rows) can truncate large lists at runtime. | scr_Reports, scr_Home galleries | Watch for truncated data, not errors |

## 5. Resolution plan (ordered)

1. **Get the actual error list** — open the app in Studio → View → Errors (or the checker pane). Share the list (paste in chat or drop the export file into the repo like `v5_import_errors`). This converts R1–R4 from guesses into exact fixes.
2. **Fix confirmed formula errors** in `src/Src/*.pa.yaml`, rerun the three guards, repack with `tools/repack_msapp.py --prune`, update the release asset.
3. **Verify SharePoint schema** against the column/choice lists used (provide list column names if different from above).
4. **Walk the screens end-to-end** in Play mode: splash → Home → Projects → Activities → Monthly Reports → Report Form → Report View → Approved Reports → Approval Queue → Users, checking data loads and the Approve/Reject/Return actions.
5. **Confirm splash timing** (R5) and adjust if the 10 s → My Activities rule from v5 should apply here too.

## 6. What I need from you

- The Studio error list (import log and/or formula-checker entries), or
- the names of the failing screens + what you see when you open them, and
- confirmation of the SharePoint list/column names if they differ from the pack's expectations.

With that, each item becomes a direct edit → verify → repack → republish cycle.
