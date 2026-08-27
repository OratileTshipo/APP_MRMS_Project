# APP-MRMS — End-to-End Manual Test Cases

**Version:** 2.5 (24Aug-09h38 build)  
**Date:** 2026-08-26  
**Tester:** _______________  
**Environment:** Power Apps Studio / Browser  
**Test Data:** SharePoint site `nwpg.sharepoint.com/sites/DPWRPerformanceandMonitoring`

---

## Pre-Test Setup

### Prerequisites
1. ✅ SharePoint lists provisioned (11 lists + EvidenceLibrary)
2. ✅ APP_Users seeded with test accounts for each role:
   - Administrator: `admin@nwpg.gov.za`
   - DeputyDirectorME: `ddme@nwpg.gov.za`
   - ProgrammeManager: `pm@nwpg.gov.za`
   - Supervisor: `supervisor@nwpg.gov.za`
   - Contributor: `contributor@nwpg.gov.za`
3. ✅ `AppPassword` column added to APP_Users (if Login screen is used)
4. ✅ Sample data loaded (Directorates, Programmes, Projects, Activities)
5. ✅ Browser: Chrome/Edge latest, desktop viewport 1366×768

### Test Data Requirements
| List | Minimum Records |
|------|----------------|
| Directorates | 3 (with active flag) |
| Programmes | 2 (with active flag) |
| Projects | 5 (across 2 programmes) |
| Activities | 10 (across 5 projects, with owners) |
| APP_Users | 5 (one per role) |

---

## TC-LOGIN: Login Screen

**Screen:** `scr_Login`  
**Prerequisites:** AppPassword column exists on APP_Users

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| L-01 | Open the app | Login screen displays with email field, password field, Login button, DPWR logo | | |
| L-02 | Leave both fields empty, click Login | Button is disabled (both fields required) | | |
| L-03 | Enter valid email, leave password empty | Button remains disabled | | |
| L-04 | Enter valid email + wrong password | Error: "Invalid email or password." Login attempts counter increments | | |
| L-05 | Enter invalid email + any password | Error: "Invalid email or password." | | |
| L-06 | Enter valid email + correct password | Navigates to scr_Home with correct user context | | |
| L-07 | Repeat wrong password 5 times | Error: "Too many failed attempts. Close and reopen the app to try again." | | |
| L-08 | Close and reopen app, login with correct credentials | Login works again (counter reset) | | |
| L-09 | Login as Administrator | User sees all data across all directorates | | |
| L-10 | Login as Contributor | User sees only their own activities | | |

---

## TC-SPLASH: Splash Screen

**Screen:** `scr_Splash`

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| SP-01 | Open the app | Splash screen shows DPWR logo and app name | | |
| SP-02 | Wait 1.8 seconds | Auto-navigates to scr_Home (or scr_Login if Login screen is active) | | |
| SP-03 | Observe transition | Smooth fade transition | | |

---

## TC-HOME: Home Dashboard

