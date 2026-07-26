# Claim 4 source audit

Source retrieved 2026-07-26 from
`https://ar5iv.labs.arxiv.org/html/2606.01292` with explicit User-Agent
`OpenResearch-Reproduction/1.0`. SHA-256:
`4d29b2ae21c4611695532f6fd304b22f678139a19311e21e9b65d8a6d0b00089`.

The PGR definition at TeX lines 350–356 is
`(R_T-R_T2S)/(R_T-R_S)`. Theorem 5 at lines 780–800 states an optimal `n`,
optimal T2S risk, and `1-PGR` rate. Its proof at lines 2522–2609 instead sets
`1-PGR=R_T2S/R_T`; exact cross multiplication shows this requires
`R_S*(R_T-R_T2S)=0`, an assumption the theorem does not state.

The proof first derives an optimal effective cutoff
`k* ~ N^[1/(alpha_T(2 alpha_S+1))]` and then reports the same exponent for
sample count `n`. Appendix B.4 (lines 2323–2331) independently derives
`k* ~ (n/log n)^(1/alpha_S)`. Therefore fixed-step SGD requires the exponent
of `n` to be `alpha_S` times the exponent of `k*`, except in the coincidence
case `alpha_S=1`.
