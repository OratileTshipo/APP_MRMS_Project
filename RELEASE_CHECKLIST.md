# APP-MRMS — Production Release Checklist

**Version:** v5 (mimo-2.5 branch)
**Date:** 2026-08-19
**Last commit:** `accb7e5`

---

## Pre-Release Sign-Off

| Gate | Owner | Status |
|---|---|---|
| All source code tests pass (22/22) | Developer | ☐ |
| Flow package validated (4 flows) | Developer | ☐ |
| Performance fixes applied | Developer | ☐ |
| Known issues resolved or documented | Developer | ☐ |
| Product owner decisions captured | Product Owner | ☐ |
| SharePoint lists ready | SharePoint Admin | ☐ |
| UAT completed | QA | ☐ |

---

## Phase 0: Code Freeze Verification

Run these commands from the repo root before starting deployment:

```bash
# 1. Screen Registry (expect 0 problems)
cd APP_MRMS && python3 tools/check_screen_registry.py

# 2. Control Properties (expect 0 errors, ~36 expected warnings)
python3 tools/check_control_props.py

# 3. Power Fx Static (expect 0 errors)
python3 tools/verify_powerfx.py --strict

# 4. YAML Parse Gate (expect no errors)
python3 -c "import yaml,glob; [yaml.compose(open(f,encoding='utf-8')) for f in glob.glob('src/Src/*.pa.yaml')]"

# 5. Playwright Tests (expect 22 passed)
cd .. && npx playwright test tests/powerapp-e2e.spec.ts --reporter=list
```

| Check | Expected | Actual |
|---|---|---|
| Screen Registry | 12 files ↔ 12 entries, 0 problems | ☐ |
| Control Properties | 0 errors, 36 warnings (expected) | ☐ |
| Power Fx Static | 0 errors, 0 warnings | ☐ |
| YAML Parse | All files parse | ☐ |
| Playwright Tests | 22/22 pass, 1 skipped | ☐ |

---

## Phase 1: SharePoint Environment Setup

### 1.1 Create SharePoint Site

- [ ] Create site: `https://<tenant>.sharepoint.com/sites/APP-MRMS`
- [ ] Verify permissions: Site Owner or Contributor
- [ ] Set privacy to **Private**

### 1.2 Create Lists (10 lists)

Follow `MANUAL_SHAREPOINT_SETUP.md` for step-by-step UI instructions.

| # | List Name | Columns | Seed Data |
|---|---|---|---|
| 1 | Directorates | 7 | 18 rows |
| 2 | Programmes | 6 | 5 rows |
| 3 | Projects | 16 | 54 rows |
| 4 | Activities | 15 | 516 rows |
| 5 | MonthlyReports | 23 | 4 rows |
| 6 | APP_Users | 5 | 5 rows |
| 7 | Notifications | 6 | — |
| 8 | AuditLog | 7 | — |
| 9 | ReportComments | 5 | — |
| 10 | KPIDefinitions | 5 | — |

### 1.3 Critical Column Verification

**MonthlyReports.Status must include:**

- [ ] Draft
- [ ] Submitted
- [ ] **SupervisorApproved** ← CRITICAL (Flow 2 trigger)
- [ ] Approved
- [ ] Rejected
- [ ] Escalated

**MonthlyReports.ReportingMonth must include:**

- [ ] January (NOT "Fecbruary" — already fixed)

**APP_Users.Role must include:**

- [ ] Administrator
- [ ] ProgrammeManager
- [ ] Supervisor
- [ ] Contributor
- [ ] DeputyDirectorME

### 1.4 APP_Users Seeding

Create at least one real M365 account per role:

| Role | Account | Name |
|---|---|---|
| Administrator | _________________ | _________________ |
| ProgrammeManager | _________________ | _________________ |
| Supervisor | _________________ | _________________ |
| Contributor | _________________ | _________________ |
| DeputyDirectorME | _________________ | _________________ |

### 1.5 Get List GUIDs

After creating lists, get GUIDs from List Settings URLs:

| List | GUID |
|---|---|
| MonthlyReports | _________________ |
| Activities | _________________ |
| Notifications | _________________ |
| AuditLog | _________________ |
| APP_Users | _________________ |

---

## Phase 2: Flow Package Deployment

### 2.1 Rebuild Flow Package with Real GUIDs

