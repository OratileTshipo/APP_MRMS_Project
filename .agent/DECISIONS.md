# DECISIONS

1. **Rebuild flow zip from derived tokens rather than regenerating GUIDs.**
   The old zip held the real production site/list GUIDs; templates hold `{{TOKEN}}`s.
   Extracted values by parallel JSON-tree walk (templates vs zip), then rebuilt via the
   repo's own `build_flow_zips.py`. Alternative (placeholder GUIDs) would recreate C4.

2. **Loop-prevention test scoped to MonthlyReports (`{{MR_GUID}}`-aware).**
   First version flagged any `item/Status` write; evidence showed the only write is
   `Activities.Status = Completed` (legitimate finalize step). Test now only fails on
   review-status writes targeting MonthlyReports (template token or resolved GUID).

3. **msapp validation = ZIP container check (PK header + EOCD), not OLE magic.**
   Observed packs are ZIPs (`PK\x03\x04`), not OLE compound docs. Initial OLE assertion
   was wrong; corrected after inspecting bytes. Name↔App.pa.yaml matching dropped —
   repo convention renames packs freely; no enforced link exists.

4. **Playwright workers capped at 4 locally (CI keeps 1).**
   Default 24 parallel workers each spawning Python subprocesses OOM'd a 4 GB sandbox
   ("Killed"). Suite is I/O + subprocess bound; 4 is sufficient (4.5 s runtime).

5. **Untrack node_modules/playwright-report/test-results via `git rm --cached`; keep local files.**
   187 dependency files + throwaway artifacts were tracked. `--cached` avoids touching
   the working tree; `.gitignore` updated to prevent regression. Deleted `.gitmodules`
   (submodule `APP_MRMS` no longer exists; stale entry breaks fresh clones).

6. **Fix-pass record lives in `docs/2026-09-05-dev-fix-pass.md`, not appended to CHANGES.md.**
   `str_replace` cannot match strings in the tail of the 78 KB CHANGES.md (reached via
   read_files but not by the editor's matcher; ASCII-only probes also failed → size
   limit, not encoding). Rewriting the whole file would violate minimal-diff discipline.
   Cross-referenced from README.

7. **`knowledge.md` created verbatim as requested; not gitignored, left untracked.**
   User-provided directive file; committing it is the user's call alongside the fix pass.

8. **Commits deferred.** Freebuff workspace rule: Changes panel owns commits/pushes;
   run git delivery only on explicit ask. All fix-pass changes sit in the working tree
   (plus 191 staged index deletions) ready for the user to commit or for an explicit ask.
