# Research: Power Automate Flow Import/Export Methods

## Objective
Create a production-ready Power Automate flow package that can be downloaded and imported without errors.

## Methods for Creating Importable Flow Packages

### Method 1: Export from Power Automate Portal (Recommended)
**Process:**
1. Go to https://make.powerautomate.com
2. Navigate to "My flows" → Select the flow
3. Click "..." → Export → Package as ZIP
4. Download the `.zip` file containing:
   - `definition.json` - Flow definition
   - `connections.json` - Connection references
   - `parameters.json` - Flow parameters
   - `workflow.json` - Workflow metadata

**Advantages:**
- Guaranteed compatibility with Power Automate
- Includes all metadata and connection references
- Microsoft-supported method
- Preserves flow version history

**Considerations:**
- Requires existing flow in the environment
- Connections must be re-mapped on import

---

### Method 2: ARM Template Export (Enterprise ALM)
**Process:**
1. Use PowerShell: `Export-AzLogicApp` or Azure CLI
2. Generates ARM template JSON
3. Deploy via Azure DevOps pipelines or manual ARM deployment

**File Structure:**
```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "resources": [
    {
      "type": "Microsoft.Logic/workflows",
      "name": "[parameters('flowName')]",
      "properties": {
        "definition": { ... },
        "parameters": { ... }
      }
    }
  ]
}
```

**Advantages:**
- Infrastructure-as-Code approach
- Version control friendly
- Supports CI/CD pipelines
- Environment-specific parameterization

**Considerations:**
- Requires Azure subscription
- More complex setup
- Overkill for single-flow deployments

---

### Method 3: Manual JSON Construction (Not Recommended)
**Process:**
- Manually write `definition.json` following Power Automate schema
- Create `connections.json` with proper connection references
- Package into ZIP

**Risks:**
- High error rate due to schema complexity
- Missing internal IDs and metadata
- Connection reference mismatches
- Not officially supported by Microsoft

**Verdict:** ❌ Avoid for production use

---

### Method 4: Power Platform CLI (pac CLI)
**Process:**
```bash
# Export flow
pac flow export --id <flow-id> --path ./exported-flow

# Import flow
pac flow import --path ./exported-flow --environment <env-id>
```

**File Structure Generated:**
```
/exported-flow
  ├── definition.json
  ├── connections.json
  ├── parameters.json
  └── manifest.json
```

**Advantages:**
- Official Microsoft tooling
- Scriptable and automatable
- Integrates with source control
- Part of Power Platform Build Tools

**Considerations:**
- Requires pac CLI installation
- Still needs an existing flow to export from

---

## Best Practice Recommendation for APP-MRMS Project

### Hybrid Approach: Template + Documentation

Since we cannot create flows directly in this repository, the optimal approach is:

1. **Create Flow Definition Templates** (`.json` files)
   - Document the complete flow structure
   - Include all triggers, actions, and expressions
   - Specify required connections and permissions

2. **Create Import Package Structure**
   ```
   /flows
     /approval-workflow
       ├── definition.json.template
       ├── connections.json.template
       ├── README.md (import instructions)
       └── screenshots/ (reference images)
   ```

3. **Provide Step-by-Step Build Guide**
   - Detailed instructions to recreate flow in Power Automate
   - Screenshot annotations
   - Expression copy-paste blocks
   - Connection requirements checklist

4. **Post-Creation Export**
   - Once built manually, export as ZIP using Method 1
   - Store the ZIP in repository for future imports
   - Document connection re-mapping steps

---

## Critical Success Factors for Error-Free Import

### 1. Connection References
- All SharePoint connections must reference valid SharePoint connectors
- Office 365 Outlook connections for email notifications
- Ensure connection names match target environment

### 2. Environment Variables
- Use environment variables for:
  - SharePoint site URLs
  - List names
  - Email distribution lists
  - User role mappings

### 3. Expression Validation
- Test all Power Fx expressions before packaging
- Verify function availability in target environment
- Check for deprecated functions

### 4. Permissions Prerequisites
Document required permissions:
- SharePoint: Edit rights to MonthlyReports, ReportComments, Notifications, AuditLog
- Office 365: Send email as service account
- Approvals: Permission to create approval requests

### 5. Dependency Documentation
List all dependencies:
- Required SharePoint lists and columns
- Required Entra ID security groups
- Required email distribution lists
- Required Power BI datasets (if applicable)

---

## File Format Specifications

### definition.json Structure
```json
{
  "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "$connections": {
      "defaultValue": {},
      "type": "Object"
    }
  },
  "triggers": {
    "When_an_item_is_created_or_modified": {
      "type": "ApiConnectionWebhook",
      "inputs": {
        "host": {
          "connectionName": "shared_sharepointonline",
          "operationId": "OnUpdatedItem",
          "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
        },
        "parameters": {
          "site": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline/environments/@{encodeURIComponent('environment-id')}/sites/@{encodeURIComponent('site-id')}",
          "list": "@{encodeURIComponent('list-id')}"
        },
        "body": {
          "notificationUrl": "@{listCallbackUrl()}"
        }
      }
    }
  },
  "actions": { ... },
  "outputs": {}
}
```

### connections.json Structure
```json
{
  "shared_sharepointonline": {
    "connection": {
      "id": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline/connections/shared-sharepointonline-1"
    },
    "connectionName": "shared-sharepointonline-1",
    "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
  },
  "shared_office365": {
    "connection": {
      "id": "/providers/Microsoft.PowerApps/apis/shared_office365/connections/shared-office365-1"
    },
    "connectionName": "shared-office365-1",
    "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365"
  }
}
```

---

## Verification Checklist Before Import

- [ ] All connection references are valid
- [ ] No hardcoded environment-specific IDs
- [ ] All required parameters are defined
- [ ] Flow logic handles null/empty values
- [ ] Error handling scopes are configured
- [ ] Concurrency settings are appropriate
- [ ] Timeout values are set for long-running actions
- [ ] Run-after configurations are correct for conditional branches
- [ ] All dynamic content references are valid
- [ ] Flow name doesn't conflict with existing flows

---

## Conclusion

For the APP-MRMS project, the recommended approach is:

1. **Document the complete flow design** in markdown with all expressions and configurations
2. **Build flows manually** in Power Automate using the documentation
3. **Export as ZIP packages** once validated
4. **Store ZIP files in repository** for future ALM
5. **Maintain connection mapping documentation** for environment transfers

