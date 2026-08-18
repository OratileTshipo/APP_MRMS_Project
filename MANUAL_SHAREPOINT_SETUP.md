# APP-MRMS — Manual SharePoint Setup Guide

**For users without PnP PowerShell / Admin access**

This guide walks you through creating the SharePoint lists manually using the standard SharePoint web UI. You need **Contribute** permissions on the target site (or ask your site owner to create the lists for you).

---

## Prerequisites

1. A SharePoint Online site (e.g. `https://<tenant>.sharepoint.com/sites/APP-MRMS`)
2. At minimum **Contribute** permissions (or ask your site owner)
3. The CSV files in this repo (for reference on column names and values)

---

## Step 1: Create the Site (if needed)

1. Go to https://<tenant>.sharepoint.com
2. Click **+ Create** → **Team site**
3. Name: `APP-MRMS`
4. Group email: `app-mrms`
5. Privacy: **Private**
6. Click **Finish**

---

## Step 2: Create Lists (one by one)

For each list below:
1. Click **+ New** → **List** → **Blank list**
2. Enter the **List Name** exactly as shown
3. Click **Create**
4. Then add columns as described

---

### List 1: Directorates

| Column | Type | Required | Choices / Notes |
|---|---|---|---|
| Title | Text | Yes | Auto-created (rename to "Directorate") |
| DirectorateID | Text | No | e.g. ICT, IC, HR |
| Programme | Lookup | No | Points to Programmes list, Title column |
| ProgrammeCode | Text | No | e.g. PRG-001 |
| Active | Yes/No | No | Default: Yes |
| DirectorEmail | Single line of text | No | |

**Seed data:** See `APP_MRMS/Directorates.csv` — 18 rows

---

### List 2: Programmes

| Column | Type | Required | Choices / Notes |
|---|---|---|---|
| Title | Text | Yes | Auto-created (rename to "Programme") |
| ProgrammeCode | Text | No | e.g. PRG-001 |
| ProgrammeManager | Single line of text | No | |
| Active | Yes/No | No | Default: Yes |

**Seed data:** See `APP_MRMS/Programmes.csv` — 5 rows

---

### List 3: Projects

| Column | Type | Required | Choices / Notes |
|---|---|---|---|
| Title | Text | Yes | Auto-created |
| ProjectCode | Text | No | e.g. PRJ-001 |
| Directorate | Lookup | No | Points to Directorates, Title |
| Programme | Lookup | No | Points to Programmes, Title |
| DirectorateLabel | Single line of text | No | Denormalised directorate name |
| ProgrammeLabel | Single line of text | No | Denormalised programme name |
| ProjectManager | Single line of text | No | |
| StartDate | Date | No | |
| EndDate | Date | No | |
| Budget | Currency | No | |
| Status | Choice | No | **Active**, Completed, On Hold, Cancelled |
| Active | Yes/No | No | Default: Yes |
| Description | Multiple lines of text | No | |

**Seed data:** See `APP_MRMS/Projects.csv` — 54 rows

---

### List 4: Activities

| Column | Type | Required | Choices / Notes |
|---|---|---|---|
| Title | Text | Yes | Auto-created |
| ActivityShortDescription | Single line of text | No | |
| Project | Lookup | No | Points to Projects, Title |
| Directorate | Lookup | No | Points to Directorates, Title |
| Programme | Lookup | No | Points to Programmes, Title |
| DirectorateLabel | Single line of text | No | Denormalised |
| ProgrammeLabel | Single line of text | No | Denormalised |
| ActivityOwner | Person | No | People picker |
| Supervisor | Person | No | People picker |
| StartDate | Date | No | |
| EndDate | Date | No | |
| Status | Choice | No | **Active**, Completed, On Hold, Cancelled |
| Active | Yes/No | No | Default: Yes |
| Description | Multiple lines of text | No | |

**Seed data:** See `APP_MRMS/Activities.csv` — 516 rows

---

### List 5: MonthlyReports ⚠️ CRITICAL

| Column | Type | Required | Choices / Notes |
|---|---|---|---|
| Title | Text | Yes | Auto-created |
| Activity | Lookup | No | Points to Activities, Title |
| SubmittedBy | Person | No | People picker |
| ReviewedBy | Person | No | People picker |
| Status | Choice | Yes | **Draft**, **Submitted**, **SupervisorApproved**, **Approved**, **Rejected**, Escalated |
| ReportingMonth | Choice | Yes | **April**, **May**, **June**, **July**, **August**, **September**, **October**, **November**, **December**, **January**, **February**, **March** |
| FinancialYear | Choice | Yes | **2025/26**, **2026/27**, **2027/28** |
| Quarter | Choice | Yes | **Q1**, **Q2**, **Q3**, **Q4** |
| PercentageComplete | Number | No | 0-100 |
| RejectionReason | Multiple lines of text | No | |
| SubmissionDate | Date and Time | No | |
| ReviewDate | Date and Time | No | |
| Version | Number | No | Default: 1 |
| ProgrammeLabel | Single line of text | No | Denormalised |
| DirectorateLabel | Single line of text | No | Denormalised |
| IsOverdue | Yes/No | No | |

⚠️ **IMPORTANT:** The `Status` choice **MUST include `SupervisorApproved`** — this is required by Flow 2.

**Seed data:** See `APP_MRMS/MonthlyReports.csv` — 4 rows

---

### List 6: APP_Users

| Column | Type | Required | Choices / Notes |
|---|---|---|---|
| Title | Text | Yes | Display name |
| UserAccount | Person | No | People picker |
| Role | Choice | Yes | **Administrator**, **ProgrammeManager**, **Supervisor**, **Contributor**, **DeputyDirectorME** |
| Directorate | Lookup | No | Points to Directorates, Title |
| Programme | Lookup | No | Points to Programmes, Title |
| Active | Yes/No | No | Default: Yes |

