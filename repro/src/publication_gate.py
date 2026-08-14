#!/usr/bin/env python3
"""Publish a source-pinned, scoped gate from a fresh clone."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_SHA256 = "639811b3ce58ae86a01605e5c7c618b402cd5761bece8ab5ea7ec82f1d2f3d06"


def read(path: Path) -> dict:
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_lightweight_checks() -> None:
    subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "repro/tests"],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(
        [sys.executable, "repro/src/cumulative_science_gate.py"],
        cwd=ROOT,
        check=True,
    )


def main() -> int:
    run_lightweight_checks()

    sources = read(ROOT / "sources.json")
    cumulative = read(ROOT / "outputs" / "CUMULATIVE_SCIENCE_GATE.json")
    source_path = ROOT / sources["active_tex"]
    canonical_docs = (
        ROOT / "README.md",
        ROOT / "STATUS.md",
        ROOT / "pages" / "index.md",
        ROOT / "pages" / "conclusion" / "page.md",
    )

    assert sources["openreview_id"] == "ykWN4LG9vE"
    assert sources["arxiv_id"] == "2606.01292"
    assert sources["active_tex"] == "source/arxiv/main.tex"
    assert sources["active_tex_sha256"] == SOURCE_SHA256
    assert sha256(source_path) == SOURCE_SHA256
    assert cumulative["science_gate_passed"]
    assert cumulative["hidden_runtime_dependency"] is False
    assert cumulative["claim_verdicts"] == {
        "claim_1": "VERIFIED_SCOPED",
        "claim_2": "VERIFIED_SCOPED",
        "claim_3": "FALSIFIED_AS_WRITTEN",
        "claim_4": "FALSIFIED_AS_WRITTEN",
        "claim_5": "VERIFIED_SCOPED_WITH_PROTOCOL_LIMITS",
    }

    for document in canonical_docs:
        text = document.read_text()
        assert "8–10/10" not in text
        assert "8-10/10" not in text
        assert "FULL_GATE_READY" not in text
        assert "Conservative projected score" not in text

    claim5 = read(ROOT / "evidence" / "claim-5" / "experiment_summary.json")
    claim5_checker = read(
        ROOT / "evidence" / "claim-5" / "independent_checker.json"
    )
    assert claim5["protocol"]["train_size"] == 20_000
    assert claim5["protocol"]["test_size"] == 2_000
    assert claim5["results"]["best_w2s_epoch"] == 2
    assert claim5_checker["verifier_passed"]

    result = {
        "schema_version": 1,
        "paper": {
            "title": (
                "What Makes a Strong Model? A Unified Spectral Analysis of "
                "Knowledge Transfer over High-dimensional Linear Regression"
            ),
            "openreview_id": "ykWN4LG9vE",
            "arxiv_id": "2606.01292",
            "authors": [
                "Wendao Wu",
                "Fangqing Zhang",
                "Haihan Zhang",
                "Cong Fang",
            ],
        },
        "repository": {
            "original_name": (
                "icml26-repro-ykWN4LG9vE-knowledge-transfer-spectral"
            ),
            "intended_name": "icml26-spectral-knowledge-transfer",
            "owner": "MachineLearning-Nerd",
            "clean_room": True,
        },
        "gate_status": "SCOPED_PASS",
        "overall_status": "VERIFIED_SCOPED_WITH_SOURCE_DEFECTS",
        "strict_paper_gate": "NOT_READY",
        "claim_outcomes": cumulative["claim_verdicts"],
        "verification": {
            "pytest": True,
            "cumulative_science_gate": True,
            "committed_evidence_bundle": True,
            "source_pin_verified": True,
            "hidden_runtime_dependency": False,
        },
        "scope_limits": [
            "Exact UTKFace train/test indices are unpublished.",
            "The separate ViT-L/16 fine-tuning arm from Figure 2 was not run.",
            "No score change is claimed without a new live judge verdict.",
        ],
        "score_context": {
            "previous_live_score": "6/10",
            "score_change_claimed": False,
        },
    }
    encoded = json.dumps(result, indent=2) + "\n"
    for target in (
        ROOT / "publication_gate.json",
        ROOT / "outputs" / "publication_gate.json",
        ROOT / "outputs" / "RELEASE_CANDIDATE_READY.json",
    ):
        target.write_text(encoded)
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
