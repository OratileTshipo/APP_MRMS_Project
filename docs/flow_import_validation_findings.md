# Power Automate Package Import Validation — Findings

How the APP-MRMS approval-workflow package was iterated through Power Automate's
import validation until the flow resources were accepted, what each failure meant,
and the exact definition shapes that pass.

## 1. Background

- Package: `flows/APP-MRMS-Approval.zip` (three flows: Notify Supervisor,
  Route to Deputy, Finalize on approval).
- Import target: Power Automate environment `APP-MRMS`, SharePoint site
  `https://nwpg.sharepoint.com/sites/DPWRPerformanceandMonitoring`.
- Import model: raw flow `.zip` package (root `manifest.json` +
  `Microsoft.Flow/flows/manifest.json` + one folder per flow GUID with
  `definition.json`, `apisMap.json`, `connectionsMap.json`). Connectors:
  SharePoint (`shared_sharepointonline`) and Office 365 Outlook (`shared_office365`).
- Flows are hand-built from the proven portal export
  `AutomateITCalllogging_20260818132403.zip` and the source-of-truth lists
  (GUIDs from `APP-MRMS_Project_app_v6.msapp`).

On import, each flow's `definition.json` is run through the Logic Apps workflow
validator. Failures surface one at a time; the error text is authoritative and the
validator short-circuits on the first problem it finds. Fix, rebuild, re-import.

## 2. Validation errors encountered and their fixes

### 2.1 `WorkflowRunActionInputsInvalidProperty` — `authentication` on nested actions

**Observed error**

```
Flow save failed with code 'WorkflowRunActionInputsInvalidProperty' and message
'The 'inputs' of workflow run action 'Get_activity' of type 'OpenApiConnection'
should not have the property 'authentication'.'
```

**Root cause**

The `authentication` property (`@parameters('$authentication')`) is only valid on
the **trigger** and on **top-level actions**. Actions nested inside a scope
(Condition `actions`/`else`, Switch, Scope, etc.) must NOT carry it — the scope
inherits authentication. All of our actions sit inside the `Condition_Status_*`
block, so all of them violated this.

**Fix**

Removed `"authentication": "@parameters('$authentication')"` from every action
`inputs`; kept it on the trigger only.

**Correct shapes**

Trigger (keeps `authentication`):

```json
{
  "type": "OpenApiConnection",
  "inputs": {
    "parameters": { "dataset": "...", "table": "..." },
    "host": {
      "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
      "connectionName": "shared_sharepointonline",
      "operationId": "GetOnChangedItems"
    },
    "authentication": "@parameters('$authentication')"
  }
}
```

Action inside a Condition (no `authentication`):

```json
{
  "type": "OpenApiConnection",
  "inputs": {
    "parameters": { "...": "..." },
    "host": {
      "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
      "connectionReferenceName": "shared_sharepointonline",
      "operationId": "GetItem"
    }
  }
}
```

### 2.2 `WorkflowRunActionInputsMissingProperty` — `host.connectionReferenceName`

**Observed error**

```
Flow save failed with code 'WorkflowRunActionInputsMissingProperty' and message
'The 'inputs' of workflow run action 'Get_activity' of type 'OpenApiConnection' is
not valid. Property 'host.connectionReferenceName' is missing.'
```

**Root cause**

Actions must reference their connection through
`host.connectionReferenceName` (the logical connection name —
`shared_sharepointonline` / `shared_office365`), not `host.connectionName`.
The trigger keeps `host.connectionName`; actions use `connectionReferenceName`.

**Fix**

Replaced `host.connectionName` with `host.connectionReferenceName` on every
action (same value), left the triggers as `connectionName`.

The value must match the keys in the flow folder's `connectionsMap.json` /
`apisMap.json` (and therefore the connection resources in the root `manifest.json`).

### 2.3 Invalid trigger parameter `changeType` on `GetOnChangedItems`

**Observed error**

Generic package-level failure: connectors imported, all flow templates rejected.

**Root cause**

The current SharePoint connector's `GetOnChangedItems` ("When an item is modified")
accepts only `dataset` and `table` (optional `folderPath`, `view`). We were passing
`changeType: "Modified"`, which is not a parameter of this operation in the current
connector; the extra property invalidated every flow template.

**Verification source**

The connector's own Swagger (`microsoft/Power-Fx`
`src/tests/Microsoft.PowerFx.Connectors.Tests.Shared/Swagger/SharePoint.json`)
defines `GetOnChangedItems` with path params `dataset`, `table` only.

