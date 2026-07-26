# Claim-by-claim conclusion

Previous live judged score: **6/10**. No score change is claimed before a new
live judge verdict.

| Claim | Current evidence verdict | Confidence | What changed |
| --- | --- | --- | --- |
| 1 | VERIFIED | HIGH | Prior full-credit evidence preserved and rerun |
| 2 | VERIFIED | HIGH | Prior exact certificate and finite run preserved and rerun |
| 3 | FALSIFIED | HIGH | Exact `D=4096` assumption-satisfying counterexample replaces D=60 toy evidence |
| 4 | FALSIFIED | HIGH | Exact PGR identity, undefined-denominator, and stopping-rate contradictions replace qualitative D=60 evidence |
| 5 | VERIFIED | MEDIUM | Paper-scale ResNet18→official CLIP ViT-B/32 UTKFace run plus stopping CI and controls |

Conservative projected score after publication: **8–10/10**. Best-supported
possible score: **10/10 forecast**, not a judge result. The principal risk is
Claim 5's explicitly unrun, CPU-prohibitive ViT-L/16 fine-tuning arm from the
separate Figure 2 real-KD experiment.

Claims 3 and 4 are marked `FALSIFIED`, not “failed reproduction”: each
counterexample directly checks the stated assumptions and quantified
conclusion. Claim 5 is not described as covering every real-model panel.

Release status: **awaiting live judge after publication**. This phrase is a
workflow status only; it is not a score change.
