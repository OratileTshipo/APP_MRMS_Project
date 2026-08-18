# APP-MRMS — Power Automate Flow Import Guide

**Based on verified working flow structure (AutomateITCalllogging.zip)**

---

## Overview

This guide explains the exact structure required for Power Automate flow import packages. The structure was reverse-engineered from a **verified working flow** exported directly from Power Automate.

---

## Package Structure

```
APP-MRMS-Approval.zip
├── manifest.json                          ← Root package manifest
└── Microsoft.Flow/
    └── flows/
        ├── manifest.json                  ← Flow assets list
        ├── <flow-guid-1>/
        │   ├── definition.json            ← Flow definition (the actual flow)
        │   ├── apisMap.json               ← API ID mappings
        │   └── connectionsMap.json        ← Connection ID mappings
        ├── <flow-guid-2>/
        │   ├── definition.json
        │   ├── apisMap.json
        │   └── connectionsMap.json
        └── ...
```

---

## File Formats

### 1. Root manifest.json

```json
{
  "schema": "1.0",
  "details": {
    "displayName": "APP-MRMS Approval Workflow Flows",
    "description": "Monthly report approval workflow",
    "createdTime": "2026-08-18T00:00:00.0000000Z",
    "packageTelemetryId": "<unique-guid>",
    "creator": "N/A",
    "sourceEnvironment": "APP-MRMS"
  },
  "resources": {
    "<flow-guid>": {
      "type": "Microsoft.Flow/flows",
      "suggestedCreationType": "Update",
      "creationType": "Existing, New, Update",
      "details": {
        "displayName": "Flow Display Name"
      },
      "configurableBy": "User",
      "hierarchy": "Root",
      "dependsOn": [
        "<sharepoint-api-guid>",
        "<sharepoint-connection-guid>",
        "<outlook-api-guid>",
        "<outlook-connection-guid>"
      ]
    },
    "<sharepoint-api-guid>": {
      "id": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
      "name": "shared_sharepointonline",
      "type": "Microsoft.PowerApps/apis",
      "suggestedCreationType": "Existing",
      "details": {
        "displayName": "SharePoint"
      },
      "configurableBy": "System",
      "hierarchy": "Child",
      "dependsOn": []
    },
    "<sharepoint-connection-guid>": {
      "type": "Microsoft.PowerApps/apis/connections",
      "suggestedCreationType": "Existing",
      "creationType": "Existing",
      "details": {
        "displayName": "Your SharePoint Connection"
      },
      "configurableBy": "User",
      "hierarchy": "Child",
      "dependsOn": ["<sharepoint-api-guid>"]
    },
    "<outlook-api-guid>": {
      "id": "/providers/Microsoft.PowerApps/apis/shared_office365",
      "name": "shared_office365",
      "type": "Microsoft.PowerApps/apis",
      "suggestedCreationType": "Existing",
      "details": {
        "displayName": "Office 365 Outlook"
      },
      "configurableBy": "System",
      "hierarchy": "Child",
      "dependsOn": []
    },
    "<outlook-connection-guid>": {
      "type": "Microsoft.PowerApps/apis/connections",
      "suggestedCreationType": "Existing",
      "creationType": "Existing",
      "details": {
        "displayName": "Your Outlook Connection"
      },
      "configurableBy": "User",
      "hierarchy": "Child",
      "dependsOn": ["<outlook-api-guid>"]
    }
  }
}
```

---

### 2. Flow manifest.json

```json
{
  "packageSchemaVersion": "1.0",
  "flowAssets": {
    "assetPaths": [
      "<flow-guid-1>",
      "<flow-guid-2>"
    ]
  }
}
```

---

### 3. definition.json (The Flow)

```json
{
  "name": "<flow-id>",
  "id": "/providers/Microsoft.Flow/flows/<flow-id>",
  "type": "Microsoft.Flow/flows",
  "properties": {
    "apiId": "/providers/Microsoft.PowerApps/apis/shared_logicflows",
    "displayName": "Flow Display Name",
    "definition": {
      "metadata": {
        "provisioningMethod": "FromDefinition",
        "creationSource": "Portal",
        "modifiedSources": "Portal"
      },
      "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
      "contentVersion": "1.0.0.0",
      "parameters": {
        "$authentication": {
          "defaultValue": {},
          "type": "SecureObject"
        },
        "$connections": {
          "defaultValue": {},
          "type": "Object"
        }
      },
      "triggers": {
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
              "dataset": "<site-url>",
              "table": "<list-guid>",
              "changeType": "Modified"
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
        "Condition_Status_Submitted": {
          "runAfter": {},
          "type": "If",
          "expression": {
            "and": [
              {
                "equals": [
                  "@triggerBody()?['Status/Value']",
                  "Submitted"
                ]
              }
            ]
          },
          "actions": {
            "Get_activity": {
              "runAfter": {},
              "type": "OpenApiConnection",
              "inputs": {
                "parameters": {
                  "dataset": "<site-url>",
                  "table": "<activities-list-guid>",
                  "id": "@triggerBody()?['Activity/Id']"
                },
                "host": {
                  "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
                  "connectionName": "shared_sharepointonline",
                  "operationId": "GetItem"
                },
                "authentication": "@parameters('$authentication')"
              }
            },
            "Notify_Supervisor": {
              "runAfter": {
                "Get_activity": ["Succeeded"]
              },
              "type": "OpenApiConnection",
              "inputs": {
                "parameters": {
                  "emailMessage/To": "@outputs('Get_activity')?['body/Supervisor/EMail']",
                  "emailMessage/Subject": "New monthly report awaiting your review",
                  "emailMessage/Body": "<p>Dear @{outputs('Get_activity')?['body/Supervisor/Value']},</p><p>A monthly report was submitted and awaits your review.</p>",
                  "emailMessage/Importance": "Normal"
                },
                "host": {
                  "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
                  "connectionName": "shared_office365",
                  "operationId": "SendEmailV2"
                },
                "authentication": "@parameters('$authentication')"
              }
            }
          },
          "else": {}
        }
      },
      "outputs": {}
    },
    "connectionReferences": {
      "shared_sharepointonline": {
        "connectionName": "<your-connection-id>",
        "source": "Embedded",
        "id": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
        "tier": "NotSpecified",
        "apiName": "sharepointonline"
      },
      "shared_office365": {
        "connectionName": "<your-connection-id>",
        "source": "Embedded",
        "id": "/providers/Microsoft.PowerApps/apis/shared_office365",
        "tier": "NotSpecified",
        "apiName": "office365"
      }
    }
  }
}
```

