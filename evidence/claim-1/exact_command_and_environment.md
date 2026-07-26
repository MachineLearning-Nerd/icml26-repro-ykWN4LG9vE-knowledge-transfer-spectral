# Claim 1 command and environment

- Fixed command: `uv sync --frozen && uv run python repro/src/run_all.py`
- Environment: repository `pyproject.toml` plus `uv.lock`, Python 3.12
- Formal image: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
- Backend/flavor: Hugging Face `cpu-upgrade`
- Numerical threads: one for inherited synthetic checks
- Seeds: `19`, `260601292`, `260601293`, and the preserved decomposition's
  deterministic `20000+s` sequence

The final cumulative run records its Git SHA, actual allocation, and runtime
in the log and release manifest:

- Final cumulative run: `de09d92b-ea82-4644-9341-d390cc9785b0`
- Git: `e1a3b3a3248f1386118f3c3303e7412859cd72bd`
- Actual allocation: 64 logical CPUs
- Claim 1 verifier runtime: 94.237 s; preserved decomposition regression:
  6.240 s
- Fixed-command runtime: 1,912.079 s; remote elapsed time: 32m34s
