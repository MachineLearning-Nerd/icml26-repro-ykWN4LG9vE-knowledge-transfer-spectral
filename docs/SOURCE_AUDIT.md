# Source and paper audit

## Paper identity

- **Title:** What Makes a Strong Model? A Unified Spectral Analysis of
  Knowledge Transfer over High-dimensional Linear Regression
- **Authors:** Wendao Wu, Fangqing Zhang, Haihan Zhang, Cong Fang
- **arXiv:** [2606.01292](https://arxiv.org/abs/2606.01292)
- **OpenReview:** [ykWN4LG9vE](https://openreview.net/forum?id=ykWN4LG9vE)
- **Source record:** [`sources.json`](../sources.json)

## Pinning

The accepted source archive is identified by the SHA-256 recorded in
`sources.json`:

```text
source tar: 6be526270e43be790c30465ffb8c55a993b60e0195577014e0b120d468b7c36d
```

The active TeX file preserved in this repository is
[`source/arxiv/main.tex`](../source/arxiv/main.tex):

```text
main.tex: 639811b3ce58ae86a01605e5c7c618b402cd5761bece8ab5ea7ec82f1d2f3d06
```

Verify the local pin with:

```bash
shasum -a 256 source/arxiv/main.tex
```

The source archive contained the paper, bibliography, style files, and figures
but no author implementation. The reproduction code in `repro/` is therefore
clean-room code written against the pinned paper source.

## Source anchors used by the audit

| Audit area | Source anchor |
| --- | --- |
| T2S decomposition | Theorem 1 and the decomposition equations in `main.tex` |
| DER rate | Theorem 3, Eqs. 12–13, 113–117, and 173 |
| Eventual W2S guarantee | Theorem 4 and Appendix D.1 |
| PGR/stopping rates | Theorem 5, Section 6, and Appendix B.4 |
| Real-architecture protocol | Figures 2–3 and the UTKFace experiment section |

Each claim's `source_audit.md` file records the narrower lines and assumptions
used by its verifier. The audit does not treat an abstract, figure caption, or
secondary summary as a substitute for the theorem statement.

## Reproduction boundaries

The source does not publish exact UTKFace train/test indices or an author
implementation. Claim 5 consequently records the dataset revision, seeded
split, model checkpoints, hashes, resource policy, and protocol, but does not
claim bit-identical data selection. The paper's separate ViT-L/16 fine-tuning
arm was not run. These are explicit scope limits, not hidden assumptions.
