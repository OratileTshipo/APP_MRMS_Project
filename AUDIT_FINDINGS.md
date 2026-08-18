# APP-MRMS — Full Repository Audit

**Audit Date:** 2026-08-18  
**Branch:** `mimo-2.5` (from `dev`)  
**Auditor:** Buffy (AI coding agent)

---

## 1. Verification Status — ALL PASS ✅

| Check | Tool | Result |
|---|---|---|
| Screen registry | `check_screen_registry.py` | ✅ 11 files ↔ 11 entries |
| Control properties | `check_control_props.py` | ✅ 998 controls, 0 errors, 36 warnings |
| Power Fx static | `verify_powerfx.py --strict` | ✅ 12,687 formulas, 0 errors |
| Pack round-trip | `pac canvas pack/unpack` | ✅ Byte-identical |

---

## 2. Critical Issues (Block Import)

### C1: SupervisorApproved Status Missing
- **Location:** MonthlyReports.csv Status choices
- **Current:** Draft / Submitted / Approved / Rejected / Escalated
- **Required:** Draft / Submitted / **SupervisorApproved** / Approved / Rejected / Escalated
- **Impact:** Flow 2 (Supervisor Approved → Route to Deputy) fires on `Status = SupervisorApproved` — this choice doesn't exist
- **Fix:** Add `SupervisorApproved` to MonthlyReports.Status in SharePoint before importing flows

### C2: SharePoint Site Not Provisioned
- **Impact:** 11 lists need creation with exact CSV schemas
- **Fix:** Provision SharePoint site, create all lists, verify column names match CSVs exactly

### C3: APP_Users Needs Seeding
- **Current:** 5 rows (System Admin, Test User, Test User2, user 20, Oratile Tshipo)
- **Required:** At least 1 user per role with real M365 accounts
- **Roles:** Administrator, ProgrammeManager, Supervisor, Contributor, DeputyDirectorME

### C4: Flow Package Has Placeholder GUIDs
- **Location:** `flows/APP-MRMS-Approval.zip`
- **Current:** Uses `1111…1111` placeholders
- **Fix:** Rebuild with real list GUIDs via `python3 tools/build_flow_zips.py`

---

## 3. High Issues (Need Decision)

### H1: DeputyDirectorME Role
- **BRD says:** Escalation-only ("may intervene on ANY report at ANY stage")
- **Flow package assumes:** Mandatory 2nd stage approval
- **Decision needed:** Is Deputy approval required for every report, or only escalation-worthy ones?

### H2: Activity Completion Logic
- **Current:** Flow 3 sets `Activities.Status = Completed, Active = false` on approval
- **Problem:** An Activity can have 12 monthly reports. Marking Completed on first approval blocks remaining 11
- **Options:**
  - Completed after all 12 months approved
  - Completed after EndDate with final report
  - Per-Activity Frequency (Monthly → 12, Quarterly → 4, Annual → 1)

### H3: Rejection Flow Excluded
- **Reason:** Duplicate action-name validation error
- **Template location:** `flows/templates/APP-MRMS-Approval/Microsoft.Flow/flows/d4f9a27c-8851-44ba-9f3c-4989a0e6d467/`
- **Fix:** Rename duplicate actions to unique names

### H4: Splash Timing
- **Current:** 1800ms → Home
- **v5 spec was:** 10s → My Activities
- **Decision needed:** Which is correct for production?

---

## 4. Medium Issues (Runtime Verification)

### M1: SharePoint Column/List Mismatch Risk
- **Impact:** Formulas reference specific columns. If any list was renamed, every formula shows errors
- **Mitigation:** Import into Studio, check error pane

### M2: Choice-Value String Matching
- **Impact:** `Status.Value = "Submitted"` must match SharePoint exactly (case-sensitive)
- **Mitigation:** Verify choice values in live SharePoint lists

### M3: Modern-Control Version Skew
- **Controls:** ModernDropdown@1.0.2, ModernText@1.0.0, ModernCombobox@1.1.1, TypedDataCard@1.0.7
- **Risk:** Studio version mismatch can surface as errors
- **Mitigation:** Test import in target Studio version

### M4: Delegation at Runtime
- **Impact:** SharePoint delegation limits (2,000 rows) can truncate large lists
- **Mitigation:** Monitor for truncated data in galleries

---

## 5. Low Issues (Technical Debt)

