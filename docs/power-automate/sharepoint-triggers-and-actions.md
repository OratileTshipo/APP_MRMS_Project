# SharePoint Connector — Triggers and Actions Reference

The SharePoint connector (`shared_sharepointonline`) is the primary connector for APP-MRMS flows.

---

## Triggers

### When an item is created (`GetOnCreatedItems`)
Fires when a new item is added to a SharePoint list.

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `dataset` | Yes | SharePoint site URL |
| `table` | Yes | List GUID |

**Note:** Not used by APP-MRMS (we use "modified" trigger instead).

---

### When an item is modified (`GetOnChangedItems`)
Fires when an existing item is updated in a SharePoint list.

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `dataset` | Yes | SharePoint site URL, e.g. `https://org.sharepoint.com/sites/APP-MRMS` |
| `table` | Yes | List GUID, e.g. `31b39eaa-cf11-426d-b9a1-c3df5bae7cbe` |

**Important:** The `changeType` parameter is **NOT valid** for this operation. Do not include it.

**Output:** Array of changed items (via `splitOn: @triggerOutputs()?['body/value']`).

**Polling interval:** Default 3 minutes. Configurable in trigger settings.

**Example trigger body:**
```json
{
  "Id": 1,
  "Title": "ICTM-RP-0001",
  "Status": { "Value": "Submitted", "Id": "1" },
  "Activity": { "Value": "ICMTS-AC-0001", "Id": "5" },
  "ReportingMonth": { "Value": "August", "Id": "8" },
  "SubmittedBy": { "DisplayName": "John Doe", "Email": "john@org.com" }
}
```

---

## Actions

### Get Item (`GetItem`)
Retrieve a single item by its ID.

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `dataset` | Yes | SharePoint site URL |
| `table` | Yes | List GUID |
| `id` | Yes | Item ID (numeric) |

**Output:** Single item object.

---

### Get Items (`GetItems`)
Retrieve multiple items with optional filtering.

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `dataset` | Yes | SharePoint site URL |
| `table` | Yes | List GUID |
| `filterQuery` | No | OData filter expression |
| `top` | No | Max items to return (default 100, max 5000) |
| `orderBy` | No | Sort expression |

**Filter Query (OData) Examples:**
```
Title eq 'ICMTS-AC-0001'
Active eq 1 and Frequency eq 'Monthly'
Status eq 'Submitted' and ReportingMonth eq 'August'
substringof('search term',Title)
```

**Important:** Lists with >5,000 items require indexed columns and pagination. See [troubleshooting.md](troubleshooting.md) for "view threshold" errors.

**Example with dynamic content in filter:**
```json
{
  "filterQuery": "Activity eq '@{triggerBody()?['Activity']?['Value']}'"
}
```

**Expression-based filter (current month):**
```
Activity eq '@{items('Apply_to_each')?['Title']}' and ReportingMonth eq '@{formatDateTime(utcNow(), 'MMMM')}'
```

---

### Create Item (`CreateItem`)
Add a new item to a list.

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `dataset` | Yes | SharePoint site URL |
| `table` | Yes | List GUID |
| List columns | Varies | Column values to set |

**Example (create notification):**
```json
{
  "dataset": "https://org.sharepoint.com/sites/APP-MRMS",
  "table": "60fa50dd-588f-4ae6-b838-aae60fc3092d",
  "Title": "Report @{triggerBody()?['Title']} submitted",
  "Message": "Your report has been submitted for review",
  "RecipientEmail": "@{triggerBody()?['SubmittedBy']?['Email']}",
  "IsRead": false
}
```

---

### Update Item (`UpdateItem`)
Modify an existing item.

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `dataset` | Yes | SharePoint site URL |
| `table` | Yes | List GUID |
| `id` | Yes | Item ID |
| List columns | Varies | Columns to update |

**Example (mark activity completed):**
```json
{
  "dataset": "https://org.sharepoint.com/sites/APP-MRMS",
  "table": "dc7c7e42-8fd5-4b0a-8275-a7d9c4f4c67f",
  "id": "@{body('Get_activity')?['Id']}",
  "Active": false,
  "Status": { "Value": "Completed" }
}
```

---

### Delete Item (`DeleteItem`)
Remove an item from a list.

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `dataset` | Yes | SharePoint site URL |
| `table` | Yes | List GUID |
| `id` | Yes | Item ID |

---

## Person/Lookup Column Access Patterns

SharePoint Person columns return a complex object. Common access patterns:

```javascript
// Person column
triggerBody()?['SubmittedBy']?['DisplayName']    // "John Doe"
triggerBody()?['SubmittedBy']?['Email']           // "john@org.com"
triggerBody()?['SubmittedBy']?['Claims']           // "i:0#.f|membership|john@org.com"

// Choice column
triggerBody()?['Status']?['Value']                // "Submitted"
triggerBody()?['ReportStatus']?['Value']          // "Supervisor Rejected"

// Lookup column
triggerBody()?['Activity']?['Value']              // "ICMTS-AC-0001" (display value)
triggerBody()?['Activity']?['Id']                 // "5" (lookup ID)

// Person column inside Apply to Each
items('Apply_to_each')?['ActivityOwner']?['Email']
items('Apply_to_each')?['Supervisor']?['Email']
```

---

## Authentication in Definition JSON

**Triggers** use `host.connectionName`:
```json
{
  "host": {
    "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
    "connectionName": "shared_sharepointonline",
    "operationId": "GetOnChangedItems"
  },
  "authentication": "@parameters('$authentication')"
}
```

**Actions** use `host.connectionReferenceName` (NOT `connectionName`):
```json
{
  "host": {
    "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
    "connectionReferenceName": "shared_sharepointonline",
    "operationId": "GetItem"
  }
}
```

**Key rule:** Actions inside nested scopes (Condition, Switch, Scope) must **NOT** have `authentication` — the scope inherits it from the trigger.

---

## Common OData Filter Patterns

| Pattern | Example |
|---------|---------|
| Equality | `Status eq 'Submitted'` |
| Not equal | `Status ne 'Draft'` |
| Greater than | `PercentageComplete gt 50` |
| Less than | `PercentageComplete lt 100` |
| AND | `Active eq 1 and Frequency eq 'Monthly'` |
| OR | `Status eq 'Submitted' or Status eq 'Approved'` |
| Contains | `substringof('search',Title)` |
| Starts with | `startswith(Title,'ICMTS')` |
| Date comparison | `DueDate le '@{formatDateTime(utcNow(),'yyyy-MM-dd')}'` |
| Null check | `Supervisor ne null` |

**Note:** OData filter queries are **case-sensitive** for string values.

---

*Source: Microsoft Learn Power Automate — SharePoint connector documentation*