---

### 4. apisMap.json

```json
{
  "shared_sharepointonline": "<sharepoint-api-guid>",
  "shared_office365": "<outlook-api-guid>"
}
```

---

### 5. connectionsMap.json

```json
{
  "shared_sharepointonline": "<sharepoint-connection-guid>",
  "shared_office365": "<outlook-connection-guid>"
}
```

---

## Key Structure Elements

### Trigger Types

| Trigger | operationId | Use Case |
|---|---|---|
| `When_an_item_is_created` | `GetOnNewItems` | New items only |
| `When_an_item_is_modified` | `GetOnChangedItems` | Status changes |

### Action Types

| Action | operationId | Purpose |
|---|---|---|
| `Get item` | `GetItem` | Fetch single item by ID |
| `Get items` | `GetItems` | Fetch multiple items with filter |
| `Create item` | `CreateItem` | Add new row |
| `Update item` | `UpdateItem` | Modify existing row |
| `Send email` | `SendEmailV2` | Send Outlook email |

### Expression Syntax

```powerfx
// Trigger body
@triggerBody()?['ID']
@triggerBody()?['Status/Value']
@triggerBody()?['SubmittedBy/EMail']

// Get item output
@outputs('Get_item')?['body/Title']
@outputs('Get_activity')?['body/Supervisor/EMail']

// Compose expressions
@concat('Report ', triggerBody()?['ID'], ' was approved')
@if(equals(triggerBody()?['Status/Value'], 'Submitted'), 'Pending', 'Other')

// Date functions
@utcNow()
@addDays(utcNow(), 5)
@formatDateTime(utcNow(), 'yyyy-MM-dd')
```

---

## Connection References

### Required Connections

| Connection | API | Purpose |
|---|---|---|
| `shared_sharepointonline` | SharePoint Online | Read/write lists |
| `shared_office365` | Office 365 Outlook | Send emails |

### Connection GUIDs

When you import the package, Power Automate will ask you to map connections. The connection IDs in the package are placeholders - you'll select your own connections during import.

---

## Import Steps

1. Go to https://make.powerautomate.com
2. Click **My flows** → **Import** → **Package (.zip)**
3. Upload `APP-MRMS-Approval.zip`
4. For each connection:
   - **SharePoint:** Select your account (needs Contribute on the site)
   - **Office 365 Outlook:** Select your account (needs send permissions)
5. Click **Import**
6. Open each flow → **Turn on**

---

## Microsoft Best Practices Applied

### 1. One Flow Per Status Transition
- Prevents infinite loops
- Easier to debug
- Clear separation of concerns

### 2. Never Write Status from Flows
- Only Power Apps buttons set Status
- Flows only write to side tables (Notifications, AuditLog)
- Prevents re-trigger loops

### 3. Use Conditions for Status Checks
- Always check `Status/Value` before acting
- Prevents unnecessary processing
- Reduces API calls

### 4. Sequential Actions with runAfter
- Each action waits for the previous to succeed
- Prevents partial updates
- Ensures data consistency

### 5. Proper Error Handling
- Actions have `runAfter` dependencies
- Failed actions don't trigger downstream
- Audit log captures all status changes

---

## Common Import Errors

| Error | Cause | Fix |
|---|---|---|
| `Invalid connection` | Connection expired | Re-authenticate in Power Automate |
| `List not found` | Wrong GUID or site URL | Verify list GUIDs |
| `Column not found` | Column name mismatch | Check column internal names |
| `Duplicate action names` | Actions have same name | Rename actions uniquely |
| `Invalid JSON` | Malformed definition.json | Validate JSON structure |

---

## Testing After Import

1. Check each flow is **Turned on** (green toggle)
2. Create a test item in SharePoint
3. Check **Run history** for each flow
4. Verify email delivery
5. Check Notifications list for new entries
6. Check AuditLog for entries
