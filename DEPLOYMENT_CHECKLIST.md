# APP-MRMS — Deployment Checklist

**Version:** v6  
**Date:** 2026-08-18

---

## Phase 1: Environment Setup

### 1.1 SharePoint Site Provisioning
- [ ] Create SharePoint site `APP-MRMS` at `https://<tenant>.sharepoint.com/sites/APP-MRMS`
- [ ] Create **Directorates** list with columns:
  - [ ] Title (Text, required) — display name = "DirectorateName"
  - [ ] DirectorateID (Text) — short code like "ICT", "HRM"
  - [ ] Programme (Text)
  - [ ] Director (Person)
  - [ ] DeputyDirector (Person)
  - [ ] Deligate (Person)
  - [ ] Active (Boolean, default: Yes)
- [ ] Create **APP_Users** list with columns:
  - [ ] Title (Text, required)
  - [ ] UserAccount (Person)
  - [ ] Role (Choice): Administrator / ProgrammeManager / Supervisor / Contributor / DeputyDirectorME
  - [ ] Directorate (Text)
  - [ ] Directorate: DirectorateID (Lookup → Directorates)
  - [ ] Programme (Text)
  - [ ] Active (Boolean, default: Yes)
- [ ] Create **MonthlyReports** list with columns:
  - [ ] Title (Text, required)
  - [ ] Programme (Text)
  - [ ] Directorate (Text)
  - [ ] ProgrammeLabel (Text)
  - [ ] DirectorateLabel (Text)
  - [ ] Project (Lookup → Projects)
  - [ ] ProjectOwnerLabel (Text)
  - [ ] Activity (Lookup → Activities)
  - [ ] ActivityOwnerLabel (Text)
  - [ ] Activity: ActivityShortDescription (Lookup column)
  - [ ] Activity: StartDate (Lookup column)
  - [ ] Activity: EndDate (Lookup column)
  - [ ] Activity: DueDate (Lookup column)
  - [ ] ReportingMonth (Choice): April / May / June / July / August / September / October / November / December / January / February / March
  - [ ] Quarter (Choice): Q1 / Q2 / Q3 / Q4 / All
  - [ ] FinancialYear (Choice): 2026/27 / 2025/26 / 2024/25 / All
  - [ ] PlannedAct (Multi-line text)
  - [ ] PercentageComplete (Number, 0-100)
  - [ ] Status (Choice): **Draft / Submitted / SupervisorApproved** / Approved / Rejected / Escalated
  - [ ] Version (Number)
  - [ ] SubmittedBy (Person)
  - [ ] SubmissionDate (Date)
  - [ ] ReviewedBy (Person)
  - [ ] ReviewDate (Date)
  - [ ] RejectionReason (Multi-line text)
  - [ ] IsOverdue (Boolean)
  - [ ] isFlagged (Boolean)
  - [ ] ReasonForDeviation (Multi-line text)
  - [ ] RemedialAction (Multi-line text)
  - [ ] Output (Multi-line text)
- [ ] Create **Activities** list with columns:
  - [ ] Title (Text, required)
  - [ ] ActivityCode (Text)
  - [ ] ActivityDescription (Multi-line text)
  - [ ] ActivityShortDescription (Text)
  - [ ] Directorate (Lookup → Directorates)
  - [ ] DirectorateLabel (Text)
  - [ ] ProgrammeLabel (Text)
  - [ ] Project (Lookup → Projects)
  - [ ] Project: Reference (Lookup column)
  - [ ] Frequency (Choice): Monthly / Quarterly / Annual
  - [ ] Owner (Person)
  - [ ] ActivityOwner (Person)
  - [ ] Supervisor (Person)
  - [ ] StartDate (Date)
  - [ ] EndDate (Date)
  - [ ] DueDate (Date)
  - [ ] Active (Boolean, default: Yes)
  - [ ] Status (Choice): Active / Completed / Not Started
- [ ] Create **Projects** list with columns:
  - [ ] Title (Text) — display name = "ProjectID"
  - [ ] ProjectCode (Text)
  - [ ] PriorityChallenge (Text)
  - [ ] ProjectGoalDescription (Multi-line text)
  - [ ] KeyDeliverable (Multi-line text)
  - [ ] AnnualTarget (Multi-line text)
  - [ ] Reference (Text)
  - [ ] Budget (Text) — NOT Currency
  - [ ] Directorate (Lookup → Directorates)
  - [ ] Directorate: Title (Lookup column)
  - [ ] Programme (Text) — NOT a Lookup
  - [ ] Responsibility (Person)
  - [ ] StartDate (Date)
  - [ ] CompletionDate (Date)
  - [ ] FinancialYear (Choice): 2026/27 / 2025/26 / 2024/25 / 2023/24 / 2022/23
  - [ ] Status (Choice): Active / Closed / Cancelled
- [ ] Create **Programmes** list with columns:
  - [ ] Title (Text, required)
  - [ ] ProgrammeCode (Text)
  - [ ] ProgrammeManager (Person)
  - [ ] Description (Multi-line text)
  - [ ] Active (Boolean, default: Yes)
