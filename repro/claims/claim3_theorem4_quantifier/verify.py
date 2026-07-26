#!/usr/bin/env python3
"""Exact counterexample certificate for the universal quantifier in Theorem 4."""
from __future__ import annotations

import json
import hashlib
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / ".openresearch" / "artifacts" / "claim-3"


def compact_fraction(value: Fraction) -> dict:
    """Keep exact provenance without flooding logs with million-digit integers."""
    exact = f"{value.numerator}/{value.denominator}"
    return {
        "decimal_17_digits": format(float(value), ".17g"),
        "sign": (value > 0) - (value < 0),
        "numerator_digits": len(str(abs(value.numerator))),
        "denominator_digits": len(str(value.denominator)),
        "exact_fraction_sha256": hashlib.sha256(exact.encode()).hexdigest(),
    }


def schedule(total: int, gamma0: Fraction) -> list[Fraction]:
    """Paper Algorithm 1: gamma_t=gamma0*2^-floor(t/K), K=N/log2(N)."""
    assert total > 0 and total & (total - 1) == 0
    phases = total.bit_length() - 1
    assert total % phases == 0
    interval = total // phases
    return [gamma0 / (2 ** (t // interval)) for t in range(1, total + 1)]


def teacher_moments(
    *, total: int, gamma0: Fraction, signal: Fraction, noise_variance: Fraction
) -> tuple[Fraction, Fraction]:
    """Return E[w_T]/w* coefficient c and Var(w_T), exactly."""
    gains = schedule(total, gamma0)
    remaining = Fraction(1)
    variance = Fraction(0)
    # Reverse recursion: each independent Gaussian noise coefficient is
    # gamma_t times every later contraction.
    for gain in reversed(gains):
        variance += noise_variance * (gain * remaining) ** 2
        remaining *= 1 - gain
    coefficient = 1 - remaining
    return coefficient, variance


def assumption_audit(
    *, gamma0: Fraction, signal: Fraction, full_expressivity: bool = True
) -> bool:
    # D=1, Phi(x)=x with x uniform on {-1,+1}. Sigma=1, psi=1.
    # The paper's strict step-size bound is gamma0 < min(1/2,1/2,1/100).
    return (
        0 < gamma0 < Fraction(1, 100)
        and signal != 0
        and full_expressivity
    )


def certify(
    *,
    gamma0: Fraction,
    signal: Fraction,
    noise_variance: Fraction,
    full_expressivity: bool = True,
) -> dict:
    assumptions = assumption_audit(
        gamma0=gamma0, signal=signal, full_expressivity=full_expressivity
    )
    coefficient, teacher_variance = teacher_moments(
        total=256,
        gamma0=gamma0,
        signal=signal,
        noise_variance=noise_variance,
    )
    # For every finite student horizon, w_S=a*w_T with 0<a<1. The exact
    # expected-risk difference factors as
    # (1-a)/2 * [c(2-c(1+a))*w*^2 - (1+a)V].
    # Its bracket is decreasing on a in [0,1], so its exact minimum is at a=1.
    uniform_bracket_min = 2 * (
        coefficient * (1 - coefficient) * signal**2 - teacher_variance
    )
    theorem_contradicted = assumptions and uniform_bracket_min > 0
    return {
        "assumptions_satisfied": assumptions,
        "dimension": 1,
        "teacher_samples_N": 256,
        "fourth_moment_psi": 1,
        "covariance": "Sigma=1",
        "teacher_and_student_projection": "identity",
        "intrinsic_cutoff_k_dagger": 1,
        "signal": compact_fraction(signal),
        "gaussian_noise_variance": compact_fraction(noise_variance),
        "teacher_step_gamma0": compact_fraction(gamma0),
        "teacher_mean_coefficient_c": compact_fraction(coefficient),
        "teacher_variance_V": compact_fraction(teacher_variance),
        "uniform_risk_gap_bracket_min": compact_fraction(uniform_bracket_min),
        "student_risk_strictly_above_teacher_for_every_finite_n": theorem_contradicted,
        "limit_n_to_infinity": "student risk approaches teacher risk from above",
        "verdict": "FALSIFIED" if theorem_contradicted else "NOT_ESTABLISHED",
    }


def main() -> None:
    gamma0 = Fraction(1, 1000)
    signal = Fraction(1)
    unit_noise_c, unit_noise_variance = teacher_moments(
        total=256,
        gamma0=gamma0,
        signal=signal,
        noise_variance=Fraction(1),
    )
    # Teacher variance is linear in label-noise variance. This exact choice
    # makes V=2*c*(1-c), so the witness bracket becomes strictly negative.
    high_noise_variance = (
        2 * unit_noise_c * (1 - unit_noise_c) / unit_noise_variance
    )
    witness = certify(
        gamma0=gamma0,
        signal=signal,
        noise_variance=Fraction(1, 1_000_000),
    )
    controls = {
        "zero_signal_rejected": not certify(
            gamma0=Fraction(1, 1000),
            signal=Fraction(0),
            noise_variance=Fraction(1, 1_000_000),
        )["assumptions_satisfied"],
        "unstable_step_rejected": not certify(
            gamma0=Fraction(1, 100),
            signal=Fraction(1),
            noise_variance=Fraction(1, 1_000_000),
        )["assumptions_satisfied"],
        "nonexpressive_model_rejected": not certify(
            gamma0=Fraction(1, 1000),
            signal=Fraction(1),
            noise_variance=Fraction(1, 1_000_000),
            full_expressivity=False,
        )["assumptions_satisfied"],
        "high_noise_breaks_counterexample": not certify(
            gamma0=gamma0,
            signal=signal,
            noise_variance=high_noise_variance,
        )["student_risk_strictly_above_teacher_for_every_finite_n"],
    }
    result = {
        "claim": "Theorem 4 universal eventual-W2S guarantee",
        "source_sha256": "4d29b2ae21c4611695532f6fd304b22f678139a19311e21e9b65d8a6d0b00089",
        "source_anchor": "main.tex lines 733-745; Appendix D.1 lines 2447-2523",
        "exact_witness": witness,
        "negative_controls": controls,
        "high_noise_control_variance": compact_fraction(high_noise_variance),
        "all_checks_passed": (
            witness["verdict"] == "FALSIFIED" and all(controls.values())
        ),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "exact_counterexample.json"
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if not result["all_checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
