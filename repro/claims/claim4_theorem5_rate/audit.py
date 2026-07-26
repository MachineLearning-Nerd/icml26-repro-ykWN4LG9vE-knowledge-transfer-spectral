#!/usr/bin/env python3
"""Independent reconstruction of Claim 4 exponents and finite cutoffs."""
from __future__ import annotations

import csv
import json
import math
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / ".openresearch" / "artifacts" / "claim-4"


def main() -> None:
    alpha_t = Fraction(2)
    alpha_s = Fraction(2)
    target_cutoff_exponent = Fraction(1, 10)
    theorem_n_exponent = Fraction(1, 10)
    reconstructed_n_exponent = Fraction(1, 5)

    rows = []
    for log10_N in (20, 40, 80, 120, 160, 200):
        for route, n_exponent in (
            ("theorem", float(theorem_n_exponent)),
            ("reconstructed", float(reconstructed_n_exponent)),
        ):
            log_n = n_exponent * log10_N * math.log(10)
            # From lambda_k=k^-2 and lambda_k ~ log(n)/n:
            # log(k*) = (log(n)-log(log(n)))/2 up to constants.
            log_k = (log_n - math.log(log_n)) / float(alpha_s)
            rows.append(
                {
                    "route": route,
                    "log10_N": log10_N,
                    "effective_cutoff_logN_slope": log_k
                    / (log10_N * math.log(10)),
                }
            )

    theorem_slopes = [
        row["effective_cutoff_logN_slope"]
        for row in rows
        if row["route"] == "theorem"
    ]
    corrected_slopes = [
        row["effective_cutoff_logN_slope"]
        for row in rows
        if row["route"] == "reconstructed"
    ]
    result = {
        "independent_implementation": True,
        "alpha_teacher": "2",
        "alpha_student": "2",
        "target_cutoff_N_exponent": "1/10",
        "theorem_n_N_exponent": "1/10",
        "reconstructed_n_N_exponent": "1/5",
        "limiting_cutoff_exponent_theorem_route": "1/20",
        "limiting_cutoff_exponent_reconstructed_route": "1/10",
        "largest_horizon_theorem_slope": theorem_slopes[-1],
        "largest_horizon_reconstructed_slope": corrected_slopes[-1],
        "theorem_route_misses_target": theorem_slopes[-1] < 0.075,
        "reconstructed_route_approaches_target": corrected_slopes[-1] > 0.085,
        "audit_passed": (
            theorem_slopes[-1] < 0.075
            and corrected_slopes[-1] > 0.085
            and theorem_n_exponent != reconstructed_n_exponent
        ),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "independent_cutoff_sweep.csv").open(
        "w", newline=""
    ) as handle:
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
