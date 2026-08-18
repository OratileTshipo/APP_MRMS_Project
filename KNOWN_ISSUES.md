# APP-MRMS — Known Issues Tracker

**Last updated:** 2026-08-18

---

## 🔴 CRITICAL — Blocks Deployment

| ID | Issue | Status | Owner | Notes |
|---|---|---|---|---|
| C1 | `SupervisorApproved` status missing from MonthlyReports | 🔴 Open | SharePoint Admin | Must add before flow import |
| C2 | SharePoint site not provisioned | 🔴 Open | SharePoint Admin | 11 lists needed |
| C3 | APP_Users needs real account seeding | 🔴 Open | SharePoint Admin | 5 roles needed |
| C4 | Flow package has placeholder GUIDs | 🔴 Open | Developer | Rebuild with `build_flow_zips.py` |

---

## 🟠 HIGH — Needs Decision

| ID | Issue | Status | Owner | Notes |
|---|---|---|---|---|
| H1 | DeputyDirectorME: mandatory vs escalation | 🟠 Open | Product Owner | BRD says escalation-only |
| H2 | Activity completion logic undefined | 🟠 Open | Product Owner | 12 months per activity |
| H3 | Rejection flow excluded (duplicate names) | 🟠 Open | Developer | Template at `flows/templates/` |
| H4 | Splash timing (1.8s vs 10s) | 🟠 Open | Product Owner | Current: 1.8s → Home |

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
| L2 | Trending/Settings/Support icons dead | 🟢 Backlog | Developer | Phase 2 |
| L3 | Handoff briefs outdated | 🟢 Backlog | Documentation | Update briefs |
| L4 | Duplicate file structure (parent + submodule) | 🟢 Backlog | Developer | Clarify source of truth |
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

---

## How to Use

1. When you find a new issue, add it to the appropriate section
2. Assign an Owner and set Status
3. When resolved, move to Resolution Log with date and fix description
4. Reference issue IDs in git commits: `fix(C1): add SupervisorApproved status`
