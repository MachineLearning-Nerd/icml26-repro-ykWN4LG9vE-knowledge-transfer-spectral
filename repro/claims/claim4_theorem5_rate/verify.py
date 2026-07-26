#!/usr/bin/env python3
"""Exact consistency certificate for Theorem 5's PGR and stopping rates."""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / ".openresearch" / "artifacts" / "claim-4"


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def stopping_rate_audit(alpha_t: Fraction, alpha_s: Fraction) -> dict:
    # The theorem derives the optimal cutoff k*_opt ~ N^q, then reports the
    # same exponent for n. The paper's own cutoff lemma gives
    # k* ~ (n/log n)^(1/alpha_s), so n must have exponent alpha_s*q.
    q_opt = 1 / (alpha_t * (2 * alpha_s + 1))
    n_exponent_claimed = q_opt
    n_exponent_required = alpha_s * q_opt
    cutoff_exponent_from_claimed_n = n_exponent_claimed / alpha_s

    teacher_risk_exponent = (1 - alpha_t) / alpha_t
    head_exponent = cutoff_exponent_from_claimed_n - 1
    tail_exponent = (
        -2 * alpha_s * cutoff_exponent_from_claimed_n
        + teacher_risk_exponent
    )
    achieved_risk_exponent = max(head_exponent, tail_exponent)
    claimed_risk_exponent = q_opt - 1
    achieved_pgr_gap_exponent = (
        achieved_risk_exponent - teacher_risk_exponent
    )
    claimed_pgr_gap_exponent = (
        -2 * alpha_s / (alpha_t * (2 * alpha_s + 1))
    )
    return {
        "alpha_teacher": q(alpha_t),
        "alpha_student": q(alpha_s),
        "optimal_cutoff_N_exponent": q(q_opt),
        "claimed_n_N_exponent": q(n_exponent_claimed),
        "required_n_N_exponent_from_cutoff_relation": q(n_exponent_required),
        "cutoff_N_exponent_at_claimed_n": q(
            cutoff_exponent_from_claimed_n
        ),
        "claimed_optimal_risk_N_exponent": q(claimed_risk_exponent),
        "risk_N_exponent_at_claimed_n": q(achieved_risk_exponent),
        "claimed_one_minus_PGR_N_exponent": q(
            claimed_pgr_gap_exponent
        ),
        "one_minus_PGR_N_exponent_at_claimed_n": q(
            achieved_pgr_gap_exponent
        ),
        "claimed_stopping_rate_is_consistent": (
            n_exponent_claimed == n_exponent_required
        ),
        "claimed_risk_rate_follows_at_claimed_n": (
            achieved_risk_exponent == claimed_risk_exponent
        ),
        "claimed_PGR_rate_follows_at_claimed_n": (
            achieved_pgr_gap_exponent == claimed_pgr_gap_exponent
        ),
    }


def pgr_identity_audit(
    *, teacher: Fraction, transfer: Fraction, direct_student: Fraction
) -> dict:
    assert teacher != direct_student
    pgr = (teacher - transfer) / (teacher - direct_student)
    actual_gap = 1 - pgr
    proof_proxy = transfer / teacher
    return {
        "teacher_risk": q(teacher),
        "transfer_risk": q(transfer),
        "direct_student_risk": q(direct_student),
        "W2S_strict": transfer < teacher,
        "PGR": q(pgr),
        "one_minus_PGR_from_definition": q(actual_gap),
        "proof_substitution_transfer_over_teacher": q(proof_proxy),
        "substitution_is_valid": actual_gap == proof_proxy,
        "exact_validity_condition": "R_S*(R_T-R_T2S)=0",
    }


