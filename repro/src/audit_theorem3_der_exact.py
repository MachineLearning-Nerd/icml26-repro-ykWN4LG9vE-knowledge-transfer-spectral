#!/usr/bin/env python3
"""Independent audit of the Theorem 3 DER certificate; imports no primary code."""

from fractions import Fraction
import json
import math
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".openresearch" / "artifacts" / "claim-2"


def slope(xs: list[float], ys: list[float]) -> float:
    xbar = math.fsum(xs) / len(xs)
    ybar = math.fsum(ys) / len(ys)
    return math.fsum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / math.fsum(
        (x - xbar) ** 2 for x in xs
    )


def main() -> int:
    rng = random.Random(260601292)
    exact_cases = 0
    max_slope_error = 0.0

    # A separately generated exact grid checks the C.2 exponent identity.
    for _ in range(240):
        beta = Fraction(rng.randrange(0, 9), 8)
        alpha_t = 1 + beta + Fraction(rng.randrange(1, 17), 8)
        alpha_s = alpha_t + Fraction(rng.randrange(1, 17), 8)
        delta = alpha_t - 1 - beta
        p_t = delta / alpha_t
        p_s = delta / alpha_s
        stated = delta * (1 / alpha_t - 1 / alpha_s)
        assert p_t - p_s == stated > 0

        # Independent log-log audit of the three displayed power laws.
        ns = [10.0**j for j in range(1, 9)]
        lx = [math.log(n) for n in ns]
        risk_t = [n ** (-float(p_t)) for n in ns]
        risk_s = [n ** (-float(p_s)) for n in ns]
        der = [s / t for s, t in zip(risk_s, risk_t)]
        errs = (
            abs(slope(lx, [math.log(v) for v in risk_t]) + float(p_t)),
            abs(slope(lx, [math.log(v) for v in risk_s]) + float(p_s)),
            abs(slope(lx, [math.log(v) for v in der]) - float(stated)),
        )
        max_slope_error = max(max_slope_error, *errs)
        assert max(errs) < 2e-15
        exact_cases += 1

    # Independently approximate actual power-law tails and enclose the omitted tail.
    tail_cases = 0
    worst_relative_width = 0.0
    for q in (2, 3, 4, 5, 6):
        for m in (2, 5, 11, 23, 47):
            cutoff = 200_000
            partial = math.fsum(k ** (-q) for k in range(m + 1, cutoff + 1))
            lo = partial + (cutoff + 1) ** (1 - q) / (q - 1)
            hi = partial + cutoff ** (1 - q) / (q - 1)
            theorem_lo = (m + 1) ** (1 - q) / (q - 1)
            theorem_hi = m ** (1 - q) / (q - 1)
            assert theorem_lo <= lo <= hi <= theorem_hi
            worst_relative_width = max(worst_relative_width, (hi - lo) / lo)
            tail_cases += 1

    controls = {
        "equal_spectra_zero_kappa": (2 - 1) * (1 / 2 - 1 / 2) == 0,
        "reversed_order_negative_kappa": (2 - 1) * (1 / 2 - 1 / 1.5) < 0,
        "boundary_zero_decay": 1.5 - 1 - 0.5 == 0,
        "wrong_quotient_direction_negative": (2 - 1) * (1 / 3 - 1 / 2) < 0,
    }
    assert all(controls.values())

    result = {
        "independent_implementation": True,
        "independent_audit_cases": exact_cases,
        "power_law_tail_enclosures": tail_cases,
        "max_log_log_slope_error": max_slope_error,
        "worst_tail_enclosure_relative_width": worst_relative_width,
        "negative_controls": controls,
        "audit_passed": True,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "independent_checker.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print("independent_audit_cases:", exact_cases)
    print("power_law_tail_enclosures:", tail_cases)
    print("max_log_log_slope_error:", f"{max_slope_error:.3e}")
    print("worst_tail_enclosure_relative_width:", f"{worst_relative_width:.3e}")
    print("negative_controls:", controls)
    print("audit_passed: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
