# Featured-candidate preparation assessment

Sparse ordering is stronger after this preparation round. Four historical power-network admittance matrices were added, unchanged numerically and without diagonal shifts. Three improved against AMD plus four seeded METIS baselines: 494_bus fell from 1,414 to 1,412; 685_bus from 3,650 to 3,630; and 1138_bus from 3,265 to 3,263 factor nonzeros. 662_bus remained at 2,549. Exact symbolic checks and CHOLMOD numerical/SPD/residual checks passed.

The launch catalog then inherited the best of every previous local candidate, baseline and METIS restart. A fixed donor rehearsal (2,048 proposals, seed 2301) improved all six selected instances beyond that reconciled frontier:

| Instance | Inherited factor nonzeros | New factor nonzeros |
|---|---:|---:|
| bcsstk04 |3273|3258|
| bcsstk06 |10895|10843|
| bcsstk08 |30957|30645|
| geometric-2 |16341|16167|
| banded_random-0 |3094|3044|
|685_bus|3630|3618|

These gains are promoted in frozen frontier v002. New donors start there; v001 and all trial traces remain available. The active catalog has 28 unique inputs: 12 historical matrices across two empirical families and 16 synthetic examples. The donor instances were selected, not a randomized estimate of participation success. No novelty relative to all literature is claimed.

The original broader-round numerical timing results remain mixed. This preparation strengthens the case for a featured symbolic-ordering project, not a general acceleration claim. The public brief separates these claims explicitly.

Distribution tooling now includes strict hash-bound submissions, safe permutation checks before the native scorer, independent symbolic validation, current-vs-historical frontier reporting, versioned promotion, staged base-code PR validation, contributor templates and clean-install checks. Prepared Ubuntu automation has not run locally because Docker is unavailable. Historical input redistribution review and an independent numerical-linear-algebra review remain outstanding launch checks.

The candidate-PR verifier was also rehearsed in an isolated Git repository: a valid certificate passed despite a deliberately broken verifier on the candidate branch, while a forged metric failed. The trusted base checker handled both; candidate code was not executed. See pr-check-rehearsal.json.