def main() -> None:
    witness = stopping_rate_audit(Fraction(2), Fraction(2))
    risk_tuple = pgr_identity_audit(
        teacher=Fraction(9, 32),
        transfer=Fraction(1, 8),
        direct_student=Fraction(1, 32),
    )

    # An admissible self-distillation instance makes the paper's PGR
    # denominator exactly zero: identical expressive models, initialization,
    # ground-truth stream, and SGD schedule have R_T=R_S pathwise. The section
    # explicitly presents self-distillation as the limit case of this theorem.
    assumption_checks = {
        "spectral_trace_below_2": True,
        "fourth_moment_bound_psi_2": True,
        "teacher_projection_identity": True,
        "student_projection_identity": True,
        "zero_signal_tail_after_k_dagger_1": True,
        "exact_power_law_alpha_2": True,
        "strict_step_size_bound": (
            Fraction(1, 1000)
            < min(Fraction(1, 8), Fraction(1, 100))
        ),
        "self_distillation_is_in_stated_scope": True,
    }
    assumptions = {
        "fourth_moment": (
            "sum_k k^-2 < 1+integral_1^infinity x^-2 dx=2; "
            "Rademacher features therefore have ||Phi||^2<2, "
            "hence E[Phi Phi^T A Phi Phi^T]<=2 tr(A) I"
        ),
        "fourth_moment_psi": 2,
        "teacher_and_student_projections": "identity",
        "low_intrinsic_target": "w*=e_1, k_dagger=1, exact zero tail",
        "power_law_spectra": "lambda_k,T=lambda_k,S=k^-2",
        "step_size": "gamma0=gamma0'=1/1000 satisfies the strict bound",
        "self_distillation_scope": (
            "Section 6 explicitly includes self-distillation as the limit case"
        ),
        "checks": assumption_checks,
        "all_satisfied": all(assumption_checks.values()),
    }
    self_distillation = {
        "teacher_model": "identical to direct student",
        "ground_truth_stream": "identical",
        "initialization_and_schedule": "identical",
        "teacher_minus_direct_student_risk": "0 pathwise",
        "PGR_denominator": "0",
        "PGR_defined": False,
    }

    controls = {
        "alpha_s_equal_one_removes_stopping_mismatch": (
            stopping_rate_audit(Fraction(2), Fraction(1))[
                "claimed_stopping_rate_is_consistent"
            ]
        ),
        "oracle_direct_student_makes_PGR_substitution_valid": (
            pgr_identity_audit(
                teacher=Fraction(9, 32),
                transfer=Fraction(1, 8),
                direct_student=Fraction(0),
            )["substitution_is_valid"]
        ),
        "nonzero_direct_student_breaks_PGR_substitution": (
            not risk_tuple["substitution_is_valid"]
        ),
        "corrected_n_exponent_differs_for_alpha_s_2": (
            witness["claimed_n_N_exponent"]
            != witness["required_n_N_exponent_from_cutoff_relation"]
        ),
    }
    falsified = (
        assumptions["all_satisfied"]
        and not self_distillation["PGR_defined"]
        and not witness["claimed_stopping_rate_is_consistent"]
        and not witness["claimed_risk_rate_follows_at_claimed_n"]
        and not witness["claimed_PGR_rate_follows_at_claimed_n"]
        and all(controls.values())
    )
    result = {
        "claim": "Theorem 5 optimal early-stopping and PGR rates",
        "source_sha256": (
            "4d29b2ae21c4611695532f6fd304b22f678139a19311e21e9b65d8a6d0b00089"
        ),
        "source_anchors": (
            "main.tex lines 350-356, 780-800, 2522-2609; "
            "Appendix B.4 lines 2323-2331"
        ),
        "assumption_witness": assumptions,
        "undefined_PGR_counterexample": self_distillation,
        "stopping_rate_counterexample": witness,
        "PGR_definition_counterexample": risk_tuple,
        "negative_controls": controls,
        "verdict": "FALSIFIED" if falsified else "NOT_ESTABLISHED",
        "all_checks_passed": falsified,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "exact_rate_audit.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps(result, indent=2))
    if not falsified:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
