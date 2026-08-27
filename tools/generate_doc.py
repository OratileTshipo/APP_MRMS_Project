#!/usr/bin/env python3
"""Generate APP-MRMS Solution Documentation as a Word document."""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
import datetime

doc = Document()

# ── Styles ──────────────────────────────────────────────────────────────
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# ── Title Page ──────────────────────────────────────────────────────────
for _ in range(6):
    doc.add_paragraph('')

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('APP-MRMS')
run.bold = True
run.font.size = Pt(36)
run.font.color.rgb = RGBColor(0x12, 0x29, 0x52)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run('Annual Performance Plan\nMonitoring, Reporting & Management System')
run.font.size = Pt(18)
run.font.color.rgb = RGBColor(0x2E, 0x75, 0xB6)

doc.add_paragraph('')

meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = meta.add_run(f'Solution Documentation\nVersion 2.5 — {datetime.date.today().strftime("%B %Y")}')
run.font.size = Pt(12)
run.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

doc.add_page_break()

# ── Table of Contents placeholder ──────────────────────────────────────
doc.add_heading('Table of Contents', level=1)
toc_items = [
    '1. Executive Summary',
    '2. Solution Overview',
    '3. Data Model & SharePoint Lists',
    '4. Role-Based Access Control',
    '5. Screen-by-Screen Guide',
    '6. Reporting Period & Financial Year Logic',
    '7. Approval Workflow',
    '8. Architecture & Technical Design',
    '9. Delegation & Performance Strategy',
    '10. Accessibility Compliance',
    '11. Build Pipeline & Developer Guide',
    '12. Known Issues & Roadmap',
    '13. Appendix: Screen Inventory',
]
for item in toc_items:
    p = doc.add_paragraph(item)
    p.paragraph_format.space_after = Pt(4)

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════
# 1. EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════════════════════
doc.add_heading('1. Executive Summary', level=1)

doc.add_paragraph(
    'APP-MRMS (Annual Performance Plan — Monitoring, Reporting & Management System) '
    'is a Power Apps Canvas application built for the Department of the Premier, '
    'North West Provincial Government. It digitises the department\'s Annual Performance Plan '
    'lifecycle — from project and activity registration through monthly activity reporting '
    'to a two-stage approval queue.'
)
doc.add_paragraph(
    'The system serves five user roles across 11 directorates and 4 programmes, '
    'enabling role-scoped dashboards, personal activity worklists, monthly report '
    'submissions, and supervisor/deputy-director approval workflows. All data is stored '
    'in SharePoint Online lists, and the app is designed for both desktop and tablet use '
    'with responsive layout.'
)
doc.add_paragraph(
    'Key outcomes delivered by this solution:'
)
bullets = [
    'Centralised tracking of 11 directorates, 4 programmes, and their projects/activities',
    'Role-based data scoping — users see only what they are authorised to view',
    'Monthly reporting cycle with automated status tracking (Not Started → Draft → Submitted → Approved)',
    'Two-stage approval: Supervisor first, then Deputy Director M&E',
    'Real-time dashboard with KPIs, trend charts, and programme progress indicators',
    'WCAG AA accessibility compliance across all interactive controls',
]
for b in bullets:
    doc.add_paragraph(b, style='List Bullet')

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════
# 2. SOLUTION OVERVIEW
# ══════════════════════════════════════════════════════════════════════════
doc.add_heading('2. Solution Overview', level=1)

doc.add_heading('2.1 What the App Does', level=2)
doc.add_paragraph(
    'APP-MRMS manages the full lifecycle of the department\'s Annual Performance Plan:'
)
steps = [
    'Projects are registered with directorates, programmes, budgets, targets, and responsible directors',
    'Activities are created under projects with owners, supervisors, start/end dates, and frequencies (Monthly, Quarterly, Annual)',
    'Contributors submit monthly reports against their assigned activities, describing progress and outputs',
    'Supervisors review and approve reports; Deputy Director M&E provides final sign-off',
    'The Home dashboard aggregates all data into KPIs, trend charts, and programme progress visualisations',
]
for i, s in enumerate(steps, 1):
    doc.add_paragraph(f'{i}. {s}')

