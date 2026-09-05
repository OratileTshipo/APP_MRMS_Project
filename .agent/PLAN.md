# PLAN — Fix everything broken on the `dev` branch (APP-MRMS)

Task source: user request "Fix everything that's not working in this repo in Dev branch".
Branch: `dev` (upstream `origin/dev`). Status: **COMPLETE — all phases verified.**

## Phases & completion criteria

- [x] **1. Understand** — survey repo, run all existing gates, read trackers (KNOWN_ISSUES, AUDIT_FINDINGS), inspect CI history via `gh run list`.
  Criteria: inventory of concrete failures with evidence. ✅ 12/23 Playwright failures (dead `APP_MRMS/` submodule paths), stale 3-of-4 flow zip (C4), `Fecbruary` CSV regression (L7), 191 junk files tracked, placeholder `package.json`.
- [x] **2. Data/schema fixes** — MonthlyReports.csv `Fecbruary` → `February` (3 occurrences in embedded SharePoint schema).
  Criteria: `grep -c Fecbruary` = 0; regression test in suite. ✅
- [x] **3. Flow package rebuild** — `flows/APP-MRMS-Approval.zip` via `tools/build_flow_zips.py` with real tokens derived from the previous pack.
  Criteria: 4/4 manifest flows present, all JSON parses, no leftover `{{TOKEN}}`. ✅
- [x] **4. Test suite** — rewrite `tests/powerapp-e2e.spec.ts` for single-repo layout.
  Criteria: full suite green. ✅ 22/22.
- [x] **5. Repo hygiene** — untrack `node_modules/`, `playwright-report/`, `test-results/`; gitignore them; remove stale `.gitmodules`; fix `package.json`.
  Criteria: `git ls-files node_modules` = 0; `check-ignore` confirms rules. ✅
- [x] **6. CI** — add `structure-tests` job to `.github/workflows/ci.yml`.
  Criteria: job defined, mirrors local green run. ✅
- [x] **7. Docs** — KNOWN_ISSUES.md C4/L7 resolution log; README rows; `docs/2026-09-05-dev-fix-pass.md` full record. ✅
- [x] **8. Final verification** — 3 Python gates + Playwright suite + `npm run verify`. ✅ (re-confirmed this session, see STATE.md)

## Standing rules

- Never overwrite an existing msapp pack; new packs get a new `_vN_`/date name (repo convention).
- Commits/pushes belong to the Freebuff Changes panel; only on explicit user ask.
