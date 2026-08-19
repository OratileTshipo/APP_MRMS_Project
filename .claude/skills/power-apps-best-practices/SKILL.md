---
name: power-apps-best-practices
description: Power Apps canvas app best practices, compliance review, and troubleshooting
invoked_by: /power-apps-best-practices
---

# Power Apps Canvas App Best Practices

Reference: Official Microsoft Learn "Power Apps maker" documentation.
Scope: canvas apps — external editing, pack/import workflow, and app architecture.

---

## 1. External Editing & Pack/Import Workflow

### Source File Format (*.pa.yaml)
- Only `src/Src/*.pa.yaml` files are source code — never hand-edit JSON files
- `Control: Name@version` defines control type; `Variant:` identifies variant
- Only properties differing from defaults are serialized
- All controls use ascending ZIndex starting at 1

### Pack/Import Cycle
```bash
# Unpack
pac canvas unpack --msapp app.msapp --sources src --layout SourceCode --overwrite

# Edit src/Src/*.pa.yaml files

# Pack
pac canvas pack --sources src --msapp app_vN.msapp --layout SourceCode --overwrite

# Import into Power Apps Studio, then open once for edit to validate
```

### Import-Safety Rules
1. Edit only `Src/*.pa.yaml` and `_EditorState.pa.yaml`
2. Keep the `.msapr` (resources) file
3. Keep YAML inside supported schema
4. When adding a screen, register it in `_EditorState.pa.yaml` `ScreensOrder`
5. When renaming/removing, update all `Navigate(...)` cross-references
6. After packing, verify round trip and open in Studio once

---

## 2. Best Practices

### Delegation & Data Payloads
- Keep data payloads small (100-200 records per query)
- Use delegable operators: `Filter`, `Search`, `SortByColumns`
- SharePoint does NOT delegate: `CountRows`, `CountIf`, `GroupBy`, `AddColumns`, `FirstN`, `Distinct`, `ForAll`, `Sum`/`Average`
- Avoid multi-condition `Filter` with `||` across columns

### App-Level Values
- Named formulas (`App.Formulas`) cannot round-trip through pa.yaml
- Use `Set()` in `App.OnStart` for hand-edited YAML
- Keep `App.OnStart` lean with immutable values in named formulas (Studio only)

### Naming Conventions
| Prefix | Type | Example |
|--------|------|---------|
| `var` | Variable | `varCurrentUser` |
| `col` | Collection | `colReportsInScope` |
| `scr` | Screen | `scr_Reports` |
| `cmp` | Component | `cmp_AppHeader` |
| `btn` | Button | `btnSubmit` |
| `gal` | Gallery | `galActivities` |

### Performance
- Split long formulas (>256k characters) with `With()` or named formulas
- Use `Concurrent()` for independent data calls
- Use `With()` instead of nested `LookUp` chains
- Remove dead code and commented-out blocks

### Business Logic
- **Power Fx**: low-latency, in-app logic
- **Power Automate**: long-running, multi-connector, async work

---

## 3. Common Issues & Fixes

### Import Errors
| Error | Fix |
|-------|-----|
| PA2108 (Unknown property) | Remove invalid property in `.pa.yaml` |
| Screen registry mismatch | Add missing entry in `_EditorState.pa.yaml` |
| YAML parse error | Check syntax (quotes, indentation) |

### Formula Errors
- Unbalanced brackets: count opening/closing
- Invalid column ref: check CSV schemas
- Named formula in wrong place: move to `App.Formulas`

### Delegation Issues
- SharePoint OR filters often non-delegable
- Use role-first, delegable filters
- Stay within 500-2,000 row collected set

### Date/Time Issues
- Check stored value in data source first
- Verify timezone match (UTC vs Local)
- MonthlyReports uses choice values, not raw DateTimes

---

## 4. Debugging

### Live Monitor
- Shows real-time data operations, timing, errors
- Watch for non-delegable-query warnings
- Filter to specific screen for diagnosis

### Debug Labels
- Place Label outside Gallery/Form
- Show `CountRows(Filter(...))` or `First(Filter(...)).Field`
- Work from innermost expression outward

### Minimal Repro
- Smallest app that reproduces issue
- Replace external data with `ClearCollect` samples
- Simplify/remove components
- Scrub private data before sharing

---

## 5. APP-MRMS Specific

### Current Status
- Role-first delegable scope filters implemented
- Collections (`colReportsInScope`, `colProjectsInScope`) used instead of raw SharePoint
- Components (`cmp_AppHeader`, `cmp_NavRail`) applied to all screens
- Dead code and commented blocks removed

### Watch Areas
- `CountRows`/`Distinct`/`ForAll` on raw SharePoint (non-delegable)
- `Sequence(12)` trend gallery formula (heavy per-screen calc)
- MonthlyReports period logic uses choice values, not DateTimes