doc.add_heading('2.2 Technology Stack', level=2)
table = doc.add_table(rows=7, cols=2)
table.style = 'Light Grid Accent 1'
data = [
    ('Component', 'Technology'),
    ('Frontend', 'Power Apps Canvas App (Modern + Classic controls)'),
    ('Backend', 'SharePoint Online lists (11 lists)'),
    ('Automation', 'Power Automate flows (4 flows: approval, rejection, completion, reminders)'),
    ('Authentication', 'Azure AD / Microsoft 365 (SSO via User().Email)'),
    ('Build Pipeline', 'Unpacked YAML source → repack_msapp.py → .msapp binary'),
    ('IDE', 'Power Apps Studio + VS Code (YAML source control)'),
]
for i, (k, v) in enumerate(data):
    table.rows[i].cells[0].text = k
    table.rows[i].cells[1].text = v
    if i == 0:
        for cell in table.rows[i].cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.bold = True

doc.add_heading('2.3 User Roles', level=2)
doc.add_paragraph(
    'The app supports five distinct roles, each with different data visibility and capabilities:'
)
roles_table = doc.add_table(rows=6, cols=4)
roles_table.style = 'Light Grid Accent 1'
roles_data = [
    ('Role', 'Scope', 'Can Submit Reports', 'Can Approve'),
    ('Administrator', 'All directorates & programmes', 'Yes', 'Yes'),
    ('DeputyDirectorME', 'All directorates & programmes', 'Yes', 'Yes (final)'),
    ('ProgrammeManager', 'Own programme only', 'Yes', 'Yes (Supervisor stage)'),
    ('Supervisor', 'Own directorate only', 'Yes', 'Yes (Supervisor stage)'),
    ('Contributor', 'Own activities only', 'Yes', 'No'),
]
for i, row_data in enumerate(roles_data):
    for j, cell_text in enumerate(row_data):
        roles_table.rows[i].cells[j].text = cell_text
        if i == 0:
            for paragraph in roles_table.rows[i].cells[j].paragraphs:
                for run in paragraph.runs:
                    run.bold = True

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════
# 3. DATA MODEL
# ══════════════════════════════════════════════════════════════════════════
doc.add_heading('3. Data Model & SharePoint Lists', level=1)

doc.add_paragraph(
    'The application is backed by 11 SharePoint Online lists. The core entity '
    'relationships form a hierarchy: Directorates contain Programmes, which contain '
    'Projects, which contain Activities. MonthlyReports are generated per Activity '
    'per reporting period.'
)

doc.add_heading('3.1 Entity Relationship Diagram (Text)', level=2)
er_text = """
Directorates (1) ──── (*) Programmes
     │                       │
     │                       │
     ├── (*) Projects        ├── (*) Activities
     │        │              │         │
     │        └──────────────┘         │
     │                                 │
     └── (*) APP_Users                 ├── (*) MonthlyReports
                                      │         │
                                      │    (*) Notifications
                                      │
                                      └── (*) ApprovalQueue (derived)
"""
p = doc.add_paragraph()
run = p.add_run(er_text)
run.font.name = 'Consolas'
run.font.size = Pt(9)

doc.add_heading('3.2 SharePoint Lists', level=2)

lists_data = [
    ('Directorates', '11', 'DirectorateID (text), Title (name), Programme, Director (user), DeputyDirector (user), Active (bool)'),
    ('Programmes', '4', 'Title, Active (bool)'),
    ('Projects', '~30', 'Title (ProjectID), PriorityChallenge, KeyDeliverable, AnnualTarget, Reference, Budget, Directorate (Lookup), Programme, FinancialYear, Status (Choice: Active/Closed/Cancelled)'),
    ('Activities', '~60', 'Title (ActivityID), ActivityDescription, ActivityShortDescription, DirectorateLabel (text), ProgrammeLabel (text), Project (Lookup), Frequency (Choice: Monthly/Quarterly/Annual), ActivityOwner (user), Supervisor (user), StartDate, EndDate, DueDate, Status (Choice: Active/Completed)'),
    ('MonthlyReports', '~200', 'Title, Activity (Lookup), Directoratelabel, ProgrammeLabel, ReportingMonth (Choice), FinancialYear (Choice), SupervisorApproved (bool), DeputyDirectorApproved (bool), ReportStatus (Choice: Not Started/Draft/Submitted/Approved/Rejected), IsOverdue (calc), SubmittedBy (user), plus narrative fields'),
    ('APP_Users', '~20', 'Title, UserAccount (user), Role (Choice: Administrator/ProgrammeManager/Supervisor/Contributor/DeputyDirectorME), Directorate (Lookup), DirectorateID (text), Programme (Lookup), Active (bool)'),
    ('Notifications', '~50', 'Title, RecipientUser (user), IsRead (bool), NotificationType, RelatedItemID'),
]

