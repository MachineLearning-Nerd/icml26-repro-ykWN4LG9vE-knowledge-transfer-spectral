#!/usr/bin/env python3
"""Fail-closed gate over the committed five-claim evidence bundle."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "evidence"


def read(path: Path) -> dict:
    return json.loads(path.read_text())


def row_count(path: Path) -> int:
    with path.open() as handle:
        return sum(1 for _ in handle)


def main() -> None:
    baseline = read(ROOT / "outputs" / "independent_verification.json")
    decomposition = read(EVIDENCE / "claim-1" / "distill_results.json")
    claim2 = read(EVIDENCE / "claim-2" / "exact_der_certificate.json")
    claim2_checker = read(EVIDENCE / "claim-2" / "independent_checker.json")
    claim3 = read(EVIDENCE / "claim-3" / "exact_counterexample.json")
    claim3_checker = read(EVIDENCE / "claim-3" / "independent_checker.json")
    claim4 = read(EVIDENCE / "claim-4" / "exact_rate_audit.json")
    claim4_checker = read(EVIDENCE / "claim-4" / "independent_checker.json")
    claim5 = read(EVIDENCE / "claim-5" / "experiment_summary.json")
    claim5_checker = read(EVIDENCE / "claim-5" / "independent_checker.json")

    checks = {
        "claim1_static_identity": baseline[
            "claim_1_geometric_decomposition"
        ]["max_static_gap_identity_error"]
        < 1e-10,
        "claim1_three_part_decomposition": (
            decomposition["thm1_components_nonneg"]
            and decomposition["thm1_sum_matches_risk"]
        ),
        "claim2_finite_corrob": baseline["claim_2_kd_horizon"][
            "minimum_der"
        ]
        > 1,
        "claim2_exact_certificate": (
            claim2["all_checks_passed"]
            and all(claim2["negative_controls"].values())
            and claim2_checker["audit_passed"]
        ),
        "claim3_exact_falsification": (
            claim3["exact_witness"]["verdict"] == "FALSIFIED"
            and claim3["exact_witness"]["assumptions_satisfied"]
            and claim3["exact_witness"][
                "student_risk_strictly_above_teacher_for_every_finite_n"
            ]
            and all(claim3["negative_controls"].values())
            and claim3_checker["audit_passed"]
        ),
        "claim4_exact_falsification": (
            claim4["verdict"] == "FALSIFIED"
            and claim4["assumption_witness"]["all_satisfied"]
            and not claim4["undefined_PGR_counterexample"]["PGR_defined"]
            and not claim4["stopping_rate_counterexample"][
                "claimed_stopping_rate_is_consistent"
            ]
            and not claim4["PGR_definition_counterexample"][
                "substitution_is_valid"
            ]
            and all(claim4["negative_controls"].values())
            and claim4_checker["audit_passed"]
        ),
        "claim5_real_architecture": (
            claim5["verdict"] == "VERIFIED"
            and claim5["results"]["real_architecture_W2S_verified"]
            and claim5["results"]["early_stopping_critical_verified"]
            and claim5["results"]["shuffled_pseudolabel_control_passed"]
            and claim5_checker["verifier_passed"]
            and all(claim5_checker["checks"].values())
        ),
        "claim5_raw_predictions": row_count(
            EVIDENCE / "claim-5" / "test_predictions.csv"
        )
        == 2_001,
        "historical_toy_not_default": (
            "HISTORICAL_REJECTED_BASELINE"
            in (ROOT / "pages" / "claim-w2s-recovery" / "page.md").read_text()
            and "Historical rejected baseline"
            in (ROOT / "pages" / "index.md").read_text()
        ),
    }
    result = {
        "schema_version": 1,
        "paper": {
            "openreview_id": "ykWN4LG9vE",
            "arxiv_id": "2606.01292",
        },
        "checks": checks,
        "claim_verdicts": {
            "claim_1": "VERIFIED_SCOPED",
            "claim_2": "VERIFIED_SCOPED",
            "claim_3": "FALSIFIED_AS_WRITTEN",
            "claim_4": "FALSIFIED_AS_WRITTEN",
            "claim_5": "VERIFIED_SCOPED_WITH_PROTOCOL_LIMITS",
        },
        "science_gate_passed": all(checks.values()),
        "evidence_source": "committed/evidence",
        "hidden_runtime_dependency": False,
    }
    target = ROOT / "outputs" / "CUMULATIVE_SCIENCE_GATE.json"
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(f"CUMULATIVE_SCIENCE_GATE_JSON={json.dumps(result, sort_keys=True)}")
    if not result["science_gate_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
