# Claim 4 command and environment

- Fixed command: `uv sync --frozen && uv run python repro/src/run_all.py`
- Formal run: `36f6aceb-e4c0-4f7f-abe3-37f9d26b4736`
- Git: `d255238`
- Backend/flavor: Hugging Face `cpu-upgrade`
- Image: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
- Estimated useful cores: one; actual allocation: 64 logical CPUs
- Cumulative runtime: 107.463 s
- Exact exponents: `Fraction`; independent horizons: `N=10^20...10^200`

The frozen claim run above established the result. Final cumulative
regression run `de09d92b-ea82-4644-9341-d390cc9785b0` at Git
`e1a3b3a3248f1386118f3c3303e7412859cd72bd` reran it in 0.178 s on
64 allocated logical CPUs; the fixed command took 1,912.079 s (32m34s
including remote setup).
