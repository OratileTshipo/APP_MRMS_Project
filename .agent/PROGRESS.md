# PROGRESS — chronological checkpoints

## Checkpoint 1 — Survey (2026-09-05, session 1)
- Fetched `origin/dev`, checked out local `dev` (was `main`).
- Ran repo gates: screen registry OK, control props 0 errors, powerfx --strict clean.
- `gh run list`: latest dev CI green; earlier failures already fixed by prior commits.
- Ran Playwright suite: 12/23 failed — all pointing at removed `APP_MRMS/` submodule layout.
- Found: flow zip stale (manifest 4 flows, 3 packed — C4), `Fecbruary` ×3 in MonthlyReports.csv schema (L7), `node_modules/` + artifacts tracked, stale `.gitmodules`, placeholder `package.json`.

## Checkpoint 2 — Flow package (C4)
- Derived exact `{{TOKEN}}` values by parallel JSON-tree walk of templates vs old zip (site URL + 5 list GUIDs).
- Rebuilt zip with `tools/build_flow_zips.py`; verified 4/4 flows, JSON valid, 0 leftover placeholders.

## Checkpoint 3 — CSV fix (L7)
- `Fecbruary` → `February` ×3 (choice list + 2 CustomFormatter operands) in MonthlyReports.csv.

## Checkpoint 4 — Test suite rewrite
- Rewrote `tests/powerapp-e2e.spec.ts` for current layout: source structure, `_EditorState` registration, Navigate targets, flow-package integrity (C4 guard, `{{MR_GUID}}`-aware loop prevention), CSV schemas, docs, msapp ZIP-container validation, tool `py_compile`, 3 CI gates end-to-end.
- Fixed own initial mis-assertions after evidence: flows write `Status` to Activities (legitimate), msapp packs are ZIP not OLE, pack-name↔App.pa.yaml match not enforced by repo → dropped that test.
- Capped Playwright workers at 4 (24 workers OOM'd 4 GB sandbox). Result: 22/22 pass.

## Checkpoint 5 — Repo hygiene + CI + docs
- `git rm -r --cached node_modules playwright-report test-results` (191 index deletions, files kept on disk); `.gitignore` += playwright outputs; removed `.gitmodules`.
- `package.json`: real description, working `test`/`test:report`/`verify` scripts, keywords.
- `.github/workflows/ci.yml`: added `structure-tests` job (Node 20, npm ci, playwright test).
- KNOWN_ISSUES.md: C4 → Resolved + resolution log entries (C4, L7, suite rewrite).
- README: CI row, test-suite row, `npm test` in sanity-check block.
- `docs/2026-09-05-dev-fix-pass.md`: full record (CHANGES.md append blocked by edit-tool matching limit on 78 KB file — see DECISIONS.md).

## Checkpoint 6 — Protocol adoption (2026-09-05, session 2)
- Created `knowledge.md` (GLM 5.3 output directives) per user request — verbatim, root.
- Scaffolded `.agent/` state files; re-ran full verification (see STATE.md).

## Checkpoint 7 — Commit, push, re-verify (2026-09-05, session 3)
- Reviewed full diff (MonthlyReports.csv = single-line schema file; no index.php/skill.md in repo).
- Created branch `GLM52` from `dev` @ 6d58648; committed all fix-pass changes as 3ecdd1c
  (206 files, +762/−363,583 — bulk is node_modules untracking) with conventional message + Codebuff footer.
- Pushed: origin/GLM52 = 3ecdd1ce65ba, tracking established.
- Re-verification battery: registry 0 problems / props 0 errors / powerfx --strict clean /
  Playwright 22/22 / node_modules tracked 0 / Fecbruary 0 / artifacts untracked + gitignore
  effective / flow zip 4-of-4 with 0 leftover tokens / working tree clean.
- GitHub Actions CI on GLM52: run 33994575072 → success (18s).
