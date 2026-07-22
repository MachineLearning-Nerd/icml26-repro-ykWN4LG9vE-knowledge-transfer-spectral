# Claim 2 — exact Theorem 3 spectral-horizon DER rate

---
<!-- trackio-cell

{"type":"markdown","id":"cell_thm3_exact_scope","created_at":"2026-07-22T15:00:00+00:00","title":"Paper-exact scope"}

-->

## Result: verified proof-level certificate

This additive audit targets the paper's **Theorem 3 (Asymptotic DER Rate)**, the exact rate result behind Claim 2's spectral-horizon mechanism. It is deliberately a deterministic proof certificate, not a claim that a finite neural-network experiment proves an asymptotic theorem.

Paper source: `https://ar5iv.labs.arxiv.org/html/2606.01292` (SHA-256 `4d29b2ae21c4611695532f6fd304b22f678139a19311e21e9b65d8a6d0b00089`). Scope: Section 3.3 DER definition; Section 5 Assumptions 2–3 and Theorem 3 (Eqs. 12–13); Appendix A.6 (Eqs. 113–117); Appendix C.2 (Eq. 173).

The source gives, in the learnable heavy-tail regime `alpha_T > 1 + beta`, the teacher/distilled rate

`E_T2S(N, n→∞) = O~(N^{-(alpha_T-1-beta)/alpha_T})`.

For a strictly weaker student (`alpha_S > alpha_T`), Appendix C.2 compares this with the direct-student rate

`E_S(N) ~ N^{-(alpha_T-1-beta)/alpha_S}`,

so their quotient obeys

`DER_N = E_S(N)/E_T2S(N,n) = Omega~(N^kappa)`,

`kappa = (alpha_T-1-beta)(1/alpha_T - 1/alpha_S) > 0`.

---
<!-- trackio-cell

{"type":"code","id":"cell_thm3_exact_primary","created_at":"2026-07-22T15:00:00+00:00","title":"Exact verifier","command":["python","repro/src/verify_theorem3_der_exact.py"],"exit_code":0}

-->

The primary verifier checks the quotient identity and strict positivity using exact `Fraction` arithmetic on 180 admissible rational parameter triples. It separately certifies 40 power-law tail sandwiches using exact finite sums plus exact integral-remainder bounds, and 28 perfect-power horizon cases where `k*_nu=N^(1/alpha_nu)` makes `DER=N^kappa` an exact integer identity.

Five falsification controls are required to fire: equal teacher/student decay, reversed capacity order, the non-learnable boundary, a sign-flipped formula, and a corrupted direct-student denominator. All are detected.

---
<!-- trackio-cell

{"type":"code","id":"cell_thm3_exact_auditor","created_at":"2026-07-22T15:00:00+00:00","title":"Independent auditor","command":["python","repro/src/audit_theorem3_der_exact.py"],"exit_code":0}

-->

An independent implementation (no import from the primary verifier) audits 240 separately generated admissible cases, recovers the three predicted log-log slopes, encloses 25 numerical power-law tails, and repeats four boundary/sign controls.

Together these checks reproduce the exact Appendix C.2 rate calculation: a strong teacher's faster spectral-horizon expansion changes the exponent inherited by the distilled student, while direct learning retains the weaker student's denominator. Their exponent gap is exactly the positive `kappa` stated by Theorem 3.
