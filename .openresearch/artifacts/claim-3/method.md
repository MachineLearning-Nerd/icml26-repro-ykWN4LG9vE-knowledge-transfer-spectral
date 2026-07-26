# Claim 3 method

Use a nonzero one-dimensional task, `Phi(x)=x` with Rademacher `x`, target
`w*=1`, and positive Gaussian label-noise variance `10^-6`. Both models have
identity feature maps. Thus `Sigma=1`, the fourth-moment condition holds with
`psi=1`, both projections are identity, and the signal is exactly supported at
`k_dagger=1`.

The teacher takes `N=256` Algorithm 1 steps from zero with `gamma_0=10^-3`,
well below the paper's strict `10^-2` stability ceiling. Exact Fraction
recursion gives `w_T=c w*+zeta`, with zero-mean `zeta` and variance `V`.
For every finite student horizon, the same algorithm gives `w_S=a w_T` with
`0<a<1`. The expected risk difference factors exactly as

`(1-a)/2 * [c(2-c(1+a))*w*^2 - (1+a)V]`.

The bracket decreases in `a`, so a single exact check at `a=1` proves the risk
gap is positive for every finite `n`. An independent 80-digit Decimal
implementation reconstructs the teacher recursion and audits horizons through
`n=1,048,576`.

Controls reject a zero target, a boundary-violating step size, and a
non-expressive model; a deliberately high-noise instance must break the
counterexample certificate.
