# Claim 1 — teacher-to-student risk decomposition

## Current verdict: VERIFIED_SCOPED

Theorem 1 bounds expected transfer risk by three interpretable terms:
propagated teacher error, student optimization error, and irreducible
alignment bias. In the learned head, teacher error has coefficient one; in
the unlearned tail it is multiplied by `2 delta^2`.

The committed evidence and lightweight tests cover two accepted checks:

- 9,000 random noncommuting teacher/student subspace systems satisfy the
  static alignment-bias identity with maximum absolute error
  `9.769962616701378e-15`;
- in the paper's linear-Gaussian setting at `D=60`, propagated error
  `0.01978` + optimization error `0.0` + alignment bias `0.00562` =
  measured T2S risk `0.02541`.

The evidence producers are `repro/src/verify_transfer.py` and the preserved
judged regression `repro/src/verify_distill.py`; the independent regression is
`repro/tests/test_transfer.py`. The fixed experiment command is:

```bash
uv sync --frozen && uv run python repro/src/run_all.py
```

The numerical decomposition is finite-scale evidence for the displayed
components, not a formal proof of every constant in the upper bound. It
preserves the prior full-credit evidence without expanding its scope.

## Evaluator bundle

- Exact claim and assumptions: [contract](../../evidence/claim-1/claim_contract.json)
  and [source audit](../../evidence/claim-1/source_audit.md)
- Raw outputs: [decomposition](../../evidence/claim-1/distill_results.json)
  and [independent 9,000-system audit](../../evidence/claim-1/independent_verification.json)
- Executable current checks:
  [transfer verifier](../../repro/src/verify_transfer.py),
  [preserved decomposition regression](../../repro/src/verify_distill.py), and
  [cumulative gate](../../repro/src/cumulative_science_gate.py)
- [Method](../../evidence/claim-1/method.md),
  [fixed command/environment](../../evidence/claim-1/exact_command_and_environment.md),
  [limitations](../../evidence/claim-1/limitations.md), and
  [evaluation record](../../evidence/claim-1/EVAL.md)

The current publication gate validates the committed records without requiring
the historical remote run or any hidden OpenResearch artifact.