This ensures production-ready flows with minimal import errors while maintaining flexibility for environment-specific configurations.

---

# Power Automate Flow Packaging & Re-Import — Technical Research (APP-MRMS)

**Scope**: How to export, unpack, modify and re-import Power Automate cloud flows as `.zip` packages, applied to the APP-MRMS Monthly Reporting Management System. Based on the shipped example package `AutomateITCalllogging_20260818132403.zip`, the MRMS SharePoint list schemas (verified from `MonthlyReports.csv`, `Activities.csv`, `APP_Users.csv`), and the architecture docs (`APP_MRMS_Architecture_Pack.docx`, `APPMRMS_Phase1_ExecutionGuide.docx`, `APP-MRMS_BRD_FDS_TDS_v2.docx`).

---

## 1. How Power Automate flow packages are structured

A Power Automate flow export is a plain ZIP with a fixed layout. The shipped example `AutomateITCalllogging_20260818132403.zip` contains exactly this structure:

```
AutomateITCalllogging_<timestamp>.zip
├── manifest.json                                      # ROOT package manifest (schema 1.0)
└── Microsoft.Flow/
    ├── flows/
    │   ├── manifest.json                              # packageSchemaVersion + assetPaths
    │   └── 33685bad-4ac9-4068-95b1-dfaa812a4b95/      # ONE folder per flow GUID
    │       ├── definition.json                        # the Logic-App-style workflow definition
    │       ├── apisMap.json                           # logical connection name -> API GUID
    │       └── connectionsMap.json                    # logical connection name -> connection GUID
```

### 1.1 Root `manifest.json`

```json
{
  "schema": "1.0",
  "details": {
    "displayName": "Automate IT Call logging",
    "description": "",
    "createdTime": "2026-08-18T13:24:03.1446041Z",
    "packageTelemetryId": "db7ce543-5541-450f-ad92-eed7e70622b3",
    "creator": "N/A",
    "sourceEnvironment": "nnw"
  },
  "resources": {
    "33685bad-4ac9-4068-95b1-dfaa812a4b95": {
      "type": "Microsoft.Flow/flows",
      "suggestedCreationType": "Update",
      "creationType": "Existing, New, Update",
      "details": { "displayName": "Automate IT Call logging" },
      "configurableBy": "User",
      "hierarchy": "Root",
      "dependsOn": [
        "a7f9c889-a35f-4e9e-9f58-87c39fd6ae9c",
        "59fc2557-16b1-45d9-9606-369d53b38eee",
        "6f35e80e-b2c3-49c9-a7e8-a8d6677bfcb3",
        "1cbb6259-2021-44cc-a05a-4e59aa6e9ca3"
      ]
    },
    "a7f9c889-a35f-4e9e-9f58-87c39fd6ae9c": {
      "id": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
      "name": "shared_sharepointonline",
      "type": "Microsoft.PowerApps/apis",
      "suggestedCreationType": "Existing",
      "details": { "displayName": "SharePoint", "iconUri": "..." },
      "configurableBy": "System",
      "hierarchy": "Child",
      "dependsOn": []
    },
    "59fc2557-16b1-45d9-9606-369d53b38eee": {
      "type": "Microsoft.PowerApps/apis/connections",
      "suggestedCreationType": "Existing",
      "creationType": "Existing",
      "details": { "displayName": "OTshipo@nwpg.gov.za", "iconUri": "..." },
      "configurableBy": "User",
      "hierarchy": "Child",
      "dependsOn": ["a7f9c889-a35f-4e9e-9f58-87c39fd6ae9c"]
    }
  }
}
```

Key fields to understand before editing:

| Field | Meaning | Edit-safe? |
|---|---|---|
| `details.displayName` | Flow name shown in the portal | Yes — this becomes the imported flow's name |
| `details.sourceEnvironment` | Where it was exported from | No — informational only, cosmetic |
| `packageTelemetryId` | Telemetry GUID | No — leave as-is |
| `resources` | Resource dependency graph. Each connection/API has a GUID, `type` (`Microsoft.PowerApps/apis/connections`, `Microsoft.PowerApps/apis`), `hierarchy` (`Root`/`Child`), and `dependsOn` edges | Do NOT renumber GUIDs unless you also rewrite every reference below (see §7.1) |
| `configurableBy` | Who can supply the value on import (`User` = prompted on import; `System` = auto) | Prefer keeping connectors `System` and connections `User` |
| `suggestedCreationType` / `creationType` | How the import treats the resource (`Existing`, `New`, `Update`) | Leave — controls re-import behaviour |

### 1.2 `Microsoft.Flow/flows/manifest.json`

```json
{ "packageSchemaVersion": "1.0", "flowAssets": { "assetPaths": ["33685bad-4ac9-4068-95b1-dfaa812a4b95"] } }
```

Each flow folder listed in `flowAssets.assetPaths` must exist under `Microsoft.Flow/flows/`. Add your new flow here when packing multiple flows.

### 1.3 `apisMap.json` and `connectionsMap.json` (inside the flow folder)

These are the two "glue" files that connect the workflow definition to the resource graph in the root manifest.

```json
// apisMap.json — logical connector name used in definition.json -> API GUID in root manifest
{ "shared_sharepointonline": "a7f9c889-a35f-4e9e-9f58-87c39fd6ae9c",
  "shared_office365":          "6f35e80e-b2c3-49c9-a7e8-a8d6677bfcb3" }

// connectionsMap.json — logical connector name -> connection GUID in root manifest
{ "shared_sharepointonline": "59fc2557-16b1-45d9-9606-369d53b38eee",
  "shared_office365":          "1cbb6259-2021-44cc-a05a-4e59aa6e9ca3" }
```

Rule: the **keys** of both maps are the `host.connectionName` values inside each action/trigger of `definition.json`. The **values** are GUIDs that must also exist in root `manifest.json.resources`. If you add a new connector (e.g. `shared_approvals`), you must create entries in all three files AND the root manifest.

---

## 2. The workflow `definition.json` — schema requirements

The flow definition uses the **Azure Logic Apps Workflow Definition schema `2016-06-01`**, identical to what Power Automate renders:

```json
{
  "name": "7ed472e4-91c6-44d7-b42a-ec217df0305b",
  "id": "/providers/Microsoft.Flow/flows/7ed472e4-91c6-44d7-b42a-ec217df0305b",
  "type": "Microsoft.Flow/flows",
  "properties": {
    "apiId": "/providers/Microsoft.PowerApps/apis/shared_logicflows",
    "displayName": "Automate IT Call logging",
    "definition": {
      "metadata": { ... },               // creator, provisioningMethod, timestamps, etc.
      "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
      "contentVersion": "1.0.0.0",
      "parameters": {
        "$authentication": { "defaultValue": {}, "type": "SecureObject" },
        "$connections":    { "defaultValue": {}, "type": "Object" }
      },
      "triggers": { ... },
      "actions": { ... },
      "outputs": {}
    }
  }
}
```

### 2.1 The two mandatory parameters

Every exported flow has these two `parameters` — **never remove them**:

```json
"parameters": {
  "$authentication": { "defaultValue": {}, "type": "SecureObject" },
  "$connections":    { "defaultValue": {}, "type": "Object" }
}
```

- `$connections` is populated **at import time** by the resource-graph in root `manifest.json` (the `connectionsMap`). You never hardcode connection details here.
- `$authentication` is resolved at runtime from the connection you selected on import.

### 2.2 Trigger schema (SharePoint "When an item is created")

```json
"triggers": {
  "When_an_item_is_created": {
    "recurrence": { "frequency": "Minute", "interval": 5 },
    "evaluatedRecurrence": { "frequency": "Minute", "interval": 5 },
    "splitOn": "@triggerOutputs()?['body/value']",
    "metadata": { "operationMetadataId": "a61588e4-a5d8-4ce1-a1d3-84be04a2beaf" },
    "type": "OpenApiConnection",
    "inputs": {
      "parameters": {
        "dataset": "https://nwpg.sharepoint.com/sites/ITSupportteam",
        "table": "625ed6d4-2fe8-4da4-987a-06e5bd1783a2"
      },
      "host": {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
        "connectionName": "shared_sharepointonline",
        "operationId": "GetOnNewItems"
      },
      "authentication": "@parameters('$authentication')"
    }
  }
}
```

Points that matter for **re-import into another environment**:

| Element | Environment-specific? | Handling |
|---|---|---|
| `inputs.parameters.dataset` | YES — the site URL (`https://<tenant>.sharepoint.com/sites/<site>`) | You MUST edit this before importing to a different site, or the flow fails with "dataset not found" / wrong site |
| `inputs.parameters.table` | YES — the SharePoint list **internal GUID** (`625ed6d4-...`) | Not the list display name. Obtain the GUID: site → list settings → URL query string `?List=%7BGUID%7D`, or via PnP `Get-PnPList -Identity 'MonthlyReports'` |
| `host.connectionName` | NO — logical name, stays `shared_sharepointonline` | Must match `apisMap.json` / `connectionsMap.json` keys |
| `host.apiId` | NO | Generic connector path |
| `metadata.operationMetadataId` | NO | Do not change — it is the connector operation identity |
| `recurrence` | NO | Flow scheduling |
| `splitOn` | NO | Batch mode for "When an item is created" — leave intact |

### 2.3 Action schema (two connector types used in MRMS)

**SharePoint "Get item"** (uses the SharePoint connection):

```json
"Get_item": {
  "runAfter": {},
  "type": "OpenApiConnection",
  "inputs": {
    "parameters": {
      "dataset": "https://nwpg.sharepoint.com/sites/APP-MRMS",
      "table": "<MonthlyReports-GUID>",
      "id": "@triggerBody()?['ID']"
    },
    "host": {
      "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
      "connectionName": "shared_sharepointonline",
      "operationId": "GetItem"
    },
    "authentication": "@parameters('$authentication')"
  }
}
```

**Office 365 Outlook "Send email (V2)"** (uses the Outlook connection):

```json
"Send_an_email_to_user": {
  "runAfter": { "Get_item": ["Succeeded"] },
  "type": "OpenApiConnection",
  "inputs": {
    "parameters": {
      "emailMessage/To": "@triggerBody()?['EmailUser/Value']",
      "emailMessage/Subject": "DPWR IT Helpdesk",
      "emailMessage/Body": "<p>...</p>",
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
```

Action schema rules:

1. **`runAfter`** is the entire sequencing model. `"runAfter": {}` means "run first". An action runs only after the listed actions reach the listed statuses (`Succeeded`, `Failed`, `TimedOut`, `Skipped`). To make B run after A regardless of outcome: `"runAfter": { "A": ["Succeeded","Failed","TimedOut"] }`. This is how you build the Try/Catch/Finally pattern from `APP_MRMS_Architecture_Pack.docx` §10.1.
2. **`type`** is `OpenApiConnection` for standard connectors. Other types used in flow packages: `If` (Condition), `Switch`, `Foreach`, `Scope`, `Http`, `Request`, `Response`, `Compose`, `InitializeVariable`, `SetVariable`, `AppendToStringArrayVariable`, `Terminate`, `Wait`. Each has its own `inputs` shape.
3. **`authentication": "@parameters('$authentication')"`** is mandatory on every connector action. Without it the import fails validation.
4. Expression references use the Logic Apps syntax: `@triggerBody()?['ColumnInternalName']`, `@outputs('ActionName')?['body/...']`, `@parameters('$connections')` for connection lookups.
5. **SharePoint internal column names**: use `EmailUser/Value` (user field value), `ID` (item id), `Status/Value` (choice value). The `/Value` suffix is how Power Automate returns Choice and Person fields — do NOT strip it in expressions.

### 2.4 Condition (If) action schema

```json
"Condition": {
  "runAfter": { "Get_item": ["Succeeded"] },
  "type": "If",
  "expression": {
    "and": [
      { "equals": [ "@triggerBody()?['Status/Value']", "Submitted" ] }
    ]
  },
  "actions": { "then_true": { "type": "Compose", "inputs": "route to supervisor" } },
  "else": { "else_false": { "type": "Compose", "inputs": "no-op" } },
  "runAfter": {}
}
```

`expression` uses the Logic Apps condition operators (`equals`, `not`, `and`, `or`, `greater`, `less`, ...). Nested `actions`/`else` blocks are inlined in the JSON (no separate files).

---

## 3. Step-by-step: export, modify, re-import

### 3.1 Export (Power Automate portal)

1. Power Automate → **My flows** → select the flow → **Save a copy** (optional safety copy).
2. Open the flow → `...` (more commands) → **Export** → **Package (.zip)**.
3. Choose whether to include connections (recommended: include so the resource graph is complete).
4. Download the `.zip`. It is the package described in §1.