**Seed data:** See `APP_MRMS/APP_Users.csv` — 5 rows

---

### List 7: Notifications

| Column | Type | Required | Choices / Notes |
|---|---|---|---|
| Title | Text | Yes | Auto-created |
| RecipientUser | Person | No | People picker |
| RelatedEntity | Single line of text | No | e.g. MonthlyReports:123 |
| Message | Multiple lines of text | No | |
| IsRead | Yes/No | No | Default: No |
| CreatedDate | Date and Time | No | |

---

### List 8: AuditLog

| Column | Type | Required | Choices / Notes |
|---|---|---|---|
| Title | Text | Yes | Auto-created |
| EntityType | Choice | Yes | **MonthlyReport**, **Activity**, **Project** |
| EntityId | Single line of text | No | |
| Action | Choice | Yes | **StatusChange**, **Created**, **Updated**, **Deleted** |
| ActionBy | Person | No | People picker |
| ActionDate | Date and Time | No | |
| Reason | Multiple lines of text | No | |

---

### List 9: ReportComments

| Column | Type | Required | Choices / Notes |
|---|---|---|---|
| Title | Text | Yes | Auto-created |
| ReportID | Lookup | No | Points to MonthlyReports, Title |
| CommentBy | Person | No | People picker |
| CommentText | Multiple lines of text | No | |
| CommentDate | Date and Time | No | |

---

### List 10: KPIDefinitions

| Column | Type | Required | Choices / Notes |
|---|---|---|---|
| Title | Text | Yes | Auto-created |
| KPIName | Single line of text | No | |
| KPITarget | Number | No | |
| KPIUnit | Choice | Yes | **Percentage**, **Count**, **Currency** |
| ActivityID | Lookup | No | Points to Activities, Title |

---

## Step 3: Get List GUIDs

After creating each list, you need its GUID for the flow package. Here's how:

1. Open the list in SharePoint
2. Go to **List settings** (gear icon → List settings)
3. Look at the browser URL — it will contain:
   ```
   .../Lists/AllItems.aspx?List=%7B<GUID>%7D
   ```
4. The part between `%7B` and `%7D` is your GUID (without braces)

**Example:**
```
https://tenant.sharepoint.com/sites/APP-MRMS/_layouts/15/listedit.aspx?List=%7B8a1b2c3d-4e5f-6789-abcd-123456789012%7D
```
GUID = `8a1b2c3d-4e5f-6789-abcd-123456789012`

**Write down these GUIDs:**

| List | GUID |
|---|---|
| MonthlyReports | _______________ |
| Activities | _______________ |
| Notifications | _______________ |
| AuditLog | _______________ |
| APP_Users | _______________ |

---

## Step 4: Seed Data

For each list with seed data:
1. Open the list
2. Click **+ New**
3. Enter the data from the CSV files in `APP_MRMS/`

**Minimum required seed data:**

### APP_Users (at least 1 per role)

| Title | Role | UserAccount |
|---|---|---|
| System Admin | Administrator | Your admin email |
| Programme Manager | ProgrammeManager | Your PM email |
| Supervisor | Supervisor | Your supervisor email |
| Contributor | Contributor | Your contributor email |
| Deputy Director | DeputyDirectorME | Your deputy email |

---

## Step 5: Build Flow Package

Once you have the GUIDs, run:

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

---

## Step 6: Import Flows

1. Go to https://make.powerautomate.com
2. **My flows** → **Import** → **Package (.zip)**
3. Upload `flows/APP-MRMS-Approval.zip`
4. For each connection:
   - **SharePoint:** Select your account (needs Contribute on the site)
   - **Office 365 Outlook:** Select your account (needs send permissions)
5. Click **Import**
6. Open each flow → **Turn on**

---

## Step 7: Import Power App

1. Go to https://make.powerapps.com
2. **Apps** → **Import** → **Package (.zip)**
3. Upload `APP-MRMS_Project_app_v6.msapp` (or the latest version)
4. Map connections (same as flows)
5. Click **Import**
6. Open the app → **Edit** → Test in Power Apps Studio

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Can't create lists | Ask your site owner to create them |
| Can't find GUIDs | Ask your site owner for List settings access |
| Flow won't trigger | Check MonthlyReports.Status has "SupervisorApproved" choice |
| Email not received | Check Outlook connection is valid |
| Infinite loops | Verify flows don't write to MonthlyReports.Status |

---

## Quick Reference: List URLs

After creating lists, bookmark these:

| List | URL |
|---|---|
| Directorates | `https://<tenant>.sharepoint.com/sites/APP-MRMS/Lists/Directorates` |
| Programmes | `https://<tenant>.sharepoint.com/sites/APP-MRMS/Lists/Programmes` |
| Projects | `https://<tenant>.sharepoint.com/sites/APP-MRMS/Lists/Projects` |
| Activities | `https://<tenant>.sharepoint.com/sites/APP-MRMS/Lists/Activities` |
| MonthlyReports | `https://<tenant>.sharepoint.com/sites/APP-MRMS/Lists/MonthlyReports` |
| APP_Users | `https://<tenant>.sharepoint.com/sites/APP-MRMS/Lists/APP_Users` |
| Notifications | `https://<tenant>.sharepoint.com/sites/APP-MRMS/Lists/Notifications` |
| AuditLog | `https://<tenant>.sharepoint.com/sites/APP-MRMS/Lists/AuditLog` |
| ReportComments | `https://<tenant>.sharepoint.com/sites/APP-MRMS/Lists/ReportComments` |
| KPIDefinitions | `https://<tenant>.sharepoint.com/sites/APP-MRMS/Lists/KPIDefinitions` |
