# Claim 5 command and environment

- Fixed command: `uv sync --frozen && uv run python repro/src/run_all.py`
- Formal run: `490d55c1-62c7-45ba-a22f-0abb3693ac39`
- Git: `3a71e66759eb4b8f05cd17c19e07a514bff76b03`
- Backend/flavor: Hugging Face `cpu-upgrade`
- Image: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
- Estimated useful cores: 24 (16 Torch compute, 8 image-loader workers)
- Actual allocation: 64 logical CPUs
- Claim runtime: 1,437.113 s; cumulative runtime: 1,530.238 s
- Seed: `260601295`
- Dataset revision: `fb7f7d7102fd040c4211002b0c43e3ab727afffc`
- Torch/torchvision: `2.7.1+cpu` / `0.22.1+cpu`
