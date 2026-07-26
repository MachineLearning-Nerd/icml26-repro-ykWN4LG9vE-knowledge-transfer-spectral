# Claim 1 — teacher-to-student risk decomposition

## Current verdict: VERIFIED

Theorem 1 bounds expected transfer risk by three interpretable terms:
propagated teacher error, student optimization error, and irreducible
alignment bias. In the learned head, teacher error has coefficient one; in
the unlearned tail it is multiplied by `2 delta^2`.

The current cumulative verifier reruns two accepted checks:

- 9,000 random noncommuting teacher/student subspace systems satisfy the
  static alignment-bias identity with maximum absolute error
  `9.769962616701378e-15`;
- in the paper's linear-Gaussian setting at `D=60`, propagated error
  `0.01978` + optimization error `0.0` + alignment bias `0.00562` =
  measured T2S risk `0.02541`.

The executable checks are `repro/src/verify_transfer.py` and the preserved
judged regression `repro/src/verify_distill.py`. The fixed command is:

```bash
uv sync --frozen && uv run python repro/src/run_all.py
```

The numerical decomposition is finite-scale evidence for the displayed
components, not a formal proof of every constant in the upper bound. It
preserves the prior full-credit evidence without expanding its scope.
