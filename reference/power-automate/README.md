# Power Automate Documentation Reference

**Source:** Microsoft Learn (https://learn.microsoft.com/en-us/power-automate/)  
**Extracted:** 2026-08-18  
**Purpose:** Reference for APP-MRMS approval workflow development

---

## 1. Overview

Power Automate is a cloud-based service that allows users to create automated workflows between apps and services. For APP-MRMS, we use **cloud flows** triggered by SharePoint list changes.

---

## 2. Flow Types

| Type | Trigger | Use Case in APP-MRMS |
|---|---|---|
| **Automated Cloud Flow** | Event-based (SharePoint item created/modified) | Status change notifications |
| **Instant Cloud Flow** | Manual trigger (button, HTTP) | Approve/Reject actions from Power Apps |
| **Scheduled Cloud Flow** | Time-based (recurring) | Monthly reminders, overdue escalation |

---

## 3. SharePoint Connector

### 3.1 Triggers

| Trigger | Description | APP-MRMS Usage |
|---|---|---|
| `When an item is created` | Fires when new item added | Not used (reports start as Draft) |
| `When an item is created or modified` | Fires on any change | ✅ **Main trigger** for approval flows |
| `When an item is deleted` | Fires on delete | Not used |
| `For a selected item` | Manual trigger from SharePoint | Optional: manual approval |

### 3.2 Actions

| Action | Description | APP-MRMS Usage |
|---|---|---|
| `Create item` | Add new row to list | Create Notifications, AuditLog |
| `Get item` | Get single item by ID | Get report details |
| `Get items` | Get multiple items with filter | Get DeputyDirectorME user |
| `Update item` | Modify existing row | Update Status, ReviewedBy |
| `Send an HTTP request to SharePoint` | Custom REST API call | Advanced scenarios |

### 3.3 Key Expression Syntax

```
// Trigger body (current item)
@triggerBody()?['ID']
@triggerBody()?['Status/Value']
@triggerBody()?['SubmittedBy/EMail']
@triggerBody()?['ReviewedBy/EMail']
@triggerBody()?['RejectionReason']

// Get item output
@outputs('Get_item')?['body/Title']
@outputs('Get_item')?['body/Supervisor/EMail']

// Compose expressions
@concat('Report ', triggerBody()?['ID'], ' was approved')
@if(equals(triggerBody()?['Status/Value'], 'Submitted'), 'Pending', 'Other')

// Date functions
@utcNow()
@addDays(utcNow(), 5)
@formatDateTime(utcNow(), 'yyyy-MM-dd')

// String functions
@toLower(triggerBody()?['Title'])
@contains(triggerBody()?['Status/Value'], 'Reject')
```

---

## 4. APP-MRMS Flow Architecture

### 4.1 Flow 1: Report Submitted → Notify Supervisor
```
Trigger: When an item is modified (MonthlyReports)
Condition: Status/Value = "Submitted"
Actions:
  1. Get activity details (Get item → Activities)
  2. Get supervisor email (from activity)
  3. Send email to supervisor
  4. Create notification record
  5. Write audit log
```

### 4.2 Flow 2: Supervisor Approved → Route to Deputy
```
Trigger: When an item is modified (MonthlyReports)
Condition: Status/Value = "SupervisorApproved"
Actions:
  1. Get deputy director (Get items → APP_Users where Role = "DeputyDirectorME")
  2. Send email to deputy
  3. Send email to contributor
  4. Create notification records
  5. Write audit log
```

### 4.3 Flow 3: Report Rejected → Notify and Route Back
```
Trigger: When an item is modified (MonthlyReports)
Condition: Status/Value = "Rejected"
Branch: Who rejected? (ReviewedBy = Deputy?)
  Then (Deputy rejected):
    1. Email contributor
    2. Email supervisor
    3. Create notifications
  Else (Supervisor rejected):
    1. Email contributor
    2. Create notification
Actions:
  Write audit log
```

### 4.4 Flow 4: Report Approved → Finalize
```
Trigger: When an item is modified (MonthlyReports)
Condition: Status/Value = "Approved"
Actions:
  1. Get activity details
  2. Email contributor
  3. Email supervisor
  4. Create notifications
  5. Update activity (Status = "Completed", Active = false)
  6. Write audit log
```

---

## 5. Loop Prevention

**Critical:** Power Automate flows triggered by "item modified" will re-trigger if they write to the same item.

### Rules for APP-MRMS:
1. **Never write Status from a flow** — only Power Apps buttons set Status
2. **Flows only write to side tables:** Notifications, AuditLog
3. **Exception:** Flow 4 can update Activity (not MonthlyReports)
4. **Use conditions:** Check `Status/Value` before acting

### If loop occurs:
- Check if flow writes to the triggering list
- Add a condition to skip if the change was made by the flow itself
- Use a "marker column" to detect flow-initiated changes

---

## 6. Connection References

### Required for APP-MRMS:
| Connection | API | Purpose |
|---|---|---|
| `shared_sharepointonline` | SharePoint | Read/write lists |
| `shared_office365` | Office 365 Outlook | Send emails |

### Import Instructions:
1. Power Automate → Import → Package (.zip)
2. For each connection, select/create a valid connection
3. Ensure the connection user has:
   - SharePoint: Contribute on the APP-MRMS site
   - Outlook: Send-as permissions

---

## 7. Environment Variables

For multi-environment deployment (Dev → Test → Prod), use **Environment Variables**:

| Variable | Purpose | Example |
|---|---|---|
| `MRMS_SiteUrl` | SharePoint site URL | `https://tenant.sharepoint.com/sites/APP-MRMS` |
| `MRMS_MonthlyReports_GUID` | List GUID | `{-guid}` |
| `MRMS_Activities_GUID` | List GUID | `{guid}` |
| `MRMS_Notifications_GUID` | List GUID | `{guid}` |
| `MRMS_AuditLog_GUID` | List GUID | `{guid}` |
| `MRMS_APPUsers_GUID` | List GUID | `{guid}` |

Reference in flow: `@parameters('MRMS_SiteUrl')`

---

## 8. Error Handling

### Common Errors:
| Error | Cause | Fix |
|---|---|---|
| `401 Unauthorized` | Connection expired or wrong permissions | Re-authenticate connection |
| `404 Not Found` | List GUID wrong or list deleted | Verify list GUID |
| `400 Bad Request` | Invalid column name or type | Check column internal names |
| `Trigger never fires` | Flow disabled or wrong filter | Turn on flow, check condition |

### Best Practices:
1. Use **Configure Run After** to handle failures
2. Add **Scope** actions for try/catch patterns
3. Log errors to AuditLog for debugging
4. Set **Retry Policy** on HTTP actions (429 throttling)

---

## 9. Testing

### Test a flow:
1. Open the flow → Test → Manually
2. Create/modify a SharePoint item
3. Check run history for each action
4. Verify email delivery and notification creation

### Run History:
- Power Automate → My flows → Select flow → 28-day run history
- Click a run to see inputs/outputs for each action
- Failed actions show error details

---

## 10. Import/Export

### Export a flow:
1. Power Automate → My flows → Select flow
2. ⋯ → Export → Package (.zip)
3. Include connections

### Import a flow:
1. Power Automate → Import → Package (.zip)
2. Upload the .zip file
3. Map connections
4. Choose New or Update
5. Turn on after import

### Package Structure:
```
flow-export.zip
├── manifest.json              # Root manifest
├── Microsoft.Flow/
│   ├── flows/
│   │   ├── manifest.json      # Flow assets list
│   │   └── <flow-guid>/
│   │       ├── definition.json    # Flow definition
│   │       ├── apisMap.json       # API mappings
│   │       └── connectionsMap.json # Connection mappings
```

---

## 11. Best Practices for APP-MRMS

1. **One flow per status transition** — prevents loops
2. **Never write Status from flows** — only Power Apps writes Status
3. **Use separate flows for each notification path** — easier to debug
4. **Pre-fetch related data** — Get item/activity in parallel
5. **Create notifications in bulk** — use Apply to each efficiently
6. **Test with real data** — not just test items
7. **Document connection requirements** — who owns each connection
8. **Use environment variables** — for multi-environment deployment

---

## 12. References

- [Power Automate Documentation](https://learn.microsoft.com/en-us/power-automate/)
- [SharePoint Connector Reference](https://learn.microsoft.com/en-us/sharepoint/dev/business-apps/power-automate/sharepoint-connector-actions-triggers)
- [Flow Types Overview](https://learn.microsoft.com/en-us/power-automate/flow-types)
- [Expression Reference](https://learn.microsoft.com/en-us/power-automate/reference-reference-expressions)
- [Troubleshooting](https://learn.microsoft.com/en-us/power-automate/troubleshooting-overview)