**Screen:** `scr_Home`  
**Prerequisites:** Sample data loaded, user logged in

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| H-01 | View greeting | Shows "Good morning/afternoon/evening, {User FullName}" | | |
| H-02 | View subtitle | Shows current date, quarter, FY, and directorate count | | |
| H-03 | View KPI cards | 4 cards visible: Total Reports, Pending Approvals, Overdue, Approved | | |
| H-04 | Click "Total Reports" KPI | Navigates to scr_Reports (filtered view) | | |
| H-05 | Click "Pending Approvals" KPI | Navigates to scr_ApprovalQueue (Pending tab) | | |
| H-06 | Click "Overdue" KPI | Navigates to scr_Reports (Overdue filter) | | |
| H-07 | Click "Approved" KPI | Navigates to scr_ApprovedReports | | |
| H-08 | Change FY filter dropdown | KPIs and galleries update to reflect filtered data | | |
| H-09 | Change Programme filter dropdown | Galleries filter by programme | | |
| H-10 | Change Directorate filter dropdown | Galleries filter by directorate | | |
| H-11 | Change Quarter filter dropdown | Galleries filter by quarter | | |
| H-12 | Set all filters to "All" | Full dataset shown | | |
| H-13 | View Monthly Trend chart | 12-month bar chart shows on-time vs late activities | | |
| H-14 | View Programme Progress panel | Per-programme completion rates displayed | | |
| H-15 | View Recent Reports gallery | Latest submitted/approved reports listed | | |
| H-16 | Click a report in Recent Reports | Navigates to scr_ReportView with that report | | |
| H-17 | View Notifications panel | Personal unread notifications shown | | |
| H-18 | Click notification bell icon | Shows notification list or navigates to notifications | | |
| H-19 | Resize browser to <640px | Sidebar collapses, layout becomes responsive | | |
| H-20 | Resize browser to >640px | Sidebar expands, layout returns to desktop | | |
| H-21 | Login as Administrator | KPIs show data across ALL directorates | | |
| H-22 | Login as ProgrammeManager | KPIs show data for own programme only | | |
| H-23 | Login as Supervisor | KPIs show data for own directorate only | | |
| H-24 | Login as Contributor | KPIs show own data only | | |

---

## TC-MYACTIVITIES: My Activities

**Screen:** `scr_MyActivities`  
**Prerequisites:** Contributor user has assigned activities

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| MA-01 | Navigate to My Activities | Personal activity list displayed | | |
| MA-02 | View activity list | Each row shows: activity name, project, owner, frequency, due date, report status | | |
| MA-03 | Filter by FY | Activities filtered by selected financial year | | |
| MA-04 | Filter by Month | Activities filtered by selected month | | |
| MA-05 | Filter by Status | Activities filtered by status (Not Started, Draft, Submitted, Approved, Rejected) | | |
| MA-06 | Click "New" action button | Navigates to scr_ReportForm (New mode) with activity context | | |
| MA-07 | Click "Edit" action button on Draft report | Navigates to scr_ReportForm (Edit mode) with existing report | | |
| MA-08 | Click "View" action button on Approved report | Navigates to scr_ReportView with that report | | |
| MA-09 | View report status indicator | Shows correct status pill (color-coded) | | |
| MA-10 | Click back button | Returns to previous screen | | |

---

## TC-ACTIVITIES: Activities CRUD

**Screen:** `scr_Activities`  
**Prerequisites:** Admin or Supervisor user

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| A-01 | Navigate to Activities | Activity gallery on left, detail form on right | | |
| A-02 | Search activities | Gallery filters by search text | | |
| A-03 | Click an activity in gallery | Detail form populates with activity data | | |
| A-04 | Click "New" button | Empty form for new activity | | |
| A-05 | Fill required fields | ActivityCode, Title, Description, ShortDescription, Directorate, Programme, Project, Frequency, Owner, StartDate, EndDate, DueDate, Status | | |
| A-06 | Click Save | New activity created, gallery refreshes, auto-generated ActivityCode (e.g., COMM-AC-0001) | | |
| A-07 | Edit an existing activity | Modify fields, click Save | | |
| A-08 | Verify save | Changes persisted, gallery shows updated data | | |
| A-09 | Delete an activity | Confirmation dialog, activity removed | | |
| A-10 | View as Admin | See all activities | | |
| A-11 | View as Supervisor | See activities in own directorate only | | |
| A-12 | View as Contributor | See own activities only | | |

---

## TC-PROJECTS: Projects CRUD

