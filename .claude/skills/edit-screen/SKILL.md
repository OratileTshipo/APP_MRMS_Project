---
name: edit-screen
description: Guide for editing Power Apps screen .pa.yaml files safely
invoked_by: /edit-screen
---

# Edit Power Apps Screen

Guide for safely editing `.pa.yaml` screen files.

## File Locations

- **Screens:** `src/Src/scr_*.pa.yaml`
- **Components:** `src/Src/Component/cmp_*.pa.yaml`
- **App formulas:** `src/Src/App.pa.yaml`
- **Editor state:** `src/Src/_EditorState.pa.yaml`

## Key Rules

1. **Control names are app-global** — no two controls can share a name, even across screens.

2. **Named formulas go in `App.Formulas`** — not in screen `OnStart` or `App.OnStart`.

3. **Single-line formulas cannot contain `:` or `#`** — move these to multi-line format.

4. **Use `Set()` for mutable variables only** — immutable values should be named formulas.

5. **Delegation:** Filter with role-first, delegable filters. Avoid complex `Or()`/`And()`.

## Naming Conventions

| Prefix | Type | Example |
|--------|------|---------|
| `var` | Variable | `varCurrentUser` |
| `col` | Collection | `colReportsInScope` |
| `scr` | Screen | `scr_Reports` |
| `cmp` | Component | `cmp_AppHeader` |
| `btn` | Button | `btnSubmit` |
| `gal` | Gallery | `galActivities` |

## After Editing

1. Run `/verify-app` to check for errors
2. Run `/rebuild-app` to create a new pack
3. Update `CHANGES.md` with what changed
