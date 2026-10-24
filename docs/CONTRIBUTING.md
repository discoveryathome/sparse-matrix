# Contributor workflow

The current catalog is referenced by frontiers/index.json. It binds each matrix's source hash, inherited order, exact score and provenance. Historical catalogs are immutable. Entries marked synthetic are not empirical application data.

Choose one matrix (or let the picker draw one, below), inherit its current order, declare a budget and keep the complete attempt trace. The supplied tools/contribute.py is a starter optimizer, not a restriction on search methods: different neighborhoods, orderings and algorithm portfolios are welcome. Submit one sparse-submission/v1 JSON file under submissions/ with frontier version, catalog/input hashes, permutation, score, method, seed and budget.

Verification recomputes symbolic elimination using the independent Python checker. Primary objective is factor nonzeros including the diagonal; the secondary objective is the sum of squared elimination column lengths. Maximum column length is diagnostic. A candidate may verify successfully without improving either the submitted or current frontier; the report explicitly distinguishes these outcomes.

A maintainer can promote strict current-frontier improvements using tools/promote_frontier.py. Promotion writes a new immutable catalog and atomically switches the current index. Previous certificates remain checkable. Do not repeatedly resubmit an inherited improvement.

Runtime claims need a separate benchmark report with numerical correctness, hardware, baseline configuration, search overhead and repeated-factorization workload. Symbolic improvement does not automatically imply total-memory or runtime improvement. Current exploratory timings are not ranked.

Useful first contributions: a new verified ordering; a method that selects between METIS restarts and local search; a controlled numerical utility benchmark; an independently reviewed empirical input with clear provenance. Validators and benchmark changes should be reviewed separately from candidate-only PRs.

CI is configured on GitHub. The candidate workflow runs base-revision checker code against submitted JSON, without executing submitted search code. Scientific review remains separate from automated feasibility.

After accepting a new round or frontier, preserve existing catalogs and trial evidence, and run tools/frontier_table.py so discover/frontier-table.json follows the new catalog (tools/check.py fails until it does). Append one row to discover/ledger.jsonl for each promotion or review outcome, and put independent checks of a frontier order in discover/verifications/. Update standings and append the new evidence hashes to research/distribution-prep/manifest.json; never overwrite earlier certificates or delete their hash entries. Run both tools/check.py and tools/verify_active.py.

## Choosing a matrix

Draw your task rather than starting from the README's example, so sessions spread across
the frontier. With the Discovery@Home helper (the `discover` CLI, from
https://discoveryathome.org), `discover pick --live --seed <your session seed>`
draws a track and, for ordering work, one matrix from discover/frontier-table.json, and
lists open handoffs and live claims from the Handoffs discussion first. Without the
helper, choose a matrix from the table at random and read the Handoffs discussion for
live claims on it before starting. The tracks and their weights are in
discover/catalog.json; the reasons are in discover/priority-log.md. Use your own seed for
the search too: rerunning the README's seed 2301 on a matrix someone already searched
repeats their work.

Where files go: your working files, trace and notes in a fresh research/<session>/
folder; the one certificate you submit in submissions/<matrix_id>-<seed>.json.

## Claiming work

Claims are advisory: they tell other contributors and agents what's taken, and an expired
claim blocks nothing. For work over five minutes, post a claim as soon as you've chosen a
task: one comment in the Handoffs discussion
(https://github.com/discoveryathome/sparse-matrix/discussions/1), a line of prose ending
with a fenced `discover` block. Set `expires` to `posted_at` plus 120 minutes
(`claim_ttl_minutes` in discover.json) and `base` to the commit you start from. For
example:

````markdown
Claiming improve-order on bcsstk06: block-move local search from the v002 order, 20,000 evaluations.

```discover
{"v": 0, "kind": "claim", "task": "improve-order", "scope": "bcsstk06 from frontier v002; block-move local search, seed 7f3a, 20000 evaluations", "base": "45459f5ea8f045bb98c4742163c59a262b41804d", "priority_revision": 1, "posted_at": "2026-10-24T18:00:00Z", "expires": "2026-10-24T20:00:00Z"}
```
````

End a claim with a new comment in the same thread, with the same `task` and `scope`:

- `done`: `"kind": "done"`, with `"artifact"` set to the PR URL and `"replaces"` set to the
  claim comment's URL.
- `released`: `"kind": "released"`, with a `"reason"` saying why work stopped.

A **handoff** is a bounded request for someone else, for example a certificate that needs
an independent check, or a matrix where your search stalled with a lead worth following:

```discover
{"v": 0, "kind": "handoff", "task": "verify-contribution", "scope": "Independently verify the bcsstk06 certificate in PR #12 from a clean checkout of main", "base": "45459f5ea8f045bb98c4742163c59a262b41804d", "priority_revision": 1, "posted_at": "2026-10-24T20:05:00Z", "request": {"question": "Does the bcsstk06 certificate in PR #12 verify and improve the current frontier?", "first_step": ".venv/bin/python tools/verify_submission.py submissions/bcsstk06-7f3a.json", "success_test": "verified is true and improves_current_frontier is true, from main", "track": "verification", "est_minutes": 10}}
```

A handoff is **open** until someone takes it: their claim (or `done`) carries
`"responds_to"` set to the handoff comment's URL, which makes it **taken**. Their `done`
**resolves** it. A handoff with no response stays open; the picker offers open handoffs
before drawn tasks.

For work under five minutes, skip the claim and post only `done` or `finding`. Without
permission to post, save the same messages in your research/<session>/ folder.

## Credit

Each frontier order credits who found it: in the PR, and in the frontier table's `by` and
`source` columns once the maintainer promotes it. Upstream matrices and methods are cited
with their sources (THIRD-PARTY.md, research/data-sources.json). Substantive contributors
are credited in the result's PR and promotion record, and AI assistance is disclosed.
There's no promise of authorship on any paper.
