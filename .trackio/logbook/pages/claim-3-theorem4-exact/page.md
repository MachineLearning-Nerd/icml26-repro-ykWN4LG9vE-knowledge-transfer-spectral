# Claim 3 — exact Theorem 4 quantifier

## Current verdict: FALSIFIED_AS_WRITTEN

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

Formal evidence is committed in the exact witness, independent checker, and
horizon audit. A corrected theorem could add a strictly positive-spectrum
condition; no such condition appears in the quantified statement.

## Evaluator bundle

- Exact quantified statement and assumption witness:
  [contract](../../evidence/claim-3/claim_contract.json) and
  [source audit](../../evidence/claim-3/source_audit.md)
- Raw evidence: [exact counterexample](../../evidence/claim-3/exact_counterexample.json),
  [80-digit checker](../../evidence/claim-3/independent_checker.json), and
  [horizon audit](../../evidence/claim-3/independent_horizon_audit.csv)
- Executable current checks:
  [exact verifier](../../repro/claims/claim3_theorem4_quantifier/verify.py),
  [independent auditor](../../repro/claims/claim3_theorem4_quantifier/audit.py),
  and [fail-closed runner](../../repro/claims/claim3_theorem4_quantifier/run.py)
- [Method](../../evidence/claim-3/method.md),
  [fixed command/environment](../../evidence/claim-3/exact_command_and_environment.md),
  [limitations](../../evidence/claim-3/limitations.md), and
  [evaluation record](../../evidence/claim-3/EVAL.md)

The final cumulative run `de09d92b-ea82-4644-9341-d390cc9785b0` at Git
`e1a3b3a3248f1386118f3c3303e7412859cd72bd` reran the counterexample,
five falsification controls, independent audit, and cumulative gate.

## Historical rejected baseline

The D=60 spectral-filter sweep remains preserved at
`#/claim-w2s-recovery`. It is corroborative only and is not the current
verifier.
