# Cloud Flows Overview

Power Automate provides three types of flows. This guide covers cloud flows (the type used by APP-MRMS).

---

## Types of Cloud Flows

| Type | Trigger | Use Case |
|------|---------|----------|
| **Automated** | Event-based (SharePoint item modified, email received, etc.) | Notifications, approvals, data sync |
| **Instant** | Button press, HTTP request, power app | On-demand actions, manual triggers |
| **Scheduled** | Recurrence (daily, weekly, monthly) | Reports, reminders, data aggregations |

APP-MRMS uses:
- **Automated flows** for Flows 1–4 (triggered by SharePoint `Status` changes)
- **Scheduled flow** for the MonthlyReminder (weekly recurrence)

---

## Core Concepts

### Triggers
The event that starts a flow. Examples:
- `When an item is created or modified` (SharePoint) — used by APP-MRMS Flows 1–4
- `Recurrence` — used by MonthlyReminder
- `When an HTTP request is received` — for external integrations

### Actions
Steps that execute after the trigger fires. Each action has:
- **Inputs** — parameters, dynamic content from previous steps, expressions
- **Outputs** — values available to subsequent actions via dynamic content

### Connections
Authenticated links to services (SharePoint, Outlook, etc.). Created once, reused across flows.

### Run History
Available for 28 days. Shows inputs, outputs, and status for each action in each run.

---

## Flow Lifecycle

```
Create → Configure → Test → Turn On → Monitor → Update
  │         │          │        │          │         │
  │         │          │        │          │         └─ Edit and redeploy
  │         │          │        │          └─ Check run history, fix errors
  │         │          │        └─ Enable the flow
  │         │          └─ Manual or automatic test run
  │         └─ Add trigger, actions, conditions
  └─ In portal or via import
```

---

## Cloud Flow Designer

Two designers are available:

| Feature | New Designer (Recommended) | Classic Designer |
|---------|---------------------------|------------------|
| Copilot assistance | ✅ Yes | ❌ No |
| Version history | ✅ Yes | ❌ No |
| Expression assistant | ✅ Yes | ❌ No |
| All trigger types | ⚠️ Some missing | ✅ Full support |
| Solution flows | ✅ Yes | ✅ Yes |

**Recommendation:** Use the new designer for most flows. Switch to classic for edge cases (e.g., Power Apps v1 triggers, business process flow triggers).

---

## Limits and Configuration

| Limit | Value |
|-------|-------|
| Max actions per flow | 100,000 |
| Max recurrence interval | 500 days |
| Min recurrence interval | 1 minute |
| Max payload size (HTTP) | 100 MB |
| Run history retention | 28 days |
| Max concurrent runs (per flow) | Depends on plan |
| Trigger polling interval | 1–5 minutes (varies by connector) |

---

## Licensing

| Feature | Included (M365) | Premium Required |
|---------|-----------------|------------------|
| SharePoint triggers/actions | ✅ | — |
| Office 365 Outlook | ✅ | — |
| HTTP trigger/action | — | ✅ |
| Dataverse | — | ✅ |
| Custom connectors | — | ✅ |
| Desktop flows | — | ✅ |

APP-MRMS flows use only **SharePoint** and **Office 365 Outlook** connectors — both included with M365.

---

## Connectors Used by APP-MRMS

### SharePoint (`shared_sharepointonline`)
- Triggers: `GetOnChangedItems` (when item modified), `GetOnCreatedItems` (when item created)
- Actions: `GetItem`, `GetItems`, `CreateItem`, `UpdateItem`, `DeleteItem`
- Authentication: `@parameters('$authentication')`

### Office 365 Outlook (`shared_office365`)
- Actions: `SendEmailV2` (send email)
- Authentication: `@parameters('$authentication')`

---

*Source: Microsoft Learn Power Automate documentation*