**Screen:** `scr_Projects`  
**Prerequisites:** Admin user

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| P-01 | Navigate to Projects | Project gallery on left, detail form on right | | |
| P-02 | Search projects | Gallery filters by search text | | |
| P-03 | Click a project in gallery | Detail form populates with project data | | |
| P-04 | Click "New" button | Empty form for new project | | |
| P-05 | Fill required fields | ProjectID, Title, PriorityChallenge, KeyDeliverable, AnnualTarget, Reference, Budget, Directorate (Lookup), Programme, FinancialYear, Status | | |
| P-06 | Click Save | New project created, gallery refreshes | | |
| P-07 | Edit an existing project | Modify fields, click Save | | |
| P-08 | Verify save | Changes persisted | | |
| P-09 | Delete a project | Confirmation dialog, project removed | | |
| P-10 | View as ProgrammeManager | See projects in own programme only | | |
| P-11 | Click ChevronRight icon | Navigates to project detail or shows more info | | |

---

## TC-REPORTACTIVITIES: Report Activities (Inline Report)

**Screen:** `scr_ReportActivities`  
**Prerequisites:** Activities and MonthlyReports data exist

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| RA-01 | Navigate to Report Activities | Activity gallery on left, inline report form on right | | |
| RA-02 | Select an activity | Existing report for current FY + month loads (Edit mode) | | |
| RA-03 | Select activity with no report | Empty form opens (New mode) | | |
| RA-04 | Fill report fields | Title, ReportingMonth, Quarter (auto), FinancialYear, PlannedAct, PercentageComplete, Status, ReasonForDeviation, RemedialAction, Output | | |
| RA-05 | Click Save | Report saved as Draft, form reloads in Edit mode | | |
| RA-06 | Click Submit | Report status changes to Submitted | | |
| RA-07 | Verify submission | Report appears in ApprovalQueue | | |
| RA-08 | Search activities | Gallery filters by search text | | |
| RA-09 | Filter by FY/Month | Activities filtered correctly | | |

---

## TC-REPORTFORM: Report Form

**Screen:** `scr_ReportForm`  
**Prerequisites:** Activity selected from MyActivities or ReportActivities

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| RF-01 | Open in New mode | Empty form with activity context shown | | |
| RF-02 | Open in Edit mode | Form populated with existing report data | | |
| RF-03 | View activity context card | Shows activity title, description, programme, directorate | | |
| RF-04 | Fill required fields | Title, ReportingMonth, Quarter, FinancialYear, PlannedAct, PercentageComplete, Status | | |
| RF-05 | Click Save | Report saved as Draft | | |
| RF-06 | Click Submit | Status changes to Submitted, SubmittedBy recorded | | |
| RF-07 | Verify SubmissionDate | Auto-populated on submit | | |
| RF-08 | Fill optional fields | ReasonForDeviation, RemedialAction, Output | | |
| RF-09 | Navigate back | Returns to MyActivities | | |

---

## TC-REPORTVIEW: Report View (Read-Only)

**Screen:** `scr_ReportView`  
**Prerequisites:** Submitted or approved report exists

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| RV-01 | Open report view | All report fields displayed in read-only format | | |
| RV-02 | View status indicator | Shows correct status (Submitted, Approved, Rejected) | | |
| RV-03 | View period info | Shows FinancialYear, ReportingMonth, Quarter | | |
| RV-04 | View percentage complete | Shows percentage value | | |
| RV-05 | View narrative fields | PlannedActivity, Output, ReasonForDeviation, RemedialAction | | |
| RV-06 | View submission info | SubmittedBy, SubmissionDate shown | | |
| RV-07 | View review info | ReviewedBy, ReviewDate shown (if reviewed) | | |
| RV-08 | View rejection reason | Shown if status is Rejected | | |
| RV-09 | Click back button | Returns to previous screen | | |

---

## TC-REPORTS: Reports Dashboard

