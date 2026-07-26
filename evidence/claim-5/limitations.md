# Claim 5 limitations and deviations

The paper does not publish exact UTKFace split indices, so this reproduction
uses a deterministic seeded split from a pinned public revision. The
20-epoch early-stopping audit extends the paper's five-epoch UTKFace
projection-energy run; the first five checkpoints remain the primary protocol.

This route reproduces Figure 3's real W2S architecture experiment. It does not
fine-tune the much larger ViT-L/16 teacher from Figure 2 on CPU. Synthetic
risk-inheritance evidence remains in the cumulative suite, but a reviewer may
still require the separate real ViT-L distillation arm before treating every
panel of both figures as independently reproduced.

If this one route does not meet its predeclared confidence intervals, it is
BLOCKED rather than FALSIFIED: a failed run on one public split cannot
contradict a broad empirical claim.
