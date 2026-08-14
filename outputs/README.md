# Output records

The canonical current gate is [`../publication_gate.json`](../publication_gate.json).
The duplicate [`publication_gate.json`](publication_gate.json) and
[`RELEASE_CANDIDATE_READY.json`](RELEASE_CANDIDATE_READY.json) are intentionally
byte-identical copies for consumers that expect an output directory.

[`CUMULATIVE_SCIENCE_GATE.json`](CUMULATIVE_SCIENCE_GATE.json) records the
claim-level checks over the committed `evidence/` bundle.

[`PUBLICATION_GATE_PASSED.json`](PUBLICATION_GATE_PASSED.json) is retained for
historical provenance only. It predates the exact Claim 3/4 audits and the
paper-scale Claim 5 evidence; do not use it as the current status.