**Screen:** `scr_Reports`  
**Prerequisites:** Multiple reports exist across statuses

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| R-01 | Navigate to Reports | Report gallery with filter bar | | |
| R-02 | View KPI cards | Total, Pending, Approved, Rejected counts | | |
| R-03 | Filter by FY | Reports filtered by financial year | | |
| R-04 | Filter by Quarter | Reports filtered by quarter | | |
| R-05 | Filter by Programme | Reports filtered by programme | | |
| R-06 | Filter by Directorate | Reports filtered by directorate | | |
| R-07 | Filter by Status | Reports filtered by status | | |
| R-08 | Search reports | Gallery filters by search text | | |
| R-09 | Click a report | Navigates to scr_ReportView | | |
| R-10 | View status pills | Color-coded status indicators (Draft, Submitted, Approved, Rejected, Escalated) | | |
| R-11 | Click back button (mobile) | Returns to previous screen | | |
| R-12 | Responsive layout | Sidebar collapses on small screens | | |
| R-13 | View as Admin | See all reports | | |
| R-14 | View as ProgrammeManager | See reports in own programme only | | |
| R-15 | View as Supervisor | See reports in own directorate only | | |

---

## TC-APPROVEDREPORTS: Approved Reports

**Screen:** `scr_ApprovedReports`

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| AR-01 | Navigate to Approved Reports | Read-only gallery of approved reports | | |
| AR-02 | View KPI cards | Approved count, by programme/directorate | | |
| AR-03 | Filter by FY | Reports filtered | | |
| AR-04 | Filter by Programme | Reports filtered | | |
| AR-05 | Click a report | Navigates to scr_ReportView | | |
| AR-06 | Click ChevronRight | Navigates to report detail | | |
| AR-07 | Click back button | Returns to previous screen | | |

---

## TC-APPROVALQUEUE: Approval Queue

**Screen:** `scr_ApprovalQueue`  
**Prerequisites:** Submitted reports exist, Supervisor/DDME user logged in

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| AQ-01 | Navigate to Approval Queue | Tab bar (Pending/Overdue/Escalated/Drafts), report list, detail pane | | |
| AQ-02 | View Pending tab | Shows reports with SubmissionStatus = "Submitted" | | |
| AQ-03 | View Overdue tab | Shows reports submitted >5 days ago | | |
| AQ-04 | View Escalated tab | Shows reports with SubmissionStatus = "Escalated" | | |
| AQ-05 | View Drafts tab | Shows reports in Draft status | | |
| AQ-06 | Click a report in list | Detail pane shows report content, planned activity, progress, review history | | |
| AQ-07 | Type a comment | Comment box accepts text | | |
| AQ-08 | Click Approve (Supervisor) | SubmissionStatus → "Approved", SupervisorReviewedBy/Date recorded | | |
| AQ-09 | Click Approve (DDME) | ReportStatus → "Approved", DDReviewedBy/Date recorded | | |
| AQ-10 | Click Reject with comment | Status → "Rejected", rejection reason recorded | | |
| AQ-11 | Click Reject without comment | Error: "Add a reason before rejecting." | | |
| AQ-12 | Click Return for Correction | Status → "Draft", comment recorded, contributor can re-edit | | |
| AQ-13 | Verify Supervisor → DD flow | Supervisor approves → report appears in DD's queue | | |
| AQ-14 | Verify DD final approval | DD approves → report fully approved | | |
| AQ-15 | View directorate filter | Filter by directorate (Supervisor scope) | | |
| AQ-16 | Search queue | Filter by search text | | |
| AQ-17 | View queue counts | Tab badges show correct counts | | |
| AQ-18 | Click refresh | Queue reloads with latest data | | |
| AQ-19 | View as Admin | See all queues across all directorates | | |
| AQ-20 | View as Supervisor | See only own directorate's queue | | |

---

## TC-USERS: User Management

**Screen:** `scr_Users`  
**Prerequisites:** Admin user logged in

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| U-01 | Navigate to Users | User registration form | | |
| U-02 | Fill required fields | Full Name, Email, Directorate, Programme, Role | | |
| U-03 | Select role from dropdown | Options: Administrator, ProgrammeManager, Supervisor, Contributor, DeputyDirectorME | | |
| U-04 | Click Save | New user created in APP_Users list | | |
| U-05 | Edit existing user | Modify role or directorate | | |
| U-06 | Verify role assignment | New user can login with correct role | | |
| U-07 | Search users | Gallery filters by search text | | |
| U-08 | View as non-Admin | Access denied or read-only view | | |

