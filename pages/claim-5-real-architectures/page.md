# Claim 5 — real architectures and early stopping

## Current verdict: VERIFIED

The prior judge found no real-model evidence. The current route runs the
paper's UTKFace W2S setup at its stated 20,000/2,000 scale: frozen
ImageNet-1K ResNet18 teacher, closed-form ridge head fit on 1,000 labels,
and the official OpenAI CLIP ViT-B/32 frozen pre-projection student.

| Test quantity | Result |
| --- | ---: |
| ResNet18 teacher MSE | 327.44318 |
| Best CLIP W2S MSE | 90.92108, epoch 2 |
| Epoch-20 W2S MSE | 104.00529 |
| Direct-label ceiling MSE | 43.73657 |
| Best PGR | 0.83369 |
| Shuffled-pseudolabel control MSE | 356.13712 |
| Best-epoch 80% energy dimension | 29 / 768 |

Paired bootstrap (`2,000` resamples) gives teacher-minus-best-W2S
`236.52211`, 95% CI `[211.81238,263.14850]`; final-minus-best
`13.08421`, CI `[10.06708,16.21927]`; and control-minus-best
`265.21603`, CI `[245.24461,285.83970]`. Thus the real student beats its
teacher and stopping at epoch 2 is materially better than training through
epoch 20.

The checker imports no experiment code, recomputes all displayed MSEs from
the 2,000-row CSV in float64, confirms all 20 checkpoints, and rejects a
`+0.01` corrupted summary. All 11 checks pass.

Final cumulative evidence: run `de09d92b-ea82-4644-9341-d390cc9785b0`, Git
`e1a3b3a3248f1386118f3c3303e7412859cd72bd`, HF `cpu-upgrade`;
24 useful cores estimated, 64 logical CPUs allocated; the Claim 5 command
took 1,807.543 s and the fixed command took 1,912.079 s (32m34s including
remote setup).

Raw SHA-256:

- summary `86ac978356c0a1606e78ac5c21eb9031a3a5f94b6c30dfbeb10c0cf6e76825f2`
- checkpoints `4981224dba5dbdd8de45b023ed8f2f5de8c7c7191803b1a9eab762e2845dfcae`
- 2,000 predictions `af45dbe0b75a2a32276b80240bcf2cc9baf12840ff3c53bdadf7f88b8bac0914`
- bootstrap `0ba20f1ae34e012a35b191359df8807b1fa8c93214ce0e2e41c58802496ff3e3`
- checker `e3696ef824fcf0f09a94c203dcbb92bcb0e7b627454f7fead35298d6cce3b99b`

## Evaluator bundle

- Exact claim, source scope, and assumptions:
  [contract](../../evidence/claim-5/claim_contract.json) and
  [source audit](../../evidence/claim-5/source_audit.md)
- Raw evidence: [summary](../../evidence/claim-5/experiment_summary.json),
  [all checkpoints](../../evidence/claim-5/checkpoints.csv),
  [2,000 predictions](../../evidence/claim-5/test_predictions.csv), and
  [bootstrap intervals](../../evidence/claim-5/bootstrap.json)
- Independent [checker output](../../evidence/claim-5/independent_checker.json)
  and executable [checker](../../repro/claims/claim5_real_architecture/verify.py)
- Executable [experiment](../../repro/claims/claim5_real_architecture/experiment.py),
  [fail-closed runner](../../repro/claims/claim5_real_architecture/run.py),
  and [cumulative gate](../../repro/src/cumulative_science_gate.py)
- [Method](../../evidence/claim-5/method.md),
  [fixed command/environment](../../evidence/claim-5/exact_command_and_environment.md),
  [limitations](../../evidence/claim-5/limitations.md), and
  [evaluation record](../../evidence/claim-5/EVAL.md)

## Limits

The paper does not publish exact split indices, so seed `260601295` pins
them. The 20-epoch stopping audit extends the stated five-epoch UTKFace
protocol. Together with the preserved synthetic evidence, this directly
tests the claim's missing real-model and early-stopping requirements. It does
not claim the separate CPU-prohibitive ViT-L/16 fine-tuning panel of Figure 2.
