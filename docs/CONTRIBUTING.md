# Contributor workflow

The current catalog is referenced by frontiers/index.json. It binds each matrix's source hash, inherited order, exact score and provenance. Historical catalogs are immutable. Entries marked synthetic are not empirical application data.

Choose one matrix, inherit its current order, declare a budget and keep the complete attempt trace. The supplied tools/contribute.py is a starter optimizer, not a restriction on search methods: different neighborhoods, orderings and algorithm portfolios are welcome. Submit one sparse-submission/v1 JSON file under submissions/ with frontier version, catalog/input hashes, permutation, score, method, seed and budget.

Verification recomputes symbolic elimination using the independent Python checker. Primary objective is factor nonzeros including the diagonal; the secondary objective is the sum of squared elimination column lengths. Maximum column length is diagnostic. A candidate may verify successfully without improving either the submitted or current frontier; the report explicitly distinguishes these outcomes.

A maintainer can promote strict current-frontier improvements using tools/promote_frontier.py. Promotion writes a new immutable catalog and atomically switches the current index. Previous certificates remain checkable. Do not repeatedly resubmit an inherited improvement.

Runtime claims need a separate benchmark report with numerical correctness, hardware, baseline configuration, search overhead and repeated-factorization workload. Symbolic improvement does not automatically imply total-memory or runtime improvement. Current exploratory timings are not ranked.

Useful first contributions: a new verified ordering; a method that selects between METIS restarts and local search; a controlled numerical utility benchmark; an independently reviewed empirical input with clear provenance. Validators and benchmark changes should be reviewed separately from candidate-only PRs.

CI is configured on GitHub; discussion text remains a draft. The candidate workflow runs base-revision checker code against submitted JSON, without executing submitted search code. Scientific review remains separate from automated feasibility.

After accepting a new round or frontier, preserve existing catalogs and trial evidence. Update standings and append the new evidence hashes to research/distribution-prep/manifest.json; never overwrite earlier certificates or delete their hash entries. Run both tools/check.py and tools/verify_active.py.
