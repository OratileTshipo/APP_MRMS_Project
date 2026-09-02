# Expressions and Functions Reference

Power Automate expressions use the Azure Logic Apps Workflow Definition Language. This is the complete reference for writing conditions, data transforms, and dynamic content.

---

## Syntax Basics

### Expression Format
Every expression starts with `@` and can reference functions, trigger outputs, or action outputs:

```javascript
@functionName(parameter1, parameter2)           // Function call
@triggerBody()?['FieldName']                    // Access trigger data
@body('Action_Name')?['FieldName']              // Access action output
@variables('VariableName')                      // Access a variable
```

### Interpolation (inline with text)
When an expression appears **inside plain text**, use `@{}` curly braces:

```
Correct:  "Report @{triggerBody()?['Title']} submitted"
Incorrect: "Report @triggerBody()?['Title'] submitted"
```

### Standalone expressions
When the expression **is the entire value**, no curly braces needed:

```
@equals(triggerBody()?['Status/Value'], 'Submitted')
@length(body('Get_items')?['value'])
```

---

## Trigger and Action References

### Trigger Body
```javascript
triggerBody()                                    // Entire trigger body
triggerBody()?['FieldName']                      // Specific field
triggerBody()?['Status']?['Value']               // Choice column value
triggerBody()?['SubmittedBy']?['Email']          // Person column email
triggerBody()?['Activity']?['Value']             // Lookup column display value
```

### Action Outputs
```javascript
body('Action_Name')                              // Entire output
body('Action_Name')?['FieldName']                // Specific field
body('Get_items')?['value']                      // Array of items
first(body('Get_items')?['value'])               // First item
length(body('Get_items')?['value'])              // Count of items
```

### Apply to Each Items
```javascript
items('Apply_to_each')                          // Current item
items('Apply_to_each')?['Title']                // Current item's field
```

---

## String Functions

| Function | Syntax | Description | Example Result |
|----------|--------|-------------|----------------|
| `concat` | `concat('a','b')` | Join strings | `"ab"` |
| `length` | `length('hello')` | String length | `5` |
| `toLower` | `toLower('HELLO')` | Lowercase | `"hello"` |
| `toUpper` | `toUpper('hello')` | Uppercase | `"HELLO"` |
| `trim` | `trim(' hi ')` | Remove whitespace | `"hi"` |
| `replace` | `replace('a-b','-','_')` | Replace substring | `"a_b"` |
| `substring` | `substring('hello',1,3)` | Extract substring | `"ell"` |
| `indexOf` | `indexOf('hello','l')` | First occurrence index | `2` |
| `lastIndexOf` | `lastIndexOf('hello','l')` | Last occurrence index | `3` |
| `startsWith` | `startsWith('hello','he')` | Check prefix | `true` |
| `endsWith` | `endsWith('hello','lo')` | Check suffix | `true` |
| `split` | `split('a,b,c',',')` | Split to array | `["a","b","c"]` |
| `join` | `join(['a','b'],',')` | Join array | `"a,b"` |
| `guid` | `guid()` | Generate GUID | `"c2ecc88d-..."` |
| `formatNumber` | `formatNumber(1234,'N2')` | Format number | `"1,234.00"` |
| `nthIndexOf` | `nthIndexOf('a,b,a','a',2)` | Nth occurrence | `4` |
| `chunk` | `chunk('hello',2)` | Split into chunks | `["he","ll","o"]` |

---

## Collection (Array) Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `length` | `length(body('Get_items')?['value'])` | Count items |
| `first` | `first(body('Get_items')?['value'])` | First item |
| `last` | `last(body('Get_items')?['value'])` | Last item |
| `contains` | `contains(body('Get_items')?['value'],'x')` | Check if item exists |
| `empty` | `empty(body('Get_items')?['value'])` | Check if empty |
| `join` | `join(variables('myArray'),', ')` | Join to string |
| `reverse` | `reverse(variables('myArray'))` | Reverse order |
| `sort` | `sort(variables('myArray'))` | Sort items |
| `skip` | `skip(variables('myArray'),2)` | Skip first N |
| `take` | `take(variables('myArray'),3)` | Take first N |
| `union` | `union(arr1,arr2)` | Merge arrays |
| `intersection` | `intersection(arr1,arr2)` | Common items |
| `item` | `item()` | Current item in Apply to Each |

---

## Logical Comparison Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `equals` | `equals(a,b)` | Check equality |
| `if` | `if(condition, trueVal, falseVal)` | Conditional value |
| `and` | `and(expr1, expr2)` | All true |
| `or` | `or(expr1, expr2)` | At least one true |
| `not` | `not(expr)` | Negate |
| `greater` | `greater(5,3)` | a > b |
| `greaterOrEquals` | `greaterOrEquals(5,5)` | a >= b |
| `less` | `less(3,5)` | a < b |
| `lessOrEquals` | `lessOrEquals(3,3)` | a <= b |
| `strongEquals` | `strongEquals(a,b)` | Strict equality (type + value) |