```bash
python3 tools/build_flow_zips.py \
  --site-url "https://<tenant>.sharepoint.com/sites/APP-MRMS" \
  --monthlyreports "<MonthlyReports-GUID>" \
  --activities "<Activities-GUID>" \
  --notifications "<Notifications-GUID>" \
  --auditlog "<AuditLog-GUID>" \
  --users "<APP_Users-GUID>" \
  --output flows/APP-MRMS-Approval.zip
```

- [ ] Command completed without errors
- [ ] Output file exists: `flows/APP-MRMS-Approval.zip`

### 2.2 Verify Package Contents

```bash
python3 -c "
import zipfile, json
with zipfile.ZipFile('flows/APP-MRMS-Approval.zip') as z:
    print('Files:', len(z.namelist()))
    manifest = json.loads(z.read('Microsoft.Flow/flows/manifest.json'))
    print('Flows:', len(manifest['flowAssets']['assetPaths']))
    for f in manifest['flowAssets']['assetPaths']:
        d = json.loads(z.read(f'Microsoft.Flow/flows/{f}/definition.json'))
        name = d['properties']['displayName']
        actions = len(d['properties']['definition']['actions'])
        print(f'  {name}: {actions} actions')
"
```

- [ ] 4 flows in package
- [ ] All display names correct
- [ ] All action counts match expected

### 2.3 Import to Power Automate

- [ ] Go to https://make.powerautomate.com
- [ ] **My flows** → **Import** → **Package (.zip)**
- [ ] Upload `flows/APP-MRMS-Approval.zip`
- [ ] Map SharePoint connection → `_________________`
- [ ] Map Office 365 Outlook connection → `_________________`
- [ ] Import all 4 flows
- [ ] Turn on Flow 1: Report Submitted → Notify Supervisor
- [ ] Turn on Flow 2: Supervisor Approved → Route to Deputy
- [ ] Turn on Flow 3: Report Rejected → Notify and Route Back
- [ ] Turn on Flow 4: Report Approved → Finalize

### 2.4 Flow Validation

Test each flow trigger:

| Flow | Test Action | Expected Result |
|---|---|---|
| Flow 1 | Set MonthlyReports.Status = "Submitted" | Supervisor receives email |
| Flow 2 | Set MonthlyReports.Status = "SupervisorApproved" | Deputy receives email |
| Flow 3 | Set MonthlyReports.Status = "Rejected" | Contributor receives email |
| Flow 4 | Set MonthlyReports.Status = "Approved" | Contributor + Supervisor receive email |

