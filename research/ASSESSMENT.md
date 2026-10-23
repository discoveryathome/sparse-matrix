# Initial qualification — 2026-10-23

## Assessment

The best verified order reduced symbolic Cholesky factor nonzeros on 6 of 8 matrices, representing 5 of 7 distinct sparsity patterns. The largest reduction was 1.35%. This is the strongest initial pilot of the four.

## What was tested

Eight NIST Harwell–Boeing bcsstk01–08 matrices; natural ordering, reverse Cuthill–McKee, SuiteSparse AMD and METIS nested dissection baselines. Two seeds (419, 503), 512 local proposals per seed and matrix: 8,192 proposals total. Each run starts from the strongest baseline and minimizes factor nonzeros, then a structural arithmetic proxy. Exact Python set elimination checks the native bitset scorer and every final certificate.

## What the evidence does not establish

bcsstk06 and bcsstk07 have the same structural graph. Ten of sixteen seeded runs improved factor nonzeros. Gains are instance-specific and modest; they do not establish a new competitive ordering algorithm. No numerical factorization time, amortized solve time or peak-memory advantage was measured. The corpus is small and from one structural-engineering family.

## Work we can do next

1. Add 20–30 diverse symmetric positive-definite patterns, deduplicate structural graphs and freeze a held-out set.
2. Compare matched end-to-end budgets against AMD and METIS, including optimization overhead and repeated numerical factorizations.
3. Transfer learned move selection to held-out matrices; report null results as well as wins.

## Outside help

A sparse numerical linear algebra reviewer should check baseline configurations and the connection between the symbolic objective and useful numerical workloads. Review benchmark redistribution terms before public packaging.

## Evidence and reproducibility

Inputs and source hashes: research/data-sources.json. Preregistered-in-session budgets and scope: research/protocol.json (additional follow-up protocols are separately named). Certificates, traces and summaries: results/. Dependency locks and environment snapshot are retained; native build logs and source revisions are included where applicable. research/executed-sources/ preserves the code as used in the initial rounds before packaging changes. research/manifest.json hashes frozen data, results and provenance; packaging changes are versioned by Git.

Trials and assessment were authored by the preparing Codex agent, not an independent contributor or scientific reviewer. Timing was observed on a shared host with concurrent work; do not interpret it as a controlled performance benchmark. Scientific signoff is pending, but local contribution intake is open. No external messages or public repository publication were performed for this round.
