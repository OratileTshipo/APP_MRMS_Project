# APP-MRMS — Comprehensive Audit Findings

**Audit Date:** 2026-08-20  
**Branch:** `mimo-2.5`  
**Auditor:** Buffy (AI coding agent)  
**Current Build:** `APP-MRMS_Latest_dev_scoped_v6.msapp`

---

## 1. Verification Status — ALL PASS ✅

| Check | Tool | Result |
|---|---|---|
| Screen registry | `check_screen_registry.py` | ✅ 14 files ↔ 14 entries |
| Control properties | `check_control_props.py` | ✅ 1,120 controls, 0 errors, 45 warnings |
| Power Fx static | `verify_powerfx.py` | ✅ 14,147 formulas, 0 errors, 0 warnings |
| YAML syntax | `yaml.compose()` | ✅ All files parse OK |

---

## 2. Scoping Fixes (v5 → v6)

### 2.1 Projects Screen — Lookup Delegation Fix
- **Problem:** `Filter(Projects, Directorate.Value = varUserDirectorate)` — `Directorate` is a **Lookup column**; SharePoint does NOT delegate filtering on `Lookup.Value` properties
- **Impact:** Non-admin users saw 0 projects (filter silently returned empty)
- **Fix:** Load ALL projects first, then filter in-memory:
  ```
  ClearCollect(colProjectsInScope, Projects);
  If(Not(varCanViewAllReports),
      ClearCollect(colProjectsInScope,
          Filter(colProjectsInScope, Directorate.Value = varUserDirectorate)));
  ```
- **Files:** `scr_Projects.pa.yaml`

### 2.2 ReportActivities Screen — Consistent Scoping Pattern
- **Problem:** Same delegation risk pattern as Projects (defensive fix)
- **Fix:** Load all active activities first, then filter in-memory for non-admin users
- **Files:** `scr_ReportActivities.pa.yaml`, `scr_ReportActivities_1.pa.yaml`

---

## 3. Delegation Fixes (v5 → v6)

### 3.1 CountRows on SharePoint Sources
All three save buttons used `CountRows(Filter(DataSource, StartsWith(...)))` for auto-generating sequential IDs. `CountRows` over SharePoint is NOT delegable (500/2000-row cap).

| Screen | Before (non-delegable) | After (in-memory) |
|--------|----------------------|-------------------|
| scr_Activities | `CountRows(Filter(Activities, ...))` | `CountRows(Filter(colActivitiesInScope, ...))` |
| scr_Projects | `CountRows(Filter(Projects, ...))` | `CountRows(Filter(colProjectsInScope, ...))` |
| scr_ReportActivities_1 | `CountRows(Filter(MonthlyReports, ...))` | `CountRows(Filter(colMonthlyReportsScoped, ...))` + new collection |

### 3.2 MonthlyReports Collection Added
- **File:** `scr_ReportActivities_1.pa.yaml` OnVisible
- **New collection:** `colMonthlyReportsScoped` — scoped to current FY and directorate
- **Purpose:** Provides in-memory data for ID generation without delegation limits

---

## 4. Accessibility Fixes (v6)

### 4.1 Missing AccessibleLabel on Interactive Icons
Added `AccessibleLabel` to all interactive `Classic/Icon` controls across 10 files:

| Icon Type | AccessibleLabel | Files |
|-----------|----------------|-------|
| Search | `"Search"` | Home, Activities, Projects, Reports, ApprovedReports, cmp_AppHeader, ReportActivities, ReportActivities_1 |
| Bell | `"Notifications"` | Home, Activities, Users, Projects, ApprovedReports, ReportView, cmp_AppHeader |
| ArrowLeft | `"Go back"` | ApprovedReports, ReportView, cmp_AppHeader |
| ChevronRight | `"View project details"` / `"View report details"` | Projects, ApprovedReports |

**Total: 19 icons fixed**

### 4.2 Empty OnSelect Handlers Removed
Replaced empty `OnSelect: =` (clickable but do nothing) with meaningful handlers:

| File | Control | Before | After |
|------|---------|--------|-------|
| scr_Activities | ActivityRowStatus_rec | `OnSelect: =` | `OnSelect: =Select(Parent)` |
| scr_Projects | PrjRowStatus_rec_2 | `OnSelect: =` | `OnSelect: =Select(Parent)` |
| scr_Projects | HomeBell_ico_2 | `OnSelect: =` | Removed (no handler) |

### 4.3 Tooltip Added to Bell Icons
Added `Tooltip: =\"Notifications\"` to `HomeBell_ico_2` in Projects screen (was missing).

### 4.4 Invalid Tooltip Properties Removed (PA2108)
Removed `Tooltip` from `ModernText@1.0.0` controls in `scr_MyActivities.pa.yaml` — `Tooltip` is not a valid property on ModernText (would cause PA2108 import error).

---

## 5. Other Fixes (v5 → v6)

### 5.1 Broken Reset Target
- **File:** `scr_ReportActivities.pa.yaml`
- **Problem:** `Reset(RepActPlanned_txt)` referenced a control that doesn't exist
- **Fix:** Removed both occurrences (OnVisible + gallery OnSelect)

### 5.2 Screen Registry
- **File:** `_EditorState.pa.yaml`
- **Problem:** `Screen2.pa.yaml` and `scr_ReportActivities_1.pa.yaml` missing from ScreensOrder
- **Fix:** Added both entries

---

## 6. Remaining Performance Issues

### 6.1 Home Screen — Heavy ForAll/Sequence Formulas (HIGH)

