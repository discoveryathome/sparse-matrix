# Third-party provenance and rights

The root MIT license covers newly authored pilot code and documentation only. It does not relicense datasets, inherited solutions, dependencies or external tools.

Inputs are the Harwell–Boeing structural-engineering benchmark matrices mirrored by [NIST Matrix Market](https://math.nist.gov/MatrixMarket/). Research source metadata records exact URLs and SHA-256 values. Benchmark attribution and distribution terms are separate from our MIT code license; do not claim ownership or relicense them.

External dependencies include SuiteSparse AMD (BSD-3-Clause), METIS (Apache-2.0) through PyMetis (MIT), NumPy/SciPy (BSD-3-Clause), Matplotlib and pytest. Their distributions retain their own notices. No upstream solver source is vendored into tracked files.

The distribution-prep corpus adds HB/494_bus,662_bus,685_bus and1138_bus, attributed to D. Tylavsky (1985). Matrix Market files are fetched unchanged from NIST's psadmit collection; metadata is cross-referenced to the SuiteSparse Matrix Collection. Exact source URLs and hashes are retained in research/distribution-prep/empirical-sources.json. Cite Davis and Hu (2011), DOI10.1145/2049662.2049663 for the SuiteSparse collection. Attribution does not change the outstanding redistribution review.

The CHOLMOD numerical checker dynamically links the locally installed SuiteSparse distribution. Its upstream dependency licenses are separate from the pilot's MIT source license; compiled libraries are not committed.

Public packaging does not bundle externally sourced matrices, derived matrix archives, hydraulic network files, or downloaded reference-page/article snapshots. external-inputs.json records original sources and frozen hashes. Setup fetches the required inputs directly and reconstructs derived inputs without modifying the accepted scientific certificates. Original local research archives remain intact. Upstream terms govern downloaded inputs; the project MIT license does not replace them.
