# APP-MRMS — Known Issues Tracker

**Last updated:** 2026-08-19

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

## 🟡 MEDIUM — Runtime Verification

| ID | Issue | Status | Owner | Notes |
|---|---|---|---|---|
| M1 | SharePoint column mismatch risk | 🟡 Pending | QA | Test after import |
| M2 | Choice-value string matching | 🟡 Pending | QA | Case-sensitive |
| M3 | Modern-control version skew | 🟡 Pending | QA | Test import |
| M4 | Delegation at runtime (2000 row limit) | 🟡 Pending | QA | Monitor galleries |

---

## 🟢 LOW — Technical Debt

| ID | Issue | Status | Owner | Notes |
|---|---|---|---|---|
| L1 | Sidebar/header duplication (~200 lines each) | 🟢 Backlog | Developer | Extract components |
| L2 | Trending/Settings/Support icons dead | ✅ Resolved | Developer | Wired to Dashboard, Users, Support mailto |
| L3 | Handoff briefs outdated | ✅ Resolved | Documentation | Updated to match v6 screen names |
| L4 | Duplicate file structure (parent + submodule) | ✅ Resolved | Developer | Synced ApprovalQueue, removed duplicate CSVs |
| L5 | .gitignore blocks .md files | ✅ Resolved | Developer | Removed *.md rule, added proper ignores |
| L6 | Activities missing Supervisor (rows 7-12) | 🟢 Backlog | Data Owner | COMM-AC-0013 to 0018 |
| L7 | ReportingMonth typo: `Fecbruary` | ✅ Resolved | Developer | Fixed to February in MonthlyReports.csv |

---

## Resolution Log

| Date | ID | Resolution |
|---|---|---|
| 2026-08-18 | L7 | Fixed `Fecbruary` → `February` in APP_MRMS/MonthlyReports.csv (ListSchema XML, 2 occurrences) |
| 2026-08-18 | H3 | Fixed rejection flow duplicate action names (6 actions renamed), removed from EXCLUDED_FLOW_DIRS, added to manifest, updated README |
| 2026-08-18 | L5 | Removed `*.md` from .gitignore, added proper OS/Python/temp ignores |
| 2026-08-18 | H1 | **Decided:** DeputyDirectorME is mandatory 2nd approver (not escalation-only) |
| 2026-08-18 | H2 | **Decided:** Activity completion logic: after EndDate |
| 2026-08-18 | H4 | **Decided:** Splash timing: 1.8s → Home (confirmed) |
| 2026-08-19 | C1 | Added `SupervisorApproved` to MonthlyReports.Status choices in CSV (CHOICES XML + Description + rulesOrder) |
| 2026-08-19 | L2 | Wired Trending→Dashboard, Settings→Users, Support→mailto in cmp_NavRail component |
| 2026-08-19 | L3 | Updated handoff briefs: `scr_ReportSubmission`→`scr_ReportForm`, `scr_ReportDetail`→`scr_ReportView` |
| 2026-08-19 | L4 | Copied scr_ApprovalQueue.pa.yaml to submodule, updated _EditorState, removed 4 duplicate CSVs |

---

## How to Use

1. When you find a new issue, add it to the appropriate section
2. Assign an Owner and set Status
3. When resolved, move to Resolution Log with date and fix description
4. Reference issue IDs in git commits: `fix(C1): add SupervisorApproved status`
