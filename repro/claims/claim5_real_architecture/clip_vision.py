"""Minimal OpenAI CLIP ViT-B/32 vision loader for frozen feature extraction.

The module structure follows openai/CLIP `clip/model.py` at retrieval SHA-256
9902cbe5ee90a1da2aa3e6f043e8a23dc1f8831193b963785c9af03d5c7bef2c.
Only the vision path is retained; no tokenizer or text model is needed.
"""
from __future__ import annotations

from collections import OrderedDict
from pathlib import Path

import torch
from torch import nn


class LayerNorm(nn.LayerNorm):
    def forward(self, value: torch.Tensor) -> torch.Tensor:
        original_type = value.dtype
        return super().forward(value.float()).to(original_type)


class QuickGELU(nn.Module):
    def forward(self, value: torch.Tensor) -> torch.Tensor:
        return value * torch.sigmoid(1.702 * value)


class ResidualAttentionBlock(nn.Module):
    def __init__(self, width: int, heads: int) -> None:
        super().__init__()
        self.attn = nn.MultiheadAttention(width, heads)
        self.ln_1 = LayerNorm(width)
        self.mlp = nn.Sequential(
            OrderedDict(
                [
                    ("c_fc", nn.Linear(width, width * 4)),
                    ("gelu", QuickGELU()),
                    ("c_proj", nn.Linear(width * 4, width)),
                ]
            )
        )
        self.ln_2 = LayerNorm(width)

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        attended = self.attn(
            self.ln_1(value),
            self.ln_1(value),
            self.ln_1(value),
            need_weights=False,
        )[0]
        value = value + attended
        return value + self.mlp(self.ln_2(value))


class Transformer(nn.Module):
    def __init__(self, width: int, layers: int, heads: int) -> None:
        super().__init__()
        self.resblocks = nn.Sequential(
            *[ResidualAttentionBlock(width, heads) for _ in range(layers)]
        )

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        return self.resblocks(value)


class VisionTransformer(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        input_resolution = 224
        patch_size = 32
        width = 768
        output_dim = 512
        self.conv1 = nn.Conv2d(
            3, width, kernel_size=patch_size, stride=patch_size, bias=False
        )
        scale = width**-0.5
        self.class_embedding = nn.Parameter(scale * torch.randn(width))
        self.positional_embedding = nn.Parameter(
            scale
            * torch.randn((input_resolution // patch_size) ** 2 + 1, width)
        )
        self.ln_pre = LayerNorm(width)
        self.transformer = Transformer(width, 12, 12)
        self.ln_post = LayerNorm(width)
        self.proj = nn.Parameter(scale * torch.randn(width, output_dim))

    def forward(self, images: torch.Tensor) -> torch.Tensor:
        """Return the 768-dimensional pre-projection features used by paper."""
        value = self.conv1(images)
        value = value.reshape(value.shape[0], value.shape[1], -1)
        value = value.permute(0, 2, 1)
        cls = self.class_embedding.to(value.dtype) + torch.zeros(
            value.shape[0],
            1,
            value.shape[-1],
            dtype=value.dtype,
            device=value.device,
        )
        value = torch.cat([cls, value], dim=1)
        value = self.ln_pre(
            value + self.positional_embedding.to(value.dtype)
        )
        value = self.transformer(value.permute(1, 0, 2))
        value = value.permute(1, 0, 2)
        return self.ln_post(value[:, 0, :])


def load_visual(checkpoint: Path) -> VisionTransformer:
    """Load the official OpenAI JIT archive into the minimal vision module."""
    archive = torch.jit.load(str(checkpoint), map_location="cpu")
    visual_state = {
        name.removeprefix("visual."): tensor.float()
        for name, tensor in archive.state_dict().items()
        if name.startswith("visual.")
    }
    model = VisionTransformer()
    missing, unexpected = model.load_state_dict(visual_state, strict=False)
    if missing or unexpected:
        raise RuntimeError(
            f"CLIP visual state mismatch: missing={missing}, "
            f"unexpected={unexpected}"
        )
    return model.eval()
