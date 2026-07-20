#!/usr/bin/env python3
"""Clean-room checks for the three spectral knowledge-transfer claims."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def schedule(total: int, gamma: float) -> np.ndarray:
    phase = max(1, int(total / np.log2(total)))
    return gamma * 2.0 ** -(np.arange(total) // phase)


def projectors_identity(cells: int, seed: int = 19) -> dict:
    """Appendix geometric-consistency identity, using noncommuting subspaces."""
    rng = np.random.default_rng(seed)
    largest = 0.0
    for _ in range(cells):
        dimension, teacher_rank, student_rank = 12, 8, 6
        teacher, _ = np.linalg.qr(rng.normal(size=(dimension, teacher_rank)))
        student, _ = np.linalg.qr(rng.normal(size=(dimension, student_rank)))
        pt, ps = teacher @ teacher.T, student @ student.T
        truth = rng.normal(size=dimension)
        direct = 0.5 * np.linalg.norm(ps @ truth - truth) ** 2
        transfer = 0.5 * np.linalg.norm(ps @ pt @ truth - truth) ** 2
        expected = 0.5 * np.linalg.norm(ps @ (np.eye(dimension) - pt) @ truth) ** 2
        largest = max(largest, abs((transfer - direct) - expected))
    return {"noncommuting_subspace_cells": cells, "max_static_gap_identity_error": largest}


def rate_audits() -> dict:
    """Independent numerical audit of the exponents in Theorems 4.2 and 5.2."""
    alpha_t = np.linspace(1.05, 3.0, 200)
    alpha_s = np.linspace(1.1, 4.0, 200)
    beta = np.linspace(0.0, 0.9, 10)
    at, ass, be = np.meshgrid(alpha_t, alpha_s, beta, indexing="ij")
    valid = (at > 1 + be) & (ass > at)
    kappa = (at - 1 - be) * (1 / at - 1 / ass)
    horizon_order = 10_000.0 ** (1 / at) > 10_000.0 ** (1 / ass)
    kd_violations = int(np.sum(valid & ((kappa <= 0) | ~horizon_order)))
    delta = 2 * ass / (at * (2 * ass + 1))
    w2s_valid = (at > 1) & (ass > 1)
    w2s_violations = int(np.sum(w2s_valid & ((delta <= 0) | (delta >= 1))))
    return {"kd_admissible_cells": int(valid.sum()), "kd_positive_exponent_violations": kd_violations,
            "w2s_admissible_cells": int(w2s_valid.sum()), "w2s_positive_rate_violations": w2s_violations}


def run_sgd(*, alpha_teacher: float, alpha_student: float, original: int, transfer: int,
            trials: int, noise: float, seed: int, signal_dimensions: int | None = None) -> dict:
    """Paper protocol: fresh single samples, teacher then direct/distilled student."""
    rng = np.random.default_rng(seed)
    d = 100
    modes = np.arange(1, d + 1, dtype=float)
    lt = modes ** -alpha_teacher
    ls = modes ** -alpha_student
    st, ss = np.sqrt(lt), np.sqrt(ls)
    teacher = np.zeros((trials, d)); direct = np.zeros((trials, d)); distilled = np.zeros((trials, d))
    truth = rng.normal(size=(trials, d))
    if signal_dimensions is not None:
        truth[:, signal_dimensions:] = 0.0
    # The signal is in the teacher feature coordinates, exactly as in the source.
    for lr in schedule(original, 0.01):
        x = rng.normal(size=(trials, d)); phi_t, phi_s = x * st, x * ss
        y = np.sum(phi_t * truth, axis=1) + noise * rng.normal(size=trials)
        teacher += lr * (y - np.sum(phi_t * teacher, axis=1))[:, None] * phi_t
        direct += lr * (y - np.sum(phi_s * direct, axis=1))[:, None] * phi_s
    for lr in schedule(transfer, 0.01):
        x = rng.normal(size=(trials, d)); phi_t, phi_s = x * st, x * ss
        pseudo = np.sum(phi_t * teacher, axis=1)
        distilled += lr * (pseudo - np.sum(phi_s * distilled, axis=1))[:, None] * phi_s
    # Exact population risks in the common latent Gaussian basis.
    teacher_risk = np.sum((st * (teacher - truth)) ** 2, axis=1)
    direct_risk = np.sum((ss * direct - st * truth) ** 2, axis=1)
    distilled_risk = np.sum((ss * distilled - st * truth) ** 2, axis=1)
    return {"teacher_risk": teacher_risk, "direct_risk": direct_risk, "distilled_risk": distilled_risk}


def w2s_early_stop_scan(trials: int, seed: int, noise: float = 1.0) -> dict:
    """Mechanism audit: save student checkpoints before tail-noise memorization."""
    rng = np.random.default_rng(seed)
    d, original, maximum = 100, 2000, 100_000
    modes = np.arange(1, d + 1, dtype=float)
    st, ss = modes ** (-1.5 / 2), modes ** (-1.0 / 2)
    truth = rng.normal(size=(trials, d)); truth[:, 10:] = 0.0
    teacher = np.zeros((trials, d)); student = np.zeros((trials, d))
    for lr in schedule(original, .01):
        x = rng.normal(size=(trials, d)); pt = x * st
        y = np.sum(pt * truth, axis=1) + noise * rng.normal(size=trials)
        teacher += lr * (y - np.sum(pt * teacher, axis=1))[:, None] * pt
    checkpoints = {100, 500, 2_000, 10_000, maximum}
    values = {}
    for step, lr in enumerate(schedule(maximum, .01), 1):
        x = rng.normal(size=(trials, d)); pt, ps = x * st, x * ss
        pseudo = np.sum(pt * teacher, axis=1)
        student += lr * (pseudo - np.sum(ps * student, axis=1))[:, None] * ps
        if step in checkpoints:
            values[str(step)] = np.sum((ss * student - st * truth) ** 2, axis=1)
    teacher_risk = np.sum((st * (teacher - truth)) ** 2, axis=1)
    matrix = np.stack([values[str(k)] for k in sorted(checkpoints)], axis=1)
    best = matrix.min(axis=1)
    return {"checkpoints": sorted(checkpoints), "median_risks": {str(k): float(np.median(values[str(k)])) for k in sorted(checkpoints)},
            "mean_risks": {str(k): float(np.mean(values[str(k)])) for k in sorted(checkpoints)},
            "best_student_beats_teacher_fraction": float(np.mean(best < teacher_risk)),
            "median_teacher_risk": float(np.median(teacher_risk)), "mean_teacher_risk": float(np.mean(teacher_risk)),
            "median_best_student_risk": float(np.median(best)), "mean_best_student_risk": float(np.mean(best))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="outputs/independent_verification.json")
    parser.add_argument("--trials", type=int, default=64)
    parser.add_argument("--transfer", type=int, default=500000)
    args = parser.parse_args()
    geometric, rates = projectors_identity(9000), rate_audits()
    kd = run_sgd(alpha_teacher=1.0, alpha_student=1.5, original=2000, transfer=args.transfer,
                 trials=args.trials, noise=.1, seed=260601292)
    der = kd["direct_risk"] / kd["distilled_risk"]
    # W2S control: low-dimensional target is created by retaining only its head.
    w2s = w2s_early_stop_scan(args.trials, 260601293)
    result = {"paper": "ykWN4LG9vE", "protocol": {"d": 100, "N": 2000, "n": args.transfer,
              "trials": args.trials, "alpha_teacher": 1.0, "alpha_student": 1.5, "noise_std": .1},
              "claim_1_geometric_decomposition": geometric, "claim_2_kd_horizon": {**rates,
              "median_teacher_risk": float(np.median(kd['teacher_risk'])), "median_direct_risk": float(np.median(kd['direct_risk'])),
              "median_distilled_risk": float(np.median(kd['distilled_risk'])), "minimum_der": float(der.min()), "median_der": float(np.median(der))},
              "claim_3_w2s_denoising": {"low_intrinsic_dimension": 10, **w2s}}
    target = Path(args.output); target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
