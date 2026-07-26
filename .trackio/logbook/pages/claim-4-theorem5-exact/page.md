# Claim 4 — exact Theorem 5 PGR/rate audit

## Current verdict: FALSIFIED

The displayed theorem is inconsistent with its own PGR definition and
cutoff relation.

1. Section 6 includes self-distillation. Identical expressive teacher and
   direct-student models, streams, initialization, and schedules give
   `R_T-R_S=0` pathwise, so PGR is undefined under the stated assumptions.
2. The proof replaces `1-PGR` with `R_T2S/R_T`. The definition instead gives
   `(R_T2S-R_S)/(R_T-R_S)`; equality requires the unstated condition
   `R_S*(R_T-R_T2S)=0`.
3. At `alpha_T=alpha_S=2`, the reported stopping horizon is `N^(1/10)`.
   The paper's own `k*~(n/log n)^(1/alpha_S)` relation requires `N^(1/5)`.
   The reported route produces cutoff exponent `1/20`, risk exponent `-7/10`
   rather than `-9/10`, and PGR-gap exponent `-1/5` rather than `-2/5`.

An independent sweep from `N=10^20` to `10^200` approaches slopes `0.05`
for the theorem route and `0.10` for the reconstruction. All four negative
controls fire.

Current verifier: `repro/claims/claim4_theorem5_rate/verify.py`; independent
checker: `audit.py`. Formal run `36f6aceb-e4c0-4f7f-abe3-37f9d26b4736`,
Git `d255238`, HF `cpu-upgrade`, 107.463 s cumulative.

## Historical rejected baseline

The preserved D=60 PGR sweep at `#/claim-w2s-recovery` did not test the
displayed asymptotic rate and is not the current verifier.
