# Definition JSON Reference

The `definition.json` file is the core of a Power Automate flow. This reference covers the exact JSON structure needed for importable flows.

---

## Overall Structure

```json
{
  "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "$authentication": { "defaultValue": {}, "type": "SecureObject" },
    "$connections": { "defaultValue": {}, "type": "Object" }
  },
  "triggers": {
    "<TriggerName>": {
      "type": "OpenApiConnection",
      "inputs": { ... },
      "recurrence": { ... },
      "splitOn": "...",
      "metadata": { ... }
    }
  },
  "actions": {
    "<ActionName>": {
      "type": "OpenApiConnection",
      "inputs": { ... },
      "runAfter": { ... }
    }
  },
  "outputs": {}
}
```

---

## Trigger Definition (SharePoint — When Item Modified)

```json
{
  "When_an_item_is_modified": {
    "recurrence": {
      "frequency": "Minute",
      "interval": 3
    },
    "evaluatedRecurrence": {
      "frequency": "Minute",
      "interval": 3
    },
    "splitOn": "@triggerOutputs()?['body/value']",
    "metadata": {
      "operationMetadataId": "a61588e4-a5d8-4ce1-a1d3-84be04a2beaf"
    },
    "type": "OpenApiConnection",
    "inputs": {
      "parameters": {
        "dataset": "{{SITE_URL}}",
        "table": "{{MR_GUID}}"
      },
      "host": {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
        "connectionName": "shared_sharepointonline",
        "operationId": "GetOnChangedItems"
      },
      "authentication": "@parameters('$authentication')"
    }
  }
}
```

**Key points:**
- `connectionName` (not `connectionReferenceName`) for triggers
- `authentication` is required on triggers
- `splitOn` causes the flow to run once per item in the array
- `changeType` is NOT valid — do not include it

---

## Action Definition (SharePoint — Get Item)

```json
{
  "Get_activity": {
    "runAfter": {},
    "type": "OpenApiConnection",
    "inputs": {
      "parameters": {
        "dataset": "{{SITE_URL}}",
        "table": "{{ACT_GUID}}",
        "id": "@{triggerBody()?['Activity']?['Id']}"
      },
      "host": {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
        "connectionReferenceName": "shared_sharepointonline",
        "operationId": "GetItem"
      }
    }
  }
}
```

**Key points:**
- `connectionReferenceName` (not `connectionName`) for actions
- NO `authentication` on actions inside nested scopes
- `runAfter` specifies dependencies on previous actions

---

## Action Definition (SharePoint — Get Items with Filter)