Alternative: `pac solution export` from **Power Platform CLI** when the flow is in a **solution** (see §8). For a bare flow (not in a solution), the portal Export → Package is what produces the folder layout above.

### 3.2 Unpack & inspect

```bash
unzip -o AutomateITCalllogging_*.zip -d ./flowpkg
# read the four files described in §1.1–§1.3
```

### 3.3 Modify (what you can safely edit by hand)

| Edit | Location | Notes |
|---|---|---|
| Flow name | root `manifest.json` → `details.displayName` | Also update `resources.<flowGUID>.details.displayName` |
| Site URL | every `inputs.parameters.dataset` in `definition.json` | Required for environment moves |
| List GUID | every `inputs.parameters.table` | Required for environment moves |
| Actions / triggers / conditions | `definition.json` → `triggers`/`actions` | Keep `runAfter` graph consistent, keep `authentication` on every connector action |
| Email recipients / subject / body | `emailMessage/*` parameters | Power Automate expression syntax: `@triggerBody()?['...']` |
| New connector | root `manifest.json` + `apisMap.json` + `connectionsMap.json` | Add resource GUIDs + maps entries + actions |
| Recurrence | trigger `recurrence` | e.g. `"frequency": "Day", "interval": 1` |

### 3.4 Re-zip (manifest first, preserved relative paths)

The package relies on exact relative paths and the manifest schema version. Re-zip with the original folder structure, `manifest.json` first in the archive:

```bash
cd flowpkg
zip -X ../APP-MRMS_<flow-name>.zip manifest.json Microsoft.Flow/flows/manifest.json \
  Microsoft.Flow/flows/<flowGUID>/definition.json \
  Microsoft.Flow/flows/<flowGUID>/apisMap.json \
  Microsoft.Flow/flows/<flowGUID>/connectionsMap.json
```

### 3.5 Re-import (Power Automate portal)

1. **Import** → **Package (.zip)** → choose the zip → **Upload**.
2. **Review package content**: every connection (`configurableBy: User`) is presented for you to pick/create the connection for the target environment. This is where you bind `shared_sharepointonline` and `shared_office365` to the new site / mailbox owner.
3. Choose **Update** if the flow already exists (uses the `suggestedCreationType: Update` in the manifest), or **New** for a fresh copy.
4. After import, open the flow and **turn it on**. Connections chosen at import are stored in `$connections`.

---

## 4. Adding Power Apps components / UI triggers to a flow package

There is no mechanism to embed a Power Apps control inside a `.zip` flow package — Power Apps and Power Automate stay separate artifacts that talk at **runtime**. What the research prompt calls "adding external Power Apps components" is done in one of three supported ways:

### 4.1 Power Apps → Flow via the "Power Automate" connector (for buttons/actions in the app)

The app calls a flow with `Run(<flowName>.Run(id, ...))`. The flow gets a **`Request` trigger** instead of a SharePoint trigger:

```json
"triggers": {
  "manual": {
    "kind": "Button",
    "inputs": {
      "schema": {
        "type": "object",
        "properties": {
          "ReportID": { "type": "integer", "title": "ReportID" },
          "Decision": { "type": "string", "title": "Decision", "enum": ["Approved", "Rejected"] },
          "Reason":  { "type": "string", "title": "Reason" }
        },
        "required": [ "ReportID", "Decision" ]
      }
    },
    "type": "Request"
  }
}
```

The MRMS docs (`APP-MRMS_BRD_FDS_TDS_v2.docx` §3.3) explicitly choose this pattern: *"Power Apps → Power Automate: UI actions (Submit, Approve, Reject) call flows directly via the Power Automate connector for actions that must guarantee server-side notification/audit logging."* So the Approve/Reject buttons in `scr_ApprovalQueue` call a flow whose trigger is `Request` (Button kind), receiving the report ID, decision, and rejection reason, while the flow does the email + `Notifications` + `AuditLog` writes. The app-side call is then:

```powerfx
'APP-MRMS Approve/Reject Report'.Run(ThisItem.ID, "Approved", "");
```

### 4.2 Flow → Power Apps via `PowerAppsButton` / Flow action in the app canvas

Not relevant for MRMS; listed for completeness. A flow can have a **"Power Apps or Power Automate"** action (`SendAndContinue`, i.e. a `Function` action with `operationId: PowerAppV2`). Avoid — it blocks the flow on the app.

### 4.3 Solution packaging (the ALM-correct way to bundle app + flows)

When the Canvas App and the flows must travel together, package them as a **Power Platform Solution** (`.zip`), not a raw flow export:

```
SolutionName_<guid>.zip
├── [Content_Types].xml
├── Solution.xml                       # components list: App, flows, environment variables
├── AppDefinition/                     # canvas app package (.msapp) embedded
├── Workflows/                         # each flow as its own .json + relationships
├── Other/Customizations.xml
├── Connections/                       # connection references (NOT the connections themselves)
└── EnvironmentVariables/              # value placeholders for site URL, list GUIDs, etc.
```

This matches the MRMS deployment strategy (`APP_MRMS_Architecture_Pack.docx` §14.1): *"All components (Canvas App, flows, environment variables, connection references) are packaged as a single Power Platform Solution, developed as Unmanaged in Development; SharePoint site URL and key list GUIDs are abstracted as Environment Variables / Connection References so the same managed solution can be imported into Test and Production without manual rewiring."*

**Recommendation for MRMS**: use **Environment Variables** inside the solution for:
- `MRMS_SiteUrl` (e.g. `https://<tenant>.sharepoint.com/sites/APP-MRMS`)
- `MRMS_MonthlyReports_ListGUID`
- `MRMS_Activities_ListGUID`
- `MRMS_DeputyDirectorME_Email`

and reference them in each flow action via `@parameters('<envVarName>')` (which Power Automate resolves at runtime). Then the same flow package imports to Dev/Test/Prod with zero JSON editing — the import only asks for the environment-variable values.

---

## 5. Environment-specific configuration best practices

