# APP-MRMS — Technical Handoff Brief
## Screen: `scr_MyActivities`

**Prepared for:** AI coding tool (DeepSeek) — screen-building pass
**Prepared by:** Oray (Solution Owner / Implementation Lead), via Claude (architecture/documentation owner)
**Platform:** Power Apps Canvas App on SharePoint Online
**Status:** This screen already exists as a **live screen** in the app with known bugs (see §7). This mockup and brief re-document it in the project's standard format so its intended behaviour and connections are unambiguous during the fix/rebuild pass — it is not a brand-new screen.
**Companion file:** `scr_MyActivities_mockup.html` (visual reference for layout, field grouping, and states — do not translate 1:1, it is a design reference, not a spec of control names)
**Sidebar/header:** Reuses the shared shell from `scr_ReportSubmission_mockup.html`. The **My Activities** nav item (under the **Overview** section) is the active state on this screen.

---

## 1. Purpose of this screen

`scr_MyActivities` is the Contributor's personal worklist: every `Activities` record where they are the `Owner`, shown with due-date and RAG (Red/Amber/Green) status so they can see at a glance what needs attention this month. It is the primary entry point into the reporting workflow — a Contributor rarely starts their month on `scr_ReportSubmission` directly; they start here.

This screen is **read-and-navigate**, like `scr_MyReports`. It does not create or edit `MonthlyReports` records itself — it hands off to `scr_ReportSubmission` for that.

---

## 2. Where this screen sits in the navigation flow — and a correction to confirm

```
scr_Home ──────────────▶  scr_MyActivities  ──▶  scr_ReportSubmission  ──▶  scr_MyReports
                             (this screen)          (report on the             (after Submit,
                                                       selected activity)        or via My Reports
                                                                                  row actions)
```

**Important — please confirm this is what you intend:** your instruction described clicking an activity as taking the Contributor "to my reports page to report on the activity." Based on the FDS, TDS, and the confirmed navigation table in the `scr_ReportSubmission` handoff brief (§2), the documented and already-agreed flow is:

> `scr_MyActivities` gallery → Contributor taps an activity → **`scr_ReportSubmission`** (to capture that month's report) → on Submit → **`scr_MyReports`** (to see it in their history).

`scr_MyReports` is the **history/read view** of reports already captured; it is not itself a data-entry surface. I've built this mockup and brief using the `scr_ReportSubmission` target, since that matches everything already documented. If you actually want tapping an activity to land directly on `scr_MyReports` instead — for example, to show prior submissions for that activity before deciding to file a new one — let me know and I'll adjust both this brief and the mockup's stated navigation target.

**Entry points:**

| Entry point | Condition |
|---|---|
| Sidebar nav — Overview > My Activities | Always available to any authenticated Contributor |
| `scr_Home` "APP Items" / "Overdue Reports" KPI card | Deep link with a pre-applied filter |

**Exit points (row-level actions):**

| Row state | Button label | Destination | Parameter passed |
|---|---|---|---|
| Not started / Draft / Rejected for current reporting month | Report → | `scr_ReportSubmission` | The selected `Activities` record |
| Submitted for current reporting month | View → | Read-only view (see `scr_MyReports` Open Question 1 — same unresolved decision applies here) | The related `MonthlyReports` record |

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
| Parent Project name | Lookup (via Activity → Project, or denormalised label) | Row subtitle tag |
| `DueDayOfMonth` | Number | Due date column — combined with current month/year to render an actual date |
| *(derived)* RAG status | — | Coloured dot: Green = on track, Amber = due within X days (confirm threshold with Oray), Red = overdue |
| *(derived)* Report status this month | — | Status pill: `Not started`, `Draft`, `Rejected`, `Submitted` — sourced from the related `MonthlyReports` record if one exists |

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

## 7. Known bugs on the current live version — confirm before rebuilding

Per the diagnosis already on file for this screen, the following issues exist in the live `scr_MyActivities` and must be corrected as part of this pass, not carried forward into the rebuilt version:

| Bug | Description |
|---|---|
| `.Selected` vs `ThisItem` binding mismatch | Some controls reference the gallery's `.Selected` property where they should reference `ThisItem`, causing stale or incorrect row data to display. |
| Field name mismatch | Formulas reference `DueDay`; the correct SharePoint column name is **`DueDayOfMonth`**. |
| Hardcoded RAG dot | The RAG status dot does not currently calculate from due-date logic — it is hardcoded to a single colour regardless of the row's actual status. |
| Dead filter condition | At least one filter condition includes a hardcoded `|| true`, which defeats the filter entirely and always returns all rows. |

Do not silently work around these — fix them directly as part of rebuilding this screen to the mockup/brief spec above.

---

## 8. Known pac canvas pack constraint — read before building

The activity list on this screen (`Mya_gal_Activities`) is a **Gallery**. Apply the same workaround already used on `scr_Activities`, `scr_ReportSubmission`, and `scr_MyReports`:
- If producing YAML directly: strip the gallery to a placeholder `Label` for import; Oray rebuilds the real gallery manually in Power Apps Studio.
- If producing manual build steps for Studio: this constraint does not apply.

---

## 9. Open questions for Oray before this is finalised

1. **Navigation target confirmation** — see §2 above. Please confirm tapping an activity should go to `scr_ReportSubmission`, not `scr_MyReports`, before this is built.
2. **Due-soon threshold** — how many days before `DueDayOfMonth` should a row switch from Green to Amber? Not yet specified.
3. **Multiple open reporting periods** — if an Activity has an overdue report from a prior month AND a new report due this month, does the row show both, or only the most urgent one? Not yet modelled in the mockup.

Do not guess on these three points — confirm with Oray before wiring the corresponding logic.

---

*End of brief. Reference the companion mockup (`scr_MyActivities_mockup.html`) for visual layout only — control names, exact bindings, and screen logic in this document take precedence over anything implied by the HTML.*
