# Claim 4 method

The primary verifier uses exact `Fraction` arithmetic. It tests
`alpha_T=alpha_S=2`, `k_dagger=1`, and the self-distillation limit explicitly
included by Section 6. Rademacher features with
`lambda_k,T=lambda_k,S=k^-2`, identity projections, and `w*=e_1` satisfy the
fourth-moment, expressivity, low-intrinsic-dimension, and even the implicit
power-law premises.

There are two independent contradictions:

1. Identical teacher/direct-student models, data, initialization, and SGD have
   `R_T=R_S` pathwise, so the defined PGR denominator is zero.
2. The theorem's own cutoff relation maps its claimed `n~N^(1/10)` to
   `k*~N^(1/20)`, not the required `N^(1/10)`. Substitution into its displayed
   head/tail balance gives risk exponent `-7/10`, not `-9/10`, and PGR-gap
   exponent `-1/5`, not `-2/5`.

An independent implementation reconstructs the cutoff slopes through
`N=10^200`. Controls cover the `alpha_S=1` coincidence, the unstated
zero-direct-risk special case, a nonzero direct risk, and the corrected
sample-count exponent.
