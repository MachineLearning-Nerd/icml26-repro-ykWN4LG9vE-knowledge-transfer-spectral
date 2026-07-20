# Status — ykWN4LG9vE

## Current step

The primary arXiv source is pinned and the three live claims have been traced
to Theorem 3.1, the KD horizon result (Theorem 4.2), and the W2S denoising
results (Theorems 5.1–5.2). Building an explicitly clean-room CPU verifier.

## Source-paper protocol

The synthetic KD protocol specifies dimension `d=100`, `N=2,000` original
examples, `n=500,000` teacher-labelled transfer examples, power-law teacher
and student spectra, and single-sample step-decay SGD. The paper has no author
implementation. Heavy execution waits until the currently active shared CPU job
completes; source audit and implementation work proceed without contention.

## Next action

Implement the full source-scale two-phase SGD protocol alongside independent
geometric, horizon-exponent, and W2S rate audits.
