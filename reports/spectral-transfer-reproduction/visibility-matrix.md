# Evaluator-visible evidence matrix

Audit rule: begin at `README.md`, follow `pages/index.md`, and use only files
reachable from those two canonical entrypoints. OpenResearch dashboards,
run logs, unpublished branches, and hidden local paths are excluded.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [page](../../pages/claim-1-geometric-decomposition/page.md) | [verifier](../../repro/src/verify_transfer.py) | [numbers](../../pages/claim-1-geometric-decomposition/page.md) | [JSON](../../evidence/claim-1/independent_verification.json) | [independent test](../../repro/tests/test_transfer.py) | [noncommuting systems](../../evidence/claim-1/independent_verification.json) | [contract](../../evidence/claim-1/claim_contract.json) | VERIFIED |
| 2 | [page](../../pages/claim-2-kd-horizon/page.md) | [verifier](../../repro/src/verify_theorem3_der_exact.py) | [numbers](../../pages/claim-2-kd-horizon/page.md) | [certificate](../../evidence/claim-2/exact_der_certificate.json) | [independent output](../../evidence/claim-2/independent_checker.json) | [five controls](../../evidence/claim-2/exact_der_certificate.json) | [contract](../../evidence/claim-2/claim_contract.json) | VERIFIED |
| 3 | [page](../../pages/claim-3-theorem4-exact/page.md) | [verifier](../../repro/claims/claim3_theorem4_quantifier/verify.py) | [numbers](../../pages/claim-3-theorem4-exact/page.md) | [counterexample](../../evidence/claim-3/exact_counterexample.json) | [independent output](../../evidence/claim-3/independent_checker.json) | [five controls](../../evidence/claim-3/exact_counterexample.json) | [contract](../../evidence/claim-3/claim_contract.json) | FALSIFIED |
| 4 | [page](../../pages/claim-4-theorem5-exact/page.md) | [verifier](../../repro/claims/claim4_theorem5_rate/verify.py) | [numbers](../../pages/claim-4-theorem5-exact/page.md) | [rate audit](../../evidence/claim-4/exact_rate_audit.json) | [independent output](../../evidence/claim-4/independent_checker.json) | [four controls](../../evidence/claim-4/exact_rate_audit.json) | [contract](../../evidence/claim-4/claim_contract.json) | FALSIFIED |
| 5 | [page](../../pages/claim-5-real-architectures/page.md) | [experiment](../../repro/claims/claim5_real_architecture/experiment.py) | [numbers](../../pages/claim-5-real-architectures/page.md) | [2,000 predictions](../../evidence/claim-5/test_predictions.csv) | [independent output](../../evidence/claim-5/independent_checker.json) | [shuffle/corruption](../../evidence/claim-5/independent_checker.json) | [contract](../../evidence/claim-5/claim_contract.json) | VERIFIED |

Every claim page also links its source audit, assumptions, method, fixed
command and pinned environment, limitations, raw evidence, executable
checker, and cumulative-gate provenance.