---

## Math Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `add` | `add(2,3)` | Addition |
| `sub` | `sub(5,3)` | Subtraction |
| `mul` | `mul(2,3)` | Multiplication |
| `div` | `div(6,3)` | Division |
| `mod` | `mod(7,3)` | Modulus |
| `min` | `min(1,2,3)` | Minimum value |
| `max` | `max(1,2,3)` | Maximum value |
| `range` | `range(1,5)` | Array [1,2,3,4,5] |
| `sum` | `sum(variables('arr'))` | Sum of array |
| `rand` | `rand(1,100)` | Random number |

---

## Date/Time Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `utcNow` | `utcNow()` | Current UTC time |
| `addDays` | `addDays(utcNow(),7)` | Add days to date |
| `addHours` | `addHours(utcNow(),2)` | Add hours |
| `addMinutes` | `addMinutes(utcNow(),30)` | Add minutes |
| `formatDateTime` | `formatDateTime(utcNow(),'MMMM yyyy')` | Format date |
| `dateDifference` | `dateDifference('2024-01-01',utcNow())` | Days between |
| `getFutureTime` | `getFutureTime(1,'Day')` | Future date |
| `getPastTime` | `getPastTime(1,'Day')` | Past date |
| `startOfDay` | `startOfDay(utcNow())` | Start of day |
| `startOfMonth` | `startOfMonth(utcNow())` | Start of month |

### Common Date Formats

| Format String | Example Output |
|---------------|----------------|
| `yyyy-MM-dd` | `2026-08-27` |
| `MMMM` | `August` |
| `MMMM yyyy` | `August 2026` |
| `dd MMMM yyyy` | `27 August 2026` |
| `HH:mm` | `14:30` |
| `yyyy-MM-ddTHH:mm:ssZ` | `2026-08-27T14:30:00Z` |

---

## Conversion Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `string` | `string(123)` | Convert to string |
| `int` | `int('123')` | Convert to integer |
| `float` | `float('1.5')` | Convert to float |
| `bool` | `bool(1)` | Convert to boolean |
| `json` | `json('{\"a\":1}')` | Parse JSON |
| `base64` | `base64('hello')` | Base64 encode |
| `base64ToString` | `base64ToString('aGVsbG8=')` | Base64 decode |
| `encodeUriComponent` | `encodeUriComponent('hello world')` | URL encode |
| `decodeUriComponent` | `decodeUriComponent('hello%20world')` | URL decode |

---

## Most Useful Expressions for APP-MRMS

### Check if a field is not null
```
@not(empty(triggerBody()?['SubmittedBy']?['Email']))
```

### Get current month name
```
@formatDateTime(utcNow(), 'MMMM')
```

### Conditional email recipient
```
@if(
  not(empty(body('Get_activity')?['Supervisor']?['Email'])),
  body('Get_activity')?['Supervisor']?['Email'],
  body('Get_programme')?['ProgrammeManager']?['Email']
)
```

### Check if array is empty (no reports found)
```
@equals(length(body('Get_items_2')?['value']), 0)
```

### Build email subject with dynamic content
```
@concat(
  'Report submitted: ',
  triggerBody()?['Title'],
  ' — ',
  triggerBody()?['ReportingMonth']?['Value']
)
```

### Filter items by current month
```
Activity eq '@{items('Apply_to_each')?['Title']}' and ReportingMonth eq '@{formatDateTime(utcNow(), 'MMMM')}'
```

### Null-safe field access
```
@coalesce(triggerBody()?['SupervisorRejectionReason'], 'No reason provided')
```

---

## Common Patterns

### Pattern: Check if value is one of several options
```json
{
  "expression": {
    "or": [
      { "equals": ["@triggerBody()?['Status/Value']", "Supervisor Rejected"] },
      { "equals": ["@triggerBody()?['Status/Value']", "M&E Rejected"] }
    ]
  }
}
```

### Pattern: Apply to Each with filtered Get Items
```
1. Get items → filterQuery: "Active eq 1" → output: value
2. Apply to each → select: value from step 1
3. Inside: Get items → filterQuery with items('Apply_to_each') reference
4. Inside: Condition → check length(body('Get_items_2')?['value']) eq 0
```

### Pattern: Send email only if recipient exists
```
1. Condition: @not(empty(body('Get_activity')?['Supervisor']?['Email']))
2. If yes: Send email to body('Get_activity')?['Supervisor']?['Email']
3. If no: (skip or send to fallback)
```

---

*Source: Microsoft Learn — Reference guide to functions in expressions for workflows*