- [ ] Create **Notifications** list
- [ ] Create **AuditLog** list
- [ ] Create **ReportComments** list
- [ ] Create **EvidenceLibrary** list (document library)
- [ ] Create **KPIDefinitions** list

### 1.2 APP_Users Seeding
- [ ] Create user with Role = **Administrator** (real M365 account)
- [ ] Create user with Role = **ProgrammeManager** (real M365 account)
- [ ] Create user with Role = **Supervisor** (real M365 account)
- [ ] Create user with Role = **Contributor** (real M365 account)
- [ ] Create user with Role = **DeputyDirectorME** (real M365 account)

### 1.3 Data Import
- [ ] Import Directorates.csv seed data (17 rows)
- [ ] Import Programmes.csv seed data (5 rows)
- [ ] Import Activities.csv seed data (516 rows)
- [ ] Import Projects.csv seed data
- [ ] Import MonthlyReports.csv seed data (4 rows)
- [ ] Verify all lookups resolve correctly

---

## Phase 2: Power Apps Import

### 2.1 Pre-Import Checks
- [ ] Run `python3 tools/check_screen_registry.py` — expect 0 problems
- [ ] Run `python3 tools/check_control_props.py` — expect 0 errors
- [ ] Run `python3 tools/verify_powerfx.py --strict` — expect 0 errors
- [ ] Run `python3 -c "import yaml,glob; [yaml.compose(open(f,encoding='utf-8')) for f in glob.glob('APP_MRMS/src/Src/*.pa.yaml')]"` — YAML parse OK

### 2.2 Import
- [ ] Open https://make.powerapps.com
- [ ] Sign in with account that can create apps in target environment
- [ ] Apps → Import canvas app → upload `APP-MRMS_Project_app_v6.msapp`
- [ ] Re-link data sources if prompted (11 SharePoint lists + Office365Users)
- [ ] Open imported app once for edit (loads from embedded YAML)
- [ ] Save in Studio (File → Save)

### 2.3 Post-Import Validation
- [ ] Walk splash → Home (KPIs load, filters work)
- [ ] Walk Home → Projects (list loads, CRUD works)
- [ ] Walk Home → Activities (list loads, CRUD works)
- [ ] Walk Home → Monthly Reports (activities load, report form works)
- [ ] Walk Home → My Activities (personal list loads, row actions work)
- [ ] Walk Home → Reports Dashboard (filters work, gallery loads)
- [ ] Walk Home → Approved Reports (read-only dashboard loads)
- [ ] Walk Home → Approval Queue (queue loads, Approve/Reject/Return work)
- [ ] Walk Home → Users (registration form works)
- [ ] Check sidebar rail navigation on every screen
- [ ] Check header shows signed-in user on every screen
- [ ] Check responsive behaviour (resize preview window)

---

## Phase 3: Power Automate Import

### 3.1 Pre-Import
- [ ] Find list GUIDs: MonthlyReports, Activities, Notifications, AuditLog, APP_Users
- [ ] Rebuild flow package:
  ```bash
  python3 tools/build_flow_zips.py \
    --site-url "https://<tenant>.sharepoint.com/sites/APP-MRMS" \
    --monthlyreports "<MR-GUID>" \
    --activities "<ACT-GUID>" \
    --notifications "<NOTIF-GUID>" \
    --auditlog "<AUDIT-GUID>" \
    --users "<USERS-GUID>" \
    --output flows/APP-MRMS-Approval.zip
  ```

### 3.2 Import
- [ ] Open https://make.powerautomate.com
- [ ] My flows → Import → Package (.zip)
- [ ] Upload `flows/APP-MRMS-Approval.zip`
- [ ] Create/select SharePoint connection (user with Contribute)
- [ ] Create/select Office 365 Outlook connection (licensed mailbox)
- [ ] Choose New for each flow
- [ ] Turn on each flow after import

### 3.3 Flow Validation
- [ ] Submit a report → verify Supervisor receives email + notification
- [ ] Supervisor approves → verify Deputy receives email + notification
- [ ] Deputy approves → verify Contributor + Supervisor receive email
- [ ] Check AuditLog entries created
- [ ] Check Notifications entries created

---

## Phase 4: Known Fixes

- [ ] Fix `Fecbruary` typo in MonthlyReports ReportingMonth choices (before SharePoint provisioning)
- [ ] Fix rejection flow duplicate action names (before flow import)
- [ ] Decide and implement DeputyDirectorME role (mandatory vs escalation)
- [ ] Decide and implement activity completion logic
- [ ] Confirm splash timing (1.8s vs 10s)

---

## Rollback Plan

If import fails:
1. Keep pristine `backup/original-pack/APP-MRMS_Project_app.msapp` as fallback
2. Re-run verification tools, fix errors, repack
3. Retry import

If flows fail:
1. Check connection permissions
2. Verify list GUIDs match
3. Verify choice values match
4. Check flow run history for errors
