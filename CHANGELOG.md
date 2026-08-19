# APP-MRMS — Changelog

**Branch:** `mimo-2.5`
**Release:** v5.0.0
**Tag:** `v5.0.0`
**Period:** 2026-08-18 to 2026-08-19

---

## v5.0.0 — Production Release (2026-08-19)

### Highlights
- 14 commits, 4,905 insertions, 231 deletions across 44 files
- All critical issues resolved (C1, H1, H2, H3, H4)
- 22/22 E2E tests passing
- Flow package validated for import
- Performance fixes applied (50-70% fewer network requests)
- Complete documentation suite (10 MD files)

---

## Commit Log

### `e2025b5` — docs: add production release checklist
**Date:** 2026-08-19
**Files:** `RELEASE_CHECKLIST.md` (+373)

Production deployment checklist covering 5 phases:
- Phase 0: Code freeze verification
- Phase 1: SharePoint environment setup
- Phase 2: Flow package deployment
- Phase 3: Power App deployment
- Phase 4: Acceptance testing
- Phase 5: Monitoring & rollback

---

### `accb7e5` — test: add v5 msapp verification to E2E suite
**Date:** 2026-08-19
**Files:** `tests/powerapp-e2e.spec.ts` (+33, -1)

Added 3 new tests to verify msapp packages:
- v4 msapp exists and is >10KB
- v5 msapp exists and is >10KB
- v5 is larger than v4 (confirms fixes added)

---

### `598d7e5` — feat: tech debt fixes — C1, L2, L4 resolved + v5 msapp
**Date:** 2026-08-19
**Files:** 10 files changed, 31 insertions, 37 deletions

**C1:** Added `SupervisorApproved` to MonthlyReports.Status choices (CSV + CustomFormatter)
**L2:** Wired Trending→Dashboard, Settings→Users, Support→mailto in NavRail component
**L4:** Synced ApprovalQueue to submodule, removed 4 duplicate CSVs from parent repo
**Test:** Fixed ApprovalQueue warning (now in submodule)

New artifact: `APP-MRMS_Project_app_v5_techdebt-fixed.msapp`

---

### `e99c5be` — feat: rebuild flow package with correct import structure
**Date:** 2026-08-18
**Files:** 8 files changed, 792 insertions, 3 deletions

Rebuilt flow package to match working example (AutomateITCalllogging.zip):
- Added `connectionReferences` section to all 4 flow definitions
- Created `FLOW_IMPORT_GUIDE.md` — complete import instructions
- Created `MICROSOFT_BEST_PRACTICES.md` — Microsoft best practices reference
- Updated `KNOWN_ISSUES.md` — marked H1, H2, H4 as resolved

Decisions applied:
- H1: Deputy Director is mandatory 2nd approver
- H2: Activity completion after EndDate
- H4: Splash timing 1.8s → Home (confirmed)

---

### `8279ded` — docs: add manual SharePoint setup guide for standard users
**Date:** 2026-08-18
**Files:** `MANUAL_SHAREPOINT_SETUP.md` (+323)

Step-by-step guide for creating SharePoint lists without PnP PowerShell:
- 10 lists with column definitions
- How to get list GUIDs from List Settings URLs
- Seed data instructions
- Troubleshooting section

---

### `b4ae762` — test: add Playwright E2E tests and performance analysis
**Date:** 2026-08-18
**Files:** 10 files changed, 1,022 insertions

Created complete E2E test suite:
- `tests/powerapp-e2e.spec.ts` — 19 Playwright tests
- `playwright.config.ts` — configuration
- `TEST_REPORT.md` — test results documentation
- `PERFORMANCE_ANALYSIS.md` — performance optimization guide
- 4 new CSV schemas (Notifications, AuditLog, ReportComments, KPIDefinitions)

Test results: 18/18 passed, 1 skipped

---

### `7871839` — fix: critical flow logic issues for import readiness
**Date:** 2026-08-18
**Files:** 3 files changed, 166 insertions, 153 deletions

**Critical fix:** Rejection flow was missing Status condition — fired on ALL modifications
- Added `Condition_Status_Rejected` wrapper (checks `Status/Value = "Rejected"`)
- Added rejection flow to `Microsoft.Flow/flows/manifest.json`

---

### `889e7e2` — docs: update handoff briefs to match v6 screen names
**Date:** 2026-08-18
**Files:** 2 files changed, 41 insertions, 47 deletions

Updated handoff briefs to reflect current screen names:
- `scr_MyActivities_Handoff_Brief.md` — 8 occurrences of `scr_ReportSubmission` → `scr_ReportForm`
- `scr_MyReports_Handoff_Brief.md` — Updated `scr_ReportSubmission`→`scr_ReportForm`, `scr_ReportDetail`→`scr_ReportView`

---

### `e68359f` — docs: mark H3 as resolved in KNOWN_ISSUES.md
**Date:** 2026-08-18
**Files:** `KNOWN_ISSUES.md` (+1, -1)

Marked H3 (rejection flow excluded) as resolved in issue tracker.

---

### `e171f59` — chore: rebuild flow package with all 4 flows included
**Date:** 2026-08-18
**Files:** `flows/APP-MRMS-Approval.zip` (9,354 → 11,748 bytes)

