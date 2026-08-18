# APP-MRMS — Architecture Reference

**System:** Annual Performance Plan Monthly Reporting Management System  
**Platform:** Power Apps Canvas + SharePoint Online + Power Automate  
**Organisation:** Department of Public Works and Roads (DPWR), North West Province

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        POWER APPS CANVAS                         │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Splash  │→ │   Home   │→ │ Projects │→ │Activities│        │
│  │  (1.8s)  │  │Dashboard │  │  CRUD    │  │  CRUD    │        │
│  └──────────┘  └────┬─────┘  └──────────┘  └──────────┘        │
│                     │                                            │
│       ┌─────────────┼─────────────┐                             │
│       ▼             ▼             ▼                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │   My     │  │ Report   │  │ Report   │                      │
│  │Activities│  │Activities│  │  View    │                      │
│  └──────────┘  └──────────┘  └──────────┘                      │
│                     │                                            │
│       ┌─────────────┼─────────────┐                             │
│       ▼             ▼             ▼                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │  Report  │  │ Reports  │  │ Approved │                      │
│  │   Form   │  │Dashboard │  │ Reports  │                      │
│  └──────────┘  └──────────┘  └──────────┘                      │
│                     │                                            │
│                     ▼                                            │
│              ┌──────────┐                                       │
│              │ Approval │                                       │
│              │  Queue   │                                       │
│              └──────────┘                                       │
│                                                                  │
│  Shell: Sidebar Rail (icons) + Navy Header (title + user)        │
│  Auth: M365 identity → APP_Users role lookup                     │
│  Data: 11 SharePoint lists + Office365Users                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ Patch() / Read
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                     SHAREPOINT ONLINE                             │
│                                                                   │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │MonthlyReports│◄──►│ Activities  │◄──►│  Projects   │          │
│  │  (30 cols)  │    │  (19 cols)  │    │  (18 cols)  │          │
│  └─────────────┘    └─────────────┘    └─────────────┘          │
│         ▲                   ▲                   ▲                │
│         │                   │                   │                │
│  ┌──────┴──────┐    ┌──────┴──────┐    ┌──────┴──────┐          │
│  │  APP_Users  │    │Directorates │    │ Programmes  │          │
│  │  (5 roles)  │    │  (17 rows)  │    │  (5 rows)   │          │
│  └─────────────┘    └─────────────┘    └─────────────┘          │
│                                                                   │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │Notifications│    │  AuditLog   │    │ReportComments│          │
│  └─────────────┘    └─────────────┘    └─────────────┘          │
│                                                                   │
│  ┌─────────────┐    ┌─────────────┐                              │
│  │EvidenceLib  │    │KPIDefinitions│                             │
│  └─────────────┘    └─────────────┘                              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ Trigger on Status change
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                      POWER AUTOMATE                               │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │ Flow 1: Submitted → Notify Supervisor                    │     │
│  │   Trigger: MonthlyReports.Status = "Submitted"           │     │
│  │   Actions: Email supervisor + Create notification        │     │
│  │            + Write audit log                              │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │ Flow 2: SupervisorApproved → Route to Deputy             │     │
│  │   Trigger: MonthlyReports.Status = "SupervisorApproved"  │     │
│  │   Actions: Email Deputy + Contributor                     │     │
│  │            + Create notification + Write audit log        │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │ Flow 3: Approved → Finalize                              │     │
│  │   Trigger: MonthlyReports.Status = "Approved"            │     │
│  │   Actions: Email Contributor + Supervisor                 │     │
│  │            + Mark Activity Completed                      │     │
│  │            + Create notification + Write audit log        │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                   │
│  (Flow 4: Rejected — excluded, needs fix)                        │
└──────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### Report Lifecycle
```
Contributor creates report (Draft)
    ↓
Contributor submits report (Status → Submitted)
    ↓
Flow 1 fires: Notify Supervisor
    ↓
Supervisor reviews:
    ├── Approves (Status → SupervisorApproved)
    │       ↓
    │   Flow 2 fires: Route to Deputy
    │       ↓
    │   Deputy reviews:
    │       ├── Approves (Status → Approved)
    │       │       ↓
    │       │   Flow 3 fires: Finalize + Email + Activity Complete
    │       │
    │       └── Rejects (Status → Rejected)
    │               ↓
    │           Contributor notified, can resubmit
    │
    ├── Rejects (Status → Rejected)
    │       ↓
    │   Contributor notified, can resubmit
    │
    └── Returns for correction (Status → Draft)
            ↓
        Contributor edits and resubmits
```

### Role-Based Access
```
Administrator:      See all reports, all activities, all projects
DeputyDirectorME:   See all reports, all activities, all projects
ProgrammeManager:   See reports in their programme
Supervisor:         See reports in their directorate
Contributor:        See only their own activities and reports
```

---

## Key Formulas

### App.OnStart — User Role Resolution
```powerfx
Set(varUserEmail, User().Email);
Set(varCurrentUserRecord, LookUp(APP_Users, UserAccount.Email = varUserEmail));
Set(varUserRole, varCurrentUserRecord.Role.Value);
Set(varCanViewAllReports, varUserRole = "DeputyDirectorME" || varUserRole = "Administrator");
```

### Home — Role-First Delegable Scope
```powerfx
ClearCollect(colReportsInScope,
    Switch(varUserRole,
        "Administrator", MonthlyReports,
        "DeputyDirectorME", MonthlyReports,
        "ProgrammeManager", Filter(MonthlyReports, ProgrammeLabel = varUserProgramme),
        "Supervisor", Filter(MonthlyReports, DirectorateLabel = varUserDirectorateID),
        Filter(MonthlyReports, SubmittedBy.Email = varUserEmail)
    )
);
```

### Approval Queue — Status Filter
```powerfx
Filter(colApprovalQueue,
    Switch(varQueueTab,
        "Pending", Status.Value = "Submitted",
        "Overdue", Status.Value = "Submitted" && DateDiff(SubmissionDate, Today(), TimeUnit.Days) > 5,
        "Escalated", Status.Value = "Escalated",
        true
    )
)
```

---

## Build Pipeline

```
Edit src/Src/*.pa.yaml
    ↓
Run verification tools:
  - check_screen_registry.py
  - check_control_props.py
  - verify_powerfx.py --strict
    ↓
Pack: pac canvas pack --sources src --msapp APP-MRMS_Project_app_vN.msapp --layout SourceCode
    ↓
Import to Power Apps Studio (make.powerapps.com)
    ↓
Validate in Studio (open once for edit)
    ↓
Save in Studio
```

---

## Directory Structure

```
APP_MRMS/                    ← Git submodule (source of truth)
├── src/Src/                 ← 12 screen .pa.yaml files
├── *.csv                    ← 6 SharePoint list schemas
├── *.docx                   ← BRD/FDS/TDS, Architecture Pack
├── tools/                   ← Verification and build tools
├── backup/                  ← Pristine snapshots
└── reference/               ← msapp internals, docs

flows/                       ← Power Automate package
├── APP-MRMS-Approval.zip    ← Import package (3 flows)
└── templates/               ← Token-substitutable templates

*.msapp                      ← 7 versioned packages (v1-v6)
*.html                       ← 7 screen mockups
tools/                       ← Full toolset (10 scripts)
.github/workflows/ci.yml     ← GitHub Actions CI
```
