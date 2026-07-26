# Claim 4 — exact Theorem 5 rate audit

## Current verification

The exact contract is Theorem 5's displayed optimal early-stopping, risk, and
PGR rates under Assumptions 1, 4, and 5, using the PGR definition in Section
3.3. The current verifier is
`repro/claims/claim4_theorem5_rate/verify.py`; the independent implementation
is `audit.py`.

The verifier audits both the PGR denominator and the paper's own mapping from
sample count to effective spectral cutoff. It uses exact rational exponents,
an explicit self-distillation assumption witness, four negative controls, and
an independent sweep through `N=10^200`. Raw outputs will be
`.openresearch/artifacts/claim-4/exact_rate_audit.json`,
`independent_checker.json`, and `independent_cutoff_sweep.csv`.

The executed result will be inserted additively after the OpenResearch run.

## Historical rejected baseline

The D=60 qualitative PGR sweep remains preserved at
`#/claim-w2s-recovery` in the judged Space. It did not test the displayed
rate.
