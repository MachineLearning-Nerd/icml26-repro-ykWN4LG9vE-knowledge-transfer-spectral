# Publication gate

The repository publishes two different notions of readiness so that a strong
scoped audit is not confused with a complete paper reproduction.

## Current result

- `gate_status`: `SCOPED_PASS`
- `overall_status`: `VERIFIED_SCOPED_WITH_SOURCE_DEFECTS`
- `strict_paper_gate`: `NOT_READY`
- previous live score: `6/10`
- score change claimed: `false`

The current claim verdicts are:

| Claim | Verdict |
| --- | --- |
| 1 | `VERIFIED_SCOPED` |
| 2 | `VERIFIED_SCOPED` |
| 3 | `FALSIFIED_AS_WRITTEN` |
| 4 | `FALSIFIED_AS_WRITTEN` |
| 5 | `VERIFIED_SCOPED_WITH_PROTOCOL_LIMITS` |

## What the gate checks

[`repro/src/cumulative_science_gate.py`](../repro/src/cumulative_science_gate.py)
reads only committed files under `evidence/` plus the lightweight output and
historical-page checks. It does not require `.openresearch`, Trackio, network
access, or an ephemeral remote run. It writes
[`outputs/CUMULATIVE_SCIENCE_GATE.json`](../outputs/CUMULATIVE_SCIENCE_GATE.json).

[`repro/src/publication_gate.py`](../repro/src/publication_gate.py):

1. runs the pinned unit tests;
2. checks the committed exact audit records and Claim 1/2 evidence;
3. invokes the cumulative committed-evidence gate;
4. verifies the paper/source identity and source hash;
5. checks the exact Claim 3 and Claim 4 falsification records;
6. checks the Claim 5 summary, independent checker, and 2,000-row raw file;
7. writes identical canonical JSON to `publication_gate.json`,
   `outputs/publication_gate.json`, and
   `outputs/RELEASE_CANDIDATE_READY.json`.

The full Claim 5 feature-extraction command remains documented in its evidence
record and is intentionally excluded from this lightweight gate because it is
an expensive, already-recorded experiment.

## Historical output

`outputs/PUBLICATION_GATE_PASSED.json` is preserved as a historical artifact
from the earlier Claims 1–3-only gate. It is not the current publication gate
and is not overwritten. The canonical current result is
[`publication_gate.json`](../publication_gate.json).
