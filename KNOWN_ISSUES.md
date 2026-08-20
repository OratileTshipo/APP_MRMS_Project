# APP-MRMS — Known Issues Tracker

**Last updated:** 2026-08-20

---

## 🔴 CRITICAL — Blocks Deployment

| ID | Issue | Status | Owner | Notes |
|---|---|---|---|---|
| C1 | `SupervisorApproved` status missing from MonthlyReports | ✅ Resolved | Developer | Added to CSV choices and CustomFormatter |
| C2 | SharePoint site not provisioned | 🔴 Open | SharePoint Admin | 11 lists needed |
| C3 | APP_Users needs real account seeding | 🔴 Open | SharePoint Admin | 5 roles needed |
| C4 | Flow package has placeholder GUIDs | 🔴 Open | Developer | Rebuild with `build_flow_zips.py` |

---

## 🟠 HIGH — Needs Decision

| ID | Issue | Status | Owner | Notes |
|---|---|---|---|---|
| H1 | DeputyDirectorME: mandatory vs escalation | ✅ Resolved | Product Owner | **Mandatory 2nd approver** — Deputy must approve after Supervisor |
| H2 | Activity completion logic undefined | ✅ Resolved | Product Owner | **After EndDate** — Activity marked Completed when EndDate passes |
| H3 | Rejection flow excluded (duplicate names) | ✅ Resolved | Developer | Fixed action names, rebuilt package with all 4 flows |
| H4 | Splash timing (1.8s vs 10s) | ✅ Resolved | Product Owner | **1.8s** → Home (current implementation confirmed) |

---

## 🟡 MEDIUM — Runtime / Performance

| ID | Issue | Status | Owner | Notes |
|---|---|---|---|---|
| M1 | SharePoint column mismatch risk | 🟡 Pending | QA | Test after import |
| M2 | Choice-value string matching | 🟡 Pending | QA | Case-sensitive |
| M3 | Modern-control version skew | 🟡 Pending | QA | Test import |
| M4 | Delegation at runtime (2000 row limit) | ✅ Resolved | Developer | Role-first scope filters + in-memory collections |
| M5 | Home screen heavy ForAll/Sequence formulas | 🟡 Open | Developer | MonthlyTrend + ProgrammeProgress galleries recalculates on every filter change |
| M6 | Home screen raw SharePoint query | 🟡 Open | Developer | `CountRows(Distinct(Directorates, ...))` — use collected `colDirectorates` instead |
| M7 | Color contrast on icons | 🟡 Open | Developer | Search/ChevronRight icons below WCAG AA 4.5:1 ratio |

---

## 🟢 LOW — Technical Debt / Accessibility

| ID | Issue | Status | Owner | Notes |
|---|---|---|---|---|
| L1 | Sidebar/header duplication (~200 lines each) | ✅ Resolved | Developer | Extracted to `cmp_AppHeader` + `cmp_NavRail` components |
| L2 | Trending/Settings/Support icons dead | ✅ Resolved | Developer | Wired to Dashboard, Users, Support mailto |
| L3 | Handoff briefs outdated | ✅ Resolved | Documentation | Updated to match v6 screen names |
| L4 | Duplicate file structure (parent + submodule) | ✅ Resolved | Developer | Synced ApprovalQueue, removed duplicate CSVs |
| L5 | .gitignore blocks .md files | ✅ Resolved | Developer | Removed *.md rule, added proper ignores |
| L6 | Activities missing Supervisor (rows 7-12) | 🟢 Backlog | Data Owner | COMM-AC-0013 to 0018 |
| L7 | ReportingMonth typo: `Fecbruary` | ✅ Resolved | Developer | Fixed to February in MonthlyReports.csv |
| L8 | Missing AccessibleLabel on interactive icons | ✅ Resolved | Developer | Added to Search, Bell, Back, ChevronRight icons across 10 files |
| L9 | Empty OnSelect handlers | ✅ Resolved | Developer | Replaced with `Select(Parent)` or removed |
| L10 | Invalid Tooltip on ModernText (PA2108) | ✅ Resolved | Developer | Removed from scr_MyActivities |
| L11 | Broken Reset(RepActPlanned_txt) target | ✅ Resolved | Developer | Removed from scr_ReportActivities |
| L12 | Missing screens in _EditorState | ✅ Resolved | Developer | Added Screen2 + scr_ReportActivities_1 |
| L13 | Gallery row items missing AccessibleLabel | 🟢 Backlog | Developer | Screen readers may not announce row content |
| L14 | ReportActivities re-collects Programmes | 🟢 Backlog | Developer | Already collected in App.OnStart |

---

## Resolution Log

| Date | ID | Resolution |
|---|---|---|
| 2026-08-18 | L7 | Fixed `Fecbruary` → `February` in MonthlyReports.csv |
| 2026-08-18 | H3 | Fixed rejection flow duplicate action names |
| 2026-08-18 | L5 | Removed `*.md` from .gitignore |
| 2026-08-18 | H1 | **Decided:** DeputyDirectorME is mandatory 2nd approver |
| 2026-08-18 | H2 | **Decided:** Activity completion logic: after EndDate |
| 2026-08-18 | H4 | **Decided:** Splash timing: 1.8s → Home |
| 2026-08-19 | C1 | Added `SupervisorApproved` to MonthlyReports.Status choices |
| 2026-08-19 | L2 | Wired Trending→Dashboard, Settings→Users, Support→mailto |
| 2026-08-19 | L3 | Updated handoff briefs |
| 2026-08-19 | L4 | Copied scr_ApprovalQueue to submodule, updated _EditorState |
| 2026-08-20 | M4 | Fixed Projects scoping (Lookup delegation), ReportActivities scoping, CountRows delegation |
| 2026-08-20 | L8 | Added AccessibleLabel to 19 interactive icons across 10 files |
| 2026-08-20 | L9 | Replaced 2 empty OnSelect handlers with Select(Parent), removed 1 |
| 2026-08-20 | L10 | Removed invalid Tooltip from ModernText controls |
| 2026-08-20 | L11 | Removed broken Reset(RepActPlanned_txt) calls |
| 2026-08-20 | L12 | Added Screen2 + scr_ReportActivities_1 to _EditorState |

---

## How to Use

1. When you find a new issue, add it to the appropriate section
2. Assign an Owner and set Status
3. When resolved, move to Resolution Log with date and fix description
4. Reference issue IDs in git commits: `fix(C1): add SupervisorApproved status`