table = doc.add_table(rows=len(lists_data)+1, cols=3)
table.style = 'Light Grid Accent 1'
headers = ('List Name', 'Est. Records', 'Key Columns')
for j, h in enumerate(headers):
    table.rows[0].cells[j].text = h
    for paragraph in table.rows[0].cells[j].paragraphs:
        for run in paragraph.runs:
            run.bold = True

for i, (name, count, cols) in enumerate(lists_data, 1):
    table.rows[i].cells[0].text = name
    table.rows[i].cells[1].text = count
    table.rows[i].cells[2].text = cols

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════
# 4. ROLE-BASED ACCESS CONTROL
# ══════════════════════════════════════════════════════════════════════════
doc.add_heading('4. Role-Based Access Control', level=1)

doc.add_heading('4.1 How Roles Are Determined', level=2)
doc.add_paragraph(
    'At app startup (App.OnStart), the current user\'s email is matched against '
    'the APP_Users SharePoint list to determine their role, directorate, and programme:'
)
code = """Set(varCurrentUserRecord, LookUp(APP_Users, UserAccount.Email = varUserEmail));
Set(varUserRole, Trim(varCurrentUserRecord.Role.Value));
Set(varUserDirectorate, Trim(varCurrentUserRecord.Directorate.Value));
Set(varUserProgramme, Trim(varCurrentUserRecord.Programme.Value));
Set(varCanViewAllReports, varUserRole = "DeputyDirectorME" || varUserRole = "Administrator");"""
p = doc.add_paragraph()
run = p.add_run(code)
run.font.name = 'Consolas'
run.font.size = Pt(9)

doc.add_heading('4.2 Data Scoping Pattern', level=2)
doc.add_paragraph(
    'Every screen that displays data uses a consistent scoping pattern. '
    'The app loads ALL records from SharePoint first (delegable), then narrows '
    'the results in-memory based on the user\'s role. This avoids SharePoint '
    'delegation limitations on Lookup columns.'
)
code2 = """// Example from scr_Home — role-scoped report collection
ClearCollect(
    colReportsInScope,
    Switch(
        varUserRole,
        "Administrator", MonthlyReports,
        "DeputyDirectorME", MonthlyReports,
        "ProgrammeManager", Filter(MonthlyReports, ProgrammeLabel = varUserProgramme),
        "Supervisor", Filter(MonthlyReports, DirectorateLabel = varUserDirectorate),
        Filter(MonthlyReports, SubmittedBy.Email = varUserEmail)  // Contributor
    )
);"""
p = doc.add_paragraph()
run = p.add_run(code2)
run.font.name = 'Consolas'
run.font.size = Pt(9)

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════
# 5. SCREEN-BY-SCREEN GUIDE
# ══════════════════════════════════════════════════════════════════════════
doc.add_heading('5. Screen-by-Screen Guide', level=1)

