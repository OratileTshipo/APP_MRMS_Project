# APP-MRMS Power Automate Flows - Implementation Plan

## Executive Summary

This document provides a comprehensive plan for building and deploying Power Automate flows for the APP-MRMS (Annual Performance Plan - Monthly Reporting Management System) approval workflow. The solution enables a multi-stage approval process with proper audit trails, notifications, and escalation mechanisms.

---

## 1. Research: Power Automate Import/Export Methods

### 1.1 Available Methods for Flow Deployment

#### Method A: Power Automate Portal Export/Import (RECOMMENDED)
**Process:**
1. Build flow in Development environment using Power Automate portal
2. Export as a **Solution Package** (.zip)
3. Import into Target environment via Power Automate portal
4. Re-map connections during import wizard

**Advantages:**
- ✅ Maintains all flow dependencies automatically
- ✅ Handles connection references properly
- ✅ Supported by Microsoft for production deployments
- ✅ Includes metadata for version tracking
- ✅ Minimal risk of import errors

**Disadvantages:**
- Requires manual export/import steps
- Not fully automated without additional tooling

#### Method B: Power Platform CLI (pac)
**Process:**
```bash
pac solution export --path ./solution.zip --name "APP-MRMS-Flows"
pac solution import --path ./solution.zip --activate-flows
```

**Advantages:**
- ✅ Scriptable and automatable
- ✅ Suitable for CI/CD pipelines
- ✅ Version controlled deployment

**Disadvantages:**
- Requires pac CLI installation and authentication
- Steeper learning curve
- May require Azure DevOps integration

#### Method C: Manual JSON Creation (NOT RECOMMENDED)
**Process:**
- Manually create `definition.json` and `connections.json`
- Package into .zip and import

**Advantages:**
- Full control over flow structure
- No dependency on portal

**Disadvantages:**
- ❌ High risk of syntax errors
- ❌ Missing hidden dependencies
- ❌ Connection mapping issues
- ❌ Not supported for production
- ❌ Microsoft may change internal schema without notice

### 1.2 Recommended Approach for APP-MRMS

**Primary Strategy: Hybrid Approach**

1. **Development Phase**: Build flows manually in Power Automate portal (Dev environment)
2. **Validation Phase**: Test thoroughly in Dev, fix all issues
3. **Export Phase**: Export as managed solution package (.zip)
4. **Documentation Phase**: Document all connection references and environment variables
5. **Import Phase**: Import into Production with connection re-mapping
6. **Verification Phase**: Run test scenarios to confirm functionality

**Why This Approach:**
- Balances ease of development with production reliability
- Minimizes import errors through validation
- Aligns with Microsoft's recommended ALM practices
- Suitable for government environments with strict change control

---

## 2. Solution Architecture

### 2.1 Flow Inventory

| # | Flow Name | Trigger Type | Purpose | Priority |
|---|-----------|--------------|---------|----------|
| 1 | **APP-MRMS-SubmitForApproval** | When item created/modified (MonthlyReports) | Initiates approval when contributor submits report | P0 |
| 2 | **APP-MRMS-SupervisorApproval** | When item modified (Status = Submitted) | Handles supervisor approve/reject actions | P0 |
| 3 | **APP-MRMS-DDMEApproval** | When item modified (Status = Pending DD M&E) | Handles Deputy Director M&E approve/reject | P0 |
| 4 | **APP-MRMS-SendNotifications** | When item created (Notifications list) | Sends email + creates in-app notification | P1 |
| 5 | **APP-MRMS-AuditLogger** | When item created/modified (all lists) | Captures audit trail in AuditLog list | P1 |
| 6 | **APP-MRMS-ApprovalTimeout** | Recurrence (Daily) | Escalates stalled approvals after timeout | P2 |
| 7 | **APP-MRMS-MonthlyReminders** | Recurrence (Monthly, 20th) | Reminds contributors of pending reports | P2 |
| 8 | **APP-MRMS-OverdueEscalation** | Recurrence (Daily) | Marks reports overdue and escalates | P2 |

