# Power Automate — Microsoft Best Practices for APP-MRMS

**Source:** Microsoft Learn + Verified Working Examples  
**Purpose:** Reference for building reliable, efficient approval flows

---

## 1. Flow Design Principles

### 1.1 Single Responsibility
- Each flow should do ONE thing
- One flow per status transition
- Separate notification flows from data update flows

### 1.2 Idempotency
- Flows should handle being triggered multiple times safely
- Use conditions to check if action is needed
- Don't assume state from previous runs

### 1.3 Failure Isolation
- Use Scope actions for try/catch patterns
- Log errors to AuditLog
- Don't let one failure cascade

---

## 2. Trigger Best Practices

### 2.1 Use "When an item is modified" for Status Changes
```json
{
  "type": "OpenApiConnection",
  "operationId": "GetOnChangedItems",
  "inputs": {
    "parameters": {
      "changeType": "Modified"
    }
  }
}
```

### 2.2 Set Appropriate Recurrence
- **3 minutes** for approval workflows (balanced responsiveness vs API limits)
- **5 minutes** for less time-sensitive notifications
- **1 minute** only for critical real-time needs

### 2.3 Use splitOn for Array Triggers
```json
"splitOn": "@triggerOutputs()?['body/value']"
```
- Processes each item individually
- Prevents batch failures

---

## 3. Condition Best Practices

### 3.1 Always Check Status Before Acting
```json
{
  "type": "If",
  "expression": {
    "and": [
      {
        "equals": [
          "@triggerBody()?['Status/Value']",
          "Submitted"
        ]
      }
    ]
  }
}
```

### 3.2 Use Specific Conditions
- ❌ `contains(triggerBody()?['Status'], 'Submit')`
- ✅ `equals(triggerBody()?['Status/Value'], 'Submitted')`

### 3.3 Check for Required Fields
```json
{
  "and": [
    { "equals": ["@triggerBody()?['Status/Value']", "Submitted"] },
    { "not": ["@empty(triggerBody()?['SubmittedBy/EMail'])"] }
  ]
}
```

---

## 4. Action Best Practices

### 4.1 Use runAfter for Sequential Execution
```json
{
  "Notify_Supervisor": {
    "runAfter": {
      "Get_activity": ["Succeeded"]
    }
  }
}
```

### 4.2 Parallel Actions When Possible
```json
{
  "runAfter": {},
  "type": "Parallel"
}
```

### 4.3 Use Compose for Complex Expressions
```json
{
  "Compose_EmailBody": {
    "type": "Compose",
    "inputs": "@{concat('Report ', triggerBody()?['ID'], ' was approved by ', triggerBody()?['ReviewedBy/Value'])}"
  }
}
```

### 4.4 Limit Apply to Each
- Process max 100 items per run
- Use pagination for larger sets
- Consider batch operations

---

## 5. Loop Prevention

### 5.1 Never Write to Triggering Column
- ❌ Flow writes to Status → triggers itself
- ✅ Flow writes to Notifications/AuditLog only

### 5.2 Exception: Write to Related Lists
- Flow 4 can update Activity (not MonthlyReports)
- Activity is a different list, no loop risk

### 5.3 Use Markers for Flow-Initiated Changes
```json
{
  "condition": {
    "not": {
      "equals": ["@triggerBody()?['ModifiedBy']", "FlowSystem"]
    }
  }
}
```

---

## 6. Error Handling

### 6.1 Scope Actions for Try/Catch
```json
{
  "Try": {
    "type": "Scope",
    "actions": {
      "Send_Email": { ... }
    }
  },
  "Catch": {
    "type": "Scope",
    "runAfter": {
      "Try": ["Failed"]
    },
    "actions": {
      "Log_Error": { ... }
    }
  }
}
```

### 6.2 Configure Run After
```json
{
  "runAfter": {
    "PreviousAction": ["Succeeded", "Failed", "TimedOut"]
  }
}
```

### 6.3 Retry Policies
```json
{
  "retryPolicy": {
    "type": "exponential",
    "count": 3,
    "interval": "PT10S",
    "minimumInterval": "PT5S",
    "maximumInterval": "PT1H"
  }
}
```

---

## 7. Performance Optimization

### 7.1 Minimize API Calls
- Fetch related data once, reuse in multiple actions
- Use Compose to store intermediate results
- Batch create operations when possible

### 7.2 Use Variables for Repeated Values
```json
{
  "Set_varSiteUrl": {
    "type": "SetVariable",
    "name": "varSiteUrl",
    "value": "@triggerBody()?['{SiteURL}']"
  }
}
```

### 7.3 Avoid Nested Conditions
- Flatten logic where possible
- Use parallel branches
- Keep conditions simple

---

## 8. Security Best Practices

### 8.1 Don't Hardcode Credentials
- Use connection references
- Use Azure Key Vault for secrets
- Use environment variables

### 8.2 Least Privilege
- Flows run as the connection owner
- Use service accounts for production
- Limit permissions to required lists

### 8.3 Audit Everything
- Log all status changes to AuditLog
- Record who did what and when
- Include reason for changes

---

## 9. Testing Checklist

### 9.1 Unit Testing
- [ ] Test each status transition individually
- [ ] Test with missing required fields
- [ ] Test with invalid data
- [ ] Test with concurrent modifications

### 9.2 Integration Testing
- [ ] Test full approval workflow end-to-end
- [ ] Test rejection and resubmission
- [ ] Test email delivery
- [ ] Test notification creation

### 9.3 Performance Testing
- [ ] Test with 100+ items
- [ ] Test with large attachments
- [ ] Test with complex expressions
- [ ] Monitor API throttling

---

## 10. Monitoring and Maintenance

### 10.1 Run History
- Check run history daily for first week
- Monitor for failed runs
- Review action durations

### 10.2 Alerting
- Set up error alerts
- Monitor for infinite loops
- Track email delivery failures

### 10.3 Documentation
- Document flow purpose and logic
- Record connection owners
- Maintain troubleshooting guide

---

## 11. APP-MRMS Specific Rules

### 11.1 Status Values
| Status | Meaning | Flow Trigger |
|---|---|---|
| `Draft` | Not submitted | None |
| `Submitted` | Awaiting Supervisor | Flow 1 |
| `SupervisorApproved` | Awaiting Deputy | Flow 2 |
| `Approved` | Final approval | Flow 4 |
| `Rejected` | Returned to Contributor | Flow 3 |

### 11.2 Email Recipients
| Event | Recipients |
|---|---|
| Submitted | Supervisor |
| SupervisorApproved | Deputy + Contributor |
| Approved | Contributor + Supervisor |
| Rejected (by Supervisor) | Contributor |
| Rejected (by Deputy) | Contributor + Supervisor |

### 11.3 Side Effects
| Action | Creates |
|---|---|
| Every status change | AuditLog entry |
| Every email | Notification entry |
| Final approval | Activity → Completed |