- [ ] Flow 1 triggers correctly
- [ ] Flow 2 triggers correctly
- [ ] Flow 3 triggers correctly
- [ ] Flow 4 triggers correctly
- [ ] Notifications created in SharePoint
- [ ] AuditLog entries created
- [ ] No infinite loops (flows don't write to MonthlyReports.Status)

---

## Phase 3: Power App Deployment

### 3.1 Pre-Import

- [ ] Use `APP-MRMS_Project_app_v5_techdebt-fixed.msapp` (latest)
- [ ] Verify file exists and is >10KB
- [ ] All verification tools pass (Phase 0)

### 3.2 Import to Power Apps

- [ ] Go to https://make.powerapps.com
- [ ] **Apps** → **Import** → **Package (.zip)**
- [ ] Upload `APP-MRMS_Project_app_v5_techdebt-fixed.msapp`
- [ ] Map SharePoint connection → `_________________`
- [ ] Map Office365Users connector → `_________________`
- [ ] Import completes without errors

### 3.3 Post-Import Validation

Open the app in Power Apps Studio and verify:

#### Navigation
- [ ] Splash loads and transitions to Home after 1.8s
- [ ] Sidebar rail shows all icons with active states
- [ ] Trending icon → navigates to Reports Dashboard
- [ ] Settings icon → navigates to Users screen
- [ ] Support icon → opens mailto link
- [ ] All 12 screens accessible from sidebar

#### Screens
- [ ] **Home** — KPIs load, filters work, counts display
- [ ] **Projects** — list loads, CRUD works
- [ ] **Activities** — list loads, CRUD works
- [ ] **My Activities** — personal list loads, actions work
- [ ] **Report Form** — form loads, submission works
- [ ] **Report View** — report displays correctly
- [ ] **Reports Dashboard** — filters work, gallery loads
- [ ] **Approved Reports** — read-only dashboard loads
- [ ] **Approval Queue** — queue loads, Approve/Reject/Return work
- [ ] **Users** — registration form works

#### Data
- [ ] All dropdowns populated (Programmes, Directorates, etc.)
- [ ] Cached collections load on screen entry
- [ ] Search works on Reports Dashboard
- [ ] User role determines visible data

#### Responsive
- [ ] Resize preview window — layout adapts
- [ ] No overlapping controls
- [ ] Text readable at all sizes

---

## Phase 4: Acceptance Testing

### 4.1 Contributor Workflow

- [ ] Login as Contributor
- [ ] Create new monthly report (Draft)
- [ ] Fill in all fields (Activity, Month, Quarter, FY, etc.)
- [ ] Submit report (Status → Submitted)
- [ ] Verify Supervisor receives email notification

### 4.2 Supervisor Workflow

- [ ] Login as Supervisor
- [ ] See submitted reports in Approval Queue
- [ ] Approve report (Status → SupervisorApproved)
- [ ] Verify Deputy receives email notification
- [ ] Reject a report (Status → Rejected)
- [ ] Verify Contributor receives rejection email

### 4.3 Deputy Director Workflow

- [ ] Login as DeputyDirectorME
- [ ] See SupervisorApproved reports in queue
- [ ] Approve report (Status → Approved)
- [ ] Verify Contributor + Supervisor receive approval emails
- [ ] Verify AuditLog entries created

### 4.4 Administrator Workflow

- [ ] Login as Administrator
- [ ] See all reports regardless of directorate
- [ ] Access all management screens
- [ ] User management works

### 4.5 Edge Cases

- [ ] Submit report with missing required fields → validation errors
- [ ] Approve same report twice → idempotent
- [ ] Reject with no reason → allowed
- [ ] Submit overdue report → IsOverdue flag set
- [ ] Concurrent edits → no data loss

---

## Phase 5: Monitoring & Rollback

### 5.1 Monitoring (First 48 Hours)

- [ ] Check Power Automate flow run history for errors
- [ ] Check SharePoint list item counts
- [ ] Monitor AuditLog for anomalies
- [ ] Check Notifications list for undelivered items
- [ ] Verify no duplicate email sends

### 5.2 Rollback Plan

If critical issues are found:

1. **Power App rollback:**
   - Re-import previous `.msapp` version
   - Or: Power Apps Studio → Version history → Restore previous version

2. **Flow rollback:**
   - Turn off all 4 flows
   - Debug in flow run history
   - Fix and re-import

3. **Data rollback:**
   - SharePoint list versioning (if enabled)
   - Export list data before import

---

## Post-Deployment

### Documentation Updates

- [ ] Update `KNOWN_ISSUES.md` — mark all deployment issues resolved
- [ ] Update `DEPLOYMENT_CHECKLIST.md` — record actual deployment date
- [ ] Update `CHANGES.md` — record v5 deployment
- [ ] Tag release in git: `git tag v5.0.0`

### Handoff

- [ ] Share admin credentials securely
- [ ] Share `MANUAL_SHAREPOINT_SETUP.md` with SharePoint admin
- [ ] Share `FLOW_IMPORT_GUIDE.md` with Power Automate admin
- [ ] Share `ARCHITECTURE.md` with development team
- [ ] Schedule UAT session with stakeholders

---

## Quick Reference

| Artifact | Location |
|---|---|
| Power App (v5) | `APP_MRMS/APP-MRMS_Project_app_v5_techdebt-fixed.msapp` |
| Flow Package | `flows/APP-MRMS-Approval.zip` |
| Provisioning Script | `tools/provision_sharepoint.py` |
| Flow Builder | `tools/build_flow_zips.py` |
| Manual Setup Guide | `MANUAL_SHAREPOINT_SETUP.md` |
| Flow Import Guide | `FLOW_IMPORT_GUIDE.md` |
| Architecture | `ARCHITECTURE.md` |
| Known Issues | `KNOWN_ISSUES.md` |
| Test Report | `TEST_REPORT.md` |
| Performance Analysis | `PERFORMANCE_ANALYSIS.md` |
| Best Practices | `MICROSOFT_BEST_PRACTICES.md` |

---

## Release Sign-Off

| Role | Name | Date | Signature |
|---|---|---|---|
| Developer | | | |
| SharePoint Admin | | | |
| Product Owner | | | |
| QA Lead | | | |
| Project Manager | | | |