screens = [
    ('5.1 scr_Splash', 'Splash Screen',
     'Displays the department logo and app name for 1.8 seconds, then auto-navigates to scr_Home. '
     'The timer triggers on screen visibility.'),
    ('5.2 scr_Home', 'Dashboard (Main Screen)',
     'The primary dashboard showing:\n'
     '• Dynamic greeting (Good morning/day/evening + user name)\n'
     '• Subtitle showing current date, quarter, FY, and number of directorates\n'
     '• KPI cards: Total Reports, Pending Approvals, Overdue, Approved\n'
     '• Filter bar: FY, Programme, Directorate, Quarter dropdowns\n'
     '• Monthly Trend chart (12-month bar chart of on-time vs late activities)\n'
     '• Programme Progress panel (per-programme activity completion rates)\n'
     '• Recent Reports gallery (latest submitted/approved reports)\n'
     '• Notifications panel (personal unread notifications)\n'
     '• The AllReportsCard subtitle is role-scoped: "Across all programmes" for admins, '
     '"Across {Programme}" for ProgrammeManagers, "Across {Directorate}" for others'),
    ('5.3 scr_MyActivities', 'Personal Activity Worklist',
     'Contributor-facing screen showing:\n'
     '• Personal activity list (filtered by ActivityOwner.Email = currentUser)\n'
     '• Report status for each activity (Not Started, Draft, Submitted, Approved, Rejected)\n'
     '• Action button: navigates to ReportForm to create or edit a report\n'
     '• Filter bar: FY, Month, Status dropdowns\n'
     '• Activity details: project name, owner, frequency, start/due dates'),
    ('5.4 scr_Activities', 'Activities Master List (Admin/PM)',
     'Full CRUD screen for managing activities:\n'
     '• Left panel: searchable gallery of all activities in scope\n'
     '• Right panel: activity detail form (create/edit/delete)\n'
     '• Fields: ActivityID, Title, Description, ShortDescription, Directorate, Programme, '
     'Project, Frequency, Owner, Supervisor, StartDate, EndDate, DueDate, Status\n'
     '• Auto-generates sequential ActivityIDs (e.g., COMM-AC-0001)\n'
     '• Role-scoped: admins see all, PMs see own programme, supervisors see own directorate'),
    ('5.5 scr_Projects', 'Projects Master List (Admin/PM)',
     'Full CRUD screen for managing projects:\n'
     '• Left panel: searchable gallery of projects in scope\n'
     '• Right panel: project detail form\n'
     '• Fields: ProjectID, Title, PriorityChallenge, KeyDeliverable, AnnualTarget, '
     'Reference, Budget, Directorate (Lookup), Programme, FinancialYear, Status\n'
     '• Auto-generates sequential ProjectIDs (e.g., COMM-PJ-002)\n'
     '• Delegation fix: loads all Projects then filters in-memory (avoids Lookup.Value delegation)'),
    ('5.6 scr_ReportActivities', 'Activities → Report Inline Editor',
     'Screen for linking activities to monthly reports:\n'
     '• Left panel: activity gallery with search/filter\n'
     '• Right panel: inline report form (create/edit for current period)\n'
     '• Loads existing report for selected activity + current FY + current month\n'
     '• Falls back to "New" mode if no report exists\n'
     '• Two variants: scr_ReportActivities and scr_ReportActivities_1'),
    ('5.7 scr_ReportForm', 'Monthly Report Create/Edit',
     'Full report editing form:\n'
     '• Activity selector (dropdown)\n'
     '• Financial Year and Reporting Month selectors\n'
     '• Quarter auto-derived from month\n'
     '• Narrative fields: Planned activities, Progress %, Status, Reason for variance, '
     'Remedial actions, Outputs/achievements\n'
     '• Save: stores as Draft; Submit: changes status to Submitted for approval'),
    ('5.8 scr_ReportView', 'Report Detail (Read-Only)',
     'Displays a submitted/approved report in read-only format:\n'
     '• Shows all report fields\n'
     '• Approval status indicators (Supervisor Approved, Deputy Director Approved)\n'
     '• Back button returns to previous screen'),
    ('5.9 scr_Reports', 'Reports Dashboard',
     'Comprehensive reports list with advanced filtering:\n'
     '• Filter bar: FY, Quarter, Programme, Directorate, Status, Search\n'
     '• Gallery of all reports in scope with status pills\n'
     '• Click-through to ReportView'),
    ('5.10 scr_ApprovedReports', 'Approved Reports Archive',
     'Read-only view of fully approved reports:\n'
     '• Filtered to reports where both SupervisorApproved and DeputyDirectorApproved are true\n'
     '• Status pill shows "Approved"\n'
     '• Click-through to ReportView'),
    ('5.11 scr_ApprovalQueue', 'Two-Stage Approval Queue',
     'Reviewer-facing screen for processing submitted reports:\n'
     '• Tab bar: Pending / Approved / Rejected\n'
     '• Left panel: list of reports awaiting action\n'
     '• Right panel: report detail with Approve/Reject buttons\n'
     '• Two-stage workflow: Supervisor approves first, then Deputy Director M&E\n'
     '• Comment field for rejection reasons\n'
     '• Role-scoped: admins see all, PMs see programme, supervisors see directorate'),
    ('5.12 scr_Users', 'User Registration Form',
     'Admin-only screen for registering new users:\n'
     '• Fields: Full Name, Email, Phone, Directorate, Programme, Role\n'
     '• Writes to APP_Users SharePoint list\n'
     '• Role determines data access in all other screens'),
]

