# Claim-by-claim release report

Previous live judged score: `6/10`. This report records reproduction evidence
and scope; it is not a new score sheet. No score change or score forecast is
claimed.

## Current status

The current repository result is `VERIFIED_SCOPED_WITH_SOURCE_DEFECTS`; the
strict paper-wide gate is `NOT_READY`.

| Claim | Evidence status | What passed | Remaining boundary |
| --- | --- | --- | --- |
| 1 | `VERIFIED_SCOPED` | 9,000-system identity and finite three-part decomposition | Finite evidence, not every theorem constant |
| 2 | `VERIFIED_SCOPED` | Exact rational DER certificate, independent reconstruction, finite corroboration, and controls | Declared algebraic contract rather than every asymptotic detail |
| 3 | `FALSIFIED_AS_WRITTEN` | Exact `D=4096` assumption-satisfying witness contradicts the universal eventual strict W2S quantifier | Falsifies the displayed theorem, not all W2S experiments |
| 4 | `FALSIFIED_AS_WRITTEN` | Undefined PGR denominator, invalid substitution, and exact stopping-rate mismatch | Audits the displayed definitions and rates |
| 5 | `VERIFIED_SCOPED_WITH_PROTOCOL_LIMITS` | Paper-scale ResNet18→CLIP ViT-B/32 W2S, stopping CI, shuffled-label control, and raw recomputation | Exact split indices and ViT-L/16 fine-tuning arm are unavailable/not run |

## Evidence entrypoints

- [Canonical logbook index](../../pages/index.md)
- [Illustrated report](report.md)
- [Visibility matrix](visibility-matrix.md)
- [Claim audit and production map](../../docs/CLAIM_AUDIT.md)
- [Source audit](../../docs/SOURCE_AUDIT.md)
- [Publication gate](../../docs/PUBLICATION_GATE.md)
- [Evaluator-blind red-team record](../../audit/red-team-review.md)
- [Fail-closed release verifier](../../audit/verify_release.py)
- [Cumulative science gate](../../evidence/cumulative_science_gate.json)
- [Claim 1 evidence](../../evidence/claim-1/EVAL.md)
- [Claim 2 evidence](../../evidence/claim-2/EVAL.md)
- [Claim 3 evidence](../../evidence/claim-3/EVAL.md)
- [Claim 4 evidence](../../evidence/claim-4/EVAL.md)
- [Claim 5 evidence](../../evidence/claim-5/EVAL.md)

## Reproduction contract

The environment is pinned by `pyproject.toml` and `uv.lock`. The lightweight
fresh-clone gate is:

```bash
uv sync --frozen
uv run --frozen python repro/src/publication_gate.py
```

The full real-architecture feature-extraction run is expensive and is
represented by the committed Claim 5 summary, checkpoints, predictions,
bootstrap intervals, and independent checker. Its exact historical command and
resource record remain in
[`evidence/claim-5/exact_command_and_environment.md`](../../evidence/claim-5/exact_command_and_environment.md).

## Historical safety

The exact judged revision is archived under
[`historical/judged-39d8a32354134ce1777ce9adefe8f26e86ebc11b/PROTECTED_MANIFEST.sha256`](../../historical/judged-39d8a32354134ce1777ce9adefe8f26e86ebc11b/PROTECTED_MANIFEST.sha256).
The earlier reduced-scale W2S pages remain reachable but are explicitly marked
`HISTORICAL_REJECTED_BASELINE`; they are not the current verifier.
