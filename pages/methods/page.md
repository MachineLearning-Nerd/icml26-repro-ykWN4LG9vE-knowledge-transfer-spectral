# Methods and fixed execution contract

## Source and environment

The paper identity is arXiv:2606.01292 / OpenReview `ykWN4LG9vE`. The accepted
source archive is recorded in [`sources.json`](../../sources.json), and the
matching TeX is preserved as [`source/arxiv/main.tex`](../../source/arxiv/main.tex)
with SHA-256
`639811b3ce58ae86a01605e5c7c618b402cd5761bece8ab5ea7ec82f1d2f3d06`.

Python is pinned to 3.12 and dependencies to [`pyproject.toml`](../../pyproject.toml)
plus [`uv.lock`](../../uv.lock). The formal Claim 5 run used HF `cpu-upgrade`
and CPU-only execution. No GPU result is claimed.

## Evidence contract

The current gate is intentionally fresh-clone friendly. It reads the committed
records under [`evidence/cumulative_science_gate.json`](../../evidence/cumulative_science_gate.json)
and the claim evidence files; it does not require Trackio, OpenResearch,
network access, or an ephemeral remote artifact. The claim producers remain
available under [`repro/src/publication_gate.py`](../../repro/src/publication_gate.py);
their exact commands
and environments are preserved in each claim's evidence directory.

The lightweight publication command is:

```bash
uv sync --frozen
uv run --frozen python repro/src/publication_gate.py
```

It runs the unit tests, checks the cumulative committed-evidence gate, verifies
the source pin and canonical scope limits, and writes the three identical
publication-gate JSON files. The complete Claim 5 feature-extraction run is
expensive and is represented by its pinned summary, checkpoints, predictions,
bootstrap intervals, and independent checker.

## Non-circularity

Claims 3 and 4 use exact counterexamples and identity audits rather than
choosing sample sizes from the conclusion under test. Claim 4's independent
horizon sweep compares the stated and reconstructed exponents across six
decades of `log10(N)`. Claim 5 predeclares the 20-epoch extension, confidence
intervals, and shuffled-label control; neither best epoch nor tolerances are
selected after seeing the outcomes.