### 2.2 SharePoint List Dependencies

All flows interact with the following SharePoint lists (confirmed in site):

| List Name | Key Columns | Usage |
|-----------|-------------|-------|
| **MonthlyReports** | Status, SubmissionDate, ReviewDate, RejectionReason, Contributor, Supervisor, ActivityID | Main entity for approval workflow |
| **Activities** | Active, Status, Frequency, ProgrammeID | Updated when reports approved |
| **APP_Users** | Role, Email, Directorate | Lookup for routing and permissions |
| **ReportComments** | MonthlyReport (Lookup), CommentText, Author, CommentDate | Stores rejection reasons |
| **Notifications** | RecipientUser, RelatedEntity, Message, IsRead, CreatedDate | In-app notification center |
| **AuditLog** | EntityType, EntityId, Action, FieldChanged, OldValue, NewValue, ActionBy, Reason | Immutable audit trail |

### 2.3 Approval State Machine

```
[Draft] 
   ↓ (Contributor submits)
[Submitted] → Pending Supervisor Approval
   ↓ (Supervisor approves)
[Pending DD M&E] → Pending Deputy Director Approval
   ↓ (DD M&E approves)
[Approved] → Activity marked Complete (if one-off)
   
[Submitted] → (Supervisor rejects) → [Rejected] → (Contributor corrects & resubmits) → [Submitted]
[Pending DD M&E] → (DD M&E rejects) → [Rejected] → (Contributor corrects & resubmits) → [Submitted]
```

**Status Values:**
- `Draft` - Initial state, editable
- `Submitted` - Pending supervisor review
- `Pending DD M&E` - Pending deputy director review
- `Approved` - Final approved state
- `Rejected` - Sent back for corrections
- `Overdue` - Past deadline without submission

---

## 3. Detailed Flow Specifications

### 3.1 Flow 1: APP-MRMS-SubmitForApproval

**Trigger:** When an item is created or modified (MonthlyReports list)

**Conditions:**
- Status changes to `Submitted`
- Previous status was `Draft` or `Rejected`

**Actions:**
1. Get item details (MonthlyReports)
2. Get Contributor details from APP_Users
3. Get Supervisor details from APP_Users (based on Activity/Programme)
4. Update MonthlyReports:
   - Set `SubmissionDate` = utcNow()
   - Set `Status` = `Submitted`
5. Create AuditLog entry:
   - EntityType: `MonthlyReport`
   - EntityId: `{ID}`
   - Action: `StatusChange`
   - FieldChanged: `Status`
   - OldValue: `{PreviousStatus}`
   - NewValue: `Submitted`
   - ActionBy: `{Modified By}`
6. Create Notifications item:
   - Title: `Report Submitted for Approval`
   - RecipientUser: `{Supervisor}`
   - RelatedEntity: `MonthlyReports:{ID}`
   - Message: `{Contributor} has submitted a report for activity: {ActivityTitle}`
   - IsRead: `false`
7. Send email to Supervisor:
   - Subject: `Action Required: Report Submission for {ActivityTitle}`
   - Body: Include link to approval queue, activity details, submission date
8. Lock form in Canvas App (handled via Status field check in app)

**Error Handling:**
- If Supervisor not found: Escalate to Programme Manager
- If email fails: Log error to AuditLog, continue with Notifications list

---

### 3.2 Flow 2: APP-MRMS-SupervisorApproval

**Trigger:** When an item is modified (MonthlyReports list)

**Conditions:**
- Status = `Submitted`
- Modified by user with Role = `Supervisor` or `ProgrammeManager`

**Branch Logic:**

#### Branch A: Approved
1. Validate approver is assigned Supervisor
2. Update MonthlyReports:
   - Set `Status` = `Pending DD M&E`
   - Set `ReviewDate` = utcNow()
   - Set `ReviewedBy` = `{Approver}`