**MonthlyTrend_gal.Items** (line ~1642):
```
ForAll(Sequence(12, 0, 1), With({monthAnchor: ...},
    With({dueThisMonth: Filter(colActivities, ...)},
        With({reportsForDueActivities: Filter(colReportsInScope, ...)},
            {MonthName, TotalActivities: CountRows(dueThisMonth),
             OnTimeCount, LateCount, OutstandingCount}
        ))))
```
- **Impact:** Recalculates on every filter change (12 iterations × nested Filter/LookUp/Distinct/CountRows)
- **Recommendation:** Pre-compute monthly aggregates in `OnVisible` collection

**ProgrammeProgress_gal.Items** (line ~1997):
```
ForAll(Distinct(colActivities, ProgrammeLabel), With({progName: Prog.Value},
    With({progActivities: Filter(colActivities, ...)},
        With({progReportsFY: Filter(colReportsInScope, ...), ...},
            {ProgrammeName, TotalActivities, MonthlyReportedCount,
             MonthlyApprovedCount, FYApprovedActivityCount, ...}
        ))))
```
- **Impact:** Heavy per-programme aggregation with multiple Distinct + CountRows
- **Recommendation:** Pre-compute programme stats in `OnVisible`

### 6.2 Home Screen — Raw SharePoint Query (MEDIUM)

**Subtitle label** (line ~657):
```
CountRows(Distinct(Directorates, DirectorateID))
```
- **Impact:** Queries raw SharePoint `Directorates` list on every screen visit
- **Recommendation:** Use `CountRows(colDirectorates)` (already collected in App.OnStart)

### 6.3 Home Screen — Multiple KPI Card Distinct Calls (MEDIUM)

Several KPI cards use `CountRows(Distinct(colReportsInScope, Activity.Id))` — these run on collections (OK for delegation) but are repeated multiple times with slight variations.

### 6.4 ReportActivities — Re-collecting Programmes (LOW)

**OnVisible** re-collects `ClearCollect(colProgrammes, Programmes)` every visit. Already collected in App.OnStart.

---

## 7. Remaining Accessibility Issues

### 7.1 Color Contrast (MEDIUM)
Some icons use low-contrast colors on light backgrounds:
- Search icons: `Color: =RGBA(153, 153, 153, 1)` on `#F8F8F8` background
- ChevronRight icons: `Color: =RGBA(204, 204, 204, 1)` on white
- **WCAG AA requires 4.5:1 contrast ratio for normal text/icons**

### 7.2 Gallery Row Items (LOW)
Gallery children (row titles, status labels) don't have `AccessibleLabel` set — screen readers may not announce them properly.

### 7.3 Hidden Elements (LOW)
Some elements with `Visible: =false` are still in the DOM — screen readers may still announce them.

---

## 8. Screen Inventory

| Screen | File | Lines | Purpose |
|--------|------|-------|---------|
| App | App.pa.yaml | ~95 | OnStart, theme, user role, filters |
| scr_Splash | scr_Splash.pa.yaml | ~120 | Splash screen with timer |
| scr_Home | scr_Home.pa.yaml | ~2,750 | Dashboard with KPIs, filters, galleries |
| scr_Users | scr_Users.pa.yaml | ~1,410 | User registration form |
| scr_MyActivities | scr_MyActivities.pa.yaml | ~738 | Contributor's activity worklist |
| scr_ReportForm | scr_ReportForm.pa.yaml | ~800 | Monthly report create/edit |
| scr_ReportView | scr_ReportView.pa.yaml | ~793 | Read-only report detail |
| scr_Projects | scr_Projects.pa.yaml | ~1,658 | Projects master-detail CRUD |
| scr_Activities | scr_Activities.pa.yaml | ~1,598 | Activities master-detail CRUD |
| scr_ReportActivities | scr_ReportActivities.pa.yaml | ~1,251 | Activities → Report inline master-detail |
| scr_ReportActivities_1 | scr_ReportActivities_1.pa.yaml | ~935 | Activities → Report (variant) |
| scr_Reports | scr_Reports.pa.yaml | ~4,380 | Reports dashboard with filters |
| scr_ApprovedReports | scr_ApprovedReports.pa.yaml | ~1,081 | Read-only approved reports |
| scr_ApprovalQueue | scr_ApprovalQueue.pa.yaml | ~1,500 | 2-stage review queue |
| Screen2 | Screen2.pa.yaml | ~950 | (Template/placeholder screen) |
| cmp_AppHeader | Component/cmp_AppHeader.pa.yaml | ~279 | Reusable header component |
| cmp_NavRail | Component/cmp_NavRail.pa.yaml | ~200 | Reusable nav rail component |

---

## 9. Tool Inventory

| Tool | Purpose |
|------|---------|
| `verify_powerfx.py` | Static formula verification (balance, nav, patch keys, delegation) |
| `check_screen_registry.py` | Screen file ↔ _EditorState drift detection |
| `check_control_props.py` | Control property schema validation (PA2108) |
| `repack_msapp.py` | Pack/unpack helper (replaces pac CLI when unavailable) |
| `build_flow_zips.py` | Build flow import package with real GUIDs |
| `normalize_activities.py` | Normalize Activities.csv labels |

---

## 10. Architecture Notes

1. **Source of truth:** CSV files in repo root (Directorates.csv, APP_Users.csv, etc.)
2. **Build pipeline:** Edit pa.yaml → repack_msapp.py → import to Studio → validate → save
3. **Delegation strategy:** Role-first filters, in-memory collections for non-delegable operations
4. **Scoping pattern:** Load all data → filter in-memory for non-admin users (avoids Lookup delegation issues)
5. **Components:** `cmp_AppHeader` + `cmp_NavRail` used across all screens
6. **Naming:** `var` prefix for variables, `col` for collections, `scr` for screens

---

*This document supersedes the previous AUDIT_FINDINGS.md (Aug 18) and PERFORMANCE_ANALYSIS.md (Aug 19).*
