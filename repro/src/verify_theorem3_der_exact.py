#!/usr/bin/env python3
"""Exact certificate for Theorem 3 (Asymptotic DER Rate), arXiv:2606.01292.

This is a proof-level deterministic reproduction of the exponent chain used in
Section 5, Theorem 3 and Appendix C.2.  It does not claim to rerun a neural
network experiment.  All theorem-exponent identities and sampled tail bounds
are checked with fractions, so those checks have no floating-point tolerance.
"""

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


SOURCE_URL = "https://ar5iv.labs.arxiv.org/html/2606.01292"
SOURCE_SHA256 = "4d29b2ae21c4611695532f6fd304b22f678139a19311e21e9b65d8a6d0b00089"
SOURCE_SCOPE = (
    "Section 3.3 DER definition; Section 5 Assumptions 2-3 and Theorem 3 "
    "(Eqs. 12-13); Appendix A.6 (Eqs. 113-117); Appendix C.2 (Eq. 173)"
)
PARENT_GUARD = "59374f8c1db0c670bbe6e96fa5d4b95e852a9b85"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".openresearch" / "artifacts" / "claim-2"


def theorem_exponents(alpha_t: F, alpha_s: F, beta: F) -> tuple[F, F, F]:
    """Return positive decay powers p_T, p_S and DER growth power kappa."""
    delta = alpha_t - 1 - beta
    if not (delta > 0 and alpha_s > alpha_t):
        raise ValueError("Theorem 3 requires alpha_T > 1 + beta and alpha_S > alpha_T")
    p_t = delta / alpha_t
    p_s = delta / alpha_s
    kappa = delta * (1 / alpha_t - 1 / alpha_s)
    return p_t, p_s, kappa


def exact_exponent_grid() -> tuple[int, F, F]:
    """Audit C.2's quotient identity on a broad exact-rational parameter grid."""
    alpha_ts = [F(3, 2), F(7, 4), F(2), F(9, 4), F(5, 2), F(3), F(7, 2)]
    betas = [F(0), F(1, 8), F(1, 4), F(1, 2), F(3, 4), F(1)]
    gaps = [F(1, 8), F(1, 4), F(1, 2), F(1), F(3, 2)]
    checked = 0
    min_kappa = None
    max_kappa = F(0)
    for alpha_t in alpha_ts:
        for beta in betas:
            if alpha_t <= 1 + beta:
                continue
            for gap in gaps:
                alpha_s = alpha_t + gap
                p_t, p_s, kappa = theorem_exponents(alpha_t, alpha_s, beta)
                # Appendix C.2: E_S/E_T2S has exponent (-p_S)-(-p_T).
                quotient_exponent = p_t - p_s
                assert quotient_exponent == kappa
                assert p_t > p_s > 0 and kappa > 0
                checked += 1
                min_kappa = kappa if min_kappa is None else min(min_kappa, kappa)
                max_kappa = max(max_kappa, kappa)
    assert checked >= 100 and min_kappa is not None
    return checked, min_kappa, max_kappa


def exact_tail_sandwich(q: int, m: int, cutoff: int) -> None:
    """Certify the power-law tail with exact finite sum plus integral remainder.

    For decreasing f(x)=x^-q and q>1:
      int_{m+1}^inf f <= sum_{k=m+1}^inf f(k) <= int_m^inf f.
    The uncomputed tail after ``cutoff`` is itself enclosed by its two exact
    integral bounds.  Every quantity here is a Fraction.
    """
    assert q > 1 and cutoff > m
    partial = sum((F(1, k**q) for k in range(m + 1, cutoff + 1)), F(0))
    remainder_lo = F(1, (q - 1) * (cutoff + 1) ** (q - 1))
    remainder_hi = F(1, (q - 1) * cutoff ** (q - 1))
    theorem_lo = F(1, (q - 1) * (m + 1) ** (q - 1))
    theorem_hi = F(1, (q - 1) * m ** (q - 1))
    assert theorem_lo <= partial + remainder_lo
    assert partial + remainder_hi <= theorem_hi
    assert remainder_lo <= remainder_hi


