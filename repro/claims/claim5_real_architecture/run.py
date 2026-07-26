#!/usr/bin/env python3
"""Run the real-architecture experiment and its independent checker."""
from __future__ import annotations

import base64
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = ROOT / ".openresearch" / "artifacts" / "claim-5"


def emit_artifact(path: Path) -> None:
    """Export an ephemeral worker artifact losslessly through the run log."""
    raw = path.read_bytes()
    metadata = {
        "path": str(path.relative_to(ROOT)),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "encoding": "gzip+base64",
    }
    encoded = base64.b64encode(gzip.compress(raw, mtime=0)).decode("ascii")
    print(f"CLAIM5_ARTIFACT_BEGIN_JSON={json.dumps(metadata, sort_keys=True)}")
    for start in range(0, len(encoded), 76):
        print(encoded[start : start + 76])
    print(f"CLAIM5_ARTIFACT_END={metadata['path']}")


subprocess.run(
    [sys.executable, str(HERE / "experiment.py")],
    cwd=ROOT,
    check=True,
)
verification = subprocess.run(
    [sys.executable, str(HERE / "verify.py")],
    cwd=ROOT,
    check=False,
)
for name in (
    "experiment_summary.json",
    "checkpoints.csv",
    "test_predictions.csv",
    "bootstrap.json",
    "independent_checker.json",
):
    emit_artifact(OUT / name)
if verification.returncode:
    raise SystemExit(verification.returncode)
