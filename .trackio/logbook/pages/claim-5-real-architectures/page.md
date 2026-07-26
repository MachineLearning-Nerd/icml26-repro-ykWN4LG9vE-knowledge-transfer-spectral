# Claim 5 — real architectures and early stopping

## Current verification

This page supersedes the judged omission of real-world architectures. The
current verifier is `repro/claims/claim5_real_architecture/verify.py`; the
experiment is `experiment.py`.

The real route uses the paper-scale 20,000/2,000 UTKFace split, a frozen
pretrained ResNet18 ridge teacher fit from 1,000 labels, and the official
frozen OpenAI CLIP ViT-B/32 student. It records transfer, direct-label, and
shuffled-pseudolabel heads through 20 epochs, paired uncertainty, PGR, and the
80%-projection-energy dimension. Raw outputs will be
`.openresearch/artifacts/claim-5/checkpoints.csv`,
`test_predictions.csv`, `bootstrap.json`, `experiment_summary.json`, and
`independent_checker.json`.

The executed result will be inserted additively after the HF CPU run.

## Scope

The inherited synthetic suite covers risk inheritance and early-stopping
dynamics. This route directly addresses the prior judge's missing real-model
component. The separate CPU-prohibitive ViT-L/16 fine-tuning arm of Figure 2
is not claimed.