1. **Never hardcode site URLs or list GUIDs in action parameters.** Use Environment Variables (solution) or, for a bare flow zip, document that `dataset`/`table` must be edited per environment (see §3.3).
2. **Connection references over connections**: in a solution, define one connection reference per connector and bind it to the target environment's connection at import. The raw-flow zip instead embeds a `connectionsMap` per environment — export a fresh zip per environment rather than reusing one.
3. **Keep `configurableBy` correct**: APIs stay `System`, connections stay `User`, so import always prompts for the human-appropriate choice.
4. **Don't ship the source mailbox owner's address in the flow** when it differs per environment. MRMS email notifications should target the *record's* people (`Activity/ActivityOwner/EMail`, `Activity/Supervisor/EMail`, `SubmittedBy/EMail`, `ReviewedBy/EMail`) using dynamic expressions, not static addresses. Only the **fixed** recipients (DeputyDirectorME mailbox) may be static, and that belongs in an Environment Variable.
5. **SharePoint Person fields in expressions**: to send email to a Person field value use `@triggerBody()?['ActivityOwner/EMail']` (single user) — for the flow, add a "Get user profile" (`shared_aaduser`) action if you need display names, or rely on the `/EMail` projection that SharePoint connector exposes directly.
6. **Source-control the zip**: commit the unpacked folders (like this repo does for `src/` and the `.msapp`) and the modified zip, so `git diff` is reviewable. Do not hand-edit and lose the provenance; keep the pristine export in `backup/`.

---

## 6. Troubleshooting common import / runtime errors

Cross-referenced with this repo's own import evidence (`v5_import_errors`, `v6_error_scan.md` are canvas-app errors — the equivalent *flow* errors are below).

| Error / symptom | Cause | Fix |
|---|---|---|
| `The workflow is missing a trigger. It must have at least one trigger.` | `definition.json` `triggers` block empty/malformed | Restore `triggers`; ensure the trigger has `type` + `inputs` |
| `The workflow trigger has invalid recurrence` | `recurrence` malformed, wrong frequency, or interval `0` | `"frequency": "Minute"` + `"interval": >= 1`, or `Day`/`Week`/`Month`/`Year` |
| `Invalid template: 'Parameter '$connections' is not defined'` | `parameters.$connections` removed or typo'd | Restore the two standard parameters (§2.1) |
| `The host 'shared_xxx' has an invalid apiId / connectionName` | `host.connectionName` key not present in `apisMap.json`/`connectionsMap.json` | Add/align the map keys with every action's `host.connectionName` |
| `Connection <GUID> is not a valid reference` on import | Root `manifest.json` resource GUID missing while `connectionsMap.json` points at it | Add the API+connection resource blocks to root `manifest.json.resources` |
| `Microsoft.Flow/flows` resource `dependsOn` references a GUID that doesn't exist | Stale dependency edge | Rebuild `dependsOn` lists to only reference GUIDs present in the manifest |
| Flow runs but action fails `BadRequest` on `dataset`/`table` | Site URL or list GUID stale from another environment | Update `inputs.parameters.dataset`/`table`; verify the list GUID (§2.2) |
| `The remote server returned an error: (401) Unauthorized` at runtime | Import connection bound to a user without access to the SharePoint site/list | Re-create the connection with a user who has at least Contribute; verify list permission mapping per `APP_MRMS_Architecture_Pack.docx` §11.2 |
| `(403) Forbidden` on email action | Outlook connection owner lacks send rights, or shared mailbox | Bind `shared_office365` connection to a licensed account with mailbox access |
| `HttpTrigger`/`Request` flow "This flow will not trigger automatically" | Trigger is `Request` (Button) — by design | Invoke from the Power App via `.Run(...)`; it is not list-triggered |
| Import succeeds but flow shows "Turn on flow" needed | Imported flow defaults to Off | Open flow → Turn on (document this in the import runbook) |
| Duplicate runs / multiple triggers firing | Both a list "modified" flow and the Canvas app `Patch` write the same field | Keep **one** writer: let the app set `Status`, and have the flow watch only `Status` transitions; guard with a `LastTriggered`/`TriggerContext` compare, or use `triggerBody()?['Status/Value']` change detection |
| Flow loops (approve → re-notify → approve) | Flow reacts to its own `Patch` writes (e.g. it sets `Status` after sending email) | Use a `Condition` on `@triggerBody()?['Status/Value']` so it only acts on `Submitted`→`SupervisorApproved`→`Approved` transitions, never on already-final states; separate flows per transition also prevent loops |

### 6.1 The classic loop bug in MRMS-style status flows

SharePoint "When an item is created or modified" fires on **every** write. If the flow itself `Patch`es the same item (e.g. writes `IsOverdue`, `Status`, or an `AuditLog` link), the flow re-triggers. Defences (in order of preference):

1. Use **separate flows per state transition**, each guarded by a condition on the incoming `Status/Value`:
   - `Report Submitted - Notify Supervisor (APP-MRMS)` → on `Status = Submitted`
   - `Supervisor Decision - Notify/Route (APP-MRMS)` → on `Status = SupervisorApproved` or `Status = Rejected`
   - `Deputy Director Decision - Finalize (APP-MRMS)` → on `Status = Approved` or `Status = Rejected`
   - `Report Rejected - Return to Contributor (APP-MRMS)` → on `Status = Rejected`
2. Never `Patch` the `Status` column from inside the flow that triggers on `Status` changes — instead the flow writes **only** to `Notifications` / `AuditLog` / `Activities` (the side lists), and the app (or a separate intake flow) is the only writer of `MonthlyReports.Status`.
3. If a flow must touch `MonthlyReports`, add a `Condition` comparing `@triggerBody()?['Status/Value']` against the *previous* value, or write to a marker column and check `triggerOutputs()?['body/...']`.

---

## 7. Working example — the shipped flow, modified and re-imported

### 7.1 Example: retarget `AutomateITCalllogging` to another site

1. `unzip` the package (see §3.2).
2. In `definition.json` replace both occurrences of `dataset: "https://nwpg.sharepoint.com/sites/ITSupportteam"` with the target site, and `table: "625ed6d4-2fe8-4da4-987a-06e5bd1783a2"` with the target list GUID.
3. If you also want a different technician mailbox, change `emailMessage/To` in `Send_an_email_to_Technician`.
4. Re-zip (manifest first, §3.4), import, select/create the two connections (`shared_sharepointonline`, `shared_office365`), turn the flow on.

Because the example only touches the two standard connectors, **no changes to `apisMap.json`, `connectionsMap.json` or the root `manifest.json` are required** — this is the minimal, proven modification path.

### 7.2 Example: add a third connector (e.g. Teams notification)

To add an Office 365 Groups / Teams action:

1. In root `manifest.json.resources` add:
```json
"<new-api-guid>": {
  "id": "/providers/Microsoft.PowerApps/apis/shared_office365groups",
  "name": "shared_office365groups",
  "type": "Microsoft.PowerApps/apis",
  "suggestedCreationType": "Existing",
  "details": { "displayName": "Office 365 Groups" },
  "configurableBy": "System",
  "hierarchy": "Child",
  "dependsOn": []
},
"<new-conn-guid>": {
  "type": "Microsoft.PowerApps/apis/connections",
  "suggestedCreationType": "Existing",
  "creationType": "Existing",
  "details": { "displayName": "<connection owner>" },
  "configurableBy": "User",
  "hierarchy": "Child",
  "dependsOn": ["<new-api-guid>"]
}
```
2. Add the flow's dependency edge: `resources.<flowGUID>.dependsOn` += the two new GUIDs.
3. Add to `apisMap.json`: `"shared_office365groups": "<new-api-guid>"`, and to `connectionsMap.json`: `"shared_office365groups": "<new-conn-guid>"`.
4. Add the action in `definition.json` with `host.connectionName: "shared_office365groups"` and `operationId: "PostMessageToGroup"`.
5. Re-zip and import. The import wizard will now prompt for the Teams connection.

**Guidance**: generate fresh GUIDs with `[guid]::NewGuid()` / `uuidgen`. Never reuse a GUID that appears elsewhere in the same package.

---

## 8. Microsoft's official guidelines for flow package management

| Topic | Official guidance |
|---|---|
| Export flow package | Power Automate → flow → Export → **Package (.zip)**; works for non-solution flows |
| ALM / solutions | Power Platform docs: use **solutions** for production ALM; `pac solution export` / `pac solution import`; environments (Dev→Test→Prod) |
| Connection references | Define connection references + environment variables so managed solutions migrate without editing |
| Workflow definition schema | Logic Apps Workflow Definition Language — schema `2016-06-01`; `$schema` link in the definition itself |
| Environment variables | `Microsoft.PowerPlatform/EnvironmentVariable`; secure vs plain; referenced as `@parameters('<name>')` in flows |
| Connector operations | `operationId` must match the connector's OpenAPI operation (e.g. `GetOnNewItems`, `GetItem`, `SendEmailV2`) |
| Run history & retry | Every connector action supports `retryPolicy` (`Count`, `Interval`, `minimumInterval`, `maximumInterval`) for 429 throttling |
| Managed vs unmanaged | Unmanaged in Dev, convert to Managed for Test/Prod to make flows/components non-editable |
| DLP | Data Loss Prevention policies classify connectors; SharePoint/Outlook/Approvals are Business connectors (see `APP_MRMS_Architecture_Pack.docx` §11.4) |

> **Documented fact**: the MRMS `definition.json` metadata shows `"provisioningMethod": "FromDefinition"` — exactly the "import a definition as a flow" path documented for flow packaging. The example package in this repo is a faithful, unmodified portal export.

---

## 9. Integration patterns — Power Apps ↔ Power Automate in packaged MRMS

### 9.1 Pattern matrix

| Pattern | Trigger type | Use in MRMS | Latency |
|---|---|---|---|
| **Server-side workflow on data change** | SharePoint `When an item is created or modified` | Status-transition flows: notify Supervisor on submit, notify Contributor on decision, escalate overdue | ~5 min polling (recurrence) |
| **UI-triggered synchronous/async flow** | `Request` (Button) | Approve / Reject / Return buttons from `scr_ApprovalQueue` calling `Run(...)` so email + audit happen server-side even if the app closes | seconds |
| **Scheduled** | `Recurrence` | Monthly Reminder, Overdue Escalation, Quarterly/Annual Consolidation, Power BI dataset refresh | daily/monthly |
| **Forms intake** | `When a new response is submitted` (Forms) | Low-connectivity field capture → MonthlyReports Draft/Submitted + photo → EvidenceLibrary | seconds |

### 9.2 The MRMS flow set (from `APP_MRMS_BRD_FDS_TDS_v2.docx` §3.8 + `APP_MRMS_Architecture_Pack.docx` §10)

| Flow (naming: `[Trigger] - [Action] (APP-MRMS)`) | Trigger | Writes to |
|---|---|---|
| `Report Submitted - Notify Supervisor (APP-MRMS)` | MonthlyReports modified, `Status = Submitted` | `Notifications`, email → `Activity/Supervisor/EMail`, `AuditLog` |
| `Supervisor Approved - Route to Deputy (APP-MRMS)` | MonthlyReports modified, `Status = SupervisorApproved` | `Notifications`, email → DeputyDirectorME + Contributor, `AuditLog` |
| `Supervisor Rejected - Return to Contributor (APP-MRMS)` | MonthlyReports modified, `Status = Rejected` | `Notifications`, email → Contributor with `RejectionReason`, `AuditLog` |
| `Deputy Approved - Finalize Report (APP-MRMS)` | MonthlyReports modified, `Status = Approved` | `Notifications`, email → Contributor + Supervisor, mark `Activities.Status = Completed` / `Active = false`, recalc KPI, `AuditLog` |
| `Deputy Rejected - Route Back (APP-MRMS)` | MonthlyReports modified, `Status = Rejected` (by Deputy) | `Notifications`, email → Contributor + Supervisor, `AuditLog` |
| `Monthly Reminder (APP-MRMS)` | Recurrence, ~5 days before month-end | Email open-Activity Contributors, `Notifications` |
| `Overdue Escalation (APP-MRMS)` | Recurrence, daily | Set `IsOverdue`; notify Supervisor (day 1–3) then Programme Manager/DeputyDirectorME (day 4+) |
| `Audit Log Writer (APP-MRMS)` | Item created/modified on master lists | `AuditLog` with before/after |
| `Comment Notification (APP-MRMS)` | ReportComments created | Notify report owner + prior commenters |
| `Quarterly / Annual Consolidation (APP-MRMS)` | Recurrence | Aggregated summaries, archive prior FY, Power BI refresh |

### 9.3 Approved-report accounting ("final approved report counted against the activity")

The KPI roll-up (FR-801) uses **the latest Approved report's `PercentageComplete`** per Activity (`APP_MRMS_Architecture_Pack.docx` §9.5). In flow terms, on `Status = Approved` the flow (or the Power BI dataset) does:

```json
// Conceptual — filter Approved reports per Activity, take max SubmissionDate
"Get_latest_approved_reports": {
  "runAfter": { "Condition_Deputy_Approved": ["Succeeded"] },
  "type": "OpenApiConnection",
  "inputs": {
    "parameters": {
      "dataset": "@parameters('MRMS_SiteUrl')",
      "table": "@parameters('MRMS_MonthlyReports_ListGUID')",
      "filterQuery": "Status eq 'Approved'"
    },
    "host": { "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
              "connectionName": "shared_sharepointonline", "operationId": "GetItems" },
    "authentication": "@parameters('$authentication')"
  }
}
```

Only the newest approved report per `Activity` per `ReportingMonth` participates — older rejected/superseded versions are excluded by the `Status = Approved` filter plus `Version` ordering. This is exactly "the approved report gets counted as a final approved report against the activity".

---

## 10. Reference — full MRMS flow definition skeleton (ready to import)

A minimal, importable `definition.json` for the two-stage approval, using the same schema as the shipped example. This is the **recommended baseline**: one flow per transition (see §6.1) keeps `runAfter` simple and prevents loops. The skeleton below is the first flow ("Report Submitted - Notify Supervisor"). Reuse the pattern for the other transitions.

```json
{
  "name": "9d0a0000-0000-4000-8000-000000000001",
  "id": "/providers/Microsoft.Flow/flows/9d0a0000-0000-4000-8000-000000000001",
  "type": "Microsoft.Flow/flows",
  "properties": {
    "apiId": "/providers/Microsoft.PowerApps/apis/shared_logicflows",
    "displayName": "Report Submitted - Notify Supervisor (APP-MRMS)",
    "definition": {
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
          "metadata": { "operationMetadataId": "a61588e4-a5d8-4ce1-a1d3-84be04a2beaf" },
          "type": "OpenApiConnection",
          "inputs": {
            "parameters": {
              "dataset": "@parameters('MRMS_SiteUrl')",
              "table": "@parameters('MRMS_MonthlyReports_ListGUID')"
            },
            "host": {
              "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
              "connectionName": "shared_sharepointonline",
              "operationId": "GetOnNewItems"
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
            "and": [ { "equals": [ "@triggerBody()?['Status/Value']", "Submitted" ] } ]
          },
          "actions": {
            "Notify_Supervisor": {
              "type": "OpenApiConnection",
              "inputs": {
                "parameters": {
                  "emailMessage/To": "@triggerBody()?['ActivitySupervisor/EMail']",
                  "emailMessage/Subject": "Monthly report submitted for review",
                  "emailMessage/Body": "<p>A report for <b>@{triggerBody()?['Activity/Value']}</b> "
                    + "was submitted by @{triggerBody()?['SubmittedBy/Value']} and is awaiting your review.</p>"
                },
                "host": { "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
                          "connectionName": "shared_office365", "operationId": "SendEmailV2" },
                "authentication": "@parameters('$authentication')"
              },
              "runAfter": {}
            },
            "Create_Notification": {
              "type": "OpenApiConnection",
              "inputs": {
                "parameters": {
                  "dataset": "@parameters('MRMS_SiteUrl')",
                  "table": "@parameters('MRMS_Notifications_ListGUID')",
                  "item/Title": "New report awaiting review",
                  "item/RecipientUser/Value": "@triggerBody()?['ActivitySupervisor/Id']",
                  "item/RelatedEntity": "MonthlyReports:@{triggerBody()?['ID']}",
                  "item/IsRead": false
                },
                "host": { "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
                          "connectionName": "shared_sharepointonline", "operationId": "CreateItem" },
                "authentication": "@parameters('$authentication')"
              },
              "runAfter": { "Notify_Supervisor": ["Succeeded"] }
            },
            "Write_AuditLog": {
              "type": "OpenApiConnection",
              "inputs": {
                "parameters": {
                  "dataset": "@parameters('MRMS_SiteUrl')",
                  "table": "@parameters('MRMS_AuditLog_ListGUID')",
                  "item/Title": "StatusChange MonthlyReports:@{triggerBody()?['ID']}",
                  "item/EntityType": "MonthlyReport",
                  "item/EntityId": "@triggerBody()?['ID']",
                  "item/Action": "StatusChange",
                  "item/ActionDate": "@utcNow()",
                  "item/Reason": "Submitted"
                },
                "host": { "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
                          "connectionName": "shared_sharepointonline", "operationId": "CreateItem" },
                "authentication": "@parameters('$authentication')"
              },
              "runAfter": { "Create_Notification": ["Succeeded"] }
            }
          },
          "else": {}
        }
      },
      "outputs": {}
    }
  }
}
```

> Column names in the skeleton assume the live `MonthlyReports` schema (see `MonthlyReports.csv`). **Verify each internal name in your SharePoint list before import** — the connector fails at runtime, not at import, if a column name differs.

---

## 11. Your MRMS approval flow — validation against the repo docs

This section validates the flow description you provided against `APP-MRMS_BRD_FDS_TDS_v2.docx`, `APP_MRMS_Architecture_Pack.docx`, `APPMRMS_Phase1_ExecutionGuide.docx` and the live list schemas. Confirmed **correct** in your description, and gaps/decisions you still need to make.

### 11.1 Confirmed correct

- ✅ MonthlyReports is the transactional list where reports are created (`MonthlyReports.csv`; TDS §3.2.5).
- ✅ Contributor submits → routed to the Activity's Supervisor (FR-601/BR-03; `Activities.Supervisor` Person column).
- ✅ Supervisor may Approve or Reject; rejection requires a mandatory comment (`RejectionReason`, BR-04; `APP_Users` matrix — only Supervisor/Administrator approve-reject for own directorate).
- ✅ On final approval the approved report is counted against the Activity's KPI/progress (FR-801; `APP_MRMS_Architecture_Pack.docx` §9.5 uses latest Approved `PercentageComplete`).
- ✅ Contributor + Supervisor get in-app and email notifications (in-app = `Notifications` list; email = Outlook connector). FR-1002: Supervisor on submission, Contributor on decision.
- ✅ Rejection returns the report to the Contributor for correction, and Version increments on resubmission (BR-04, FR-504, BR-08).

### 11.2 Gaps and decisions you still need to make (things you missed / that differ from the docs)

