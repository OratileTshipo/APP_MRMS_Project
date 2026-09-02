# Troubleshooting Power Automate Flows

Common errors, error codes, and their fixes.

---

## Quick Reference Table

| Error | Category | Most Likely Fix |
|-------|----------|-----------------|
| `InvalidTemplate` | Design-time | Fix expression syntax |
| `ExpressionEvaluationFailed` | Runtime | Add null checks, validate types |
| `ActionFailed` | Runtime | Check action outputs for API error |
| `FlowCheckerError` | Design-time | Fill required fields, fix connections |
| `InvalidConnection` | Connection | Re-authenticate the connection |
| `ConnectionNotConfigured` | Connection | Select or create a connection |
| `Unauthorized (401)` | Auth | Fix connection, rotate credentials |
| `Forbidden (403)` | Auth | Check DLP policies, permissions |
| `BadRequest (400)` | API | Validate input data format |
| `NotFound (404)` | API | Verify resource exists, update references |
| `TriggerConditionNotMet` | Trigger | Review trigger condition expression |
| `ActionTimedOut` | Timeout | Increase timeout in action settings |
| `DuplicateActionName` | Design-time | Rename one of the duplicate actions |
| `MissingRequiredProperty` | Design-time | Fill in required fields |
| `ContentConversionFailed` | Runtime | Use explicit type conversions |
| `WorkflowRunActionRepetitionQuotaExceeded` | Throttling | Filter data before looping |
| `DirectApiAuthorizationRequired` | Licensing | Assign premium license to caller |
| `FlowRunQuotaExceeded` | Throttling | Optimize action count, upgrade license |
| `ConnectionAuthorizationFailed` | Connection | Fix connection, re-authenticate |
| `OperationTimedOut` | Timeout | Set explicit timeouts, use relay pattern |

---

## Common Error Messages and Fixes

### "The requested operation is prohibited because it exceeds the list view threshold."
**Translation:** SharePoint Get Items is returning more than 5,000 items.

**Fix:**
- Add an OData filter to reduce results
- Use `$top=5000` with pagination
- Filter on an indexed column

---

### "Invalid type. Expected String but got Null."
**Translation:** A field you're referencing is empty (null) and the action expects text.

**Fix:**
- Wrap in `coalesce(field, '')` or `if(empty(field), '', field)`
- Add a Condition to check for null first

---

### "ActionFailed. An action failed. No dependent actions succeeded."
**Translation:** A Scope block failed, cancelling subsequent actions.

**Fix:**
- Find the specific action inside the Scope that failed first
- Fix that action

---

### "Flow run timed out."
**Translation:** The flow exceeded the 30-day maximum duration.

**Fix:**
- Redesign long-running flows
- Use a child flow for the long-running part
- Split into multiple flows with a status flag

---

### "ExpressionEvaluationFailed."
**Translation:** An expression has a syntax error or references a non-existent value.

**Fix:**
- Check expression syntax (misspelled function names, wrong parameter counts)
- Verify referenced steps actually executed
- Check for null values

---

### "The connection is not valid."
**Translation:** The connection was deleted or credentials expired.

**Fix:**
- Go to Connections → find the broken one → Fix connection
- Re-authenticate or create new connection

---

### "Nested flows are not supported in this context."
**Translation:** Calling a child flow from inside Apply to Each.

**Fix:**
- Move the child flow call outside the loop
- Pass the full array to the child flow and loop inside it

---

### "The template action names must be unique."
**Translation:** Two actions in the same flow have the same name.

**Fix:**
- Rename duplicate actions (action names must be globally unique across the entire flow)

---

## Flow Doesn't Trigger

### Symptoms
- No runs appear in run history
- Trigger shows as "waiting"

### Checklist
1. **Is the flow turned on?** Check flow status on the details page
2. **Trigger conditions match exactly?** Case-sensitive for Choice values
3. **SharePoint connection valid?** Go to Connections → SharePoint → check status
4. **Trigger event occurred?** Create a new test item and wait 5–10 minutes (polling interval)
5. **Flow suspended?** Check flow status — suspended flows stop triggering until fixed

---

## Emails Not Received

### Checklist
1. Check spam/junk folder
2. Verify Person column contains valid M365 accounts (not text email addresses)
3. Check Outlook connection in Power Automate → Connections
4. Review run history — click the email action to see if it succeeded
5. Check the `To` field — dynamic content may reference a null value

---

## "Column does not exist" Error

### Fix
1. Ensure column internal names match what you're using in expressions
2. Go to SharePoint list → List Settings → click the column → check the URL for the `Field=` parameter (internal name)
3. Special characters in column names: use internal name, not display name

---

## Flow Runs but Email Body is Empty

### Checklist
1. Dynamic content references match correct step names
2. If you renamed steps, dynamic content references may have broken — re-select them
3. Check expression syntax — missing `?` for null-safe access
4. Verify the upstream step actually returned data

---

## Supervisor Column is Empty

### Fix
Add a Condition step before sending:
1. Condition: `Supervisor Email is not equal to null`
2. If yes: Send to Supervisor
3. If no: Send to Programme Manager as fallback (or skip)

---

## SharePoint View Threshold (>5,000 items)

### Prevention
- Always use `filterQuery` on indexed columns
- Use `top` parameter to limit results
- For large lists, create indexed columns in SharePoint List Settings

### Example: Safe query with filter
```
filterQuery: "Active eq 1 and Frequency eq 'Monthly'"
top: 500
```

---

## Debugging Techniques

### 1. Use Compose Actions
Add Compose actions at key points to inspect intermediate values:
1. Add a Compose action
2. Set its input to the dynamic content you want to check
3. Run the flow
4. Check the Compose output in run history

### 2. Check Run History
1. Open the flow → Click **All runs**
2. Click on a specific run
3. Expand each action to see inputs/outputs
4. Look for red (failed) actions

### 3. Test Step by Step
1. Turn off the flow
2. Click **Test** → **Manually**
3. Perform the trigger action
4. Watch the flow execute in real-time
5. Check each action's result

### 4. Expression Debugging
1. Copy the expression to a text editor
2. Replace dynamic content references with sample values
3. Verify the expression evaluates correctly
4. Common issues: missing `?` for null-safe access, wrong field names

---

## Connection Failures

### Step 1: Is the flow turned on?
Check the flow details page.

### Step 2: Check connection status
1. Go to **My flows** → **Connections**
2. Find the connection (SharePoint, Outlook)
3. Check if it shows "Connected" or "Needs attention"
4. If broken: click **⋯** → **Fix connection**

### Step 3: Check DLP policies
1. Go to **Power Platform admin center**
2. Check Data Loss Prevention policies
3. Ensure the connectors used by your flow are in the same group

### Step 4: Re-authenticate
1. Go to **Connections**
2. Find the broken connection
3. Click **⋯** → **Fix connection**
4. Sign in again with your credentials

---

*Source: Microsoft Learn Power Automate — Troubleshoot cloud flow errors documentation*