3. Create AuditLog entry (StatusChange: Submitted → Pending DD M&E)
4. Get Deputy Director M&E details from APP_Users
5. Create Notifications item for DD M&E
6. Send email to DD M&E:
   - Subject: `Action Required: Report Approval for {ActivityTitle}`
   - Body: Include report details, contributor info, supervisor approval note

#### Branch B: Rejected
1. Get rejection reason from trigger inputs (or latest ReportComment)
2. Update MonthlyReports:
   - Set `Status` = `Rejected`
   - Set `RejectionReason` = `{Reason}`
   - Set `RejectedBy` = `{Approver}`
3. Create ReportComments item:
   - MonthlyReport: `{ID}`
   - CommentText: `{RejectionReason}`
   - Author: `{Approver}`
   - CommentDate: utcNow()
4. Create AuditLog entry:
   - Action: `StatusChange`
   - Reason: `{RejectionReason}`
5. Create Notifications item for Contributor
6. Send email to Contributor:
   - Subject: `Report Rejected: {ActivityTitle}`
   - Body: Include rejection reason, link to edit report, supervisor contact

**Concurrency Control:** Set to `1` to prevent race conditions

---

### 3.3 Flow 3: APP-MRMS-DDMEApproval

**Trigger:** When an item is modified (MonthlyReports list)

**Conditions:**
- Status = `Pending DD M&E`
- Modified by user with Role = `DeputyDirectorME`

**Branch Logic:**

#### Branch A: Approved
1. Validate approver role
2. Update MonthlyReports:
   - Set `Status` = `Approved`
   - Set `ApprovalDate` = utcNow()
   - Set `ApprovedBy` = `{Approver}`
3. Get related Activity details
4. Update Activity:
   - If Frequency = `Once-off`: Set `Status` = `Completed`, `Active` = `No`
   - If Frequency = `Monthly/Quarterly/Annual`: Mark specific period as complete
5. Create AuditLog entry (StatusChange: Pending DD M&E → Approved)
6. Create Notifications items for:
   - Contributor (approval confirmation)
   - Supervisor (notification of final approval)
7. Send emails to both parties
8. Trigger KPI roll-up calculation (separate flow or inline)

#### Branch B: Rejected
1. Get rejection reason
2. Update MonthlyReports:
   - Set `Status` = `Rejected`
   - Set `RejectionReason` = `{Reason}`
   - Set `RejectedBy` = `{Approver}`
3. Create ReportComments item (same as Flow 2)
4. Create AuditLog entry with Reason field
5. Create Notifications items for:
   - Contributor
   - Supervisor (inform of DD rejection)
6. Send emails to both parties with rejection details

**Note:** Rejection by DD M&E sends report back to `Submitted` state after contributor corrections, restarting full approval chain.

---

### 3.4 Flow 4: APP-MRMS-SendNotifications

**Trigger:** When an item is created (Notifications list)

**Purpose:** Centralized notification sender to avoid duplicate email logic across flows

**Actions:**
1. Get notification item details
2. Get recipient email from RecipientUser field
3. Parse RelatedEntity to extract:
   - Entity type (MonthlyReports/Activities/etc.)
   - Entity ID
   - Construct deep link to Canvas App screen
4. Send email:
   - To: `{RecipientEmail}`
   - Subject: `{Title}`
   - Body: `{Message}` + deep link button
5. Optional: Send Teams notification if user has Teams email
6. Log success/failure to AuditLog

**Benefits:**
- Single point of maintenance for email templates
- Consistent branding and formatting
- Easy to add new notification channels (SMS, Teams, etc.)

---

### 3.5 Flow 5: APP-MRMS-AuditLogger

**Trigger:** When an item is created or modified (Multiple lists)

**Lists Monitored:**
- MonthlyReports
- Activities
- Programmes
- Projects
- APP_Users
- ReportComments