```json
{
  "Get_items": {
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

## Action Definition (SharePoint — Create Item)

```json
{
  "Create_Notification": {
    "runAfter": {
      "PreviousAction": ["Succeeded"]
    },
    "type": "OpenApiConnection",
    "inputs": {
      "parameters": {
        "dataset": "{{SITE_URL}}",
        "table": "{{NOTIF_GUID}}",
        "Title": "Report @{triggerBody()?['Title']} submitted",
        "Message": "Your report has been submitted for review",
        "RecipientEmail": "@{triggerBody()?['SubmittedBy']?['Email']}",
        "IsRead": false
      },
      "host": {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
        "connectionReferenceName": "shared_sharepointonline",
        "operationId": "CreateItem"
      }
    }
  }
}
```

---

## Action Definition (Office 365 Outlook — Send Email)

```json
{
  "Send_Email_Supervisor": {
    "runAfter": {
      "Get_activity": ["Succeeded"]
    },
    "type": "OpenApiConnection",
    "inputs": {
      "parameters": {
        "emailMessage/To": "@{body('Get_activity')?['Supervisor']?['Email']}",
        "emailMessage/Subject": "Report submitted: @{triggerBody()?['Title']} — @{triggerBody()?['ReportingMonth']?['Value']}",
        "emailMessage/Body": "<p><strong>A monthly report has been submitted.</strong></p>",
        "emailMessage/Importance": "High"
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

## Condition Definition

```json
{
  "Condition_Status_Rejected": {
    "runAfter": {},
    "type": "If",
    "expression": {
      "or": [
        {
          "equals": [
            "@triggerBody()?['Status/Value']",
            "Supervisor Rejected"
          ]
        },
        {
          "equals": [
            "@triggerBody()?['Status/Value']",
            "M&E Rejected"
          ]
        }
      ]
    },
    "actions": {
      "Send_Rejection_Email": {
        "runAfter": {},
        "type": "OpenApiConnection",
        "inputs": { ... }
      }
    },
    "else": {
      "actions": {
        "Send_Approval_Email": {
          "runAfter": {},
          "type": "OpenApiConnection",
          "inputs": { ... }
        }
      }
    }
  }
}
```

**Key points:**
- `expression` defines the condition logic
- `actions` is the "If yes" branch
- `else.actions` is the "If no" branch
- All actions inside must have unique names across both branches

---

## Apply to Each Definition

```json
{
  "Apply_to_each_activity": {
    "runAfter": {
      "Get_items": ["Succeeded"]
    },
    "type": "Foreach",
    "foreach": "@body('Get_items')?['value']",
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
          "Send_Reminder": {
            "runAfter": {},
            "type": "OpenApiConnection",
            "inputs": { ... }
          }
        }
      }
    }
  }
}
```

---

## runAfter Patterns

```json
// Run after previous action succeeds (default)
"runAfter": { "PreviousAction": ["Succeeded"] }

// Run after any of multiple actions
"runAfter": {
  "Action1": ["Succeeded"],
  "Action2": ["Succeeded"]
}

// Run regardless of previous action result
"runAfter": {}

// Run even if previous action failed
"runAfter": { "PreviousAction": ["Succeeded", "Failed"] }
```

---

## Complete Flow Skeleton

```json
{
  "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "$authentication": { "defaultValue": {}, "type": "SecureObject" },
    "$connections": { "defaultValue": {}, "type": "Object" }
  },
  "triggers": {
    "When_an_item_is_modified": {
      "recurrence": { "frequency": "Minute", "interval": 3 },
      "evaluatedRecurrence": { "frequency": "Minute", "interval": 3 },
      "splitOn": "@triggerOutputs()?['body/value']",
      "type": "OpenApiConnection",
      "inputs": {
        "parameters": {
          "dataset": "{{SITE_URL}}",
          "table": "{{LIST_GUID}}"
        },
        "host": {
          "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
          "connectionName": "shared_sharepointonline",
          "operationId": "GetOnChangedItems"
        },
        "authentication": "@parameters('$authentication')"
      }
    }
  },
  "actions": {
    "Condition_Check_Status": {
      "runAfter": {},
      "type": "If",
      "expression": {
        "and": [
          { "equals": ["@triggerBody()?['Status/Value']", "TARGET_VALUE"] }
        ]
      },
      "actions": {
        "Get_Related_Item": {
          "runAfter": {},
          "type": "OpenApiConnection",
          "inputs": {
            "parameters": {
              "dataset": "{{SITE_URL}}",
              "table": "{{RELATED_LIST_GUID}}",
              "id": "@{triggerBody()?['LookupField']?['Id']}"
            },
            "host": {
              "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
              "connectionReferenceName": "shared_sharepointonline",
              "operationId": "GetItem"
            }
          }
        },
        "Send_Notification_Email": {
          "runAfter": { "Get_Related_Item": ["Succeeded"] },
          "type": "OpenApiConnection",
          "inputs": {
            "parameters": {
              "emailMessage/To": "@{body('Get_Related_Item')?['PersonField']?['Email']}",
              "emailMessage/Subject": "Notification: @{triggerBody()?['Title']}",
              "emailMessage/Body": "<p>Your report has been processed.</p>",
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
  },
  "outputs": {}
}
```

---

## Validation Rules Summary

| Location | Property | Rule |
|----------|----------|------|
| Trigger inputs | `authentication` | **Required** |
| Action inputs | `authentication` | **Forbidden** (only triggers and top-level actions) |
| Action host | `connectionReferenceName` | **Required** |
| Trigger host | `connectionName` | **Required** |
| Trigger params | `changeType` | **Not valid** for `GetOnChangedItems` |
| Action names | global scope | Must be **unique** across entire definition |
| Flow GUID | name, id, folder | Must **match** |

---

*Source: Microsoft Learn Power Automate — Logic Apps workflow definition schema*
