# APP-MRMS Flow Debugging Skill

## Purpose
Debug Power Automate approval flows that fire on MonthlyReports.Status changes.

## When to Use
- Flow fails to trigger
- Flow triggers but actions fail
- Emails not received
- Notifications not created
- AuditLog not written

## Flow Architecture

### Flow 1: Report Submitted → Notify Supervisor
- **Trigger:** MonthlyReports.Status = "Submitted"
- **Actions:** Email supervisor + Create notification + Write audit log
- **Prerequisite:** Status choice "Submitted" exists in MonthlyReports

### Flow 2: Supervisor Approved → Route to Deputy
- **Trigger:** MonthlyReports.Status = "SupervisorApproved"
- **Actions:** Email Deputy + Contributor + Create notification + Write audit log
- **Prerequisite:** Status choice "SupervisorApproved" exists in MonthlyReports

### Flow 3: Approved → Finalize
- **Trigger:** MonthlyReports.Status = "Approved"
- **Actions:** Email Contributor + Supervisor + Mark Activity Completed + Create notification + Write audit log
- **Prerequisite:** Status choice "Approved" exists in MonthlyReports

## Debugging Steps

### Step 1: Check Flow Status
1. Open https://make.powerautomate.com
2. Go to My flows
3. Check each flow is **Turned on** (green toggle)
4. Check **Run history** for recent runs

### Step 2: Check Trigger Conditions
1. Open the flow → Click the trigger
2. Verify the trigger is set to the correct list and site URL
3. Verify the condition matches the Status value exactly
4. Check if the trigger is polling (recurrence) or webhook

### Step 3: Check Connection References
1. Open the flow → Click **Connections** in the left panel
2. Verify SharePoint connection is valid (green checkmark)
3. Verify Office 365 Outlook connection is valid
4. If red X, click to re-authenticate

### Step 4: Check Action Inputs
1. Open the most recent failed run
2. Click each action to see inputs/outputs
3. Look for error messages in the Outputs section
4. Common errors:
   - **Invalid user email:** Check APP_Users list for correct email
   - **Column not found:** Verify column name in SharePoint list
   - **Permission denied:** Check connection user has Contribute access

### Step 5: Check Email Delivery
1. Check the Outlook connection's mailbox for sent emails
2. Check spam/junk folders
3. Verify the recipient email is correct in APP_Users list

### Step 6: Check Notifications
1. Open the Notifications list in SharePoint
2. Verify new rows are being created
3. Check the RecipientUser field matches the intended recipient

### Step 7: Check AuditLog
1. Open the AuditLog list in SharePoint
2. Verify new rows are being created
3. Check EntityType, EntityId, Action fields

## Common Issues

### Flow doesn't trigger
- **Cause:** Status choice value doesn't match trigger condition
- **Fix:** Verify the exact string in the choice column (case-sensitive)
- **Fix:** Add "SupervisorApproved" to MonthlyReports.Status if missing

### Flow triggers but actions fail
- **Cause:** Connection reference is invalid
- **Fix:** Re-authenticate the connection in Power Automate

### Email not received
- **Cause:** Recipient email is wrong or missing in APP_Users
- **Fix:** Verify APP_Users list has correct UserAccount for the role

### Infinite trigger loop
- **Cause:** Flow writes to the same Status column it triggers on
- **Fix:** Ensure flows only write to Notifications/AuditLog, not MonthlyReports.Status

### "SupervisorApproved" not found
- **Cause:** This choice value doesn't exist in MonthlyReports.Status
- **Fix:** Add "SupervisorApproved" to the Status choice column in SharePoint

## Flow Package Rebuild
```bash
python3 tools/build_flow_zips.py \
  --site-url "https://<tenant>.sharepoint.com/sites/APP-MRMS" \
  --monthlyreports "<MR-GUID>" \
  --activities "<ACT-GUID>" \
  --notifications "<NOTIF-GUID>" \
  --auditlog "<AUDIT-GUID>" \
  --users "<USERS-GUID>" \
  --output flows/APP-MRMS-Approval.zip
```

## Testing Checklist
- [ ] Submit a report → Supervisor receives email
- [ ] Supervisor approves → Deputy receives email
- [ ] Deputy approves → Contributor + Supervisor receive emails
- [ ] Reject → Contributor receives email with reason
- [ ] Notifications list has entries for each action
- [ ] AuditLog has entries for each action
- [ ] No infinite trigger loops
