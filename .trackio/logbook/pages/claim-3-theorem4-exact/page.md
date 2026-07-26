# Claim 3 — exact Theorem 4 quantifier

## Current verdict: FALSIFIED

Theorem 4 says that under Assumptions 1, 4, and 5 there exists `n_0` such
that **every** `n>n_0` has expected T2S risk strictly below teacher risk.

The exact verifier gives an assumption-satisfying counterexample embedded in
`D=4096`: `Phi(x)=xi e_1` for Rademacher `xi`, covariance
`diag(1,0,...,0)`, identity teacher/student projections, `w*=e_1`,
`k_dagger=1`, `N=256`, positive Gaussian noise variance `10^-6`, and stable
initial steps `1/1000` and `1/2000`.

Exact fraction arithmetic factors the student-minus-teacher risk as a
positive factor times a bracket whose uniform minimum is
`0.11428578335051473`. Therefore the student risk is **strictly above** the
teacher risk for every finite positive `n`, approaching equality only from
above. The independent 80-digit implementation checks horizons through
`n=1,048,576`; its last gap is `9.6337134808993e-25`.

Five controls reject zero signal, an unstable step, nonexpressive models, a
non-low-dimensional embedding, and a high-noise value that destroys the
witness. Current verifier: `repro/claims/claim3_theorem4_quantifier/verify.py`;
independent checker: `audit.py`.

Formal evidence: run `0dfe0a37-1914-46f3-8024-e9f5f3db3ffa`, Git `cedf9ad`,
HF `cpu-upgrade`, 73.176 s cumulative. A corrected theorem could add a
strictly positive-spectrum condition; no such condition appears in the
quantified statement.

## Historical rejected baseline

The D=60 spectral-filter sweep remains preserved at
`#/claim-w2s-recovery`. It is corroborative only and is not the current
verifier.