**Fix**

Removed `"changeType": "Modified"` from the trigger parameters. The trigger still
fires on modification only, which is exactly the semantic we need for
status-transition flows.

### 2.4 Duplicate action names (the trigger for excluding the Rejected flow)

**Observed error (earlier iteration)**

```
The template action names must be unique: actions 'Create_Notification_Contributor'
are declared multiple times.
```

**Root cause**

Two Condition branches in the same flow both declared an action named
`Create_Notification_Contributor`. Action names must be globally unique within a
flow definition, including across nested scopes.

**Fix**

Renamed one instance to `Create_Notification_Contributor_SupervisorReject`. The
flow remained out of the shipped package (see §4) because the failure kept
recurring during the re-import cycle; the template source is retained and now also
carries fixes §2.1–§2.3.

## 3. Canonical definition skeleton (passes validation)

```json
{
  "name": "<flow-guid>",
  "id": "/providers/Microsoft.Flow/flows/<flow-guid>",
  "type": "Microsoft.Flow/flows",
  "properties": {
    "apiId": "/providers/Microsoft.PowerApps/apis/shared_logicflows",
    "displayName": "<Flow display name (APP-MRMS)>",
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
            "parameters": { "dataset": "<site>", "table": "<list-guid>" },
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
        "Condition_Status_<Value>": {
          "runAfter": {},
          "type": "If",
          "expression": { "and": [ { "equals": [ "@triggerBody()?['Status/Value']", "<Value>" ] } ] },
          "actions": {
            "<ActionName>": {
              "runAfter": { "<PrevAction>": ["Succeeded"] },
              "type": "OpenApiConnection",
              "inputs": {
                "parameters": { "...": "..." },
                "host": {
                  "apiId": "<connector-api-id>",
                  "connectionReferenceName": "shared_sharepointonline",
                  "operationId": "<operation-id>"
                }
              }
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

Validation rules captured:

| Location | Property | Rule |
|---|---|---|
| Trigger inputs | `authentication` | Required |
| Action inputs | `authentication` | **Forbidden** (only top-level actions may have it) |
| Action host | `connectionReferenceName` | Required; value = logical connection name |
| Trigger host | `connectionName` | Required; value = logical connection name |
| Trigger params | `dataset`, `table` | Required for `GetOnChangedItems`; `changeType` is **not** valid |
| Action names | global scope | Must be unique across the whole definition |
| Flow folder | GUID | Must equal `name`, `id`, and the folder path |

## 4. Current status

- Shipped package: 3 flows, all definitions updated with §2.1–§2.3. Zip rebuilt
  via `tools/build_flow_zips.py` with production site URL and list GUIDs.
- Excluded flow `d4f9a27c` ("Report Rejected - Notify and Route Back"): template
  kept at
  `flows/templates/APP-MRMS-Approval/Microsoft.Flow/flows/d4f9a27c-8851-44ba-9f3c-4989a0e6d467/`,
  now also carries the §2.1–§2.3 fixes. Re-add to the package by:
  1. confirming no duplicate action names,
  2. adding its GUID to the root `manifest.json` resources + flow dependency list,
  3. adding the GUID to `Microsoft.Flow/flows/manifest.json` `assetPaths`,
  4. removing the GUID from `EXCLUDED_FLOW_DIRS` in `tools/build_flow_zips.py`,
  5. rebuilding and re-importing.

## 5. Rebuild and re-import

```bash
python3 tools/build_flow_zips.py \
  --site-url "https://nwpg.sharepoint.com/sites/DPWRPerformanceandMonitoring" \
  --monthlyreports "31b39eaa-cf11-426d-b9a1-c3df5bae7cbe" \
  --activities "dc7c7e42-8fd5-4b0a-8275-a7d9c4f4c67f" \
  --notifications "60fa50dd-588f-4ae6-b838-aae60fc3092d" \
  --auditlog "ef3722f5-44eb-4376-8a02-8a2ba574304a" \
  --users "aca25b79-2f4a-4803-93b4-17feb2cac5a2" \
  --output flows/APP-MRMS-Approval.zip
```

Import notes:

- On import, choose **Create new** for each flow resource (they do not yet exist
  in the environment), and bind both connections (SharePoint + Outlook) to the
  target environment.
- After a failed import, the per-resource error in the import details is
  authoritative — it names the exact action/property that failed.
- Iterate: fix, rebuild, re-import. The validator reports one error at a time.
