# Claim 4 evaluation

## Verdict: FALSIFIED

Theorem 5's displayed PGR and early-stopping rates are internally
inconsistent as written.

1. Section 6 explicitly includes self-distillation. Identical expressive
   teacher and direct-student models, streams, initialization, and schedules
   have `R_T-R_S=0` pathwise, so the paper's PGR denominator is zero.
2. The proof substitutes `1-PGR=R_T2S/R_T`. From the stated definition,
   `1-PGR=(R_T2S-R_S)/(R_T-R_S)`; the substitution requires the unstated
   condition `R_S*(R_T-R_T2S)=0`.
3. At `alpha_T=alpha_S=2`, the theorem reports an `N^(1/10)` stopping
   horizon. Its own cutoff relation
   `k* ~ (n/log n)^(1/alpha_S)` requires `N^(1/5)` to reach the advertised
   cutoff. The claimed route yields cutoff exponent `1/20`, risk exponent
   `-7/10` instead of `-9/10`, and PGR-gap exponent `-1/5` instead of `-2/5`.

An independent sweep from `N=10^20` through `10^200` approaches cutoff
slopes `0.05` for the theorem route and `0.10` for the reconstructed route.
Four negative controls all fire.

Formal run: `36f6aceb-e4c0-4f7f-abe3-37f9d26b4736`, Git `d255238`, HF
`cpu-upgrade`, 64 logical CPUs allocated, one useful numerical core, 107.463 s
cumulative runtime. The fixed command was
`uv sync --frozen && uv run python repro/src/run_all.py`.

A corrected theorem could exclude identical models, define PGR only for a
nonzero teacher/direct gap, assume an oracle `R_S=0`, and multiply the stopping
exponent by `alpha_S`.

Final cumulative regression run `de09d92b-ea82-4644-9341-d390cc9785b0`
at Git `e1a3b3a3248f1386118f3c3303e7412859cd72bd` reran all three
contradictions, the independent checker, four controls, and cumulative gate;
all passed.
