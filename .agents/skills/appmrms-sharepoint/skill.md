# APP-MRMS SharePoint Provisioning Skill

## Purpose
Guide the creation of SharePoint lists with exact column definitions from the CSV source-of-truth files.

## When to Use
- Setting up a new environment
- Provisioning the SharePoint site for APP-MRMS
- Verifying list columns match the CSV schemas

## List Definitions

### Directorates
| Column | Type | Required | Notes |
|---|---|---|---|
| Title | Text | Yes | Display name: "DirectorateName" |
| DirectorateID | Text | No | Short code: "ICT", "HRM" |
| Programme | Text | No | e.g. "Programme 1" |
| Director | Person | No | |
| DeputyDirector | Person | No | |
| Deligate | Person | No | Note: typo is intentional (matches CSV) |
| Active | Boolean | No | Default: Yes |

### APP_Users
| Column | Type | Required | Notes |
|---|---|---|---|
| Title | Text | Yes | Display name |
| UserAccount | Person | No | M365 account |
| Role | Choice | No | Administrator/ProgrammeManager/Supervisor/Contributor/DeputyDirectorME |
| Directorate | Text | No | Full name |
| Directorate: DirectorateID | Lookup | No | → Directorates list |
| Programme | Text | No | |
| Active | Boolean | No | Default: Yes |

### MonthlyReports
| Column | Type | Required | Notes |
|---|---|---|---|
| Title | Text | Yes | Report identifier |
| Programme | Text | No | |
| Directorate | Text | No | |
| ProgrammeLabel | Text | No | Denormalised |
| DirectorateLabel | Text | No | Short code |
| Project | Lookup | No | → Projects list |
| ProjectOwnerLabel | Text | No | |
| Activity | Lookup | No | → Activities list |
| ActivityOwnerLabel | Text | No | |
| ReportingMonth | Choice | No | April/May/June/July/August/September/October/November/December/January/February/March |
| Quarter | Choice | No | Q1/Q2/Q3/Q4/All |
| FinancialYear | Choice | No | 2026/27/2025/26/2024/25/All |
| PlannedAct | Multi-line text | No | |
| PercentageComplete | Number | No | 0-100 |
| Status | Choice | No | Draft/Submitted/SupervisorApproved/Approved/Rejected/Escalated |
| Version | Number | No | |
| SubmittedBy | Person | No | |
| SubmissionDate | Date | No | |
| ReviewedBy | Person | No | |
| ReviewDate | Date | No | |
| RejectionReason | Multi-line text | No | |
| IsOverdue | Boolean | No | |
| isFlagged | Boolean | No | |
| ReasonForDeviation | Multi-line text | No | |
| RemedialAction | Multi-line text | No | |
| Output | Multi-line text | No | |

### Activities
| Column | Type | Required | Notes |
|---|---|---|---|
| Title | Text | Yes | e.g. "ICTM-AC-0001" |
| ActivityCode | Text | No | |
| ActivityDescription | Multi-line text | No | |
| ActivityShortDescription | Text | No | |
| Directorate | Lookup | No | → Directorates |
| DirectorateLabel | Text | No | Full name |
| ProgrammeLabel | Text | No | |
| Project | Lookup | No | → Projects |
| Frequency | Choice | No | Monthly/Quarterly/Annual |
| Owner | Person | No | |
| ActivityOwner | Person | No | |
| Supervisor | Person | No | Required for approval routing |
| StartDate | Date | No | |
| EndDate | Date | No | |
| DueDate | Date | No | |
| Active | Boolean | No | Default: Yes |
| Status | Choice | No | Active/Completed/Not Started |

### Projects
| Column | Type | Required | Notes |
|---|---|---|---|
| Title | Text | Yes | Display name: "ProjectID" |
| ProjectCode | Text | No | |
| PriorityChallenge | Text | No | |
| ProjectGoalDescription | Multi-line text | No | |
| KeyDeliverable | Multi-line text | No | |
| AnnualTarget | Multi-line text | No | |
| Reference | Text | No | |
| Budget | Text | No | NOT Currency |
| Directorate | Lookup | No | → Directorates |
| Programme | Text | No | NOT a Lookup |
| Responsibility | Person | No | |
| StartDate | Date | No | |
| CompletionDate | Date | No | |
| FinancialYear | Choice | No | 2026/27/2025/26/2024/25/2023/24/2022/23 |
| Status | Choice | No | Active/Closed/Cancelled |

### Programmes
| Column | Type | Required | Notes |
|---|---|---|---|
| Title | Text | Yes | e.g. "Programme 1" |
| ProgrammeCode | Text | No | |
| ProgrammeManager | Person | No | |
| Description | Multi-line text | No | |
| Active | Boolean | No | Default: Yes |

## Additional Lists
- Notifications
- AuditLog
- ReportComments
- EvidenceLibrary (document library)
- KPIDefinitions

## Verification
After provisioning, verify:
1. All list names match exactly (case-sensitive)
2. All column internal names match CSV headers
3. All choice values match CSV data exactly
4. All lookup columns resolve to correct target lists
5. Import seed data from CSVs

## Common Issues
- **Column not found:** Check for trailing spaces in column names (e.g. "Active " has a trailing space)
- **Choice mismatch:** Verify choice values are exact (case-sensitive)
- **Lookup broken:** Ensure target list exists and column is configured as Lookup type
