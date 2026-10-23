# Second qualification: advance, with a narrower performance claim

The fixed local ordering search improved symbolic Cholesky factor nonzeros on 20 of 24 unique patterns, including 8 of 9 held-out cases. The largest reduction was 3.14%. It beat the additional METIS restart comparator on 14 cases, tied 4 and lost 6. CHOLMOD tracked peak allocations decreased on 20 cases. These are useful, independently checked structural improvements; they are not new literature records.

## Scope and controls

The corpus contains 8 historical structural matrices and 16 explicitly synthetic SPD matrices across 2D grids,3D grids, geometric graphs and banded random graphs. The original duplicate bcsstk 07 is excluded. This broadens structural patterns but does NOT yet add diverse empirical application families. The held-out split covers one new historical matrix and eight larger generated instances; the algorithm and its 512 proposals per seed were fixed before evaluation and not tuned on this split.

Every run starts from the best of natural, RCM, AMD and four seeded METIS orderings. Two local runs use seeds 419 and 503. Additional seeded METIS restarts receive the local runs' combined wall budget, with a single-call granularity overrun and a 256 call safety cap; no cap was reached. Full orders, scores, traces and budgets are retained. Extra search sometimes helps METIS more than our local method, so there is no universal optimizer superiority claim.

The C bitset scorer and a separate Python set-elimination checker agree. CHOLMOD numerical factorization uses the given permutation, disables postordering and uses simplicial LL. Its symbolic counts agree with the exact checker; numerical solves pass backward-error checks. Seven interleaved batches each perform 25 refactorizations and 25 solves. Memory measurements are CHOLMOD-tracked allocations, not process RSS.

## Utility result

Candidate median refactorization time was lower on 13 of 24 cases, with mixed changes and visible shared-host noise even on unchanged patterns. A broad speedup is not established. Exploratory break-even estimates range from hundreds to tens of thousands of repeated factorizations when the observed savings are positive; they are not validated amortization promises. Search overhead matters. Peak allocation savings are real within this fixed CHOLMOD mode, but generally small.

## Next gate

Advance to empirical matrices from several application families and a controlled repeated-factorization benchmark, including CHOLMOD's normal automatic/supernodal choices. Investigate portfolios that choose between cheap ordering restarts and local improvement. Preserve held-out instances. A numerical-linear-algebra reviewer should qualify workload choice and baseline settings before public performance claims.

Evidence: corpus.json, protocol.json, summary-metrics.json and results/round2/. Source snapshot: executed-sources/. Candidate verification: tools/verify.py now supports the new NPZ inputs. Local participation remains open; scientific review pending.
