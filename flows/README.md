# APP-MRMS Approval Workflow Flows

Ready-to-import Power Automate package for the monthly report approval
workflow. One package, four flows:

| # | Flow | Fires when `MonthlyReports.Status` becomes |
|---|------|---------------------------------------------|
| 1 | Report Submitted - Notify Supervisor (APP-MRMS) | `Submitted` |
| 2 | Supervisor Approved - Route to Deputy (APP-MRMS) | `SupervisorApproved` |
| 3 | Report Rejected - Notify and Route Back (APP-MRMS) | `Rejected` (notifies Contributor/Supervisor based on who rejected) |
| 4 | Report Approved - Finalize (APP-MRMS) | `Approved` (email + notifications + marks Activity Completed/not active + AuditLog) |

## Before you import

1. **Add the `SupervisorApproved` status** to the `MonthlyReports` → `Status` choice column
   in SharePoint (currently: Draft / Submitted / Approved / Rejected / Escalated).
2. **Create at least one `APP_Users` row with Role = `DeputyDirectorME`** — flows 2 and 3
   resolve the Deputy Director's mailbox from this list.
3. **Replace the placeholder list GUIDs and site URL** (the shipped zip uses
   `1111…1111`-style placeholders and `https://nwpg.sharepoint.com/sites/APP-MRMS`).

## Rebuild the package with your values

```bash
python3 tools/build_flow_zips.py \
  --site-url "https://<your-tenant>.sharepoint.com/sites/APP-MRMS" \
  --monthlyreports  "<MonthlyReports list GUID>" \
  --activities      "<Activities list GUID>" \
  --notifications   "<Notifications list GUID>" \
  --auditlog        "<AuditLog list GUID>" \
  --users           "<APP_Users list GUID>" \
  --output flows/APP-MRMS-Approval.zip
```

Find list GUIDs: open the list → List settings → the browser URL contains
`?List=%7B<GUID>%7D`, or run `Get-PnPList -Identity '<name>' | Select Id`.

## Import

1. Power Automate (make.powerautomate.com) → **My flows** → **Import** → **Package (.zip)**.
2. Upload `flows/APP-MRMS-Approval.zip`.
3. **Review package content**: create/select the **SharePoint** connection
   (a user with Contribute on the site) and the **Office 365 Outlook** connection
   (a licensed mailbox account).
4. Choose **Update** if a flow already exists, or **New** otherwise.
5. After import, open each flow → **Turn on**.

## Design notes

- Flows never write `Status` — the Power Apps buttons (`scr_ReportSubmission`,
  `scr_ApprovalQueue`) are the only writers, which prevents infinite trigger loops.
- `scr_ApprovalQueue` must show `Status = Submitted` for Supervisors and
  `Status = SupervisorApproved` for the Deputy Director (add the second filter).
- Emails/notifications per decision:
  - Submitted → Supervisor (Flow 1)
  - SupervisorApproved → Deputy Director + Contributor (Flow 2)
  - Rejected by Supervisor → Contributor with reason (Flow 3, else branch)
  - Rejected by Deputy → Contributor + Supervisor with reason (Flow 3, then branch)
  - Approved (final) → Contributor + Supervisor; Activity set to `Completed` / `Active=false` (Flow 4)
- A `Notifications` row (in-app badge) is created alongside every email.

Templates live in `flows/templates/APP-MRMS-Approval/` (`{{SITE_URL}}`, `{{MR_GUID}}`,
`{{ACT_GUID}}`, `{{NOTIF_GUID}}`, `{{AUDIT_GUID}}`, `{{USERS_GUID}}` tokens).
