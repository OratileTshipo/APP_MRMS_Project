# APP-MRMS — Technical Handoff Brief
## Screen: `scr_MyActivities`

**Prepared for:** AI coding tool (DeepSeek) — screen-building pass
**Prepared by:** Oray (Solution Owner / Implementation Lead), via Claude (architecture/documentation owner)
**Platform:** Power Apps Canvas App on SharePoint Online
**Status:** ✅ **Built and verified** (CHANGES.md §10, §13). This screen exists as a live screen with all known bugs fixed. Navigation, filters, and RAG status are working. This brief is retained for reference.
**Companion file:** `scr_MyActivities_mockup.html` (visual reference for layout, field grouping, and states — do not translate 1:1, it is a design reference, not a spec of control names)
**Sidebar/header:** Reuses the shared shell from `scr_ReportSubmission_mockup.html`. The **My Activities** nav item (under the **Overview** section) is the active state on this screen.

---

## 1. Purpose of this screen

`scr_MyActivities` is the Contributor's personal worklist: every `Activities` record where they are the `Owner`, shown with due-date and RAG (Red/Amber/Green) status so they can see at a glance what needs attention this month. It is the primary entry point into the reporting workflow — a Contributor rarely starts their month on `scr_ReportSubmission` directly; they start here.

This screen is **read-and-navigate** — it shows the contributor's activities with status and due dates, and navigates to `scr_ReportForm` (for new/edit reports) or `scr_ReportView` (for approved reports).

---

## 2. Where this screen sits in the navigation flow — and a correction to confirm

```
scr_Home ──────────────▶  scr_MyActivities  ──┬──▶  scr_ReportForm  (new/edit report)
                             (this screen)      │
                                                └──▶  scr_ReportView  (view approved report)
```

✅ **Navigation confirmed and implemented** (CHANGES.md §10):

> `scr_MyActivities` gallery → Contributor taps an activity → **`scr_ReportForm`** (new/edit report for that activity) → on Submit → returns to `scr_MyActivities`.

The row action button navigates based on ReportStatus:
- **Not Started** → `scr_ReportForm` (new report)
- **Draft / Rejected** → `scr_ReportForm` (edit existing report)
- **Approved** → `scr_ReportView` (read-only view)

**Entry points:**

| Entry point | Condition |
|---|---|
| Sidebar nav — Overview > My Activities | Always available to any authenticated Contributor |
| `scr_Home` "APP Items" / "Overdue Reports" KPI card | Deep link with a pre-applied filter |

**Exit points (row-level actions):**

| Row state | Button label | Destination | Parameter passed |
|---|---|---|---|
| Not Started | Report → | `scr_ReportForm` (new) | The selected `Activities` record |
| Draft / Rejected | Report → | `scr_ReportForm` (edit) | The `MonthlyReports` record |
| Approved | View → | `scr_ReportView` | The `MonthlyReports` record |

If the Contributor role reaches this screen but the activity is not theirs to report on (edge case — deep link, role misconfiguration), do not show a Report button; apply the same role-scoping pattern documented in §6.

---

## 3. Data model touched by this screen

Primary read source: **`Activities`**, filtered to `Owner.Email = User().Email` and `Active = true`.
Secondary lookup per row: whether a `MonthlyReports` record already exists for `(Activity = this row, ReportingMonth = current month)`, to determine row status and RAG colour.

### Fields displayed per row

| Field | Type | Displayed as |
|---|---|---|
| `Title` / `ActivityShortDescription` | Text | Row title |
| `DirectorateLabel`, `ProgrammeLabel` | Text (denormalised) | Row subtitle |
| `Frequency` | Choice | Frequency tag (`Monthly`/`Quarterly`/`Annual`) |
| `DueDate` | DateTime | Due date |
| *(derived)* RAG status | — | Coloured dot: Green = on track, Amber = due within 7 days, Red = overdue |
| *(derived)* Report status this month | — | Status pill: `Not started`, `Draft`, `Rejected`, `Submitted`, `Approved` |

### Summary strip counts (top of screen)

- Total activities assigned to me
- On track
- Due soon
- Overdue

Same rule as `scr_MyReports`: these counts must be derived from the same filtered collection as the rows below, not calculated separately.

---

## 4. Filter and search behaviour

| Control | Behaviour |
|---|---|
| Search box | Free text against `Title`/`ActivityShortDescription`. Filter a locally cached collection, not a live call per keystroke. |
| Financial Year dropdown | Defaults to current FY (`2026/27`) |
| Quarter dropdown | `All Quarters`, `Q1`–`Q4` |
| Month dropdown | `All Months`, `April`–`March` — controls which reporting month's due date/status is evaluated per row |

Use the confirmed array-literal pattern for static dropdown options (see `scr_MyReports` brief §4 for the specific anti-pattern to avoid).

---

## 5. Control naming convention

Prefix for this screen: **`Mya`** (My Activities), following the established convention (`Prj*`, `Acy*`, `Rpt*`, `Myr*`).

Examples:
- `Mya_txt_Search`
- `Mya_drp_FinancialYear`
- `Mya_drp_Quarter`
- `Mya_drp_Month`
- `Mya_gal_Activities`
- `Mya_lbl_TotalCount`, `Mya_lbl_OnTrackCount`, `Mya_lbl_DueSoonCount`, `Mya_lbl_OverdueCount`

**This is a rebuild/fix pass on an existing live screen.** If the current live screen already has controls named under a different convention, treat this prefix as the target state to migrate toward, and flag any rename with Oray before executing — renames can break bindings elsewhere in the app (e.g. `scr_Home` KPI cards that may reference these controls or this screen's collections).

---

## 6. Role-based visibility

```
Filter: Activities.Owner.Email = User().Email And Activities.Active = true
```

Like `scr_MyReports`, this screen does not honour `varCanViewAllReports` — it is always "activities assigned to me," regardless of role. Supervisors and Programme Managers have their own oversight views elsewhere (`scr_ApprovalQueue`, Reports Dashboard); this screen is Contributor-scoped by design.

---

## 7. Known bugs — ✅ ALL FIXED

| Bug | Status | Fix |
|---|---|---|
| `.Selected` vs `ThisItem` binding mismatch | ✅ Fixed | Gallery bound to `colMyActivityStatus` with correct `ThisItem` refs (CHANGES.md §10) |
| Field name mismatch (`DueDay`) | ✅ Fixed | Corrected to `DueDate` (CHANGES.md §13) |
| Hardcoded RAG dot | ✅ Fixed | RAG now calculates from due-date logic |
| Dead filter condition (`|| true`) | ✅ Fixed | Filter corrected to proper role-based scope |

---

## 8. pac canvas pack constraint — ✅ RESOLVED

The v6 container-based shell (no components) eliminates the Gallery@2.15.0 PA3001 constraint. Galleries now pack/unpack correctly.

---

## 9. Open questions — ✅ RESOLVED

1. **Navigation target** → `scr_ReportForm` (confirmed and implemented, CHANGES.md §10)
2. **Due-soon threshold** → 7 days (implemented in RAG logic)
3. **Multiple reporting periods** → Shows current period only; prior periods visible in scr_ReportView

---

*End of brief. Reference the companion mockup (`scr_MyActivities_mockup.html`) for visual layout only — control names, exact bindings, and screen logic in this document take precedence over anything implied by the HTML.*
