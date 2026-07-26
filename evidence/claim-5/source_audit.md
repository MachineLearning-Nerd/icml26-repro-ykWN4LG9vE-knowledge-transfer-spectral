# Claim 5 source audit

Paper source retrieved 2026-07-26 from
`https://ar5iv.labs.arxiv.org/html/2606.01292` with explicit User-Agent
`OpenResearch-Reproduction/1.0`. SHA-256:
`4d29b2ae21c4611695532f6fd304b22f678139a19311e21e9b65d8a6d0b00089`.

Main-text anchors are the experiments section, TeX lines 910–1010. Appendix
anchors are lines 2721–2741 for real distillation and lines 2767–2797 for real
W2S. The UTKFace W2S route specifies 20,000 training and 2,000 test images at
224px, frozen ResNet18 and CLIP-ViT-B/32 backbones, a ridge teacher head fit on
1,000 labels with `alpha=10^-6`, and an SGD student head with batch size 128,
learning rate `10^-4`, momentum 0.9, and five primary epochs. PCA uses 10,000
student features and reports the dimension containing 80% of head energy.

The public, ungated `nlphuji/utk_faces` dataset is pinned at revision
`fb7f7d7102fd040c4211002b0c43e3ab727afffc`; its metadata and image archive
SHA-256 values are respectively
`f46078943dc84ed141b97956f49c861c5cbc5a44ac13f9349fa7b048daf237fc`
and `938b68cafa61c4f58732f312d04caa808ddd420ff24a4c9cff0c2145e8255783`.

The official OpenAI CLIP model registry was retrieved from
`https://raw.githubusercontent.com/openai/CLIP/main/clip/clip.py` with
SHA-256 `9540f200fbf8145479fa655382a56dab048d238cc698b9cbd8df3b6d86d3f1b6`.
It pins ViT-B/32 weights by SHA-256
`40d365715913c9da98579312b702a82c18be219cc2a73407c4526f58eba950af`.
The minimal vision implementation is derived from the official `model.py`
retrieved with SHA-256
`9902cbe5ee90a1da2aa3e6f043e8a23dc1f8831193b963785c9af03d5c7bef2c`.
