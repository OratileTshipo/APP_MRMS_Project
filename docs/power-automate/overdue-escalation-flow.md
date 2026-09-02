# Overdue Escalation Flow — Reference (Phase 2)

The Overdue Escalation flow is a **daily scheduled flow** that detects activities past their `DueDate`, marks them as overdue, and sends escalating notifications — first to the ActivityOwner, then to the Supervisor, and finally to the Programme Manager after 3 days of non-submission.

This flow complements the [MonthlyReminder](alerting-flow.md) (weekly) by handling activities that have already missed their deadline.

---

## Flow Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│  Recurrence Trigger — Every day at 07:00                             │
└──────────────────────┬───────────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────────┐
│  Get Items — Activities where                                        │
│    Active = 1                                                        │
│    AND Frequency = 'Monthly'                                         │
│    AND DueDate < today (overdue)                                     │
│  (Top Count: 500)                                                    │
└──────────────────────┬───────────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────────┐
│  Apply to Each Activity                                              │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ Compose — Calculate days overdue                               │  │
│  │   dateDifference(items('...')?['DueDate'], utcNow())          │  │
│  ├────────────────────────────────────────────────────────────────┤  │
│  │ Condition — Days overdue > 3?                                  │  │
│  │  ┌─── Yes (escalate) ──────────────────────────────────────┐  │  │
│  │  │ 1. Update Activity → Status = "Escalated"               │  │  │
│  │  │ 2. Send Email → Programme Manager (escalation)          │  │  │
│  │  │ 3. Send Email → Supervisor (escalation)                 │  │  │
│  │  │ 4. Create Notification row                               │  │  │
│  │  │ 5. Create AuditLog entry                                │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │  ┌─── No (still within grace period) ──────────────────────┐  │  │
│  │  │ Condition — Days overdue > 0?                            │  │  │
│  │  │  ┌─── Yes ──────────────────────────────────────────┐   │  │  │
│  │  │  │ 1. Update Activity → IsOverdue = true             │   │  │  │
│  │  │  │ 2. Send Email → ActivityOwner (warning)           │   │  │  │
│  │  │  │ 3. Send Email → Supervisor (heads-up)             │   │  │  │
│  │  │  └───────────────────────────────────────────────────┘   │  │  │
│  │  └──────────────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Escalation Tiers

| Tier | Days Overdue | Recipients | Actions | Status Change |
|------|-------------|------------|---------|---------------|
| **1 — Warning** | 1–3 days | ActivityOwner, Supervisor | Email warning | `IsOverdue = true` |
| **2 — Escalation** | > 3 days | Programme Manager, Supervisor | Email escalation | `Status = "Escalated"` |

### Why 3 days?
- Gives the ActivityOwner a grace period to submit after the due date
- The weekly MonthlyReminder may have already fired on the Monday before the due date
- 3 business days is a reasonable window before management escalation

---

## Trigger Configuration

### Recurrence Trigger

