# Claim 3 source audit

Source retrieved 2026-07-26 from `https://ar5iv.labs.arxiv.org/html/2606.01292`
with an explicit `OpenResearch-Reproduction/1.0` User-Agent. SHA-256:
`4d29b2ae21c4611695532f6fd304b22f678139a19311e21e9b65d8a6d0b00089`.
The matching TeX is in `source/arxiv/main.tex`.

The main-text theorem is `thm:w2s_bound` in Section 6 (TeX lines 733–745):
under the fourth-moment, sufficient-expressivity, and low-intrinsic-dimension
assumptions, it says there exists `n_0` such that **for all** `n > n_0` the
student's expected risk is strictly below the teacher's.

The appendix proof (D.1; TeX lines 2447–2523) instead assumes the student is
early-stopped and “weak in the tail” (`delta` small), discards positive
student-variance and bias terms as negligible, and derives a sufficient
comparison. Those added conditions do not establish the main theorem's
eventual universal quantifier.

The counterexample uses the exact Algorithm 1 updates and step-decay schedule,
not spectral truncation or ridge regression. The theorem states no lower bound
on `D`, no positive-definiteness condition on the covariance, and no
power-law-spectrum premise. We nevertheless use `D=4096`, with
`Phi(x)=xi*e_1`, `w*=e_1`, and identity teacher/student model projections.
For every PSD `A`, the fourth-moment left side is
`A_11 e_1 e_1^T <= tr(A) I`, so Assumption 1 holds with `psi=1`; the exact
signal tail after `k_dagger=1` is zero, satisfying Assumption 5.
