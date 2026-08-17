# APP-MRMS — Technical Handoff Brief
## Screen: `scr_MyReports`

**Prepared for:** AI coding tool (DeepSeek) — screen-building pass
**Prepared by:** Oray (Solution Owner / Implementation Lead), via Claude (architecture/documentation owner)
**Platform:** Power Apps Canvas App on SharePoint Online
**Status:** Design mockup only. Not yet wired to live data. This brief describes the target build.
**Companion file:** `scr_MyReports_mockup.html` (visual reference for layout, field grouping, and states — do not translate 1:1, it is a design reference, not a spec of control names)
**Sidebar/header:** Reuses the shared shell from `scr_ReportSubmission_mockup.html`. The **My Reports** nav item (under the **Reporting** section) is the active state on this screen.

---

## 1. Purpose of this screen

`scr_MyReports` is the Contributor's personal history and management view of their own `MonthlyReports` records, across every Activity assigned to them. It answers three questions for the Contributor:

1. "What have I already submitted, and what's its status?"
2. "What drafts do I still need to finish?"
3. "What was rejected, and do I need to go fix it?"

This screen is **read-and-navigate**, not a data entry screen. It does not edit report content directly — it filters, summarises, and hands off to `scr_ReportSubmission` for anything that still needs writing.

---

## 2. Where this screen sits in the navigation flow

```
scr_Home ─────────────┐
scr_MyActivities ──────┼───▶  scr_MyReports  ──┬──▶  scr_ReportSubmission  (Draft → Continue, Rejected → Resubmit)
                        │        (this screen)  │
                        │                       └──▶  scr_ReportDetail / read-only drawer  (Submitted / Approved → View)
```

**Entry points:**

| Entry point | Condition |
|---|---|
| Sidebar nav — Reporting > My Reports | Always available to any authenticated Contributor |
| `scr_Home` "Pending Reports" / "Rejected Reports" KPI card | Deep link with a pre-applied Status filter |
| `scr_ReportSubmission` on Submit or Save Draft | Confirmed exit destination after a save action (per Report Submission brief §2) |

**Exit points (row-level actions):**

| Row status | Button label | Destination | Parameter passed |
|---|---|---|---|
| `Draft` | Continue → | `scr_ReportSubmission` | The existing `MonthlyReports` record |
| `Rejected` | Resubmit → | `scr_ReportSubmission` | The existing `MonthlyReports` record (triggers `varReportMode = "Rejected"` on the target screen) |
| `Submitted` | View → | Read-only detail view (drawer or dedicated screen — see Open Question 1) | The existing `MonthlyReports` record, read-only |
| `Approved` | View → | Same as above | Same as above |

This screen never navigates to `scr_ReportSubmission` for a `Submitted` or `Approved` record — those are locked from further editing by the Contributor. Only `Draft` and `Rejected` are writable states.

---

## 3. Data model touched by this screen

