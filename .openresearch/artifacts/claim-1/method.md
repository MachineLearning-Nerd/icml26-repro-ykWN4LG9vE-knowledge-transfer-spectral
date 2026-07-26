# Claim 1 method

`repro/src/verify_transfer.py` generates 9,000 independently seeded,
noncommuting teacher/student subspace systems and checks the static
alignment-bias identity. The preserved judged verifier
`repro/src/verify_distill.py` reruns the `D=60` linear-Gaussian decomposition
at the selected spectral filter and writes `outputs/distill_results.json`.

The latter is scoped only as the accepted finite numerical decomposition:
propagated teacher error plus student optimization error plus alignment bias
must be nonnegative and equal the measured T2S risk. It is not used as proof
of the now-separately-audited Theorems 4 or 5.