1. **DeputyDirectorME is a cross-cutting escalation right, NOT a mandatory second approval stage in the docs.** BR-05 and FDS §2.3: *"DeputyDirectorME may intervene on ANY report at ANY stage."* Your description makes it a mandatory stage-2 approver. If you want the mandatory two-stage flow you must:
   - **Add a new Status value** to the `MonthlyReports.Status` choice column — currently only `Draft / Submitted / Approved / Rejected / Escalated` (verified in `MonthlyReports.csv` schema XML). Add e.g. `SupervisorApproved` (or `PendingDeputyReview`). This is a SharePoint column change (choice list), which per §3.12 of the BRD goes through you as solution owner.
   - Add a **Deputy Director queue filter** in `scr_ApprovalQueue` (currently the app's queue is single-stage; `v6_error_scan.md` R2 flags exact `Status.Value` match as a risk).
   - Decide whether Deputy approval is required for **every** report or only escalation-worthy ones (the docs' intent is escalation-only).

2. **"Activity gets marked as completed / not active anymore" is NOT in the docs.** `Activities` has `Status` (Active/Completed/Not Started) and `Active` (boolean, default true) — but nothing in the BRD/FDS/TDS says a single approved monthly report completes the Activity. An Activity can have **12 monthly reports (April–March)**. Marking it Completed on the first approved month would hide it from `scr_MyActivities` (filter `Active = true`) and block the remaining 11 reports. You must define:
   - "Completed" = all reporting months of the FY have an approved report, **or**
   - "Completed" = the Activity's `EndDate` passed with an approved final report, **or**
   - per-Activity `Frequency` semantics (Monthly → 12, Quarterly → 4, Annual → 1 approved report to complete).
   The `APP_MRMS_Architecture_Pack.docx` KPI design never auto-completes Activities; it only rolls up approved `PercentageComplete`.

3. **Who is notified, when** — the docs say **Supervisor is notified on submission** and **Contributor on decision** (FR-1002). Your statement says supervisor AND contributor get notified on approval/rejection. In a two-stage model you'll want the full set:
   - Submit → **Supervisor** (email + in-app).
   - Supervisor approves → **Contributor** ("approved by your Supervisor, now with M&E") and **DeputyDirectorME** (new work item).
   - Supervisor rejects → **Contributor**.
   - Deputy approves → **Contributor + Supervisor** ("final approval received"), Activity/KPI updated.
   - Deputy rejects → **Contributor + Supervisor** ("returned by M&E with reason").
   That last one (Supervisor gets notified when Deputy rejects) is an addition beyond the docs and matches your intent — just document it as a business rule.

4. **Status on rejection: keep `Rejected` or return to `Draft`?** The docs (BR-04) say a rejected report *returns to Draft status* for editing. Your description keeps it at `Rejected` until corrected. Decide one of:
   - Keep `Status = Rejected` with `RejectionReason` (report stays visible as rejected in `scr_MyReports`, and the contributor re-edits it) — but then the re-submission must set `Status = Submitted` again and increment `Version`.
   - Or implement `Return for Correction` (a distinct action in FDS FR-602 alongside Approve/Reject) that sets `Status = Draft`.
   Either works; the key is **the app must let the Contributor re-open the item** and the flow must route re-submission exactly like a fresh submission (version +1, notify Supervisor).

5. **Re-submission "starts the approval process from scratch"** — yes, this is already the documented model: resubmit → `Submitted` → Supervisor → (approve) → Deputy. Version increments each time (FR-504). Your understanding is correct here.

6. **"Escalated" status** (a 5th value in the live list) is for the Overdue Escalation flow (BR-06/07, FR-1003) and is separate from your two-stage approval. Decide whether the Deputy Director queue also surfaces `Escalated` items.

7. **ProgrammeManager is a viewer/roll-up role** in the docs (approve/reject = No in the FDS matrix) — your flow description never mentions Programme Managers, which is consistent. Just don't add them as an approver stage unless intended.

### 11.3 Recommended status model for your two-stage flow

| Status value | Meaning | Set by |
|---|---|---|
| `Draft` | Contributor editing; no workflow | App |
| `Submitted` | Contributor submitted → Supervisor queue | App |
| `SupervisorApproved` *(NEW)* | Supervisor approved → DeputyDirectorME queue | App or flow |
| `Approved` | DeputyDirectorME final approval → KPI count, Activity complete rule | App or flow |
| `Rejected` | Returned with `RejectionReason` → back to Contributor (and Supervisor if Deputy rejected) | App |
| `Escalated` | Overdue escalation path (existing) | Overdue flow |

---

## 12. Proven implementation runbook (summary)

1. **Extend the SharePoint Status choice** with `SupervisorApproved` (if adopting mandatory two-stage).
2. **Build the flows as one flow per transition** (§9.2), each `When_an_item_is_modified` on `MonthlyReports` guarded by a `Condition` on `Status/Value`. No flow writes `Status`; the app (buttons in `scr_ApprovalQueue`, `scr_ReportSubmission`) is the sole `Status` writer — this kills the loop problem (§6.1).
3. **Use Request triggers for the app-called actions** (Approve/Reject/Return buttons) so email + `Notifications` + `AuditLog` writes are server-side and cannot be skipped by closing the app (§4.1).
4. **Package each flow** as a portal `.zip` (or all flows inside one Power Platform solution with Environment Variables for site URL / list GUIDs / Deputy mailbox, §4.3).
5. **On import**: bind connections (`shared_sharepointonline`, `shared_office365`), supply Environment Variables, turn flows on, and smoke-test each transition with a real report (Draft → Submitted → SupervisorApproved → Approved, and the two Reject paths).
6. **Wire the app's `scr_ApprovalQueue`** to filter `Status = Submitted` (Supervisor) and `Status = SupervisorApproved` (DeputyDirectorME) — the v6 queue currently filters a single status list.
7. **Notifications** = create a row in `Notifications` (in-app badge via `icoNotificationsBell` count) + Outlook email, per the FR-1002 matrix in §11.2 item 3.
8. **After final approval**: flow updates the KPI/approved-count semantics (only latest Approved report per Activity per ReportingMonth counts, §9.3) and, per your decision in §11.2 item 2, optionally marks the Activity Completed.

---

*Prepared from the repository's live data layer (`MonthlyReports.csv`, `Activities.csv`, `APP_Users.csv`), the architecture/BRD/FDS/TDS docs, the shipped `AutomateITCalllogging_*.zip` flow package, and Microsoft's Logic Apps Workflow Definition Language / Power Platform ALM guidance. `research_powerautomate_import.md` is intended as the reference input for DeepSeek or other models executing the flow-package modification and re-import work.*
