# Claim 3 — exact Theorem 4 quantifier

## Current verification

This page supersedes the reduced-scale spectral-filter page for Theorem 4.
The exact contract is the main-text quantifier: under Assumptions 1, 4, and 5,
there exists `n_0` such that **every** `n>n_0` has expected student risk
strictly below expected teacher risk.

The current verifier is
`repro/claims/claim3_theorem4_quantifier/verify.py`; the independent
implementation is `audit.py`. They use the paper's Algorithm 1, exact rational
arithmetic, positive signal and positive Gaussian noise, explicit assumption
checks, and four falsification controls. Raw outputs are
`.openresearch/artifacts/claim-3/exact_counterexample.json`,
`independent_checker.json`, and `independent_horizon_audit.csv`.

The executed result will be inserted additively after the OpenResearch run.

## Historical rejected baseline

The D=60 ridge-to-spectral-truncation sweep remains preserved at
`#/claim-w2s-recovery`. It is corroborative but does not establish this
universal theorem.