for title, heading, desc in screens:
    doc.add_heading(title, level=2)
    doc.add_paragraph(desc)

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════
# 6. REPORTING PERIOD
# ══════════════════════════════════════════════════════════════════════════
doc.add_heading('6. Reporting Period & Financial Year Logic', level=1)

doc.add_paragraph(
    'The app uses the South African government financial year (April–March). '
    'All period calculations are derived from Today() at app startup:'
)

doc.add_heading('6.1 Financial Year', level=2)
doc.add_paragraph(
    'If current month ≥ April: FY = "YYYY/(YY+1)" e.g., April 2026 → "2026/27"\n'
    'If current month < April: FY = "(YYYY-1)/YY" e.g., January 2026 → "2025/26"'
)

doc.add_heading('6.2 Current Quarter', level=2)
q_table = doc.add_table(rows=5, cols=2)
q_table.style = 'Light Grid Accent 1'
q_data = [
    ('Quarter', 'Months'),
    ('Q1', 'April – June'),
    ('Q2', 'July – September'),
    ('Q3', 'October – December'),
    ('Q4', 'January – March'),
]
for i, (q, m) in enumerate(q_data):
    q_table.rows[i].cells[0].text = q
    q_table.rows[i].cells[1].text = m
    if i == 0:
        for cell in q_table.rows[i].cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.bold = True

doc.add_heading('6.3 Overdue Detection', level=2)
doc.add_paragraph(
    'A report is marked as IsOverdue when:\n'
    '• The activity\'s EndDate has passed, AND\n'
    '• The report status is still "Not Started" or "Draft"\n'
    'This drives the Overdue KPI card on the Home dashboard.'
)

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════
# 7. APPROVAL WORKFLOW
# ══════════════════════════════════════════════════════════════════════════
doc.add_heading('7. Approval Workflow', level=1)

doc.add_paragraph(
    'The approval process follows a mandatory two-stage workflow:'
)

flow_table = doc.add_table(rows=6, cols=3)
flow_table.style = 'Light Grid Accent 1'
flow_data = [
    ('Stage', 'Action', 'Result'),
    ('1. Draft', 'Contributor creates/edits report', 'ReportStatus = "Draft"'),
    ('2. Submit', 'Contributor clicks Submit', 'ReportStatus = "Submitted"'),
    ('3. Supervisor', 'Supervisor reviews and approves', 'SupervisorApproved = true'),
    ('4. Deputy Director', 'Deputy Director M&E reviews and approves', 'DeputyDirectorApproved = true, ReportStatus = "Approved"'),
    ('5. Rejection', 'Any reviewer rejects', 'ReportStatus = "Rejected", comment recorded'),
]
for i, row_data in enumerate(flow_data):
    for j, cell_text in enumerate(row_data):
        flow_table.rows[i].cells[j].text = cell_text
        if i == 0:
            for paragraph in flow_table.rows[i].cells[j].paragraphs:
                for run in paragraph.runs:
                    run.bold = True

doc.add_paragraph(
    '\nKey rules:\n'
    '• Deputy Director M&E approval is mandatory — cannot be skipped\n'
    '• Rejection returns the report to the contributor with a comment\n'
    '• Rejected reports can be re-edited and re-submitted\n'
    '• Power Automate flows handle approval notifications'
)

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════
# 8. ARCHITECTURE
# ══════════════════════════════════════════════════════════════════════════
doc.add_heading('8. Architecture & Technical Design', level=1)

