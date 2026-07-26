# Claim 5 — real architectures and early stopping

## Current verdict: VERIFIED within the exact real W2S arm

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

Formal evidence: run `490d55c1-62c7-45ba-a22f-0abb3693ac39`, Git
`3a71e66759eb4b8f05cd17c19e07a514bff76b03`, HF `cpu-upgrade`;
24 useful cores estimated, 64 logical CPUs allocated; 1,530.238 s cumulative.

Raw SHA-256:

- summary `68a5acb6...`
- checkpoints `4981224d...`
- 2,000 predictions `af45dbe0...`
- bootstrap `0ba20f1a...`
- checker `e3696ef8...`

## Limits

The paper does not publish exact split indices, so seed `260601295` pins
them. The 20-epoch stopping audit extends the stated five-epoch UTKFace
protocol. This route verifies the missing real W2S arm; it does not claim the
separate CPU-prohibitive ViT-L/16 fine-tuning arm of Figure 2.
