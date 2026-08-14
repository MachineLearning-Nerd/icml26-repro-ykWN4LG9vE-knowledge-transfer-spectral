# ICML 2026 — What Makes a Strong Model?

Claim-by-claim, source-pinned reproduction audit for **“What Makes a Strong
Model? A Unified Spectral Analysis of Knowledge Transfer over High-dimensional
Linear Regression.”**

Paper: [arXiv:2606.01292](https://arxiv.org/abs/2606.01292) · OpenReview:
[`ykWN4LG9vE`](https://openreview.net/forum?id=ykWN4LG9vE)

Authors: Wendao Wu, Fangqing Zhang, Haihan Zhang, and Cong Fang.

## Status

The committed audit is **`VERIFIED_SCOPED_WITH_SOURCE_DEFECTS`**. Claims 1, 2,
and the real-architecture arm of Claim 5 are verified within their stated
scope. Theorem 4 (Claim 3) and Theorem 5 (Claim 4) are falsified as written by
assumption-satisfying exact audits. The strict paper-wide gate is
**`NOT_READY`** because Claim 5 does not include the paper's separate ViT-L/16
fine-tuning arm and the paper's exact UTKFace split indices are unpublished.

The previous live judged score was **6/10**. This repository makes **no claim
that the score has changed** and gives no score forecast.

The final intended repository name is
[`MachineLearning-Nerd/icml26-spectral-knowledge-transfer`](https://github.com/MachineLearning-Nerd/icml26-spectral-knowledge-transfer).

## What the paper studies

The paper develops a unified spectral account of knowledge transfer. Its
claims connect (1) teacher-to-student risk decomposition, (2) a distillation
effective-rate/horizon result, (3) an eventual weak-to-strong guarantee, (4)
performance-recovery and stopping-rate asymptotics, and (5) synthetic and
real-architecture experiments.

This repository is a **clean-room implementation**. The accepted source
archive contained the paper and figures but no author implementation. The
active TeX source is pinned at [`source/arxiv/main.tex`](source/arxiv/main.tex);
the complete source provenance is in [the source audit](docs/SOURCE_AUDIT.md).

## Claim ledger: how each result is produced

| Claim | Current verdict | Producer and independent check | Committed evidence | Boundary |
| --- | --- | --- | --- | --- |
| 1 — T2S decomposition | `VERIFIED_SCOPED` | [`verify_transfer.py`](repro/src/verify_transfer.py), [`verify_distill.py`](repro/src/verify_distill.py), and [`test_transfer.py`](repro/tests/test_transfer.py) | [`claim_contract.json`](evidence/claim-1/claim_contract.json) | Finite identity/decomposition checks; not a proof of every theorem constant |
| 2 — DER horizon rate | `VERIFIED_SCOPED` | [`verify_theorem3_der_exact.py`](repro/src/verify_theorem3_der_exact.py) and [`audit_theorem3_der_exact.py`](repro/src/audit_theorem3_der_exact.py) | [`exact_der_certificate.json`](evidence/claim-2/exact_der_certificate.json) | Exact rational/tail/horizon certificate plus finite corroboration |
| 3 — Theorem 4 eventual W2S guarantee | `FALSIFIED_AS_WRITTEN` | [`verify.py`](repro/claims/claim3_theorem4_quantifier/verify.py) and independent [`audit.py`](repro/claims/claim3_theorem4_quantifier/audit.py) | [`exact_counterexample.json`](evidence/claim-3/exact_counterexample.json) | One admissible `D=4096` witness has student risk above teacher for every finite horizon |
| 4 — Theorem 5 PGR/stopping rate | `FALSIFIED_AS_WRITTEN` | [`verify.py`](repro/claims/claim4_theorem5_rate/verify.py) and independent [`audit.py`](repro/claims/claim4_theorem5_rate/audit.py) | [`exact_rate_audit.json`](evidence/claim-4/exact_rate_audit.json) | Exact undefined-denominator, substitution, and exponent contradictions |
| 5 — real architectures and stopping | `VERIFIED_SCOPED_WITH_PROTOCOL_LIMITS` | [`experiment.py`](repro/claims/claim5_real_architecture/experiment.py) and independent [`verify.py`](repro/claims/claim5_real_architecture/verify.py) | [`experiment_summary.json`](evidence/claim-5/experiment_summary.json) | Paper-scale ResNet18→CLIP ViT-B/32 W2S arm; ViT-L/16 fine-tuning not run |

The detailed claim contracts, assumptions, production paths, controls, and
limitations are in [the claim audit](docs/CLAIM_AUDIT.md). The canonical
machine-readable result is [`publication_gate.json`](publication_gate.json),
with the gate semantics documented in [docs/PUBLICATION_GATE.md](docs/PUBLICATION_GATE.md).

## Headline evidence

- **Claim 1:** 9,000 noncommuting systems satisfy the static identity with
  maximum error `9.769962616701378e-15`; the finite decomposition is
  `0.01978 + 0 + 0.00562 = 0.02541`.
- **Claim 2:** the exact certificate covers 180 rational exponent cases, 40
  tail sandwiches, and 28 perfect-power horizons; the finite corroboration's
  minimum DER is `1.215879`.
- **Claim 3:** an assumption-satisfying `D=4096` exact witness has a positive
  student-minus-teacher risk gap for every finite positive `n`, approaching
  zero only from above.
- **Claim 4:** self-distillation can make the PGR denominator zero; the proof's
  PGR substitution is not an identity in general; and the displayed stopping,
  risk, and PGR exponents disagree at `alpha_T=alpha_S=2`.
- **Claim 5:** on the pinned UTKFace split, frozen ResNet18 teacher MSE is
  `327.44318`, best frozen CLIP ViT-B/32 W2S MSE is `90.92108` at epoch 2,
  epoch-20 MSE is `104.00529`, and the shuffled-pseudolabel control is
  `356.13712`. Bootstrap paired 95% CIs are positive for all three declared
  comparisons.

## Branch map

The original branches were generated by an experiment runner and used the
`orx/` prefix. They are normalized below to describe the evidence they carry;
the old names are retained only as provenance. Exact original tips, final tips,
and commit-identity checks are in [the branch audit](docs/BRANCH_AUDIT.md).

| Final branch | Former branch | Purpose |
| --- | --- | --- |
| `main` | `main` | Public landing page, canonical evidence, and release gate |
| `baseline/judged-locked-uv` | `orx/judged-baseline-with-locked-uv-environment` | Reproduce and freeze the judged Claims 1–2 baseline |
| `audit/claim-3-theorem4-quantifier` | `orx/claim-3-exact-theorem-4-quantifier-audit` | Exact Theorem 4 quantifier audit |
| `audit/claim-3-high-dimensional-witness` | `orx/claim-3-high-dimensional-exact-embedding` | High-dimensional admissible counterexample |
| `audit/claim-4-pgr-stopping-rate` | `orx/claim-4-exact-pgr-and-stopping-rate-audit` | Exact PGR and stopping-rate audit |
| `experiment/claim-5-real-architecture-w2s` | `orx/claim-5-utkface-real-architecture-w2s` | Paper-scale UTKFace ResNet18→CLIP W2S experiment |
| `release/cumulative-candidate` | `orx/cumulative-release-candidate-and-evaluator-visib` | Cumulative evidence, visibility, and release candidate |

Every published branch is normalized to the exact GitHub no-reply identity
`MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>`.

## Reproduce and verify

The environment is pinned by [`pyproject.toml`](pyproject.toml) and
[`uv.lock`](uv.lock). From a fresh clone:

```bash
uv sync --frozen
uv run --frozen python -m pytest -q repro/tests
uv run --frozen python repro/src/verify_transfer.py --output /tmp/claim1.json
uv run --frozen python repro/src/verify_theorem3_der_exact.py
uv run --frozen python repro/src/audit_theorem3_der_exact.py
uv run --frozen python repro/claims/claim3_theorem4_quantifier/verify.py
uv run --frozen python repro/claims/claim3_theorem4_quantifier/audit.py
uv run --frozen python repro/claims/claim4_theorem5_rate/verify.py
uv run --frozen python repro/claims/claim4_theorem5_rate/audit.py
uv run --frozen python repro/src/cumulative_science_gate.py
uv run --frozen python repro/src/publication_gate.py
```

The publication gate validates the committed source-pinned evidence bundle and
reruns the lightweight tests; the exact audit records are checked as committed
evidence. The full Claim 5 feature-extraction experiment is intentionally
not part of the lightweight gate: the recorded run took about 30 minutes on a
64-logical-CPU HF `cpu-upgrade` machine. Its exact command and environment are
recorded in [`evidence/claim-5/exact_command_and_environment.md`](evidence/claim-5/exact_command_and_environment.md).

## Citation

```bibtex
@article{wu2026strongmodel,
  title         = {What Makes a Strong Model? A Unified Spectral Analysis of Knowledge Transfer over High-dimensional Linear Regression},
  author        = {Wu, Wendao and Zhang, Fangqing and Zhang, Haihan and Fang, Cong},
  journal       = {arXiv preprint arXiv:2606.01292},
  year          = {2026},
  doi           = {10.48550/arXiv.2606.01292}
}
```

## Thank you

Thank you to Wendao Wu, Fangqing Zhang, Haihan Zhang, and Cong Fang for
developing and sharing this spectral perspective on knowledge transfer. The
paper's explicit assumptions and mathematical structure made a claim-by-claim,
clean-room audit possible. This repository is an independent reproduction and
audit, not an author-maintained implementation.

## License and attribution

The paper source and figures remain attributed to their authors and the source
archive. The reproduction code and audit artifacts are published by
MachineLearning-Nerd; consult the source archive and any upstream dataset/model
licenses before redistribution.