**Logic:**
1. Detect change type (Create vs Modify)
2. For Modify actions:
   - Compare current vs previous values (using `triggerOutputs()['body']` vs `triggerOutputs()['headers']['x-ms-referrer-id']`)
   - Identify changed fields
3. For each changed field:
   - Create AuditLog item:
     - EntityType: `{ListName}`
     - EntityId: `{ItemID}`
     - Action: `Update`
     - FieldChanged: `{FieldName}`
     - OldValue: `{PreviousValue}`
     - NewValue: `{CurrentValue}`
     - ActionBy: `{Modified By}`
     - ActionDate: utcNow()
4. For Create actions:
   - Create single AuditLog item with Action = `Create`

**Performance Optimization:**
- Use scope to group related field changes
- Limit to critical fields only (avoid logging every metadata change)
- Consider batching multiple field changes into single AuditLog entry with JSON payload

**Security:**
- Flow runs with elevated privileges (service account)
- AuditLog list has restricted permissions (Read for users, Write for flow only)

---

### 3.6 Flow 6: APP-MRMS-ApprovalTimeout

**Trigger:** Recurrence (Daily at 8:00 AM SAST)

**Purpose:** Prevent approval bottlenecks when reviewers are unavailable

**Actions:**
1. Get all MonthlyReports where:
   - Status = `Submitted` OR `Pending DD M&E`
   - SubmissionDate < addDays(utcNow(), -3) (3 business days)
   - Not already escalated
2. For each item:
   - Check if first reminder sent (custom flag field)
   - If no: Send reminder email to current approver, set Reminder1Sent = true
   - If yes and < 5 days: Do nothing (wait)
   - If >= 5 business days:
     - Escalate to Programme Manager
     - Update MonthlyReports: EscalationLevel = 1
     - Create AuditLog entry: Action = `Escalation`
     - Send notification to Programme Manager and original approver
3. Log summary to AuditLog

**Configuration:**
- Timeout thresholds stored in separate Config list for easy adjustment
- Business days calculation excludes weekends and public holidays

---

### 3.7 Flow 7: APP-MRMS-MonthlyReminders

**Trigger:** Recurrence (Monthly, 20th day at 9:00 AM SAST)

**Purpose:** Proactive reminders for contributors to submit reports

**Actions:**
1. Get current Financial Year and Month
2. Get all Activities where:
   - Active = `Yes`
   - Frequency includes current month
   - No approved report exists for current period
3. Group by Contributor
4. For each Contributor:
   - Count pending activities
   - Get supervisor contact
   - Send email:
     - Subject: `Monthly Report Reminder: {Count} Activities Pending`
     - Body: List of pending activities, due date (25th), submission link
   - Create Notifications item for in-app bell
5. Send summary to Supervisors of contributors with >3 pending items

---

### 3.8 Flow 8: APP-MRMS-OverdueEscalation

**Trigger:** Recurrence (Daily at 5:00 PM SAST)

**Purpose:** Mark reports as overdue and initiate escalation

**Actions:**
1. Get all MonthlyReports where:
   - DueDate < utcNow()
   - Status NOT IN (`Approved`, `Overdue`)
2. For each item:
   - Update Status = `Overdue`
   - Calculate days overdue
   - If daysOverdue <= 2: Send warning to Contributor
   - If daysOverdue > 2 and <= 5: Escalate to Supervisor
   - If daysOverdue > 5: Escalate to Programme Manager + DD M&E
3. Create AuditLog entries for status changes
4. Send daily digest to Programme Managers with all overdue reports in their programmes

---

## 4. Environment Configuration

### 4.1 Environment Variables

Create these in Power Automate solution for easy environment switching:

| Variable Name | Type | Dev Value | Prod Value | Usage |
|---------------|------|-----------|------------|-------|
| `SharePointSiteURL` | String | `https://dev-site.sharepoint.com/sites/APPMRMS` | `https://nw-dpwr.sharepoint.com/sites/APPMRMS` | Target site |
| `MonthlyReportsListName` | String | `MonthlyReports_Dev` | `MonthlyReports` | List name |
| `ApprovalTimeoutDays` | Integer | `1` | `3` | Days before reminder |
| `EscalationTimeoutDays` | Integer | `2` | `5` | Days before escalation |
| `SupportEmail` | String | `dev-support@test.com` | `appmrms-support@dpwr.nwpg.gov.za` | Support contact |
| `CanvasAppDeepLinkBase` | String | `https://apps.powerapps.com/play/dev-app-id` | `https://apps.powerapps.com/play/prod-app-id` | Deep link prefix |

### 4.2 Connection References

| Connection Name | Connector | Purpose |
|-----------------|-----------|---------|
| `SharePoint-APP-MRMS` | SharePoint | All list operations |
| `Office365-Outlook` | Office 365 Outlook | Email notifications |
| `AzureAD-APP-MRMS` | Azure AD | User lookup (optional) |

**Important:** During import, these must be re-mapped to production connections.

### 4.3 Security Roles

| Role | Permissions |
|------|-------------|
| **Flow Owner** | Full control over flows, can modify and re-export |
| **Flow Runner** | Service account that executes flows (minimum: Read on all lists, Write on MonthlyReports/Notifications/AuditLog/ReportComments) |
| **Auditor** | Read-only on AuditLog list |

---

## 5. Testing Strategy

### 5.1 Unit Testing

Test each flow independently with mock data:

| Test Case | Input | Expected Output | Pass/Fail |
|-----------|-------|-----------------|-----------|
| TC-001 | Submit report with valid data | Status = Submitted, Supervisor notified | ☐ |
| TC-002 | Supervisor approves | Status = Pending DD M&E, DD notified | ☐ |
| TC-003 | Supervisor rejects with reason | Status = Rejected, Comment created, Contributor notified | ☐ |
| TC-004 | DD M&E approves | Status = Approved, Activity completed, both notified | ☐ |
| TC-005 | DD M&E rejects | Status = Rejected, Comments to both parties | ☐ |
| TC-006 | Timeout trigger (3 days) | Reminder sent to approver | ☐ |
| TC-007 | Timeout trigger (5 days) | Escalation to Programme Manager | ☐ |
| TC-008 | Monthly reminder (20th) | Emails to contributors with pending items | ☐ |

### 5.2 Integration Testing

Test end-to-end scenarios:

| Scenario | Steps | Validation |
|----------|-------|------------|
| Happy Path | Submit → Approve (Supervisor) → Approve (DD) | Activity marked complete, all notifications sent, audit trail complete |
| Rejection Loop | Submit → Reject → Correct → Resubmit → Approve → Approve | Proper status transitions, comments preserved, notifications at each step |
| Timeout Escalation | Submit → Wait 6 days (no action) | Escalation emails sent, AuditLog shows escalation events |
| Concurrent Submissions | Multiple contributors submit simultaneously | No race conditions, all items processed correctly |

### 5.3 User Acceptance Testing (UAT)

Involve actual users from each role:
- **Contributors**: Verify submission process, rejection feedback clarity
- **Supervisors**: Test approval queue, email notifications, mobile experience
- **Deputy Director M&E**: Validate executive view, bulk approval options
- **Administrators**: Confirm audit logs, escalation triggers, error handling

---

## 6. Deployment Procedure

### 6.1 Pre-Deployment Checklist

- [ ] All flows tested in Dev environment
- [ ] Environment variables configured
- [ ] Connection references documented
- [ ] SharePoint lists created in Prod with identical schema
- [ ] Security groups configured in Prod
- [ ] Backup of existing Prod flows (if any)
- [ ] Change request approved (if required by governance)

### 6.2 Export from Dev

1. Navigate to Power Automate portal (dev environment)
2. Select all 8 flows (use Ctrl+click)
3. Click **Export** → **Package**
4. Choose **Managed** (recommended for production)
5. Add metadata:
   - Publisher: `APP-MRMS Team`
   - Version: `1.0.0.0`
   - Description: `APP-MRMS Approval Workflows Phase 2`