---

## TC-NAVIGATION: Navigation Rail

**Component:** `cmp_NavRail`  
**Applies to:** All screens

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| N-01 | Click Home icon | Navigates to scr_Home | | |
| N-02 | Click My Activities icon | Navigates to scr_MyActivities | | |
| N-03 | Click Activities icon | Navigates to scr_Activities | | |
| N-04 | Click Projects icon | Navigates to scr_Projects | | |
| N-05 | Click Monthly Reports icon | Navigates to scr_ReportActivities | | |
| N-06 | Click Users icon | Navigates to scr_Users | | |
| N-07 | Click Approval Queue icon | Navigates to scr_ApprovalQueue | | |
| N-08 | Verify active icon highlight | Current screen's icon is highlighted | | |
| N-09 | Verify icons work on every screen | Test navigation from each screen | | |

---

## TC-HEADER: App Header

**Component:** `cmp_AppHeader`  
**Applies to:** All screens

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| H-01 | View page title | Correct title for current screen | | |
| H-02 | View user greeting | Shows user's full name | | |
| H-03 | Click Search icon | Search input appears/focuses | | |
| H-04 | Type search text | SearchText output updates | | |
| H-05 | Click Bell icon | Shows notifications or navigates | | |
| H-06 | Click Back button (on detail screens) | Returns to previous screen | | |
| H-07 | View subtitle | Shows context-appropriate subtitle | | |

---

## TC-ACCESSIBILITY: Accessibility Checks

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| AC-01 | Tab through all interactive controls | Logical tab order, no skipped controls | | |
| AC-02 | Use screen reader (NVDA/VoiceOver) | All interactive controls announced with labels | | |
| AC-03 | Check color contrast (WCAG AA) | 4.5:1 ratio for text, 3:1 for large text/icons | | |
| AC-04 | Check focus indicators | Visible focus ring on all interactive elements | | |
| AC-05 | Check keyboard-only navigation | All actions achievable without mouse | | |
| AC-06 | Check error messages | Errors announced by screen readers (Live=Assertive) | | |

---

## TC-RESPONSIVE: Responsive Layout

| # | Step | Expected Result | Pass/Fail | Notes |
|---|------|----------------|-----------|-------|
| RS-01 | Desktop (1366×768) | Full layout with sidebar | | |
| RS-02 | Tablet (768×1024) | Adapted layout, sidebar may collapse | | |
| RS-03 | Mobile (<640px) | Sidebar collapses, back button appears, single-column layout | | |
| RS-04 | Resize animation | Smooth transitions, no content overflow | | |
| RS-05 | Touch targets | All interactive elements ≥44×44px on mobile | | |

---

## Test Execution Summary

| Screen | Total Tests | Pass | Fail | Blocked | Notes |
|--------|------------|------|------|---------|-------|
| TC-LOGIN | 10 | | | | |
| TC-SPLASH | 3 | | | | |
| TC-HOME | 24 | | | | |
| TC-MYACTIVITIES | 10 | | | | |
| TC-ACTIVITIES | 12 | | | | |
| TC-PROJECTS | 11 | | | | |
| TC-REPORTACTIVITIES | 9 | | | | |
| TC-REPORTFORM | 9 | | | | |
| TC-REPORTVIEW | 9 | | | | |
| TC-REPORTS | 15 | | | | |
| TC-APPROVEDREPORTS | 7 | | | | |
| TC-APPROVALQUEUE | 20 | | | | |
| TC-USERS | 8 | | | | |
| TC-NAVIGATION | 9 | | | | |
| TC-HEADER | 7 | | | | |
| TC-ACCESSIBILITY | 6 | | | | |
| TC-RESPONSIVE | 5 | | | | |
| **TOTAL** | **174** | | | | |

---

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Tester | | | |
| Reviewer | | | |
| Approver | | | |

---

*Generated by Buffy (AI coding agent) — 2026-08-26*