doc.add_heading('8.1 App Startup Flow (App.OnStart)', level=2)
doc.add_paragraph(
    'The app initialises in a deterministic order at startup:'
)
init_steps = [
    'Theme colours — Navy (#122952), Blue (#2E75B6), Green (#1E8A44), Amber (#E6A100), Red (#C0392B)',
    'Responsive breakpoints — varIsMobile (<640px), varIsTablet (640–1100px)',
    'Current user lookup — email → APP_Users → role, directorate, programme, varCanViewAllReports',
    'Reporting period — FY, current month, current quarter derived from Today()',
    'Filter defaults — reset to "All" for all filter dropdowns',
    'Reference data collections — Concurrent() loads Programmes, Projects, Activities, Directorates',
    'Notifications — personal unread notifications collected',
    'UI state flags — navOpen, sidePanelOpen, formIsValid reset to defaults',
]
for i, s in enumerate(init_steps, 1):
    doc.add_paragraph(f'{i}. {s}')

doc.add_heading('8.2 Component Architecture', level=2)
doc.add_paragraph(
    'The app uses two reusable components to ensure consistency across screens:'
)
comp_table = doc.add_table(rows=3, cols=3)
comp_table.style = 'Light Grid Accent 1'
comp_data = [
    ('Component', 'Purpose', 'Used In'),
    ('cmp_AppHeader', 'Top header bar with logo, greeting, search, notifications bell, back button', 'All screens'),
    ('cmp_NavRail', 'Side navigation rail with menu items (Home, My Activities, Activities, Projects, Reports, Users)', 'All screens'),
]
for i, row_data in enumerate(comp_data):
    for j, cell_text in enumerate(row_data):
        comp_table.rows[i].cells[j].text = cell_text
        if i == 0:
            for paragraph in comp_table.rows[i].cells[j].paragraphs:
                for run in paragraph.runs:
                    run.bold = True

doc.add_heading('8.3 Naming Conventions', level=2)
naming_table = doc.add_table(rows=6, cols=3)
naming_table.style = 'Light Grid Accent 1'
naming_data = [
    ('Prefix', 'Type', 'Example'),
    ('var', 'Global variable', 'varUserRole, varCanViewAllReports'),
    ('col', 'Collection', 'colReportsInScope, colActivities'),
    ('scr', 'Screen', 'scr_Home, scr_Activities'),
    ('cmp', 'Component', 'cmp_AppHeader, cmp_NavRail'),
    ('_lbl / _ico / _btn / _txt / _drp', 'Control suffix', 'RepActTitle_lbl, HomeSearch_ico'),
]
for i, row_data in enumerate(naming_data):
    for j, cell_text in enumerate(row_data):
        naming_table.rows[i].cells[j].text = cell_text
        if i == 0:
            for paragraph in naming_table.rows[i].cells[j].paragraphs:
                for run in paragraph.runs:
                    run.bold = True

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════
# 9. DELEGATION & PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════
doc.add_heading('9. Delegation & Performance Strategy', level=1)

doc.add_heading('9.1 SharePoint Delegation Limits', level=2)
doc.add_paragraph(
    'SharePoint Online imposes a 2,000-row delegation limit. When a Power Fx formula '
    'cannot be delegated, only the first 2,000 rows are returned, potentially causing '
    'incorrect results. The app mitigates this through:'
)
mitigations = [
    'Single-column filters — Only filter on one SharePoint column at a time (OR across columns is not delegable)',
    'StartsWith() for text search — Delegable, unlike Contains()',
    'In-memory collections — Load all data first, then filter in-memory for role scoping',
    'Avoiding CountRows on SharePoint — Use in-memory collections for counting',
]
for m in mitigations:
    doc.add_paragraph(m, style='List Bullet')

doc.add_heading('9.2 Known Delegation Patterns', level=2)
doc.add_paragraph(
    'Projects screen: Directorate is a Lookup column. SharePoint does NOT delegate '
    'filtering on Lookup.Value. Fix: load all Projects, filter in-memory.\n\n'
    'CountRows in save actions: Used for auto-generating sequential IDs. '
    'Fix: use in-memory collections (colActivitiesInScope, colProjectsInScope, colMonthlyReportsScoped).\n\n'
    'ReportActivities: Same Lookup delegation risk as Projects. '
    'Fix: load all active activities, filter in-memory.'
)