6. Download `.zip` package

### 6.3 Import to Prod

1. Navigate to Power Automate portal (prod environment)
2. Click **Import** → **Upload package**
3. Select downloaded `.zip` file
4. **Import Setup**:
   - Select **Update existing** if flows exist, otherwise **Create as new**
   - Map environment variables to prod values
   - **Re-map connections**:
     - Select prod SharePoint connection
     - Select prod Office 365 Outlook connection
5. Click **Import**
6. Wait for completion (monitor status)

### 6.4 Post-Import Validation

1. Verify all flows show **On** status
2. Check flow run history for initial test runs
3. Manually trigger each flow once with test data
4. Verify:
   - Emails sent successfully
   - SharePoint items updated correctly
   - AuditLog entries created
   - Notifications appear in app
5. Test Canvas App integration (form locking, notification bell)

### 6.5 Rollback Plan

If import fails or flows malfunction:
1. Document error messages
2. Export failed package for analysis
3. Re-import previous stable version (if exists)
4. If no previous version: Delete partially imported flows, fix issues in Dev, re-export
5. Communicate downtime to users if necessary

---

## 7. Maintenance & Monitoring

### 7.1 Ongoing Monitoring

| Metric | Threshold | Alert Method |
|--------|-----------|--------------|
| Flow failure rate | > 5% per week | Email to admin |
| Average approval time | > 5 days | Weekly report |
| Overdue reports | > 10% of total | Dashboard alert |
| AuditLog growth | > 1000 items/day | Storage warning |

### 7.2 Scheduled Reviews

- **Weekly**: Review flow run history for failures
- **Monthly**: Analyze approval metrics, adjust timeouts if needed
- **Quarterly**: Review audit logs for anomalies
- **Annually**: Full flow documentation update, schema review

### 7.3 Version Control

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | TBD | Initial release | [Your Name] |
| 1.0.1 | TBD | Bug fixes, timeout adjustments | |
| 1.1.0 | TBD | Add bulk approval feature | |

---

## 8. Risk Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Import errors due to connection mismatch | High | Medium | Document all connections, use environment variables |
| Flow throttling due to high volume | Medium | Low | Implement batching, use concurrency controls |
| Email delivery failures | Medium | Low | Fallback to Notifications list, retry logic |
| SharePoint list schema changes | High | Low | Version control list schemas, change management process |
| Approver unavailability causing bottlenecks | High | Medium | Timeout/escalation logic, delegate approval feature |
| AuditLog list grows too large | Medium | High | Archive old entries annually, implement retention policy |

---

## 9. Success Criteria

The implementation will be considered successful when:

- ✅ All 8 flows imported without errors
- ✅ End-to-end approval process completes in < 2 minutes per stage
- ✅ 100% of approval actions generate audit trail entries
- ✅ Email notifications delivered within 1 minute of trigger
- ✅ In-app notifications appear in real-time
- ✅ Timeout escalations trigger correctly after configured periods
- ✅ Zero data loss during rejection/resubmission cycles
- ✅ Forms properly lock during pending approval states
- ✅ Activities correctly marked as complete upon final approval
- ✅ All UAT scenarios pass with stakeholder sign-off

---

## 10. Next Steps

### Immediate Actions:
1. **Review this plan** with stakeholders (Programme Managers, IT Admin, DD M&E)
2. **Confirm SharePoint list schemas** match specifications
3. **Set up Dev environment** with test data
4. **Build Flow 1 (SubmitForApproval)** as proof of concept
5. **Validate import/export process** with test package

### Timeline Estimate:
| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Plan Review & Sign-off | 2-3 days | Stakeholder availability |
| Dev Environment Setup | 1 day | IT support |
| Flow Development (all 8) | 5-7 days | Completed setup |
| Testing & Bug Fixes | 3-4 days | Development complete |
| UAT & Adjustments | 3-5 days | Test sign-off |
| Production Deployment | 1 day | Change approval |
| **Total** | **15-21 days** | |