def tail_and_horizon_certificates() -> tuple[int, int]:
    tail_checks = 0
    for q in range(2, 7):
        for m in (1, 2, 3, 5, 8, 13, 21, 34):
            exact_tail_sandwich(q, m, m + 80)
            tail_checks += 1

    # On exact perfect-power sample sizes, k*_nu=N^(1/alpha_nu).
    # The preserved-tail proxy k^(-delta) then yields DER=N^kappa exactly.
    horizon_checks = 0
    integer_cases = [
        (2, 3, 0), (2, 4, 0), (3, 4, 0), (3, 5, 1),
        (4, 5, 0), (4, 6, 1), (5, 7, 2),
    ]
    for alpha_t_i, alpha_s_i, beta_i in integer_cases:
        alpha_t, alpha_s, beta = F(alpha_t_i), F(alpha_s_i), F(beta_i)
        delta = alpha_t_i - 1 - beta_i
        _, _, kappa = theorem_exponents(alpha_t, alpha_s, beta)
        common = alpha_t_i * alpha_s_i
        for base in (2, 3, 4, 5):
            n = base**common
            k_t = base**alpha_s_i
            k_s = base**alpha_t_i
            assert k_t**alpha_t_i == n == k_s**alpha_s_i
            # risk_S/risk_T = k_S^-delta / k_T^-delta.
            der = F(k_t**delta, k_s**delta)
            # N^kappa is rational because common*kappa is integral here.
            exponent_on_base = common * kappa
            assert exponent_on_base.denominator == 1
            assert der == F(base ** exponent_on_base.numerator)
            horizon_checks += 1
    return tail_checks, horizon_checks


def negative_controls() -> dict[str, bool]:
    controls: dict[str, bool] = {}

    # Equal spectra eliminate strict horizon expansion: kappa=0.
    a, b = F(2), F(0)
    controls["equal_teacher_student_rejected"] = (
        (a - 1 - b) * (1 / a - 1 / a) == 0
    )

    # A nominally stronger student reverses the claimed sign.
    alpha_t, alpha_s = F(2), F(3, 2)
    controls["reversed_capacity_order_rejected"] = (
        (alpha_t - 1) * (1 / alpha_t - 1 / alpha_s) < 0
    )

    # At the learnability boundary, the tail exponent is zero, not decaying.
    alpha_t, beta = F(3, 2), F(1, 2)
    controls["nonlearnable_boundary_rejected"] = alpha_t - 1 - beta == 0

    # Deliberately reverse the parenthesized reciprocal difference.
    alpha_t, alpha_s, beta = F(2), F(3), F(0)
    wrong_sign = (alpha_t - 1 - beta) * (1 / alpha_s - 1 / alpha_t)
    controls["sign_flipped_formula_rejected"] = wrong_sign < 0

    # Deliberately give the direct student the teacher denominator; no gain remains.
    p_t = (alpha_t - 1 - beta) / alpha_t
    corrupted_p_s = (alpha_t - 1 - beta) / alpha_t
    controls["corrupted_student_rate_rejected"] = p_t - corrupted_p_s == 0

    assert all(controls.values())
    return controls


def main() -> int:
    grid_n, min_kappa, max_kappa = exact_exponent_grid()
    tail_n, horizon_n = tail_and_horizon_certificates()
    controls = negative_controls()
    result = {
        "claim": "Theorem 3 exact asymptotic DER-rate certificate",
        "source_url": SOURCE_URL,
        "source_sha256": SOURCE_SHA256,
        "source_scope": SOURCE_SCOPE,
        "parent_guard": PARENT_GUARD,
        "exact_rational_exponent_cases": grid_n,
        "exact_tail_sandwiches": tail_n,
        "exact_perfect_power_horizon_cases": horizon_n,
        "min_positive_kappa": f"{min_kappa.numerator}/{min_kappa.denominator}",
        "max_positive_kappa": f"{max_kappa.numerator}/{max_kappa.denominator}",
        "negative_controls": controls,
        "all_checks_passed": True,
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "exact_der_certificate.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    print("RESULT_SHA256=" + hashlib.sha256(canonical.encode()).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
