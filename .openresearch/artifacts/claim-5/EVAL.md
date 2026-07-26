# Claim 5 evaluation

## Verdict: VERIFIED within the exact real W2S arm

The paper's UTKFace protocol was run at its stated 20,000/2,000 scale with a
frozen ImageNet-1K ResNet18 teacher fit by ridge regression on 1,000 labels and
the official OpenAI CLIP ViT-B/32 frozen pre-projection student. The paper's
five epochs were reproduced, and a predeclared 20-epoch extension tested
whether stopping early materially matters.

| Quantity | Result |
| --- | ---: |
| Teacher test MSE | 327.44318 |
| Best W2S test MSE | 90.92108 at epoch 2 |
| Final W2S test MSE | 104.00529 at epoch 20 |
| Best direct-label ceiling MSE | 43.73657 |
| Best PGR | 0.83369 |
| Best shuffled-pseudolabel MSE | 356.13712 |
| 80% projection-energy dimension at best W2S | 29 / 768 |

Paired 2,000-resample bootstrap differences:

- teacher minus best W2S: `236.52211`, 95% CI
  `[211.81238, 263.14850]`;
- final minus best W2S: `13.08421`, 95% CI
  `[10.06708, 16.21927]`;
- shuffled control minus best W2S: `265.21603`, 95% CI
  `[245.24461, 285.83970]`.

The independent checker imports no experiment code, recomputes four MSEs from
the 2,000-row prediction CSV in float64, confirms all 20 checkpoints, and
rejects a `+0.01` corrupted summary. All 11 checks pass.

Formal run: `490d55c1-62c7-45ba-a22f-0abb3693ac39`, Git
`3a71e66759eb4b8f05cd17c19e07a514bff76b03`, HF `cpu-upgrade`. Estimated
useful cores: 24 (16 Torch compute plus 8 image loaders); actual allocation:
64 logical CPUs. Claim stage: 1,437.113 s; cumulative runtime: 1,530.238 s.
Fixed command: `uv sync --frozen && uv run python repro/src/run_all.py`.

Raw SHA-256:

- `experiment_summary.json`: `68a5acb6b27514db135b21a958c61d6920da902ba1283523a9a432ee174c85f4`
- `checkpoints.csv`: `4981224dba5dbdd8de45b023ed8f2f5de8c7c7191803b1a9eab762e2845dfcae`
- `test_predictions.csv`: `af45dbe0b75a2a32276b80240bcf2cc9baf12840ff3c53bdadf7f88b8bac0914`
- `bootstrap.json`: `0ba20f1ae34e012a35b191359df8807b1fa8c93214ce0e2e41c58802496ff3e3`
- `independent_checker.json`: `e3696ef824fcf0f09a94c203dcbb92bcb0e7b627454f7fead35298d6cce3b99b`

Limitations: the paper does not publish exact split indices, so the split is
pinned by seed `260601295`; the 20-epoch audit extends its five-epoch UTKFace
protocol; this verifies the missing real W2S arm but does not claim the
separate CPU-prohibitive ViT-L/16 fine-tuning arm of Figure 2.
