#!/usr/bin/env python3
"""Independent high-precision audit; intentionally imports no primary code."""
from __future__ import annotations

import csv
import json
from decimal import Decimal, getcontext
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / ".openresearch" / "artifacts" / "claim-3"
getcontext().prec = 80


def contraction(total: int, initial: Decimal) -> Decimal:
    phases = total.bit_length() - 1
    product = Decimal(1)
    # Count indices with q=floor(t*phases/total), t=1,...,total, without
    # enumerating a million updates.
    for q in range(phases + 1):
        lower = max(1, (q * total + phases - 1) // phases)
        upper = min(total, ((q + 1) * total + phases - 1) // phases - 1)
        count = max(0, upper - lower + 1)
        if count:
            product *= (
                Decimal(1) - initial / (Decimal(2) ** q)
            ) ** count
    return product


def main() -> None:
    teacher_gamma = Decimal(1) / Decimal(1000)
    teacher_remaining = contraction(256, teacher_gamma)
    c = Decimal(1) - teacher_remaining
    noise_variance = Decimal(1) / Decimal(1_000_000)

    # Independent forward variance recursion.
    variance = Decimal(0)
    phases = 8
    interval = 32
    for t in range(1, 257):
        gain = teacher_gamma / (Decimal(2) ** (t // interval))
        variance = (Decimal(1) - gain) ** 2 * variance + gain**2 * noise_variance

    teacher_risk = ((Decimal(1) - c) ** 2 + variance) / Decimal(2)
    rows = []
    for n in (256, 1024, 4096, 16384, 65536, 1048576):
        a = Decimal(1) - contraction(n, Decimal(1) / Decimal(2000))
        student_risk = (
            (Decimal(1) - a * c) ** 2 + a**2 * variance
        ) / Decimal(2)
        rows.append(
            {
                "n": n,
                "student_coefficient_a": str(a),
                "teacher_risk": str(teacher_risk),
                "student_risk": str(student_risk),
                "student_minus_teacher": str(student_risk - teacher_risk),
            }
        )
    all_positive = all(Decimal(row["student_minus_teacher"]) > 0 for row in rows)
    monotone_to_zero = all(
        Decimal(rows[i]["student_minus_teacher"])
        > Decimal(rows[i + 1]["student_minus_teacher"])
        for i in range(len(rows) - 1)
    )
    result = {
        "independent_implementation": True,
        "precision_decimal_digits": getcontext().prec,
        "teacher_mean_coefficient": str(c),
        "teacher_variance": str(variance),
        "tested_horizons": [row["n"] for row in rows],
        "all_sampled_student_risks_above_teacher": all_positive,
        "gaps_decrease_toward_zero_from_above": monotone_to_zero,
        "audit_passed": all_positive and monotone_to_zero,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "independent_horizon_audit.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (OUT / "independent_checker.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps(result, indent=2))
    print(json.dumps(rows, indent=2))
    if not result["audit_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