Primary read source: **`MonthlyReports`**, filtered to `SubmittedBy.Email = User().Email` (or, for Drafts not yet submitted, to the record's implicit owner via its parent `Activity.Owner`).

### Fields displayed per row

| Field | Type | Displayed as |
|---|---|---|
| `Activity.Title` / `ActivityShortDescription` | Lookup / Text | Row title |
| `DirectorateLabel` | Text (denormalised) | Row subtitle |
| `ReportingMonth`, `FinancialYear` | Choice | Row subtitle |
| `Version` | Number | Row subtitle (e.g. "v2") |
| `PercentageComplete` | Number | Progress bar + label |
| `Status` | Choice | Status pill (`Draft` / `Submitted` / `Approved` / `Rejected`) |
| `SubmissionDate` / `ReviewDate` | Date | Right-aligned meta text, contextual to status |

### Summary strip counts (top of screen)

Four rollup counts scoped to the current user's records for the selected Financial Year:
- Drafts: `CountRows(Filter(MonthlyReports, Status = "Draft", ...))`
- Submitted (awaiting review): `Status = "Submitted"`
- Approved: `Status = "Approved"`
- Rejected: `Status = "Rejected"`

These four counts must use the **same filter context** as the list below them (search box, FY, Quarter, Month) so the numbers and the visible rows never disagree. Do not hardcode them separately.

---

## 4. Filter and search behaviour

| Control | Behaviour |
|---|---|
| Search box | Free text against `Activity.Title`/`ActivityShortDescription`. Debounce, do not filter on every keystroke against a live SharePoint call — filter a locally cached collection. |
| Status dropdown | `All Statuses`, `Draft`, `Submitted`, `Approved`, `Rejected` |
| Financial Year dropdown | Defaults to current FY (`2026/27`) |
| Quarter dropdown | `All Quarters`, `Q1`–`Q4` |
| Month dropdown | `All Months`, `April`–`March` |
| Clear filters link | Resets all of the above to defaults in one action |

Per the project's confirmed Power Fx pattern, static dropdown options must use array literal syntax (`=["All Statuses", "Draft", ...]`) — do not attempt the `Table({Value:"All"}) & Choices(...)` union pattern, which has previously crashed in this app.

---

## 5. Control naming convention

Prefix for this screen: **`Myr`** (My Reports), following the same convention as `Prj*`, `Acy*`, `Rpt*`.

Examples:
- `Myr_txt_Search`
- `Myr_drp_Status`
- `Myr_drp_FinancialYear`
- `Myr_drp_Quarter`
- `Myr_drp_Month`
- `Myr_gal_Reports`
- `Myr_lbl_DraftCount`, `Myr_lbl_SubmittedCount`, `Myr_lbl_ApprovedCount`, `Myr_lbl_RejectedCount`
- `Myr_btn_ClearFilters`

Do not reuse control names from `scr_MyActivities`, `scr_ReportSubmission`, or any other screen — names must be globally unique per the `pac canvas pack` constraint.

---

## 6. Known pac canvas pack constraint — read before building

The report list on this screen (`Myr_gal_Reports`) is a **Gallery**. Per the project's established constraint, hand-authored `Gallery@2.15.0` controls in YAML crash `pac canvas pack` with a PA3001 null-reference error (missing paired EditorState metadata).

Apply the same workaround already used on `scr_Activities` and `scr_ReportSubmission`:
- If producing YAML directly: strip the gallery to a placeholder `Label` (e.g. `Myr_lbl_ReportsPlaceholder`) for import, and Oray will rebuild the real gallery manually in Power Apps Studio.
- If producing manual build steps for Studio: this constraint does not apply, build the gallery directly.

---

## 7. Role-based visibility

`scr_MyReports` is scoped to the current user's own records only:

```
Filter: MonthlyReports.SubmittedBy.Email = User().Email
     Or (Status = "Draft" And Activity.Owner.Email = User().Email)
```

This screen does **not** honour `varCanViewAllReports` (the flag that lets DeputyDirectorME/Administrator see everything) — that broader view belongs to `scr_ApprovalQueue` and the Reports Dashboard, not here. `scr_MyReports` is always "my own records," regardless of role.

---

## 8. Open questions for Oray before this is finalised

1. **Read-only detail view for Submitted/Approved rows** — does "View" open a modal/drawer on this same screen, or navigate to a dedicated `scr_ReportDetail` screen? Not yet decided. The mockup does not model this interaction.
2. **Comment visibility** — should `ManagerComments`/`ReviewedBy` feedback for Approved reports be visible from this list (not just Rejected), e.g. an "Approved with comments" indicator?
3. **Pagination/paging** — at what row count should this gallery switch from a simple scroll to paged loading? Not yet specified; flag for later once real data volumes are known.

Do not guess on these three points — confirm with Oray before wiring the corresponding logic.

---

*End of brief. Reference the companion mockup (`scr_MyReports_mockup.html`) for visual layout only — control names, exact bindings, and screen logic in this document take precedence over anything implied by the HTML.*
