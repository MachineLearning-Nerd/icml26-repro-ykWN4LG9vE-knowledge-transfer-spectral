# What Makes a Strong Model? — current verification

Previous live judged score: **6/10**. This candidate makes no claim that the
score has changed.

## Current claim navigation

| Claim | Canonical page | Current verdict |
| --- | --- | --- |
| 1 | [Teacher-to-student decomposition](#/claim-1-geometric-decomposition) | VERIFIED |
| 2 | [Exact DER rate](#/claim-2-kd-horizon) | VERIFIED |
| 3 | [Exact Theorem 4 quantifier](#/claim-3-theorem4-exact) | FALSIFIED |
| 4 | [Exact Theorem 5 PGR/rate audit](#/claim-4-theorem5-exact) | FALSIFIED |
| 5 | [Real architectures and early stopping](#/claim-5-real-architectures) | VERIFIED |

Supporting pages: [methods](#/methods),
[negative controls](#/negative-controls), and
[claim-by-claim conclusion](#/conclusion).

## Evaluator-visible evidence matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Claim 1](#/claim-1-geometric-decomposition) | [verifier](../repro/src/verify_transfer.py) | [inline](#/claim-1-geometric-decomposition) | [JSON](../evidence/claim-1/independent_verification.json) | [test](../repro/tests/test_transfer.py) | [noncommuting audit](../evidence/claim-1/independent_verification.json) | [contract](../evidence/claim-1/claim_contract.json) | VERIFIED |
| 2 | [Claim 2](#/claim-2-kd-horizon) | [verifier](../repro/src/verify_theorem3_der_exact.py) | [inline](#/claim-2-kd-horizon) | [JSON](../evidence/claim-2/exact_der_certificate.json) | [independent](../evidence/claim-2/independent_checker.json) | [five controls](../evidence/claim-2/exact_der_certificate.json) | [contract](../evidence/claim-2/claim_contract.json) | VERIFIED |
| 3 | [Claim 3](#/claim-3-theorem4-exact) | [verifier](../repro/claims/claim3_theorem4_quantifier/verify.py) | [inline](#/claim-3-theorem4-exact) | [JSON](../evidence/claim-3/exact_counterexample.json) | [independent](../evidence/claim-3/independent_checker.json) | [five controls](../evidence/claim-3/exact_counterexample.json) | [contract](../evidence/claim-3/claim_contract.json) | FALSIFIED |
| 4 | [Claim 4](#/claim-4-theorem5-exact) | [verifier](../repro/claims/claim4_theorem5_rate/verify.py) | [inline](#/claim-4-theorem5-exact) | [JSON](../evidence/claim-4/exact_rate_audit.json) | [independent](../evidence/claim-4/independent_checker.json) | [four controls](../evidence/claim-4/exact_rate_audit.json) | [contract](../evidence/claim-4/claim_contract.json) | FALSIFIED |
| 5 | [Claim 5](#/claim-5-real-architectures) | [experiment](../repro/claims/claim5_real_architecture/experiment.py) | [inline](#/claim-5-real-architectures) | [2,000 rows](../evidence/claim-5/test_predictions.csv) | [independent](../evidence/claim-5/independent_checker.json) | [shuffle/corruption](../evidence/claim-5/independent_checker.json) | [contract](../evidence/claim-5/claim_contract.json) | VERIFIED |

The candidate was audited from this entrypoint without repository or
OpenResearch-dashboard context. The detailed
[visibility matrix](../reports/spectral-transfer-reproduction/visibility-matrix.md)
records every reachable file.

## Historical evidence

[Historical rejected baseline — reduced-scale Claim 3/4 W2S
page](#/claim-3-w2s-denoising) remains reachable and unchanged. The judged
Space's original pages are preserved additively; none is the default current
verifier.
