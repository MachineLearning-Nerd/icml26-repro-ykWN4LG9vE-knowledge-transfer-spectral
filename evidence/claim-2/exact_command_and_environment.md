# Claim 2 command and environment

- Fixed command: `uv sync --frozen && uv run python repro/src/run_all.py`
- Environment: repository `pyproject.toml` and `uv.lock`, Python 3.12
- Formal image: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
- Backend/flavor: Hugging Face `cpu-upgrade`
- Useful numerical threads: one; actual allocation recorded by each run
- Deterministic audit seed: `260601292`

Exact output is written to `exact_der_certificate.json`; the separate
auditor writes `independent_checker.json`.

- Final cumulative run: `de09d92b-ea82-4644-9341-d390cc9785b0`
- Git: `e1a3b3a3248f1386118f3c3303e7412859cd72bd`
- Actual allocation: 64 logical CPUs
- Exact certificate runtime: 0.088 s; independent audit: 0.959 s
- Fixed-command runtime: 1,912.079 s; remote elapsed time: 32m34s
