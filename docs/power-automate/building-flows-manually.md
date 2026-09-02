# Building Flows Manually in Power Automate

Step-by-step guide for creating cloud flows in the Power Automate portal without Copilot.

---

## Prerequisites

- Microsoft 365 licence with Power Automate access
- SharePoint site with target lists already created
- Lists have the required columns (see [sharepoint-triggers-and-actions.md](sharepoint-triggers-and-actions.md))
- User has Contribute permission on the SharePoint site
- User has a licensed Office 365 mailbox (for Outlook connector)

---

## Step 1: Create the Flow

1. Go to **https://make.powerautomate.com**
2. Click **+ Create** in the left sidebar
3. Select flow type:
   - **Automated cloud flow** — for event-triggered flows (APP-MRMS Flows 1–4)
   - **Scheduled cloud flow** — for recurring flows (MonthlyReminder)
4. Enter flow name (e.g., `APP-MRMS Report Submitted Notify Supervisor`)
5. For automated flows: search for and select the trigger (e.g., `When an item is created or modified` — SharePoint)
6. Click **Create**

---

## Step 2: Configure the Trigger

1. **Site Address:** Select your SharePoint site
2. **List Name:** Select the target list
3. Click **⋯** → **Settings** → **Trigger Conditions**
4. Add trigger condition expression:
   ```
   @equals(triggerBody()?['Status/Value'], 'Submitted')
   ```
5. Set **Concurrency Control** to **Off** (for sequential processing)
6. Click **Done**

---

## Step 3: Add Actions

### Get Items (SharePoint)
1. Click **+ New step** → Search `Get items` (SharePoint)
2. Configure:
   - **Site Address:** Same SharePoint site
   - **List Name:** Target list
   - **Filter Query:** OData expression (see [sharepoint-triggers-and-actions.md](sharepoint-triggers-and-actions.md))
   - **Top Count:** Set if needed (e.g., `1` for single lookup)

### Condition
1. Click **+ New step** → Search `Condition`
2. Configure the condition:
   - Left field: Dynamic content or expression
   - Operator: `is equal to`, `contains`, etc.
   - Right field: Value to compare
3. **If yes** branch: Add actions for true case
4. **If no** branch: Add actions for false case

### Send Email (Office 365 Outlook)
1. Click **+ New step** → Search `Send an email (V2)`
2. Configure:
   - **To:** Dynamic content (e.g., `Supervisor Email` from Get items)
   - **Subject:** Text with dynamic content expressions
   - **Body:** HTML (click `</>` to switch to HTML mode)
   - **Importance:** `High` or `Normal`

### Apply to Each
1. Click **+ New step** → Search `Apply to Each`
2. **Select an output from previous steps:** Click → select `value` from Get items
3. Inside the loop: Add actions that reference `items('Apply_to_each')` for current item

---

## Step 4: Write Expressions

### Access Dynamic Content
1. Click in a text field
2. Click **Dynamic content** in the popup
3. Select the value from a previous step

### Write Expressions
1. Click in a text field
2. Click **Expression** in the popup
3. Type the expression
4. Click **OK**

### Common Expression Patterns for APP-MRMS

**Access trigger body fields:**
```
triggerBody()?['Title']
triggerBody()?['Status']?['Value']
triggerBody()?['SubmittedBy']?['Email']
triggerBody()?['Activity']?['Value']
```

**Access action outputs:**
```
body('Get_items')?['value']
body('Get_activity')?['Supervisor']?['Email']
```

**Access Apply to Each items:**
```
items('Apply_to_each')?['Title']
items('Apply_to_each')?['ActivityOwner']?['Email']
```

**Format date:**
```
formatDateTime(utcNow(), 'MMMM yyyy')
```

**Check if empty:**
```
equals(length(body('Get_items')?['value']), 0)
```

---

## Step 5: HTML Email Body

Click the `</>` icon in the email body field to switch to HTML mode.

### Basic HTML Email Template
```html
<p><strong>A monthly report has been submitted for your review.</strong></p>
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; font-family:Segoe UI, Arial, sans-serif;">
  <tr><td style="background:#f0f0f0;"><strong>Report</strong></td><td>@{triggerBody()?['Title']}</td></tr>
  <tr><td style="background:#f0f0f0;"><strong>Activity</strong></td><td>@{triggerBody()?['Activity']?['Value']}</td></tr>
  <tr><td style="background:#f0f0f0;"><strong>Status</strong></td><td>@{triggerBody()?['Status']?['Value']}</td></tr>
  <tr><td style="background:#f0f0f0;"><strong>Submitted By</strong></td><td>@{triggerBody()?['SubmittedBy']?['DisplayName']}</td></tr>
</table>
<p>Please review this report in the <strong>APP-MRMS</strong> application.</p>
<p><em>This is an automated notification from the APP Monthly Reporting Management System.</em></p>
```

---

## Step 6: Save and Test

1. Click **Save**
2. Click **Test** → **Manually** → **Test**
3. Perform the trigger action in SharePoint (e.g., change Status to "Submitted")
4. Wait for the flow to complete (green checkmarks = success)
5. Check the target email inbox
6. Review run history for any errors

---

## Step 7: Turn On

After successful testing:
1. Click **Turn on** in the flow details page
2. The flow is now active and will trigger automatically

---

## Tips

- **Save frequently** — Ctrl+S in the designer
- **Test with real data** — Create test items in SharePoint before testing
- **Check run history** — After testing, review each action's inputs/outputs
- **Use Compose actions** — Add Compose steps to inspect intermediate values
- **Copy complex expressions** — Save expression text in a separate file before saving the flow
- **Rename actions** — Give actions descriptive names (e.g., `Get_activity` instead of `Get items`) for easier debugging

---

## APP-MRMS Flow Checklist

For each flow, verify:

- [ ] Trigger is set to the correct list (`MonthlyReports`)
- [ ] Trigger condition matches the correct `Status` value
- [ ] Concurrency control is **Off**
- [ ] Get Items filter queries reference correct list GUIDs
- [ ] Email recipients use Person column `Email` field
- [ ] HTML email body includes all required fields
- [ ] No action writes back to `Status` (prevents infinite loops)
- [ ] All connections (SharePoint, Outlook) are configured
- [ ] Flow has been tested successfully
- [ ] Flow is turned **On**

---

*Source: Microsoft Learn Power Automate — Create flows documentation*
