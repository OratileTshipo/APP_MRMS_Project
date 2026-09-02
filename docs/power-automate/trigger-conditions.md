# Trigger Conditions, Filtering, and Concurrency

Trigger conditions control **when** a flow fires. Without them, a flow fires on every item modification — which can cause infinite loops or unnecessary runs.

---

## Trigger Conditions

Trigger conditions are expressions added in the trigger's **Settings** panel. The flow only fires when **ALL** conditions evaluate to `true`.

### How to Add Trigger Conditions

1. Click **⋯** (three dots) on the trigger card
2. Select **Settings**
3. Under **Trigger Conditions**, click **+ Add**
4. Enter the expression (must start with `@`)
5. Click **+ Add** for additional conditions
6. Click **Done**

### Expression Format

Trigger conditions use the same expression syntax as actions:

```
@equals(triggerBody()?['Status/Value'], 'Submitted')
```

**Important:** Multiple trigger conditions are ANDed together (all must be true).

### APP-MRMS Trigger Conditions

**Flow 1 (Report Submitted):**
```
@equals(triggerBody()?['Status/Value'], 'Submitted')
```

**Flow 2 (Supervisor Approved):**
```
@equals(triggerBody()?['Status/Value'], 'SupervisorApproved')
```

**Flow 3 (Report Rejected):**
```
@equals(triggerBody()?['Status/Value'], 'Rejected')
```

**Flow 4 (Report Approved):**
```
@equals(triggerBody()?['Status/Value'], 'Approved')
```

---

## Concurrency Control

### Sequential (Default)
- `Concurrency Control` = **Off** (default)
- Flows process items one at a time
- Guarantees order of execution
- **Recommended for APP-MRMS** — prevents race conditions on Status updates

### Parallel
- `Concurrency Control` = **On**
- Set `Degree of Parallelism` (1–50)
- Multiple instances run simultaneously
- Use for independent items that don't affect each other
- **Caution:** Can cause duplicate notifications if trigger fires faster than flow completes

### Configuration
1. Click **⋯** on the trigger → **Settings**
2. Find **Concurrency Control**
3. Toggle **On** or **Off**
4. If On, set **Degree of Parallelism**

---

## Trigger Polling Intervals

Event-based triggers (SharePoint) use polling, not real-time push:

| Connector | Default Interval | Configurable |
|-----------|-----------------|--------------|
| SharePoint | 3 minutes | Yes (1 min–18 hr) |
| Office 365 Outlook | 3 minutes | Yes |
| Forms | 1 minute | Yes |

### How to Change Polling Interval
1. Click **⋯** on the trigger → **Settings**
2. Find **Frequency** and **Interval**
3. Set desired values

**Note:** Shorter intervals increase API calls. For APP-MRMS, the default 3-minute interval is appropriate.

---

## Trigger Splitting (Concurrency)

When a trigger returns an array of items (e.g., multiple items modified at once), you can split the flow to process each item individually:

```json
{
  "splitOn": "@triggerOutputs()?['body/value']"
}
```

This causes the flow to run **once per item** in the array, each with its own trigger body.

**APP-MRMS:** The `GetOnChangedItems` trigger includes `splitOn` by default, so each modified item triggers a separate flow run.

---

## Filtering in Actions (Not Trigger)

For more complex filtering, use **Get Items** with OData `filterQuery`:

### Example: Get activities due this month
```
filterQuery: "Active eq 1 and DueDate le '@{formatDateTime(utcNow(),'yyyy-MM-dd')}'"
```

### Example: Get reports for a specific activity
```
filterQuery: "Activity eq '@{triggerBody()?['Activity']?['Value']}' and ReportingMonth eq '@{formatDateTime(utcNow(), 'MMMM')}'"
```

---

## Preventing Infinite Loops

**Critical rule for APP-MRMS:** Flows must never write to the column that triggers them.

| Flow | Reads From | Writes To | Safe? |
|------|-----------|-----------|-------|
| Flow 1 (Submitted) | MonthlyReports.Status | Email only | ✅ |
| Flow 2 (SupervisorApproved) | MonthlyReports.Status | Email + Notifications | ✅ |
| Flow 3 (Rejected) | MonthlyReports.Status | Email + Notifications | ✅ |
| Flow 4 (Approved) | MonthlyReports.Status | Email + Notifications + Activities + AuditLog | ✅ |

If a flow wrote back to `Status`, it would trigger itself infinitely.

---

## Scope and Error Handling

### Scope Action
Wraps multiple actions. If any action inside fails, the scope catches it.

```json
{
  "type": "Scope",
  "actions": {
    "Action1": { ... },
    "Action2": { ... }
  },
  "runAfter": {}
}
```

### Configure Run After
Control when an action runs based on previous action status:

```json
{
  "runAfter": {
    "PreviousAction": ["Succeeded"]
  }
}
```

**Options:** `Succeeded`, `Failed`, `Skipped`, `TimedOut`

### Pattern: Continue on failure
```json
{
  "runAfter": {
    "RiskyAction": ["Succeeded", "Failed"]
  }
}
```

---

*Source: Microsoft Learn Power Automate — Triggers and actions documentation*
