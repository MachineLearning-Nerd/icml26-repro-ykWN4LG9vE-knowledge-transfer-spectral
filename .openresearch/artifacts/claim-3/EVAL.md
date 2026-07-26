# Claim 3 evaluation

## Verdict: FALSIFIED

Theorem 4 states a universal eventual strict inequality: under Assumptions 1,
4, and 5 there exists `n_0` such that every `n > n_0` has expected T2S risk
strictly below the teacher risk. The exact verifier constructs an admissible
`D=4096` instance for which the reverse strict inequality holds for every
finite positive `n`.

- Feature distribution: `Phi(x)=xi e_1`, with Rademacher `xi`
- Covariance: `diag(1,0,...,0)`
- Teacher and student projections: `I_4096`
- Target: `w*=e_1`, hence `k_dagger=1` and exact zero signal tail
- Teacher samples: `N=256`
- Positive Gaussian label-noise variance: `10^-6`
- Teacher/student initial steps: `1/1000` and `1/2000`
- Exact uniform positive risk-gap bracket: `0.11428578335051473`

The independent 80-digit implementation checked horizons through `n=2^20`;
the gap decreases toward zero from above, with the final sampled gap
`9.6337134808993e-25`. Five controls reject zero signal, an unstable step,
non-expressive models, a non-low-dimensional embedding, and a high-noise
setting that destroys the witness.

Formal run: `0dfe0a37-1914-46f3-8024-e9f5f3db3ffa`, Git `cedf9ad`, HF
`cpu-upgrade`, 64 logical CPUs allocated, one useful numerical core, 73.176 s
cumulative runtime. The fixed command was
`uv sync --frozen && uv run python repro/src/run_all.py`.

This is a valid falsification only of the theorem as written. A corrected
theorem could require a strictly positive covariance spectrum or another
non-degeneracy condition not present in the statement.
