# Claim-by-claim conclusion

Previous live judged score: **6/10**. No score change is claimed before a new
live judge verdict.

| Claim | Current evidence verdict | Confidence | What the evidence establishes |
| --- | --- | --- | --- |
| 1 | `VERIFIED_SCOPED` | HIGH | Finite decomposition and 9,000-system identity audit pass |
| 2 | `VERIFIED_SCOPED` | HIGH | Exact DER certificate, independent audit, and controls pass |
| 3 | `FALSIFIED_AS_WRITTEN` | HIGH | Exact `D=4096` assumption-satisfying counterexample |
| 4 | `FALSIFIED_AS_WRITTEN` | HIGH | Exact PGR-definition and stopping-rate contradictions |
| 5 | `VERIFIED_SCOPED_WITH_PROTOCOL_LIMITS` | MEDIUM | Paper-scale ResNet18→CLIP ViT-B/32 W2S and stopping/control audit |

The scoped collection gate passes because every committed claim contract,
independent checker, negative control, and raw-file count passes. The strict
paper-wide gate remains `NOT_READY`: exact UTKFace split indices are unpublished
and the separate ViT-L/16 fine-tuning arm from Figure 2 was not run.

Claims 3 and 4 are marked `FALSIFIED_AS_WRITTEN`, not “failed reproduction”:
each counterexample checks the stated assumptions and quantified conclusion.
Claim 5 is not described as covering every real-model panel.

Release status: **ready for scoped publication; awaiting any new live judge
verdict**. This is a workflow status, not a score change.