doc.add_heading('9.3 Performance Optimisations', level=2)
doc.add_paragraph(
    'Home screen galleries use pre-filtering with With() before ForAll loops:'
)
perf_items = [
    'MonthlyTrend: Pre-filters colActivities and colReportsInScope once, then slices by month in ForAll(Sequence(12)) — reduces from 24 collection scans to 14',
    'ProgrammeProgress: Pre-filters base collections once, then slices by programme — reduces from 3N scans to N+3',
    'Home subtitle: Uses CountRows(colDirectorates) instead of raw SharePoint query',
]
for p_item in perf_items:
    doc.add_paragraph(p_item, style='List Bullet')

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════
# 10. ACCESSIBILITY
# ══════════════════════════════════════════════════════════════════════════
doc.add_heading('10. Accessibility Compliance', level=1)

doc.add_paragraph(
    'The app has been audited and remediated for WCAG 2.1 AA compliance:'
)

acc_table = doc.add_table(rows=6, cols=2)
acc_table.style = 'Light Grid Accent 1'
acc_data = [
    ('Category', 'Status'),
    ('AccessibleLabel on interactive icons', '✅ 19 icons across 10 files'),
    ('AccessibleLabel on gallery row items', '✅ All data labels in 6 screens'),
    ('Icon color contrast (WCAG AA 4.5:1)', '✅ Search & ChevronRight icons updated to 7:1 ratio'),
    ('Empty OnSelect handlers', '✅ 3 removed/replaced with Select(Parent)'),
    ('Invalid properties (PA2108)', '✅ Tooltip removed from ModernText controls'),
]
for i, (cat, status) in enumerate(acc_data):
    acc_table.rows[i].cells[0].text = cat
    acc_table.rows[i].cells[1].text = status
    if i == 0:
        for cell in acc_table.rows[i].cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.bold = True

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════
# 11. BUILD PIPELINE
# ══════════════════════════════════════════════════════════════════════════
doc.add_heading('11. Build Pipeline & Developer Guide', level=1)

doc.add_heading('11.1 Source of Truth', level=2)
doc.add_paragraph(
    'The YAML source files in src/Src/ are the canonical source of truth. '
    'The .msapp binary is generated from these files for import into Power Apps Studio.'
)

doc.add_heading('11.2 Build Steps', level=2)
build_steps = [
    'Edit .pa.yaml files in src/Src/',
    'Run verification: python3 tools/verify_powerfx.py (checks formula balance, delegation, nav)',
    'Run screen registry check: python3 tools/check_screen_registry.py',
    'Run control property check: python3 tools/check_control_props.py',
    'Pack: python3 tools/repack_msapp.py --msapp BASE.msapp --out OUTPUT.msapp',
    'Import OUTPUT.msapp into Power Apps Studio',
    'Validate in Studio → Save → Export back to repo',
]
for i, s in enumerate(build_steps, 1):
    doc.add_paragraph(f'{i}. {s}')

doc.add_heading('11.3 Available Tools', level=2)
tools_table = doc.add_table(rows=7, cols=2)
tools_table.style = 'Light Grid Accent 1'
tools_data = [
    ('Tool', 'Purpose'),
    ('verify_powerfx.py', 'Static formula verification (balance, navigation, patch keys, delegation)'),
    ('check_screen_registry.py', 'Screen file ↔ _EditorState drift detection'),
    ('check_control_props.py', 'Control property schema validation (PA2108 errors)'),
    ('repack_msapp.py', 'Pack unpacked YAML into .msapp binary (replaces pac CLI)'),
    ('build_flow_zips.py', 'Build Power Automate flow import package with real GUIDs'),
    ('normalize_activities.py', 'Normalise Activities.csv labels'),
]
for i, (tool, purpose) in enumerate(tools_data):
    tools_table.rows[i].cells[0].text = tool
    tools_table.rows[i].cells[1].text = purpose
    if i == 0:
        for cell in tools_table.rows[i].cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.bold = True

doc.add_heading('11.4 Git Workflow', level=2)
doc.add_paragraph(
    'Branch: mimo-2.5 (active development branch)\n'
    'Commit convention: type(scope): description\n'
    '• fix: bug fixes\n'
    '• feat: new features\n'
    '• chore: maintenance tasks\n'
    '• data: CSV/data changes\n'
    '• docs: documentation'
)

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════
# 12. KNOWN ISSUES
# ══════════════════════════════════════════════════════════════════════════
doc.add_heading('12. Known Issues & Roadmap', level=1)

