# Power Automate Reference Documentation

Extracted and organized from the official Microsoft Learn Power Automate documentation (3,950 pages) for the APP-MRMS project. These files serve as reference for both **building flows manually** in Power Automate Studio and **importing flows** via `.zip` packages.

---

## Reference Files

| File | Purpose | Use When |
|------|---------|----------|
| [cloud-flows-overview.md](cloud-flows-overview.md) | Types of flows, core concepts, lifecycle | Starting from scratch, understanding the platform |
| [sharepoint-triggers-and-actions.md](sharepoint-triggers-and-actions.md) | SharePoint connector triggers, actions, OData filtering | Building any SharePoint-connected flow |
| [expressions-and-functions.md](expressions-and-functions.md) | Complete expressions/functions reference | Writing conditions, dynamic content, data transforms |
| [expression-cheat-sheet.md](expression-cheat-sheet.md) | **Quick reference** — 20 most-used expressions for this project | Copy-paste expressions while building flows |
| [trigger-conditions.md](trigger-conditions.md) | Trigger conditions, concurrency, polling intervals | Fine-tuning when flows fire |
| [building-flows-manually.md](building-flows-manually.md) | Step-by-step guide to build flows in the portal | Creating flows without Copilot, or via the classic designer |
| [flow-import-export.md](flow-import-export.md) | Import/export package format, validation rules, rebuild script | Importing the `.zip` package, fixing import errors |
| [alerting-flow.md](alerting-flow.md) | MonthlyReminder scheduled flow pattern — full reference | Building or importing the weekly reminder flow |
| [troubleshooting.md](troubleshooting.md) | Common errors, error codes, fixes | Debugging failed flows, fixing connections |
| [definition-json-reference.md](definition-json-reference.md) | `definition.json` structure for importable flows | Hand-crafting or editing flow definitions for import |

---

## Quick Start

### Building a flow manually (in the portal)
→ See [building-flows-manually.md](building-flows-manually.md) for the full walkthrough.

### Importing the existing APP-MRMS package
→ See [flow-import-export.md](flow-import-export.md) for the import process and validation rules.

### Writing an expression or condition
→ See [expression-cheat-sheet.md](expression-cheat-sheet.md) for the 20 most-used expressions (quick copy-paste).
→ See [expressions-and-functions.md](expressions-and-functions.md) for the complete function reference.

### Debugging a failed flow
→ See [troubleshooting.md](troubleshooting.md) for the error-to-fix lookup table.

---

## APP-MRMS Flow Architecture

The APP-MRMS system uses **5 cloud flows** — 4 event-triggered approval flows plus 1 scheduled reminder flow:

```
┌─────────────────────────────────────────────────────────────┐
│                    MonthlyReports (SharePoint)               │
│  Status: Draft → Submitted → SupervisorApproved → Approved  │
│                ↘ Rejected                                   │
└──────────────────────┬──────────────────────────────────────┘
                       │ Status changes
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  Flow 1: Report Submitted - Notify Supervisor               │
│  Trigger: Status = "Submitted"                               │
│  Action: Email Supervisor                                    │
├──────────────────────────────────────────────────────────────┤
│  Flow 2: Supervisor Approved - Route to Deputy              │
│  Trigger: Status = "SupervisorApproved"                      │
│  Action: Email Deputy Director + Contributor                 │
├──────────────────────────────────────────────────────────────┤
│  Flow 3: Report Rejected - Notify and Route Back            │
│  Trigger: Status = "Rejected"                                │
│  Action: Email Contributor (with rejection reason)           │
│          If Deputy rejected → also email Supervisor          │
├──────────────────────────────────────────────────────────────┤
│  Flow 4: Report Approved - Finalize                         │
│  Trigger: Status = "Approved"                                │
│  Action: Email Contributor + Supervisor                      │
│          Mark Activity Completed                             │
│          Create AuditLog entry                               │
│          Create Notifications row                            │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  Flow 5: Monthly Reminder (Scheduled)                        │
│  Trigger: Recurrence — Every Monday at 08:00                 │
│  Action: Loop all active monthly activities                  │
│          If no report for current month → email owner        │
│  See: alerting-flow.md                                       │
└──────────────────────────────────────────────────────────────┘
```

**Key design rule:** Flows **never write** `Status` — the Power Apps buttons are the only writers, which prevents infinite trigger loops.

---

## Related Project Files

- `flow build instructions` — Detailed manual setup guide for 3 notification flows (including MonthlyReminder)
- `docs/power-automate/alerting-flow.md` — Complete reference for the MonthlyReminder scheduled flow pattern
- `flows/APP-MRMS-Approval.zip` — Importable package (4 flows)
- `flows/templates/APP-MRMS-Approval/` — Template source with `{{TOKEN}}` placeholders
- `tools/build_flow_zips.py` — Script to rebuild the package with real site URL and list GUIDs
- `docs/flow_import_validation_findings.md` — Validation errors encountered during import and their fixes

---

## 📚 Reference Documentation Index

| # | File | Description |
|---|------|-------------|
| 1 | [`cloud-flows-overview.md`](cloud-flows-overview.md) | Types of flows, core concepts, lifecycle, licensing, connectors |
| 2 | [`sharepoint-triggers-and-actions.md`](sharepoint-triggers-and-actions.md) | SharePoint connector: triggers, actions, OData filters, Person/Lookup access |
| 3 | [`expressions-and-functions.md`](expressions-and-functions.md) | Complete expressions/functions reference — strings, collections, logic, dates |
| 4 | [`expression-cheat-sheet.md`](expression-cheat-sheet.md) | **Quick reference** — 20 most-used expressions for this project |
| 5 | [`trigger-conditions.md`](trigger-conditions.md) | Trigger conditions, concurrency control, polling intervals, loop prevention |
| 6 | [`building-flows-manually.md`](building-flows-manually.md) | Step-by-step guide to build flows in the portal without Copilot |
| 7 | [`alerting-flow.md`](alerting-flow.md) | MonthlyReminder scheduled flow pattern — full reference with variations |
| 8 | [`flow-import-export.md`](flow-import-export.md) | Import/export package format, validation rules, rebuild script usage |
| 9 | [`definition-json-reference.md`](definition-json-reference.md) | `definition.json` structure for importable flows |
| 10 | [`troubleshooting.md`](troubleshooting.md) | Error codes, common errors with fixes, debugging techniques |

### How the files connect

```
  flow build instructions (this file's sibling)
       │
       ├── links to ──► expression-cheat-sheet.md (copy-paste while building)
       ├── links to ──► trigger-conditions.md (when adding trigger settings)
       ├── links to ──► sharepoint-triggers-and-actions.md (OData filters)
       ├── links to ──► expressions-and-functions.md (expression details)
       ├── links to ──► alerting-flow.md (MonthlyReminder deep dive)
       ├── links to ──► troubleshooting.md (when something breaks)
       ├── links to ──► flow-import-export.md (import via package)
       └── links to ──► definition-json-reference.md (JSON structure)

  flows/APP-MRMS-Approval.zip (importable package)
       │
       ├── built by ──► tools/build_flow_zips.py
       ├── validated against ──► docs/flow_import_validation_findings.md
       └── reference ──► definition-json-reference.md
```

---

*Extracted from: Microsoft Learn Power Automate documentation (August 2026)*
*Project: APP-MRMS (APP Monthly Reporting Management System)*