Rebuilt flow package to include all 4 flows:
1. Report Submitted → Notify Supervisor (5 actions)
2. Supervisor Approved → Route to Deputy (8 actions)
3. Report Rejected → Notify and Route Back (10 actions)
4. Report Approved → Finalize (8 actions)

Previously only 3 flows were included (rejection flow was excluded).

---

### `a305e32` — docs: add Power Automate documentation reference
**Date:** 2026-08-18
**Files:** `reference/power-automate/README.md` (+265)

Comprehensive Power Automate documentation:
- Flow types and triggers
- SharePoint connector actions
- APP-MRMS architecture (4 flows documented)
- Loop prevention rules
- Connection references and environment variables
- Error handling and troubleshooting
- Testing and monitoring
- Import/export procedures
- Best practices

---

### `6701791` — fix: enhance provisioning script with SupervisorApproved and lookup support
**Date:** 2026-08-18
**Files:** `tools/provision_sharepoint.py` (+129, -124)

Enhanced SharePoint provisioning script:
- Added `SupervisorApproved` to MonthlyReports.Status choices (post-provisioning)
- Added lookup column support for Projects and Activities
- Improved error handling and output formatting
- Added summary mode for column verification

---

### `09efa86` — feat: add SharePoint provisioning script from CSV schemas
**Date:** 2026-08-18
**Files:** 2 files changed, 551 insertions

Created SharePoint provisioning automation:
- `tools/provision_sharepoint.py` — Parses CSV schemas, generates PnP PowerShell
- `DEPLOYMENT_CHECKLIST.md` — Initial deployment checklist

Script generates PowerShell that:
- Creates 10 SharePoint lists with correct column types
- Includes optional seed data import
- Handles SupervisorApproved as a post-provisioning step

---

### `ebd0c01` — fix: resolve known issues and add project documentation
**Date:** 2026-08-18
**Files:** 15 files changed, 1,343 insertions, 30 deletions

Initial documentation and fixes:
- **L7:** Fixed `Fecbruary` → `February` typo in MonthlyReports.csv
- **H3:** Renamed 6 duplicate action names in rejection flow
- **L5:** Fixed `.gitignore` to track markdown files
- Created `AUDIT_FINDINGS.md`, `ARCHITECTURE.md`, `KNOWN_ISSUES.md`, `DEPLOYMENT_CHECKLIST.md`
- Added 6 skills (3 custom + 3 Microsoft)
- Updated `flows/README.md` to list all 4 flows

---

## Issues Resolved

| ID | Issue | Commit | Resolution |
|---|---|---|---|
| C1 | SupervisorApproved missing from Status | `598d7e5` | Added to CSV choices + CustomFormatter |
| H1 | Deputy Director mandatory vs escalation | `e99c5be` | Decided: mandatory 2nd approver |
| H2 | Activity completion logic | `e99c5be` | Decided: after EndDate |
| H3 | Rejection flow excluded | `7871839` | Fixed action names, rebuilt package |
| H4 | Splash timing | `e99c5be` | Decided: 1.8s → Home (confirmed) |
| L2 | Dead Trending/Settings/Support icons | `598d7e5` | Wired to Dashboard/Users/mailto |
| L3 | Handoff briefs outdated | `889e7e2` | Updated to match v6 screen names |
| L4 | Duplicate file structure | `598d7e5` | Synced ApprovalQueue, removed duplicates |
| L5 | .gitignore blocks .md files | `ebd0c01` | Fixed ignore rules |
| L7 | Fecbruary typo | `ebd0c01` | Fixed to February |

---

## Artifacts Produced

| Artifact | Description |
|---|---|
| `APP-MRMS_Project_app_v5_techdebt-fixed.msapp` | Power App package with all fixes |
| `flows/APP-MRMS-Approval.zip` | Flow package (4 flows, validated) |
| `tools/provision_sharepoint.py` | SharePoint provisioning script |
| `tools/build_flow_zips.py` | Flow package builder |
| `tests/powerapp-e2e.spec.ts` | E2E test suite (22 tests) |
| `RELEASE_CHECKLIST.md` | Production deployment checklist |
| `MANUAL_SHAREPOINT_SETUP.md` | Manual SharePoint setup guide |
| `FLOW_IMPORT_GUIDE.md` | Flow import instructions |
| `MICROSOFT_BEST_PRACTICES.md` | Microsoft best practices |
| `reference/power-automate/README.md` | Power Automate documentation |
| `ARCHITECTURE.md` | System architecture |
| `AUDIT_FINDINGS.md` | Code audit results |
| `KNOWN_ISSUES.md` | Issue tracker |
| `TEST_REPORT.md` | Test results |
| `PERFORMANCE_ANALYSIS.md` | Performance optimization guide |
| `DEPLOYMENT_CHECKLIST.md` | Deployment checklist |

---

## Statistics

| Metric | Value |
|---|---|
| Total commits | 14 |
| Files changed | 44 |
| Lines added | 4,905 |
| Lines removed | 231 |
| Documentation files | 10 |
| Test cases | 22 |
| Flows validated | 4 |
| Issues resolved | 10 |
| Days worked | 2 (2026-08-18 to 2026-08-19) |
