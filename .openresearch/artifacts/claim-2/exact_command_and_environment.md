# Claim 2 command and environment

- Fixed command: `uv sync --frozen && uv run python repro/src/run_all.py`
- Environment: repository `pyproject.toml` and `uv.lock`, Python 3.12
- Formal image: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
- Backend/flavor: Hugging Face `cpu-upgrade`
- Useful numerical threads: one; actual allocation recorded by each run
- Deterministic audit seed: `260601292`

Exact output is written to `exact_der_certificate.json`; the separate
auditor writes `independent_checker.json`.