doc.add_heading('12.1 Resolved', level=2)
resolved = [
    'C1: SupervisorApproved status missing — Added to MonthlyReports choices',
    'C2: SharePoint site not provisioned — Provisioned with 11 lists',
    'C3: APP_Users needs real account seeding — 5 roles seeded',
    'M4: Delegation at runtime — Role-first scope filters + in-memory collections',
    'M6: Home subtitle raw SharePoint query — Replaced with in-memory collection',
    'M7: Icon color contrast — Updated to WCAG AA compliant values',
    'L8-L14: Accessibility fixes — Labels, contrast, redundant queries removed',
]
for r in resolved:
    doc.add_paragraph(r, style='List Bullet')

doc.add_heading('12.2 Open', level=2)
open_items = [
    'C4: Flow package has placeholder GUIDs — Rebuild with build_flow_zips.py',
    'M1-M3: QA testing needed after import to production site',
    'M5: Heavy ForAll/Sequence formulas could be pre-computed in OnVisible collections',
    'L6: Activities missing Supervisor assignments (rows 7-12)',
]
for o in open_items:
    doc.add_paragraph(o, style='List Bullet')

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════
# 13. APPENDIX
# ══════════════════════════════════════════════════════════════════════════
doc.add_heading('13. Appendix: Screen Inventory', level=1)

screen_table = doc.add_table(rows=18, cols=4)
screen_table.style = 'Light Grid Accent 1'
screen_inv = [
    ('Screen', 'File', 'Lines', 'Purpose'),
    ('App', 'App.pa.yaml', '~95', 'OnStart, theme, role, filters'),
    ('scr_Splash', 'scr_Splash.pa.yaml', '~120', 'Splash with timer'),
    ('scr_Home', 'scr_Home.pa.yaml', '~2,784', 'Dashboard with KPIs, filters, galleries'),
    ('scr_Users', 'scr_Users.pa.yaml', '~1,411', 'User registration form'),
    ('scr_MyActivities', 'scr_MyActivities.pa.yaml', '~738', 'Personal activity worklist'),
    ('scr_ReportForm', 'scr_ReportForm.pa.yaml', '~800', 'Monthly report create/edit'),
    ('scr_ReportView', 'scr_ReportView.pa.yaml', '~793', 'Read-only report detail'),
    ('scr_Projects', 'scr_Projects.pa.yaml', '~1,658', 'Projects master-detail CRUD'),
    ('scr_Activities', 'scr_Activities.pa.yaml', '~1,598', 'Activities master-detail CRUD'),
    ('scr_ReportActivities', 'scr_ReportActivities.pa.yaml', '~1,252', 'Activities → Report inline'),
    ('scr_ReportActivities_1', 'scr_ReportActivities_1.pa.yaml', '~938', 'Activities → Report variant'),
    ('scr_Reports', 'scr_Reports.pa.yaml', '~4,382', 'Reports dashboard'),
    ('scr_ApprovedReports', 'scr_ApprovedReports.pa.yaml', '~1,085', 'Approved reports archive'),
    ('scr_ApprovalQueue', 'scr_ApprovalQueue.pa.yaml', '~1,112', '2-stage review queue'),
    ('Screen2', 'Screen2.pa.yaml', '~1,545', 'Template/placeholder'),
    ('cmp_AppHeader', 'Component/cmp_AppHeader.pa.yaml', '~279', 'Reusable header'),
    ('cmp_NavRail', 'Component/cmp_NavRail.pa.yaml', '~200', 'Reusable nav rail'),
]
for i, row_data in enumerate(screen_inv):
    for j, cell_text in enumerate(row_data):
        screen_table.rows[i].cells[j].text = cell_text
        if i == 0:
            for paragraph in screen_table.rows[i].cells[j].paragraphs:
                for run in paragraph.runs:
                    run.bold = True

# ── Footer ──────────────────────────────────────────────────────────────
doc.add_paragraph('')
doc.add_paragraph('')
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('— End of Document —')
run.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
run.font.size = Pt(10)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run(f'Generated by Buffy (AI coding agent) — {datetime.date.today().strftime("%B %d, %Y")}')
run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
run.font.size = Pt(9)

# ── Save ────────────────────────────────────────────────────────────────
output_path = 'APP-MRMS_Solution_Documentation.docx'
doc.save(output_path)
print(f'Document saved: {output_path}')
