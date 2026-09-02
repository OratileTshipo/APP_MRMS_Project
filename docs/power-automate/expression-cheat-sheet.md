# Expression Cheat Sheet — APP-MRMS

The 20 most-used Power Automate expressions for this project, with copy-paste examples.

---

## Trigger Body Access

| # | Expression | Returns | Example Value |
|---|-----------|---------|---------------|
| 1 | `triggerBody()?['Title']` | Report / Activity ID | `ICTM-RP-0001` |
| 2 | `triggerBody()?['Status']?['Value']` | Choice column value | `Submitted` |
| 3 | `triggerBody()?['Activity']?['Value']` | Lookup display value | `ICMTS-AC-0001` |
| 4 | `triggerBody()?['SubmittedBy']?['Email']` | Person column email | `john@org.com` |
| 5 | `triggerBody()?['SubmittedBy']?['DisplayName']` | Person column name | `John Doe` |

---

## Action Output Access

| # | Expression | Returns | Example Value |
|---|-----------|---------|---------------|
| 6 | `body('Get_activity')?['Supervisor']?['Email']` | Supervisor email from Get Item | `sarah@org.com` |
| 7 | `body('Get_items')?['value']` | Array of items from Get Items | `[{"Title":"..."},...]` |
| 8 | `length(body('Get_items')?['value'])` | Count of items in array | `0`, `3` |

---

## Apply to Each (Loop) Access

| # | Expression | Returns | Example Value |
|---|-----------|---------|---------------|
| 9 | `items('Apply_to_each')?['Title']` | Current item's Title/ID | `ICMTS-AC-0001` |
| 10 | `items('Apply_to_each')?['ActivityOwner']?['Email']` | Owner email | `jane@org.com` |
| 11 | `items('Apply_to_each')?['Supervisor']?['Email']` | Supervisor email | `sarah@org.com` |
| 12 | `items('Apply_to_each')?['DueDate']` | Due date | `2026-09-15` |

---

## Date / Formatting

| # | Expression | Returns | Example Value |
|---|-----------|---------|---------------|
| 13 | `formatDateTime(utcNow(), 'MMMM')` | Current month name | `August` |
| 14 | `formatDateTime(utcNow(), 'MMMM yyyy')` | Month + year | `August 2026` |
| 15 | `addDays(utcNow(), 7)` | Date 7 days from now | `2026-09-03T...` |

---

## Conditions

| # | Expression | Returns | Use In |
|---|-----------|---------|--------|
| 16 | `equals(triggerBody()?['Status']?['Value'], 'Submitted')` | `true` / `false` | Trigger conditions |
| 17 | `equals(length(body('Get_items')?['value']), 0)` | `true` if no items found | Condition (no report?) |
| 18 | `not(empty(triggerBody()?['SubmittedBy']?['Email']))` | `true` if email exists | Condition (recipient exists?) |

---

## String Building

| # | Expression | Returns | Use Case |
|---|-----------|---------|----------|
| 19 | `concat('Report: ', triggerBody()?['Title'], ' — ', triggerBody()?['ReportingMonth']?['Value'])` | Combined string | Email subject |
| 20 | `coalesce(triggerBody()?['SupervisorRejectionReason'], 'No reason provided')` | Value or fallback | Null-safe text |

---

## Copy-Paste Blocks

### Trigger Condition — Check Status Value
```
@equals(triggerBody()?['Status']?['Value'], 'Submitted')
```
Replace `Status` with `ReportStatus`, `SubmissionStatus`, etc. Replace `'Submitted'` with the target value.

### OData Filter — Current Month Reports for an Activity
```
Activity eq '@{items('Apply_to_each')?['Title']}' and ReportingMonth eq '@{formatDateTime(utcNow(), 'MMMM')}'
```

### Condition — No Reports Found
Expression: `@length(body('Get_items')?['value'])`
Operator: `is equal to`
Value: `0`

### Condition — Recipient Email Not Null
Expression: `@not(empty(body('Get_activity')?['Supervisor']?['Email']))`
Operator: `is equal to`
Value: `true`

### Email Subject — Report Submitted
```
Report submitted: @{triggerBody()?['Title']} — @{triggerBody()?['ReportingMonth']?['Value']}
```

### Email Subject — Reminder
```
Reminder: @{items('Apply_to_each')?['Title']} — @{items('Apply_to_each')?['ActivityShortDescription']} due @{items('Apply_to_each')?['DueDate']}
```

---

## Syntax Rules

| Rule | Example |
|------|---------|
| Standalone expression: starts with `@` | `@triggerBody()?['Title']` |
| Inline with text: wrap in `@{}` | `"Report @{triggerBody()?['Title']} sent"` |
| Null-safe access: use `?` before property | `triggerBody()?['Field']?['SubField']` |
| Choice column: access `.Value` | `triggerBody()?['Status']?['Value']` |
| Person column: access `.Email` | `triggerBody()?['SubmittedBy']?['Email']` |
| Lookup column: access `.Value` or `.Id` | `triggerBody()?['Activity']?['Value']` |
| Loop item: use `items('loop_name')` | `items('Apply_to_each')?['Title']` |
| Action output: use `body('action_name')` | `body('Get_items')?['value']` |

---

*Quick reference for the APP-MRMS Power Automate flows*
