# Claim 5 command and environment

- Fixed command: `uv sync --frozen && uv run python repro/src/run_all.py`
- Final cumulative run: `de09d92b-ea82-4644-9341-d390cc9785b0`
- Git: `e1a3b3a3248f1386118f3c3303e7412859cd72bd`
- Backend/flavor: Hugging Face `cpu-upgrade`
- Image: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
- Estimated useful cores: 24 (16 Torch compute, 8 image-loader workers)
- Actual allocation: 64 logical CPUs
- Claim command runtime: 1,807.543 s; fixed-command runtime: 1,912.079 s;
  remote elapsed time: 32m34s
- Seed: `260601295`
- Dataset revision: `fb7f7d7102fd040c4211002b0c43e3ab727afffc`
- Torch/torchvision: `2.7.1+cpu` / `0.22.1+cpu`
