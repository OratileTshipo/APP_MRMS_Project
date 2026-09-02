# MonthlyReminder Scheduled Flow — Reference

The MonthlyReminder is a **scheduled cloud flow** that runs every Monday at 08:00 and emails Contributors who have active monthly activities with **no report submitted** for the current month. Unlike the other APP-MRMS flows (which are event-triggered), this flow uses a **Recurrence** trigger and iterates across all active activities.

---

## Flow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  Recurrence Trigger — Every Monday at 08:00                     │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  Get Items — Activities where Active=1 AND Frequency='Monthly'  │
│  (Top Count: 500)                                               │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  Apply to Each Activity                                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Get Items — MonthlyReports where                          │  │
│  │   Activity = current activity's Title                     │  │
│  │   AND ReportingMonth = current month name                 │  │
│  │   (Top Count: 1)                                          │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │ Condition — length(body('Get_items_2')?['value']) eq 0    │  │
│  │  ┌─── Yes (no report found) ──────────────────────────┐  │  │
│  │  │ Send Email to ActivityOwner                         │  │  │
│  │  │ Subject: Reminder: <Activity> — <Desc> due <Date>  │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Trigger Configuration

### Recurrence Trigger

| Setting | Value |
|---------|-------|
| Type | Scheduled |
| Frequency | Week |
| Interval | 1 |
| On these days | Monday |
| At these hours | 8 |
| At these minutes | 0 |
| Time zone | (Your tenant's default) |

**In the portal:**
1. Create → **Scheduled cloud flow**
2. Flow name: `APP-MRMS Monthly Reminder`
3. Trigger: `Recurrence`
4. Set Frequency = `Week`, Interval = `1`
5. Under "On these days": select `Monday`
6. Under "At these hours": `8`
7. Under "At these minutes": `0`

**In definition.json:**
```json
{
  "Recurrence": {
    "recurrence": {
      "frequency": "Week",
      "interval": 1,
      "startTime": "2026-08-04T08:00:00Z",
      "timeZone": "South Africa Standard Time"
    },
    "evaluatedRecurrence": {
      "frequency": "Week",
      "interval": 1,
      "startTime": "2026-08-04T08:00:00Z",
      "timeZone": "South Africa Standard Time"
    },
    "type": "Recurrence",
    "inputs": {
      "recurrence": {
        "frequency": "Week",
        "interval": 1,
        "startTime": "2026-08-04T08:00:00Z",
        "timeZone": "South Africa Standard Time"
      }
    }
  }
}
```

---

## Step 1: Get Active Activities

### Action
- **Type:** `Get items` (SharePoint)
- **Site Address:** Your SharePoint site
- **List Name:** `Activities`

### Filter Query
```
Active eq 1 and Frequency eq 'Monthly'
```

### Top Count
```
500
```

> Adjust based on your data volume. The SharePoint list view threshold is 5,000 items.

### Definition JSON
```json
{
  "Get_active_activities": {
    "runAfter": {},
    "type": "OpenApiConnection",
    "inputs": {
      "parameters": {
        "dataset": "{{SITE_URL}}",
        "table": "{{ACT_GUID}}",
        "filterQuery": "Active eq 1 and Frequency eq 'Monthly'",
        "top": 500
      },
      "host": {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
        "connectionReferenceName": "shared_sharepointonline",
        "operationId": "GetItems"
      }
    }
  }
}
```

---

## Step 2: Apply to Each Activity

### Action
- **Type:** `Foreach` (Apply to each)
- **Select an output from previous steps:** `@body('Get_active_activities')?['value']`

### Definition JSON
```json
{
  "Apply_to_each_activity": {
    "runAfter": {
      "Get_active_activities": ["Succeeded"]
    },
    "type": "Foreach",
    "foreach": "@body('Get_active_activities')?['value']",
    "actions": {
      "... inside actions ..."
    }
  }
}
```

---

## Step 3: Get Current Reports (Inside Loop)

### Action
- **Type:** `Get items` (SharePoint)
- **Site Address:** Same
- **List Name:** `MonthlyReports`

### Filter Query
```
Activity eq '@{items('Apply_to_each_activity')?['Title']}' and ReportingMonth eq '@{formatDateTime(utcNow(), 'MMMM')}'
```

**How this works:**
- `items('Apply_to_each_activity')?['Title']` — the current activity's ID (e.g., `ICMTS-AC-0001`)
- `formatDateTime(utcNow(), 'MMMM')` — current month name (e.g., `August`)
- This checks if a report exists for **this specific activity** in **the current month**

### Top Count
```
1
```

> We only need to know if at least one report exists. Top 1 is efficient.

### Definition JSON
```json
{
  "Get_current_reports": {
    "runAfter": {},
    "type": "OpenApiConnection",
    "inputs": {
      "parameters": {
        "dataset": "{{SITE_URL}}",
        "table": "{{MR_GUID}}",
        "filterQuery": "Activity eq '@{items('Apply_to_each_activity')?['Title']}' and ReportingMonth eq '@{formatDateTime(utcNow(), 'MMMM')}'",
        "top": 1
      },
      "host": {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
        "connectionReferenceName": "shared_sharepointonline",
        "operationId": "GetItems"
      }
    }
  }
}
```

---

## Step 4: Condition — Check if No Report Found

### Action
- **Type:** `If` (Condition)
- **Expression:**
```json
{
  "equals": [
    "@length(body('Get_current_reports')?['value'])",
    "0"
  ]
}
```

**Logic:** If the array of reports is empty (length = 0), no report has been submitted for this activity this month → send reminder.

### Definition JSON
```json
{
  "Condition_no_report": {
    "runAfter": {
      "Get_current_reports": ["Succeeded"]
    },
    "type": "If",
    "expression": {
      "equals": [
        "@length(body('Get_current_reports')?['value'])",
        "0"
      ]
    },
    "actions": {
      "Send_Reminder_Email": { "..." }
    },
    "else": {}
  }
}
```

---

## Step 5: Send Reminder Email

### Action
- **Type:** `Send an email (V2)` (Office 365 Outlook)

### Recipient
- **To:** `items('Apply_to_each_activity')?['ActivityOwner']?['Email']`

> **Fallback:** If `ActivityOwner` is empty, use `items('Apply_to_each_activity')?['Supervisor']?['Email']` as a fallback. Add a nested condition to check which to use.

### Subject
```
Reminder: @{items('Apply_to_each_activity')?['Title']} — @{items('Apply_to_each_activity')?['ActivityShortDescription']} due @{items('Apply_to_each_activity')?['DueDate']}
```

### Body (HTML)
```html
<p><strong>This is a reminder that your monthly activity report is due soon.</strong></p>
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; font-family:Segoe UI, Arial, sans-serif;">
  <tr><td style="background:#f0f0f0;"><strong>Activity</strong></td><td>@{items('Apply_to_each_activity')?['Title']}</td></tr>
  <tr><td style="background:#f0f0f0;"><strong>Description</strong></td><td>@{items('Apply_to_each_activity')?['ActivityShortDescription']}</td></tr>
  <tr><td style="background:#f0f0f0;"><strong>Programme</strong></td><td>@{items('Apply_to_each_activity')?['ProgrammeLabel']}</td></tr>
  <tr><td style="background:#f0f0f0;"><strong>Directorate</strong></td><td>@{items('Apply_to_each_activity')?['DirectorateLabel']}</td></tr>
  <tr><td style="background:#fff0f0;"><strong>Due Date</strong></td><td>@{items('Apply_to_each_activity')?['DueDate']}</td></tr>
  <tr><td style="background:#f0f0f0;"><strong>Reporting Month</strong></td><td>@{formatDateTime(utcNow(), 'MMMM yyyy')}</td></tr>
</table>
<p>Please open the <strong>APP-MRMS</strong> application and submit your progress report before the due date.</p>
<p><em>This is an automated reminder from the APP Monthly Reporting Management System.</em></p>
```

### Importance
```
Normal
```

### Definition JSON
```json
{
  "Send_Reminder_Email": {
    "runAfter": {},
    "type": "OpenApiConnection",
    "inputs": {
      "parameters": {
        "emailMessage/To": "@{items('Apply_to_each_activity')?['ActivityOwner']?['Email']}",
        "emailMessage/Subject": "Reminder: @{items('Apply_to_each_activity')?['Title']} — @{items('Apply_to_each_activity')?['ActivityShortDescription']} due @{items('Apply_to_each_activity')?['DueDate']}",
        "emailMessage/Body": "<p><strong>This is a reminder that your monthly activity report is due soon.</strong></p><table border=\"1\" cellpadding=\"6\" cellspacing=\"0\" style=\"border-collapse:collapse; font-family:Segoe UI, Arial, sans-serif;\"><tr><td style=\"background:#f0f0f0;\"><strong>Activity</strong></td><td>@{items('Apply_to_each_activity')?['Title']}</td></tr><tr><td style=\"background:#f0f0f0;\"><strong>Description</strong></td><td>@{items('Apply_to_each_activity')?['ActivityShortDescription']}</td></tr><tr><td style=\"background:#f0f0f0;\"><strong>Programme</strong></td><td>@{items('Apply_to_each_activity')?['ProgrammeLabel']}</td></tr><tr><td style=\"background:#f0f0f0;\"><strong>Directorate</strong></td><td>@{items('Apply_to_each_activity')?['DirectorateLabel']}</td></tr><tr><td style=\"background:#fff0f0;\"><strong>Due Date</strong></td><td>@{items('Apply_to_each_activity')?['DueDate']}</td></tr><tr><td style=\"background:#f0f0f0;\"><strong>Reporting Month</strong></td><td>@{formatDateTime(utcNow(), 'MMMM yyyy')}</td></tr></table><p>Please open the <strong>APP-MRMS</strong> application and submit your progress report before the due date.</p><p><em>This is an automated reminder from the APP Monthly Reporting Management System.</em></p>",
        "emailMessage/Importance": "Normal"
      },
      "host": {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "connectionReferenceName": "shared_office365",
        "operationId": "SendEmailV2"
      }
    }
  }
}
```

---

## Complete Definition Skeleton

```json
{
  "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "$authentication": { "defaultValue": {}, "type": "SecureObject" },
    "$connections": { "defaultValue": {}, "type": "Object" }
  },
  "triggers": {
    "Recurrence": {
      "recurrence": {
        "frequency": "Week",
        "interval": 1,
        "startTime": "2026-08-04T08:00:00Z",
        "timeZone": "South Africa Standard Time"
      },
      "evaluatedRecurrence": {
        "frequency": "Week",
        "interval": 1,
        "startTime": "2026-08-04T08:00:00Z",
        "timeZone": "South Africa Standard Time"
      },
      "type": "Recurrence",
      "inputs": {
        "recurrence": {
          "frequency": "Week",
          "interval": 1,
          "startTime": "2026-08-04T08:00:00Z",
          "timeZone": "South Africa Standard Time"
        }
      }
    }
  },
  "actions": {
    "Get_active_activities": {
      "runAfter": {},
      "type": "OpenApiConnection",
      "inputs": {
        "parameters": {
          "dataset": "{{SITE_URL}}",
          "table": "{{ACT_GUID}}",
          "filterQuery": "Active eq 1 and Frequency eq 'Monthly'",
          "top": 500
        },
        "host": {
          "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
          "connectionReferenceName": "shared_sharepointonline",
          "operationId": "GetItems"
        }
      }
    },
    "Apply_to_each_activity": {
      "runAfter": { "Get_active_activities": ["Succeeded"] },
      "type": "Foreach",
      "foreach": "@body('Get_active_activities')?['value']",
      "actions": {
        "Get_current_reports": {
          "runAfter": {},
          "type": "OpenApiConnection",
          "inputs": {
            "parameters": {
              "dataset": "{{SITE_URL}}",
              "table": "{{MR_GUID}}",
              "filterQuery": "Activity eq '@{items('Apply_to_each_activity')?['Title']}' and ReportingMonth eq '@{formatDateTime(utcNow(), 'MMMM')}'",
              "top": 1
            },
            "host": {
              "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
              "connectionReferenceName": "shared_sharepointonline",
              "operationId": "GetItems"
            }
          }
        },
        "Condition_no_report": {
          "runAfter": { "Get_current_reports": ["Succeeded"] },
          "type": "If",
          "expression": {
            "equals": [
              "@length(body('Get_current_reports')?['value'])",
              "0"
            ]
          },
          "actions": {
            "Send_Reminder_Email": {
              "runAfter": {},
              "type": "OpenApiConnection",
              "inputs": {
                "parameters": {
                  "emailMessage/To": "@{items('Apply_to_each_activity')?['ActivityOwner']?['Email']}",
                  "emailMessage/Subject": "Reminder: @{items('Apply_to_each_activity')?['Title']} — @{items('Apply_to_each_activity')?['ActivityShortDescription']} due @{items('Apply_to_each_activity')?['DueDate']}",
                  "emailMessage/Body": "<p><strong>This is a reminder that your monthly activity report is due soon.</strong></p>",
                  "emailMessage/Importance": "Normal"
                },
                "host": {
                  "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
                  "connectionReferenceName": "shared_office365",
                  "operationId": "SendEmailV2"
                }
              }
            }
          },
          "else": {}
        }
      }
    }
  },
  "outputs": {}
}
```

---

## Key Expressions Reference

| Expression | Returns |
|------------|---------|
| `@formatDateTime(utcNow(), 'MMMM')` | Current month name: `August` |
| `@formatDateTime(utcNow(), 'MMMM yyyy')` | Month + year: `August 2026` |
| `@items('Apply_to_each_activity')?['Title']` | Current activity's ID |
| `@items('Apply_to_each_activity')?['ActivityShortDescription']` | Activity description |
| `@items('Apply_to_each_activity')?['DueDate']` | Activity due date |
| `@items('Apply_to_each_activity')?['ActivityOwner']?['Email']` | Owner's email |
| `@items('Apply_to_each_activity')?['Supervisor']?['Email']` | Supervisor's email (fallback) |
| `@body('Get_current_reports')?['value']` | Array of matching reports |
| `@length(body('Get_current_reports')?['value'])` | Count of matching reports |

---

## Differences from Event-Triggered Flows

| Aspect | Event Flows (Flows 1–4) | Scheduled Flow (MonthlyReminder) |
|--------|------------------------|----------------------------------|
| Trigger | `GetOnChangedItems` (SharePoint) | `Recurrence` (Week, Monday 08:00) |
| Trigger conditions | Yes (Status value filter) | None needed |
| Connection required | SharePoint + Outlook | SharePoint + Outlook |
| `authentication` on trigger | Yes (`@parameters('$authentication')`) | No (Recurrence doesn't need auth) |
| Looping | No (single item per run) | Yes (Apply to Each over all activities) |
| Data access | `triggerBody()` | `items('Apply_to_each_activity')` |
| Items per run | 1 (via `splitOn`) | Many (batch of emails) |
| Scheduled start time | N/A | Must be in the past to run |

---

## Variations and Extensions

### Variation 1: Weekly Activities
Change the filter to include weekly activities:
```
Active eq 1 and (Frequency eq 'Monthly' or Frequency eq 'Weekly')
```

### Variation 2: Due-Date Based Filtering
Only remind for activities due within 7 days:
```
Active eq 1 and Frequency eq 'Monthly' and DueDate le '@{addDays(utcNow(), 7)}' and DueDate ge '@{utcNow()}'
```

### Variation 3: Fallback Recipient
If ActivityOwner is empty, send to Supervisor instead:

Add a nested Condition inside the "If yes" branch:
```json
{
  "Condition_has_owner": {
    "runAfter": {},
    "type": "If",
    "expression": {
      "not": [
        { "equals": ["@items('Apply_to_each_activity')?['ActivityOwner']?['Email']", ""] }
      ]
    },
    "actions": {
      "Send_to_Owner": {
        "runAfter": {},
        "type": "OpenApiConnection",
        "inputs": {
          "parameters": {
            "emailMessage/To": "@{items('Apply_to_each_activity')?['ActivityOwner']?['Email']}"
          },
          "host": {
            "connectionReferenceName": "shared_office365",
            "operationId": "SendEmailV2"
          }
        }
      }
    },
    "else": {
      "actions": {
        "Send_to_Supervisor": {
          "runAfter": {},
          "type": "OpenApiConnection",
          "inputs": {
            "parameters": {
              "emailMessage/To": "@{items('Apply_to_each_activity')?['Supervisor']?['Email']}"
            },
            "host": {
              "connectionReferenceName": "shared_office365",
              "operationId": "SendEmailV2"
            }
          }
        }
      }
    }
  }
}
```

### Variation 4: Create In-App Notification
After sending email, also create a Notifications row:
```json
{
  "Create_Notification": {
    "runAfter": { "Send_Reminder_Email": ["Succeeded"] },
    "type": "OpenApiConnection",
    "inputs": {
      "parameters": {
        "dataset": "{{SITE_URL}}",
        "table": "{{NOTIF_GUID}}",
        "Title": "Reminder: @{items('Apply_to_each_activity')?['Title']}",
        "Message": "Monthly report is overdue for activity @{items('Apply_to_each_activity')?['Title']}",
        "RecipientEmail": "@{items('Apply_to_each_activity')?['ActivityOwner']?['Email']}",
        "IsRead": false
      },
      "host": {
        "connectionReferenceName": "shared_sharepointonline",
        "operationId": "CreateItem"
      }
    }
  }
}
```

### Variation 5: Daily Overdue Escalation (Phase 2)
Change recurrence to daily and add overdue tracking:
```
Frequency: Day
Interval: 1
Filter: Active eq 1 and Frequency eq 'Monthly' and DueDate lt '@{utcNow()}'
```
Inside the loop, update the activity to mark it overdue:
```json
{
  "parameters": {
    "id": "@{items('Apply_to_each_activity')?['Id']}",
    "IsOverdue": true
  },
  "operationId": "UpdateItem"
}
```

---

## Testing the Scheduled Flow

### Manual Test
1. Save the flow
2. Click **Test** → **Manually** → **Test**
3. The flow runs immediately (ignoring the schedule)
4. Check run history for results

### Production Test
1. Turn on the flow
2. Wait for the next Monday at 08:00
3. Check run history and email inboxes

### Test with Sample Data
Before enabling, create test data in SharePoint:
1. Ensure at least 2-3 Activities with `Active = 1` and `Frequency = Monthly`
2. Ensure at least 1 Activity has **no** MonthlyReports entry for the current month
3. Ensure at least 1 Activity **has** a MonthlyReports entry (to verify it's skipped)

---

## Performance Considerations

| Concern | Mitigation |
|---------|-----------|
| Many activities (100+) | Apply to Each runs sequentially by default; consider batching |
| SharePoint API throttling | Default 3-minute polling is fine; don't shorten recurrence |
| Large Get Items results | Use `top` parameter and indexed `filterQuery` columns |
| Email volume | One email per activity with no report; could be 50+ on a Monday |
| Flow timeout | Each iteration is fast (Get + Condition + Email); 500 activities should complete in minutes |

---

*Source: Microsoft Learn Power Automate — Scheduled flows, Apply to Each, Recurrence trigger*
*APP-MRMS Project — Flow 3: MonthlyReminder*
