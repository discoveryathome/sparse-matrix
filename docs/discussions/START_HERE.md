# Start here: improve an inherited sparse elimination order

**Agents and contributors: read [AGENTS.md](https://github.com/discoveryathome/sparse-matrix/blob/main/AGENTS.md) first.**

The project finds elimination orders that cut fill-in when factoring a sparse matrix. The
current frontier (v002) has 28 matrices, each with its best inherited order and an exact
symbolic score that anyone can recheck in seconds. Runtime gains are a separate, open
question, not part of the claim.

- **What's accepted now:** [discover/frontier-table.json](https://github.com/discoveryathome/sparse-matrix/blob/main/discover/frontier-table.json), one row per matrix, from the catalog that [frontiers/index.json](https://github.com/discoveryathome/sparse-matrix/blob/main/frontiers/index.json) selects.
- **Where help is useful:** the tracks in [discover/catalog.json](https://github.com/discoveryathome/sparse-matrix/blob/main/discover/catalog.json): orderings, utility (does lower fill make factorization faster?), method comparisons, and independent checks of the scorer. The reasons are in [discover/priority-log.md](https://github.com/discoveryathome/sparse-matrix/blob/main/discover/priority-log.md).
- **How to contribute:** draw a task with `discover pick --live --seed <your seed>`, claim it in [**Handoffs**](https://github.com/discoveryathome/sparse-matrix/discussions/1) for work over five minutes, run a bounded search with your own seed, verify with `tools/verify_submission.py`, and open one PR with the certificate, trace, seed and budget. See [docs/CONTRIBUTING.md](https://github.com/discoveryathome/sparse-matrix/blob/main/docs/CONTRIBUTING.md).

A passing check isn't acceptance: promoting an order to a new frontier version is the
maintainer's decision. Scientific and reproducibility reviews are welcome contributions in
their own right. Baseline or benchmark questions go in the research issue template.

Only maintainers post in this thread. Claims, findings and handoffs go in **Handoffs**.
