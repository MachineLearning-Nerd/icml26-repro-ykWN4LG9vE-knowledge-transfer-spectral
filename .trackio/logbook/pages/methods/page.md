# Methods and fixed execution contract

## Source and environment

Paper HTML was retrieved on 2026-07-26 from
`https://ar5iv.labs.arxiv.org/html/2606.01292` using an explicit browser
User-Agent. SHA-256:
`4d29b2ae21c4611695532f6fd304b22f678139a19311e21e9b65d8a6d0b00089`.
The matching TeX is preserved as `source/arxiv/main.tex`.

Every experiment node uses exactly:

```bash
uv sync --frozen && uv run python repro/src/run_all.py
```

Python is pinned to 3.12 and dependencies to `pyproject.toml` plus `uv.lock`.
Formal runs use HF `cpu-upgrade` with
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim`; no GPU was used.

## Fail-closed structure

The fixed command reruns the accepted Claims 1–2 regressions, exact Claim 2
certificate and independent auditor, exact Claims 3–4 verifiers and
independent auditors, the paper-scale Claim 5 experiment and independent
checker, tests, and a cumulative science gate. Every verifier exits nonzero
if its contract, assumptions, independent check, or negative control fails.

Runtime-generated JSON and CSV files are gzip/base64-exported through the
OpenResearch log with byte count and SHA-256 because remote workers are
ephemeral. Release files are decoded and hash-checked before publication.

## Non-circularity

Claims 3 and 4 use exact counterexamples/identity audits rather than selecting
sample sizes from the formula under test. Claim 4's independent horizon sweep
compares the stated and reconstructed exponents across six decades of
`log10(N)`. Claim 5 predeclares the 20-epoch extension, acceptance confidence
intervals, and shuffled-label control; neither best epoch nor tolerances are
selected after seeing the outcomes.