### L1: Sidebar/Header Duplication
- **Impact:** ~200 lines of near-identical rail YAML per screen
- **Fix:** Extract `cmp_NavRail` + `cmp_AppHeader` into component library (Phase 2)

### L2: Trending/Settings/Support Icons Dead
- **Impact:** Non-interactive on every screen
- **Fix:** Wire or remove in Phase 2

### L3: Handoff Briefs Outdated
- **Impact:** `scr_MyActivities_Handoff_Brief.md` says scr_ReportForm/scr_ReportView "not yet built" — they are built
- **Fix:** Update briefs

### L4: Duplicate File Structure
- **Impact:** Parent repo has `src/Src/` AND `APP_MRMS/src/Src/`
- **Fix:** Clarify source of truth is submodule

### L5: .gitignore Blocks .md Files
- **Current:** `*.md` in `.gitignore`
- **Impact:** Changes to README.md, CHANGES.md won't be tracked in parent repo
- **Fix:** Remove `*.md` from .gitignore or add exceptions

### L6: Activities Missing Supervisor
- **Impact:** Rows 7–12 (COMM-AC-0013 to COMM-AC-0018) have no Supervisor
- **Impact:** Approval flow needs Supervisor to route to

### L7: ReportingMonth Typo
- **Current:** `Fecbruary` instead of `February`
- **Impact:** SharePoint will have this typo in choice values
- **Fix:** Correct in CSV before provisioning SharePoint

---

## 6. File Inventory

### Source Files (APP_MRMS/src/Src/)
| File | Lines | Purpose |
|---|---|---|
| App.pa.yaml | ~120 | App-level OnStart, theme, user role, filters |
| _EditorState.pa.yaml | ~15 | Screen registration order |
| scr_Splash.pa.yaml | ~120 | Splash screen with timer |
| scr_Home.pa.yaml | ~2700 | Dashboard with KPIs, filters, galleries |
| scr_Users.pa.yaml | ~1500 | User registration form |
| scr_MyActivities.pa.yaml | ~1400 | Contributor's activity worklist |
| scr_ReportForm.pa.yaml | ~800 | Monthly report create/edit |
| scr_ReportView.pa.yaml | ~400 | Read-only report detail |
| scr_Projects.pa.yaml | ~1700 | Projects master-detail CRUD |
| scr_Activities.pa.yaml | ~1700 | Activities master-detail CRUD |
| scr_ReportActivities.pa.yaml | ~1500 | Activities → Report inline master-detail |
| scr_Reports.pa.yaml | ~2000 | Reports dashboard with filters |
| scr_ApprovedReports.pa.yaml | ~1200 | Read-only approved reports |
| scr_ApprovalQueue.pa.yaml | ~1500 | 2-stage review queue |

### Tools
| Tool | Purpose |
|---|---|
| `verify_powerfx.py` | Static formula verification (balance, nav, patch keys, delegation) |
| `check_screen_registry.py` | Screen file ↔ _EditorState drift detection |
| `check_control_props.py` | Control property schema validation (PA2108) |
| `repack_msapp.py` | Pack/unpack helper |
| `build_flow_zips.py` | Build flow import package with real GUIDs |
| `normalize_activities.py` | Normalize Activities.csv labels |
| `gen_normalization_report.md` | Generate normalization diff report |

### CSV Schemas (Source of Truth)
| File | Records | Key Columns |
|---|---|---|
| Directorates.csv | 17 | DirectorateID, Title, Programme, Director, Active |
| APP_Users.csv | 5 | Title, UserAccount, Role, Directorate, Programme |
| MonthlyReports.csv | 4 seed | 30 columns, Status (5 choices), Activity lookup |
| Activities.csv | 516 | 19 columns, Frequency, Owner, Supervisor, DueDate |
| Projects.csv | Multiple | 18 columns, ProjectCode, Budget, Directorate lookup |
| Programmes.csv | 5 | Title, ProgrammeCode, ProgrammeManager, Active |

---

## 7. Architecture Decisions

1. **Source of truth:** CSV files in `APP_MRMS/` (not SharePoint, not YAML)
2. **Build pipeline:** Edit pa.yaml → pac canvas pack → import to Studio → validate → save
3. **CI:** GitHub Actions runs screen registry + control props + Power Fx verifier
4. **Flows:** Separate import package (not embedded in msapp)
5. **Roles:** 5 roles with role-first delegable scope filters
6. **Naming:** `var` prefix for variables, `col` for collections, `scr` for screens
