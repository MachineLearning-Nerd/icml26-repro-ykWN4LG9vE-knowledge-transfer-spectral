# Claim 3 command and environment

- Fixed command: `uv sync --frozen && uv run python repro/src/run_all.py`
- Formal run: `0dfe0a37-1914-46f3-8024-e9f5f3db3ffa`
- Git: `cedf9ad`
- Backend/flavor: Hugging Face `cpu-upgrade`
- Image: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
- Estimated useful cores: one; actual allocation: 64 logical CPUs
- Cumulative runtime: 73.176 s
- Deterministic arithmetic: exact `Fraction`; independent Decimal precision 80

The frozen claim run above established the result. Final cumulative
regression run `de09d92b-ea82-4644-9341-d390cc9785b0` at Git
`e1a3b3a3248f1386118f3c3303e7412859cd72bd` reran it in 0.401 s on
64 allocated logical CPUs; the fixed command took 1,912.079 s (32m34s
including remote setup).
