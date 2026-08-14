# What Makes a Strong Model? — current verification

Paper: [arXiv:2606.01292](https://arxiv.org/abs/2606.01292) · OpenReview
[`ykWN4LG9vE`](https://openreview.net/forum?id=ykWN4LG9vE)

Authors: Wendao Wu, Fangqing Zhang, Haihan Zhang, and Cong Fang.

Current collection status: **`VERIFIED_SCOPED_WITH_SOURCE_DEFECTS`**. The
strict paper-wide gate is **`NOT_READY`**. Previous live judged score: **6/10**;
no score change is claimed.

## Current claim navigation

| Claim | Canonical page | Current verdict |
| --- | --- | --- |
| 1 | [Teacher-to-student decomposition](#/claim-1-geometric-decomposition) | `VERIFIED_SCOPED` |
| 2 | [Exact DER rate](#/claim-2-kd-horizon) | `VERIFIED_SCOPED` |
| 3 | [Exact Theorem 4 quantifier](#/claim-3-theorem4-exact) | `FALSIFIED_AS_WRITTEN` |
| 4 | [Exact Theorem 5 PGR/rate audit](#/claim-4-theorem5-exact) | `FALSIFIED_AS_WRITTEN` |
| 5 | [Real architectures and early stopping](#/claim-5-real-architectures) | `VERIFIED_SCOPED_WITH_PROTOCOL_LIMITS` |

Supporting pages: [methods](#/methods), [negative controls](#/negative-controls),
[claim-by-claim conclusion](#/conclusion), and the
[claim audit](../docs/CLAIM_AUDIT.md).

## Evaluator-visible evidence matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Claim 1](#/claim-1-geometric-decomposition) | [verifier](../repro/src/verify_transfer.py) | [inline](#/claim-1-geometric-decomposition) | [JSON](../evidence/claim-1/independent_verification.json) | [test](../repro/tests/test_transfer.py) | [noncommuting audit](../evidence/claim-1/independent_verification.json) | [contract](../evidence/claim-1/claim_contract.json) | `VERIFIED_SCOPED` |
| 2 | [Claim 2](#/claim-2-kd-horizon) | [verifier](../repro/src/verify_theorem3_der_exact.py) | [inline](#/claim-2-kd-horizon) | [JSON](../evidence/claim-2/exact_der_certificate.json) | [independent](../evidence/claim-2/independent_checker.json) | [five controls](../evidence/claim-2/exact_der_certificate.json) | [contract](../evidence/claim-2/claim_contract.json) | `VERIFIED_SCOPED` |
| 3 | [Claim 3](#/claim-3-theorem4-exact) | [verifier](../repro/claims/claim3_theorem4_quantifier/verify.py) | [inline](#/claim-3-theorem4-exact) | [JSON](../evidence/claim-3/exact_counterexample.json) | [independent](../evidence/claim-3/independent_checker.json) | [five controls](../evidence/claim-3/exact_counterexample.json) | [contract](../evidence/claim-3/claim_contract.json) | `FALSIFIED_AS_WRITTEN` |
| 4 | [Claim 4](#/claim-4-theorem5-exact) | [verifier](../repro/claims/claim4_theorem5_rate/verify.py) | [inline](#/claim-4-theorem5-exact) | [JSON](../evidence/claim-4/exact_rate_audit.json) | [independent](../evidence/claim-4/independent_checker.json) | [four controls](../evidence/claim-4/exact_rate_audit.json) | [contract](../evidence/claim-4/claim_contract.json) | `FALSIFIED_AS_WRITTEN` |
| 5 | [Claim 5](#/claim-5-real-architectures) | [experiment](../repro/claims/claim5_real_architecture/experiment.py) | [inline](#/claim-5-real-architectures) | [2,000 rows](../evidence/claim-5/test_predictions.csv) | [independent](../evidence/claim-5/independent_checker.json) | [shuffle/corruption](../evidence/claim-5/independent_checker.json) | [contract](../evidence/claim-5/claim_contract.json) | `VERIFIED_SCOPED_WITH_PROTOCOL_LIMITS` |

The detailed [visibility matrix](../reports/spectral-transfer-reproduction/visibility-matrix.md)
records every required evidence path. The [publication gate](../docs/PUBLICATION_GATE.md)
explains why this is a scoped pass rather than a strict paper-wide pass.

## Historical evidence

The **Historical rejected baseline** pages are titled
`HISTORICAL_REJECTED_BASELINE` and preserve the earlier reduced-scale W2S route
for provenance. They are reachable for comparison only and are not current
claim evidence.