---

## Appendix A: Sample JSON Structures

### A.1 MonthlyReports Item Structure
```json
{
  "ID": 1234,
  "Title": "Q3 Vehicle Procurement Report",
  "ActivityID": 567,
  "Contributor": {"Email": "user@gov.za", "DisplayName": "John Doe"},
  "Status": "Submitted",
  "SubmissionDate": "2025-01-15T10:30:00Z",
  "Supervisor": {"Email": "supervisor@gov.za", "DisplayName": "Jane Smith"},
  "RejectionReason": "",
  "RejectedBy": null,
  "ReviewDate": null,
  "ApprovalDate": null,
  "IsOverdue": false,
  "EscalationLevel": 0
}
```

### A.2 AuditLog Entry Structure
```json
{
  "EntityType": "MonthlyReport",
  "EntityId": "1234",
  "Action": "StatusChange",
  "FieldChanged": "Status",
  "OldValue": "Draft",
  "NewValue": "Submitted",
  "ActionBy": {"Email": "user@gov.za", "DisplayName": "John Doe"},
  "ActionDate": "2025-01-15T10:30:00Z",
  "Reason": ""
}
```

### A.3 Notifications Item Structure
```json
{
  "Title": "Report Submitted for Approval",
  "RecipientUser": {"Email": "supervisor@gov.za", "DisplayName": "Jane Smith"},
  "RelatedEntity": "MonthlyReports:1234",
  "Message": "John Doe has submitted a report for activity: Q3 Vehicle Procurement",
  "IsRead": false,
  "CreatedDate": "2025-01-15T10:30:05Z"
}
```

---

## Appendix B: Power Automate Expression Reference

### Common Expressions Used

```powerfx
// Get current UTC timestamp
utcNow()

// Add days to current date
addDays(utcNow(), 3)

// Format date for display
formatDateTime(utcNow(), 'yyyy-MM-dd HH:mm')

// Conditional logic
if(equals(triggerBody()?['Status'], 'Submitted'), 'Approve', 'Reject')

// Get manager from Office 365
outputs('Get_manager_(V2)')?['body/mail']

// Construct deep link
concat(variables('CanvasAppDeepLinkBase'), '?screen=ScreenApprovalQueue&reportId=', triggerBody()?['ID'])

// Business days calculation (custom function)
// Note: Requires premium connector or custom code
```

---

**Document Version:** 1.0  
**Last Updated:** 2025-01-15  
**Author:** APP-MRMS Development Team  
**Reviewers:** [Pending]  

---

## Confirmation

I have completed the comprehensive implementation plan documentation. This file (`FLOW_IMPLEMENTATION_PLAN.md`) contains:

✅ **Research** on Power Automate import/export methods with recommended approach  
✅ **Complete architecture** for 8 flows with detailed specifications  
✅ **SharePoint list dependencies** and schema requirements  
✅ **Approval state machine** with all transitions  
✅ **Step-by-step flow logic** including error handling  
✅ **Environment configuration** with variables and connections  
✅ **Testing strategy** covering unit, integration, and UAT  
✅ **Deployment procedure** with export/import steps  
✅ **Risk mitigation** and rollback plans  
✅ **Success criteria** for validation  

**Should I proceed with building the actual Power Automate flow files based on this plan?** 

Note: Since Power Automate flows cannot be directly created as importable files outside the Power Automate portal without risking errors, my recommendation is to:

1. **Option A (Recommended)**: Use this plan to manually build flows in Power Automate Dev portal, then export as validated package
2. **Option B**: Create ARM template files for enterprise deployment (requires Azure setup)
3. **Option C**: Generate detailed step-by-step build instructions for each flow that a developer can follow

Which approach would you like me to take for the actual implementation?