| Setting | Value |
|---------|-------|
| Type | Scheduled |
| Frequency | Day |
| Interval | 1 |
| At these hours | 7 |
| At these minutes | 0 |
| Time zone | (Your tenant's default) |

Runs every morning at 07:00 — before the workday starts, so overdue items are flagged early.

**In the portal:**
1. Create → **Scheduled cloud flow**
2. Flow name: `APP-MRMS Overdue Escalation`
3. Trigger: `Recurrence`
4. Frequency = `Day`, Interval = `1`
5. At these hours: `7`, At these minutes: `0`

**In definition.json:**
```json
{
  "Recurrence": {
    "recurrence": {
      "frequency": "Day",
      "interval": 1,
      "startTime": "2026-09-01T07:00:00Z",
      "timeZone": "South Africa Standard Time"
    },
    "evaluatedRecurrence": {
      "frequency": "Day",
      "interval": 1,
      "startTime": "2026-09-01T07:00:00Z",
      "timeZone": "South Africa Standard Time"
    },
    "type": "Recurrence",
    "inputs": {
      "recurrence": {
        "frequency": "Day",
        "interval": 1,
        "startTime": "2026-09-01T07:00:00Z",
        "timeZone": "South Africa Standard Time"
      }
    }
  }
}
```

---

## Step 1: Get Overdue Activities

### Action
- **Type:** `Get items` (SharePoint)
- **List:** `Activities`

### Filter Query
```
Active eq 1 and Frequency eq 'Monthly' and DueDate lt '@{formatDateTime(utcNow(), 'yyyy-MM-dd')}'
```

**How this works:**
- `Active eq 1` — only active activities
- `Frequency eq 'Monthly'` — only monthly reporting activities
- `DueDate lt '@{formatDateTime(utcNow(), 'yyyy-MM-dd')}'` — due date is before today (overdue)

### Top Count
```
500
```

### Definition JSON
```json
{
  "Get_overdue_activities": {
    "runAfter": {},
    "type": "OpenApiConnection",
    "inputs": {
      "parameters": {
        "dataset": "{{SITE_URL}}",
        "table": "{{ACT_GUID}}",
        "filterQuery": "Active eq 1 and Frequency eq 'Monthly' and DueDate lt '@{formatDateTime(utcNow(), 'yyyy-MM-dd')}'",
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

### Definition JSON
```json
{
  "Apply_to_each_overdue": {
    "runAfter": { "Get_overdue_activities": ["Succeeded"] },
    "type": "Foreach",
    "foreach": "@body('Get_overdue_activities')?['value']",
    "actions": {
      "... inside actions ..."
    }
  }
}
```

---

## Step 3: Calculate Days Overdue (Inside Loop)

### Action
- **Type:** `Compose`
- **Input expression:**
```
@dateDifference(items('Apply_to_each_overdue')?['DueDate'], utcNow())
```

**Returns:** Number of days between the due date and now (e.g., `5`).

### Definition JSON
```json
{
  "Calculate_days_overdue": {
    "runAfter": {},
    "type": "Compose",
    "inputs": "@dateDifference(items('Apply_to_each_overdue')?['DueDate'], utcNow())"
  }
}
```

> **Note:** `dateDifference` returns a positive number when the second date is after the first. Since `DueDate` is before `utcNow()`, the result is positive.

---

## Step 4: Condition — Days Overdue > 3 (Escalation Tier)

### Action
- **Type:** `If` (Condition)
- **Expression:**
```json
{
  "greater": [
    "@outputs('Calculate_days_overdue')",
    "3"
  ]
}
```

### Definition JSON
```json
{
  "Condition_escalation": {
    "runAfter": { "Calculate_days_overdue": ["Succeeded"] },
    "type": "If",
    "expression": {
      "greater": [
        "@outputs('Calculate_days_overdue')",
        "3"
      ]
    },
    "actions": {
      "... escalation actions (Tier 2) ..."
    },
    "else": {
      "actions": {
        "... warning actions (Tier 1) ..."
      }
    }
  }
}
```

---

## Tier 2: Escalation Actions (Days > 3)

### 4A. Update Activity Status to "Escalated"

```json
{
  "Update_activity_escalated": {
    "runAfter": {},
    "type": "OpenApiConnection",
    "inputs": {
      "parameters": {
        "dataset": "{{SITE_URL}}",
        "table": "{{ACT_GUID}}",
        "id": "@{items('Apply_to_each_overdue')?['Id']}",
        "Status": { "Value": "Escalated" },
        "IsOverdue": true
      },
      "host": {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
        "connectionReferenceName": "shared_sharepointonline",
        "operationId": "UpdateItem"
      }
    }
  }
}
```

> **Note:** Requires `Escalated` as a choice value in the `Status` column, and `IsOverdue` as a Yes/No column on the Activities list.

### 4B. Get Programme Manager

```json
{
  "Get_programme": {
    "runAfter": {},
    "type": "OpenApiConnection",
    "inputs": {
      "parameters": {
        "dataset": "{{SITE_URL}}",
        "table": "{{PROG_GUID}}",
        "filterQuery": "Title eq '@{items('Apply_to_each_overdue')?['ProgrammeLabel']}'",
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

### 4C. Send Escalation Email to Programme Manager

```
To: body('Get_programme')?['value'][0]?['ProgrammeManager']?['Email']
Subject: ESCALATION: @{items('Apply_to_each_overdue')?['Title']} — @{outputs('Calculate_days_overdue')} days overdue
Importance: High
```

**Body (HTML):**
```html
<p><strong>This activity has been escalated — the report is @{outputs('Calculate_days_overdue')} days overdue.</strong></p>
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; font-family:Segoe UI, Arial, sans-serif;">
  <tr><td style="background:#f0f0f0;"><strong>Activity</strong></td><td>@{items('Apply_to_each_overdue')?['Title']}</td></tr>
  <tr><td style="background:#f0f0f0;"><strong>Description</strong></td><td>@{items('Apply_to_each_overdue')?['ActivityShortDescription']}</td></tr>
  <tr><td style="background:#f0f0f0;"><strong>Programme</strong></td><td>@{items('Apply_to_each_overdue')?['ProgrammeLabel']}</td></tr>
  <tr><td style="background:#f0f0f0;"><strong>Directorate</strong></td><td>@{items('Apply_to_each_overdue')?['DirectorateLabel']}</td></tr>
  <tr><td style="background:#f0f0f0;"><strong>Activity Owner</strong></td><td>@{items('Apply_to_each_overdue')?['ActivityOwner']?['DisplayName']}</td></tr>
  <tr><td style="background:#f0f0f0;"><strong>Supervisor</strong></td><td>@{items('Apply_to_each_overdue')?['Supervisor']?['DisplayName']}</td></tr>
  <tr><td style="background:#fff0f0;"><strong>Due Date</strong></td><td>@{items('Apply_to_each_overdue')?['DueDate']}</td></tr>
  <tr><td style="background:#fff0f0;"><strong>Days Overdue</strong></td><td>@{outputs('Calculate_days_overdue')}</td></tr>
</table>
<p>Please follow up with the Activity Owner and Supervisor to ensure the report is submitted immediately.</p>
<p><em>This is an automated escalation from the APP Monthly Reporting Management System.</em></p>
```

### 4D. Send Escalation Email to Supervisor

Same as 4C but to Supervisor:
```
To: items('Apply_to_each_overdue')?['Supervisor']?['Email']
Subject: ESCALATION: @{items('Apply_to_each_overdue')?['Title']} — @{outputs('Calculate_days_overdue')} days overdue
Importance: High
```

### 4E. Create AuditLog Entry

```json
{
  "Create_audit_log_escalation": {
    "runAfter": {},
    "type": "OpenApiConnection",
    "inputs": {
      "parameters": {
        "dataset": "{{SITE_URL}}",
        "table": "{{AUDIT_GUID}}",
        "Title": "Escalated: @{items('Apply_to_each_overdue')?['Title']}",
        "Activity": "@{items('Apply_to_each_overdue')?['Title']}",
        "Action": "Auto-Escalated",
        "ActorEmail": "system@automated",
        "Details": "Activity @{items('Apply_to_each_overdue')?['Title']} escalated after @{outputs('Calculate_days_overdue')} days overdue"
      },
      "host": {
        "connectionReferenceName": "shared_sharepointonline",
        "operationId": "CreateItem"
      }
    }
  }
}
```

### 4F. Create Notification Row (In-App Badge)

```json
{
  "Create_notification_escalation": {
    "runAfter": {},
    "type": "OpenApiConnection",
    "inputs": {
      "parameters": {
        "dataset": "{{SITE_URL}}",
        "table": "{{NOTIF_GUID}}",
        "Title": "ESCALATED: @{items('Apply_to_each_overdue')?['Title']}",
        "Message": "Activity is @{outputs('Calculate_days_overdue')} days overdue — escalated to Programme Manager",
        "RecipientEmail": "@{items('Apply_to_each_overdue')?['Supervisor']?['Email']}",
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

---

## Tier 1: Warning Actions (Days 1–3)

Inside the `else` branch of `Condition_escalation`:

### 5A. Mark as Overdue

```json
{
  "Update_activity_overdue": {
    "runAfter": {},
    "type": "OpenApiConnection",
    "inputs": {
      "parameters": {
        "dataset": "{{SITE_URL}}",
        "table": "{{ACT_GUID}}",
        "id": "@{items('Apply_to_each_overdue')?['Id']}",
        "IsOverdue": true
      },
      "host": {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
        "connectionReferenceName": "shared_sharepointonline",
        "operationId": "UpdateItem"
      }
    }
  }
}
```

### 5B. Condition — ActivityOwner Email Exists

```json
{
  "Condition_has_owner": {
    "runAfter": {},
    "type": "If",
    "expression": {
      "not": [
        { "equals": ["@items('Apply_to_each_overdue')?['ActivityOwner']?['Email']", ""] }
      ]
    },
    "actions": {
      "Send_warning_owner": { "..." }
    },
    "else": {
      "actions": {
        "Send_warning_supervisor_only": { "..." }
      }
    }
  }
}
```

### 5C. Send Warning Email to ActivityOwner

```
To: items('Apply_to_each_overdue')?['ActivityOwner']?['Email']
Subject: Warning: @{items('Apply_to_each_overdue')?['Title']} — @{outputs('Calculate_days_overdue')} days overdue
Importance: Normal
```

**Body (HTML):**
```html
<p><strong>Your monthly activity report is @{outputs('Calculate_days_overdue')} days overdue.</strong></p>
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; font-family:Segoe UI, Arial, sans-serif;">
  <tr><td style="background:#f0f0f0;"><strong>Activity</strong></td><td>@{items('Apply_to_each_overdue')?['Title']}</td></tr>
  <tr><td style="background:#f0f0f0;"><strong>Description</strong></td><td>@{items('Apply_to_each_overdue')?['ActivityShortDescription']}</td></tr>
  <tr><td style="background:#fff0f0;"><strong>Due Date</strong></td><td>@{items('Apply_to_each_overdue')?['DueDate']}</td></tr>
  <tr><td style="background:#fff0f0;"><strong>Days Overdue</strong></td><td>@{outputs('Calculate_days_overdue')}</td></tr>
</table>
<p>Please submit your progress report immediately. If not submitted within 3 days, this will be escalated to your Programme Manager.</p>
<p><em>This is an automated reminder from the APP Monthly Reporting Management System.</em></p>
```

### 5D. Send Warning Email to Supervisor

Same email as 5C but to Supervisor:
```
To: items('Apply_to_each_overdue')?['Supervisor']?['Email']
Subject: Warning: @{items('Apply_to_each_overdue')?['Title']} — @{outputs('Calculate_days_overdue')} days overdue
Importance: Normal
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
      "recurrence": { "frequency": "Day", "interval": 1, "startTime": "2026-09-01T07:00:00Z", "timeZone": "South Africa Standard Time" },
      "evaluatedRecurrence": { "frequency": "Day", "interval": 1, "startTime": "2026-09-01T07:00:00Z", "timeZone": "South Africa Standard Time" },
      "type": "Recurrence",
      "inputs": { "recurrence": { "frequency": "Day", "interval": 1, "startTime": "2026-09-01T07:00:00Z", "timeZone": "South Africa Standard Time" } }
    }
  },
  "actions": {
    "Get_overdue_activities": {
      "runAfter": {},
      "type": "OpenApiConnection",
      "inputs": {
        "parameters": {
          "dataset": "{{SITE_URL}}",
          "table": "{{ACT_GUID}}",
          "filterQuery": "Active eq 1 and Frequency eq 'Monthly' and DueDate lt '@{formatDateTime(utcNow(), 'yyyy-MM-dd')}'",
          "top": 500
        },
        "host": {
          "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
          "connectionReferenceName": "shared_sharepointonline",
          "operationId": "GetItems"
        }
      }
    },
    "Apply_to_each_overdue": {
      "runAfter": { "Get_overdue_activities": ["Succeeded"] },
      "type": "Foreach",
      "foreach": "@body('Get_overdue_activities')?['value']",
      "actions": {
        "Calculate_days_overdue": {
          "runAfter": {},
          "type": "Compose",
          "inputs": "@dateDifference(items('Apply_to_each_overdue')?['DueDate'], utcNow())"
        },
        "Condition_escalation": {
          "runAfter": { "Calculate_days_overdue": ["Succeeded"] },
          "type": "If",
          "expression": { "greater": ["@outputs('Calculate_days_overdue')", "3"] },
          "actions": {
            "Update_activity_escalated": {
              "runAfter": {},
              "type": "OpenApiConnection",
              "inputs": {
                "parameters": {
                  "dataset": "{{SITE_URL}}", "table": "{{ACT_GUID}}",
                  "id": "@{items('Apply_to_each_overdue')?['Id']}",
                  "Status": { "Value": "Escalated" }, "IsOverdue": true
                },
                "host": { "connectionReferenceName": "shared_sharepointonline", "operationId": "UpdateItem" }
              }
            },
            "Get_programme": {
              "runAfter": { "Update_activity_escalated": ["Succeeded"] },
              "type": "OpenApiConnection",
              "inputs": {
                "parameters": {
                  "dataset": "{{SITE_URL}}", "table": "{{PROG_GUID}}",
                  "filterQuery": "Title eq '@{items('Apply_to_each_overdue')?['ProgrammeLabel']}'",
                  "top": 1
                },
                "host": { "connectionReferenceName": "shared_sharepointonline", "operationId": "GetItems" }
              }
            },
            "Send_escalation_pm": {
              "runAfter": { "Get_programme": ["Succeeded"] },
              "type": "OpenApiConnection",
              "inputs": {
                "parameters": {
                  "emailMessage/To": "@{body('Get_programme')?['value'][0]?['ProgrammeManager']?['Email']}",
                  "emailMessage/Subject": "ESCALATION: @{items('Apply_to_each_overdue')?['Title']} — @{outputs('Calculate_days_overdue')} days overdue",
                  "emailMessage/Body": "<p><strong>Escalated — @{outputs('Calculate_days_overdue')} days overdue.</strong></p>",
                  "emailMessage/Importance": "High"
                },
                "host": { "connectionReferenceName": "shared_office365", "operationId": "SendEmailV2" }
              }
            },
            "Send_escalation_supervisor": {
              "runAfter": {},
              "type": "OpenApiConnection",
              "inputs": {
                "parameters": {
                  "emailMessage/To": "@{items('Apply_to_each_overdue')?['Supervisor']?['Email']}",
                  "emailMessage/Subject": "ESCALATION: @{items('Apply_to_each_overdue')?['Title']} — @{outputs('Calculate_days_overdue')} days overdue",
                  "emailMessage/Body": "<p><strong>Escalated — @{outputs('Calculate_days_overdue')} days overdue.</strong></p>",
                  "emailMessage/Importance": "High"
                },
                "host": { "connectionReferenceName": "shared_office365", "operationId": "SendEmailV2" }
              }
            }
          },
          "else": {
            "actions": {
              "Update_activity_overdue": {
                "runAfter": {},
                "type": "OpenApiConnection",
                "inputs": {
                  "parameters": {
                    "dataset": "{{SITE_URL}}", "table": "{{ACT_GUID}}",
                    "id": "@{items('Apply_to_each_overdue')?['Id']}",
                    "IsOverdue": true
                  },
                  "host": { "connectionReferenceName": "shared_sharepointonline", "operationId": "UpdateItem" }
                }
              },
              "Send_warning_owner": {
                "runAfter": { "Update_activity_overdue": ["Succeeded"] },
                "type": "OpenApiConnection",
                "inputs": {
                  "parameters": {
                    "emailMessage/To": "@{items('Apply_to_each_overdue')?['ActivityOwner']?['Email']}",
                    "emailMessage/Subject": "Warning: @{items('Apply_to_each_overdue')?['Title']} — @{outputs('Calculate_days_overdue')} days overdue",
                    "emailMessage/Body": "<p><strong>@{outputs('Calculate_days_overdue')} days overdue.</strong></p>",
                    "emailMessage/Importance": "Normal"
                  },
                  "host": { "connectionReferenceName": "shared_office365", "operationId": "SendEmailV2" }
                }
              },
              "Send_warning_supervisor": {
                "runAfter": {},
                "type": "OpenApiConnection",
                "inputs": {
                  "parameters": {
                    "emailMessage/To": "@{items('Apply_to_each_overdue')?['Supervisor']?['Email']}",
                    "emailMessage/Subject": "Warning: @{items('Apply_to_each_overdue')?['Title']} — @{outputs('Calculate_days_overdue')} days overdue",
                    "emailMessage/Body": "<p><strong>@{outputs('Calculate_days_overdue')} days overdue.</strong></p>",
                    "emailMessage/Importance": "Normal"
                  },
                  "host": { "connectionReferenceName": "shared_office365", "operationId": "SendEmailV2" }
                }
              }
            }
          }
        }
      }
    }
  },
  "outputs": {}
}
```

---

## Key Expressions Reference

| Expression | Returns | Example |
|------------|---------|---------|
| `@formatDateTime(utcNow(), 'yyyy-MM-dd')` | Today as date string | `2026-09-02` |
| `@dateDifference(items('Apply_to_each_overdue')?['DueDate'], utcNow())` | Days between due date and now | `5` |
| `@outputs('Calculate_days_overdue')` | Compose output (days overdue) | `5` |
| `@items('Apply_to_each_overdue')?['Title']` | Activity ID | `ICMTS-AC-0001` |
| `@items('Apply_to_each_overdue')?['ActivityOwner']?['Email']` | Owner email | `jane@org.com` |
| `@items('Apply_to_each_overdue')?['Supervisor']?['Email']` | Supervisor email | `sarah@org.com` |
| `@items('Apply_to_each_overdue')?['ProgrammeLabel']` | Programme name | `ICTMS` |
| `@body('Get_programme')?['value'][0]?['ProgrammeManager']?['Email']` | PM email from lookup | `manager@org.com` |

---

## Prerequisites

Before building this flow, ensure these columns exist on the Activities list:

| Column | Type | Notes |
|--------|------|-------|
| `IsOverdue` | Yes/No | New column — set to `true` when activity passes DueDate |
| `Status` | Choice | Must include `Escalated` as a choice value (add if not present) |

And on the Programmes list (or wherever Programme Manager is stored):

| Column | Type | Notes |
|--------|------|-------|
| `Title` | Single line text | Programme name (matches `ProgrammeLabel` on Activities) |
| `ProgrammeManager` | Person | The PM responsible for this programme |

---

## Relationship to Other Flows

| Flow | Timing | Detects | Action |
|------|--------|---------|--------|
| **MonthlyReminder** (weekly, Mon 08:00) | Before due date | No report submitted | Email reminder to ActivityOwner |
| **Overdue Escalation** (daily, 07:00) | After due date | Report still not submitted | Mark overdue → escalate to PM |
| **Flows 1–4** (event-triggered) | On Status change | Status transitions | Notify relevant parties |

### Interaction Pattern
```
Monday 08:00 — MonthlyReminder: "Your report is due soon"
Due Date     — Activity passes its deadline
Day+1 07:00  — Overdue Escalation (Tier 1): "X days overdue" → Owner + Supervisor
Day+2 07:00  — Overdue Escalation (Tier 1): "X days overdue" → Owner + Supervisor
Day+3 07:00  — Overdue Escalation (Tier 1): "X days overdue" → Owner + Supervisor
Day+4 07:00  — Overdue Escalation (Tier 2): ESCALATED → Programme Manager + Supervisor
              — Activity Status = "Escalated"
              — AuditLog entry created
              — Notification row created
```

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Daily at 07:00 (not real-time) | Avoids API throttling; catches everything within 24 hours |
| 3-day grace period | Balances urgency with not spamming for 1-day delays |
| Mark `IsOverdue` before escalating | Prevents re-escalation on subsequent days (filter on `IsOverdue eq false` if needed) |
| Programme Manager lookup from Programmes list | Decoupled from Activities — one PM per programme, not per activity |
| AuditLog + Notifications alongside email | Creates a full audit trail for compliance |
| Status = "Escalated" (not just IsOverdue) | Makes it filterable in the Power App approval queue |

---

## Optional: Prevent Re-Escalation

If the flow re-runs on Day+5, it would re-escalate. To prevent this, add a filter:

```
Active eq 1 and Frequency eq 'Monthly' and DueDate lt '@{formatDateTime(utcNow(), 'yyyy-MM-dd')}' and IsOverdue ne 1
```

This only picks up activities not yet marked overdue. For the escalation tier, add:

```
... and Status ne 'Escalated'
```

This ensures each activity is only escalated once.

---

*Source: APP-MRMS Project — Phase 2 Enhancement*
*Companion to: [alerting-flow.md](alerting-flow.md) (MonthlyReminder)*
