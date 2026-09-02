# Flow Import/Export — Package Format and Validation

How Power Automate import/export works, the package format, validation rules, and how to fix import errors.

---

## Exporting a Flow

### From the Portal
1. Open **My flows** → Select a flow
2. Click **Export** → **Package (.zip)**
3. Select **Save as new** (for a fresh package)
4. Download the `.zip` file

### Package Contents
A typical export package contains:
```
manifest.json                    # Root manifest (lists resources)
Microsoft.Flow/
  flows/
    manifest.json                # Flow asset paths
    <flow-guid>/
      definition.json            # The flow definition (triggers, actions, expressions)
      apisMap.json               # API/connector mappings
      connectionsMap.json        # Connection reference mappings
      workflow.json              # Workflow metadata
```

---

## Importing a Flow

### Via the Portal
1. Go to **https://make.powerautomate.com**
2. Click **My flows** → **Import**
3. Select **Package (.zip)**
4. Upload the `.zip` file
5. **Review package content:**
   - For each connection: create or select an existing connection
   - For each flow: choose **Update** (if exists) or **New**
6. Click **Import**
7. After import: open each flow → **Turn on**

### Import Validation
On import, each flow's `definition.json` is validated by the Logic Apps workflow validator. Errors are reported **one at a time** — fix, rebuild, re-import.

---

## APP-MRMS Package Structure

```
APP-MRMS-Approval.zip
├── manifest.json
└── Microsoft.Flow/
    └── flows/
        ├── manifest.json
        ├── <Flow1-GUID>/
        │   ├── definition.json
        │   ├── apisMap.json
        │   └── connectionsMap.json
        ├── <Flow2-GUID>/
        │   ├── definition.json
        │   ├── apisMap.json
        │   └── connectionsMap.json
        ├── <Flow3-GUID>/
        │   ├── definition.json
        │   ├── apisMap.json
        │   └── connectionsMap.json
        └── <Flow4-GUID>/
            ├── definition.json
            ├── apisMap.json
            └── connectionsMap.json
```

---

## Rebuilding the Package

The `tools/build_flow_zips.py` script rebuilds the package with real values:

```bash
python3 tools/build_flow_zips.py \
    --site-url "https://yourorg.sharepoint.com/sites/APP-MRMS" \
    --monthlyreports "<MonthlyReports list GUID>" \
    --activities "<Activities list GUID>" \
    --notifications "<Notifications list GUID>" \
    --auditlog "<AuditLog list GUID>" \
    --users "<APP_Users list GUID>" \
    --output flows/APP-MRMS-Approval.zip
```

### Finding List GUIDs
1. Open the list in SharePoint
2. Go to **List Settings**
3. Look at the browser URL: `.../Lists/AllItems.aspx?List=%7B<GUID>%7D`
4. Or use PnP PowerShell:
   ```powershell
   Connect-PnPOnline -Url <site> -Interactive
   Get-PnPList -Identity 'MonthlyReports' | Select Id
   ```

### Template Placeholders
The templates use `{{TOKEN}}` placeholders:
- `{{SITE_URL}}` — SharePoint site URL
- `{{MR_GUID}}` — MonthlyReports list GUID
- `{{ACT_GUID}}` — Activities list GUID
- `{{NOTIF_GUID}}` — Notifications list GUID
- `{{AUDIT_GUID}}` — AuditLog list GUID
- `{{USERS_GUID}}` — APP_Users list GUID

---

## Validation Rules (from Import Errors)

These rules were discovered during APP-MRMS import validation. See [../flow_import_validation_findings.md](../flow_import_validation_findings.md) for the full details.

### Rule 1: No `authentication` on nested actions
```json
// ❌ WRONG — actions inside Condition/Scope must NOT have authentication
{
  "type": "OpenApiConnection",
  "inputs": {
    "authentication": "@parameters('$authentication')",  // FORBIDDEN
    "host": { "connectionReferenceName": "shared_sharepointonline" }
  }
}

// ✅ CORRECT — only triggers and top-level actions have authentication
{
  "type": "OpenApiConnection",
  "inputs": {
    "host": { "connectionReferenceName": "shared_sharepointonline" }
  }
}
```

### Rule 2: Actions use `connectionReferenceName`, triggers use `connectionName`
```json
// Trigger (correct)
{
  "host": {
    "connectionName": "shared_sharepointonline",  // ✅ For triggers
    "operationId": "GetOnChangedItems"
  }
}

// Action (correct)
{
  "host": {
    "connectionReferenceName": "shared_sharepointonline",  // ✅ For actions
    "operationId": "GetItem"
  }
}
```

### Rule 3: No `changeType` on `GetOnChangedItems` trigger
```json
// ❌ WRONG — changeType is not a valid parameter
{
  "parameters": {
    "dataset": "...",
    "table": "...",
    "changeType": "Modified"  // INVALID
  }
}

// ✅ CORRECT
{
  "parameters": {
    "dataset": "...",
    "table": "..."
  }
}
```

### Rule 4: Action names must be globally unique
Action names must be unique across the **entire** flow definition, including across nested scopes (Condition branches, Switch cases).

```json
// ❌ WRONG — duplicate names across branches
{
  "Condition": {
    "actions": {
      "Create_Notification": { ... }  // Name used in 'if yes'
    },
    "else": {
      "actions": {
        "Create_Notification": { ... }  // DUPLICATE!
      }
    }
  }
}

// ✅ CORRECT — unique names
{
  "Condition": {
    "actions": {
      "Create_Notification_Approved": { ... }
    },
    "else": {
      "actions": {
        "Create_Notification_Rejected": { ... }
      }
    }
  }
}
```

---

## Common Import Errors and Fixes

| Error Code | Meaning | Fix |
|------------|---------|-----|
| `WorkflowRunActionInputsInvalidProperty` | `authentication` on nested action | Remove `authentication` from actions inside Condition/Scope |
| `WorkflowRunActionInputsMissingProperty` | Missing `host.connectionReferenceName` | Add `connectionReferenceName` to action host config |
| `InvalidTemplate` | Expression syntax error | Check expression syntax, parentheses, quotes |
| `DuplicateActionName` | Same action name used twice | Rename duplicate actions to be unique |
| `InvalidConnection` | Connection expired or missing | Re-authenticate or create new connection |
| `FlowCheckerError` | Required field empty | Fill in all required fields |

---

## Connection References

### Root manifest.json Connections
```json
{
  "resources": {
    "shared_sharepointonline": {
      "displayName": "SharePoint",
      "iconUri": "...",
      "brandColor": "#00706a",
      "allowedUserAssignment": "all"
    },
    "shared_office365": {
      "displayName": "Office 365 Outlook",
      "iconUri": "...",
      "brandColor": "#0070c0",
      "allowedUserAssignment": "all"
    }
  }
}
```

### Flow apisMap.json
```json
{
  "shared_sharepointonline": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
}
```

### Flow connectionsMap.json
```json
{
  "shared_sharepointonline": "shared_sharepointonline"
}
```

---

## After Import

1. **Verify connections:** Go to each flow → check connections are valid (green checkmarks)
2. **Turn on:** Each flow must be turned on individually
3. **Test:** Trigger a test event in SharePoint and verify the flow runs
4. **Monitor:** Check run history for the first few runs
5. **Update if needed:** Edit flows to adjust trigger conditions, email templates, etc.

---

*Source: Microsoft Learn Power Automate — Import/export flows documentation*
