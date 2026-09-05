# Dev-branch fix pass — 2026-09-05

Scope: everything on `dev` that was broken or stale. The canvas-app source itself was
already clean (all CI gates green on the last push), so this pass fixed the assets and
infrastructure around it.

---

## 1. Flow package rebuilt — `flows/APP-MRMS-Approval.zip` (KNOWN_ISSUES C4)

The checked-in zip was stale: its `Microsoft.Flow/flows/manifest.json` listed **4** flows
but the archive contained only **3** flow folders. The *Report Rejected — Notify and Route
Back* flow (`d4f9a27c-8851-44ba-9f3c-4989a0e6d467`) existed as a template under
`flows/templates/` but had never been packed. Power Automate rejects an import whose
manifest references a missing flow folder.

What was done:

- Derived the real `{{TOKEN}}` substitution values by walking the template and previous
  zip JSON trees in parallel:
  | Token | Value |
  |---|---|
  | `SITE_URL` | `https://nwpg.sharepoint.com/sites/DPWRPerformanceandMonitoring` |
  | `MR_GUID` (MonthlyReports) | `31b39eaa-cf11-426d-b9a1-c3df5bae7cbe` |
  | `ACT_GUID` (Activities) | `dc7c7e42-8fd5-4b0a-8275-a7d9c4f4c67f` |
  | `NOTIF_GUID` (Notifications) | `60fa50dd-588f-4ae6-b838-aae60fc3092d` |
  | `AUDIT_GUID` (AuditLog) | `ef3722f5-44eb-4376-8a02-8a2ba574304a` |
  | `USERS_GUID` (APP_Users) | `aca25b79-2f4a-4803-93b4-17feb2cac5a2` |
- Rebuilt with `tools/build_flow_zips.py` (no placeholder GUIDs anywhere — the real C4
  "placeholder" symptom was this stale pack).
- Verified: 4/4 manifest flows present as folders, all member JSON parses, 0 leftover
  `{{TOKEN}}` placeholders.

## 2. `MonthlyReports.csv` — `Fecbruary` → `February` (KNOWN_ISSUES L7 regression)

The typo had crept back into the embedded SharePoint schema header (ReportingMonth choice
list + two CustomFormatter operands). 3 occurrences fixed. A regression test now guards it.

## 3. Playwright suite rewritten for the single-repo layout

`tests/powerapp-e2e.spec.ts` still targeted the removed `APP_MRMS/` submodule — 12 of 23
tests failed. Rewritten against the current layout; it now validates:

- Source structure: all 13 screens (+ `App`, `_EditorState`) exist, `_EditorState`
  registration is complete, YAML is tab-free, `Navigate()` targets resolve.
- Flow package: zip magic, 4-flow manifest ↔ template folders (C4 regression guard),
  unique action names, JSON validity, and **no review-status writes back to
  MonthlyReports** (loop prevention — `{{MR_GUID}}`-aware; the legitimate
  `Status = Completed` write targets Activities).
- CSV schemas incl. the `Fecbruary` regression guard.
- Docs presence, msapp packs (ZIP container signature + End-Of-Central-Directory record),
  tool inventory + `py_compile` over `tools/*.py`.
- The three CI gates (`check_screen_registry`, `check_control_props`,
  `verify_powerfx --strict`) run end-to-end inside the suite.

Result: **22 passed, 0 failed**. `playwright.config.ts` workers capped at 4 locally — the
suite spawns Python subprocesses and the default 24 workers OOM'd a 4 GB sandbox.

## 4. Repo hygiene

- `node_modules/` (187 dependency files), `playwright-report/`, `test-results/` were
  **tracked in git** — untracked via `git rm --cached` and added to `.gitignore`
  (local copies kept on disk).
- Removed the stale `.gitmodules`: it referenced an `APP_MRMS` submodule that no longer
  exists in the tree (and would break fresh clones with `git submodule update --init`).
- `package.json`: real description (was the CI-badge markdown), `test` script now runs
  Playwright (was a placeholder that always errored), added `test:report` and `verify`.

## 5. CI

`.github/workflows/ci.yml`: added a `structure-tests` job (Node 20, `npm ci`,
`npx playwright test`) alongside the existing `verify-source` and `pack-roundtrip` jobs.

## 6. Verification summary

| Check | Result |
|---|---|
| `tools/check_screen_registry.py` | ✅ 0 problems (13 ↔ 13) |
| `tools/check_control_props.py` | ✅ 0 errors (34 pre-existing manifest warnings) |
| `tools/verify_powerfx.py --strict` | ✅ clean (13,674 formulas) |
| Playwright suite (`npm test`) | ✅ 22/22 |

## 7. msapp pack pruning (2026-09-05, later)

The repo root carried five tracked ~2 MB `.msapp` packs (24Aug-09h38,
03Sep2026 DDQueue/QueueFix/StatusModel, 27Aug2026 InfoIcons), all superseded.
Evidence-based pruning:

- The newest pack `APP-MRMS_Latest_dev_05Sep2026_src-sync.msapp` was verified
  before adoption: valid ZIP container (50 entries), and all 15 `Src/*.pa.yaml`
  files byte-identical (SHA-256) to `src/Src/` — it is the in-sync pack.
- `git rm --cached` the five superseded packs (files kept on disk, history
  untouched); tracked the 05Sep2026 pack as the single canonical pack.
- `.gitignore` gained a deny-pattern guard so superseded `APP-MRMS_Latest_dev_*`
  packs cannot be re-added accidentally; the canonical pack stays tracked via a
  trailing negation rule.
- CI is unaffected: `pack-roundtrip` packs from `src/` to `/tmp` and does not
  read root packs; the Playwright msapp group requires ≥1 valid root pack,
  which the canonical pack satisfies.
- README's pack tables referenced `APP-MRMS_Project_app_v1–v6.msapp` files that
  no longer exist; rows were replaced with the current pack policy.
