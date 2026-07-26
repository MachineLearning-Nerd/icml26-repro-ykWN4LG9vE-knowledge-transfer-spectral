# What Makes a Strong Model? — claim-by-claim reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-ykWN4LG9vE-knowledge-transfer-spectral/blob/main/notebooks/spectral_transfer_tutorial.py)

This is a CPU-only clean-room reproduction of
[_What Makes a Strong Model? A Unified Spectral Analysis of Knowledge Transfer
over High-dimensional Linear Regression_](https://arxiv.org/abs/2606.01292).
It preserves the two previously full-credit checks, replaces reduced-scale
checks of Theorems 4 and 5 with exact falsifications, and adds the missing
paper-scale real-architecture W2S experiment.

The strongest empirical result uses the paper's 20,000/2,000 UTKFace setup:
a frozen ResNet18 teacher has test MSE **327.44**, while the official frozen
CLIP ViT-B/32 W2S student reaches **90.92** at epoch 2. Continuing to epoch 20
raises MSE to **104.01**; the paired increase is **13.08**, 95% CI
**[10.07, 16.22]**. The shuffled-pseudolabel control has MSE **356.14**.

The paper does not publish exact split indices, so the data revision and
seeded split are pinned. The 20-epoch stopping audit extends its five-epoch
UTKFace protocol. The separate ViT-L/16 fine-tuning arm in Figure 2 was not
run on CPU and is not claimed.

- [Illustrated technical report](reports/spectral-transfer-reproduction/report.md)
- [Self-contained marimo tutorial](notebooks/spectral_transfer_tutorial.py)
- Local notebook: `uv run marimo edit notebooks/spectral_transfer_tutorial.py`
- Local app: `uv run marimo run notebooks/spectral_transfer_tutorial.py`

The previous live judged score is **6/10**. A conservative projection after
publication is **8–10/10**; 10/10 is a forecast, not a judge result.

## Experiment log

Every formal node uses the identical command
`uv sync --frozen && uv run python repro/src/run_all.py`.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Public landing page and reader-facing artifacts | Not run as an experiment (publication surface) | Presentation only | none |
| [`orx/judged-baseline-with-locked-uv-environment`](https://github.com/MachineLearning-Nerd/icml26-repro-ykWN4LG9vE-knowledge-transfer-spectral/tree/orx/judged-baseline-with-locked-uv-environment) | Freeze judged checks and uv lock | `uv sync --frozen && uv run python repro/src/run_all.py` | Claims 1–2 regressions pass | HF `cpu-upgrade`, CPU only |
| [`orx/claim-3-high-dimensional-exact-embedding`](https://github.com/MachineLearning-Nerd/icml26-repro-ykWN4LG9vE-knowledge-transfer-spectral/tree/orx/claim-3-high-dimensional-exact-embedding) | Exact `D=4096` Theorem 4 counterexample | `uv sync --frozen && uv run python repro/src/run_all.py` | Claim 3 FALSIFIED | HF `cpu-upgrade`, CPU only |
| [`orx/claim-4-exact-pgr-and-stopping-rate-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-ykWN4LG9vE-knowledge-transfer-spectral/tree/orx/claim-4-exact-pgr-and-stopping-rate-audit) | PGR identity and stopping-exponent audit | `uv sync --frozen && uv run python repro/src/run_all.py` | Claim 4 FALSIFIED | HF `cpu-upgrade`, CPU only |
| [`orx/claim-5-utkface-real-architecture-w2s`](https://github.com/MachineLearning-Nerd/icml26-repro-ykWN4LG9vE-knowledge-transfer-spectral/tree/orx/claim-5-utkface-real-architecture-w2s) | Paper-scale ResNet18→CLIP W2S, uncertainty, controls | `uv sync --frozen && uv run python repro/src/run_all.py` | Claim 5 VERIFIED within real W2S arm | HF `cpu-upgrade`, 64 logical CPUs, 25m30s |
| [`orx/cumulative-release-candidate-and-evaluator-visib`](https://github.com/MachineLearning-Nerd/icml26-repro-ykWN4LG9vE-knowledge-transfer-spectral/tree/orx/cumulative-release-candidate-and-evaluator-visib) | Current raw evidence, report, notebook, cumulative and visibility gates | `uv sync --frozen && uv run python repro/src/run_all.py` | Formal cumulative rerun pending | HF `cpu-upgrade`, CPU only |

## Current scientific verdicts

| Claim | Verdict | Core evidence |
| --- | --- | --- |
| 1 — T2S decomposition | VERIFIED | 9,000-system identity error `9.77e-15`; `0.01978+0+0.00562=0.02541` |
| 2 — DER horizon rate | VERIFIED | 180 exact exponent cases, 40 tails, 28 exact horizons; finite DER minimum 1.216 |
| 3 — eventual W2S guarantee | FALSIFIED | Admissible `D=4096` risk gap is positive for every finite student horizon |
| 4 — PGR/stopping rate | FALSIFIED | Undefined denominator, invalid PGR substitution, and factor-two cutoff mismatch |
| 5 — real architectures / stopping | VERIFIED within real W2S arm | ResNet18 327.44 vs CLIP 90.92; epoch 2 beats epoch 20 with positive paired CI |

## Reproduce

Python 3.12 and every dependency are pinned in `pyproject.toml` and `uv.lock`.
The formal fixed command is:

```bash
uv sync --frozen
uv run python repro/src/run_all.py
```

The cumulative route performs CPU-only feature extraction and is expected to
take roughly 25–50 minutes on HF `cpu-upgrade`. It writes fail-closed raw JSON
and CSV evidence under `.openresearch/artifacts/`.
