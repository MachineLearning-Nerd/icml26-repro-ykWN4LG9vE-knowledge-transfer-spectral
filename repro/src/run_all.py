#!/usr/bin/env python3
"""Fixed cumulative entrypoint for every OpenResearch experiment node."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASELINE_COMMANDS = [
    [sys.executable, "repro/src/verify_transfer.py"],
    [sys.executable, "repro/src/verify_theorem3_der_exact.py"],
    [sys.executable, "repro/src/audit_theorem3_der_exact.py"],
    [sys.executable, "-m", "pytest", "-q", "repro/tests"],
    [sys.executable, "repro/src/publication_gate.py"],
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run(command: list[str], env: dict[str, str]) -> None:
    print(f"\nRUN_COMMAND_JSON={json.dumps(command)}", flush=True)
    started = time.perf_counter()
    completed = subprocess.run(command, cwd=ROOT, env=env, check=False)
    elapsed = time.perf_counter() - started
    print(
        f"RUN_RESULT_JSON={json.dumps({'command': command, 'exit_code': completed.returncode, 'runtime_s': round(elapsed, 3)})}",
        flush=True,
    )
    if completed.returncode:
        raise SystemExit(completed.returncode)


def main() -> None:
    started = time.perf_counter()
    env = os.environ.copy()
    has_real_architecture_run = (
        ROOT / "repro" / "claims" / "claim5_real_architecture"
    ).is_dir()
    # Baseline numerical checks are designed for one core. The run is routed to
    # HF cpu-upgrade because its duration was uncertain before the first run.
    for name in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
        "NUMEXPR_NUM_THREADS",
    ):
        env[name] = "1"
    env["PYTHONHASHSEED"] = "0"

    metadata = {
        "paper": "2606.01292",
        "started_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "fixed_entrypoint": "uv sync --frozen && uv run python repro/src/run_all.py",
        "estimated_required_cores": (
            24 if has_real_architecture_run else 1
        ),
        "selected_backend": "hf",
        "selected_flavor": "cpu-upgrade",
        "selection_reason": (
            "real-architecture feature extraction requires 16 compute "
            "threads plus 8 image workers; HF cpu-upgrade required"
            if has_real_architecture_run
            else "uncertain baseline runtime; local execution prohibited "
            "by campaign policy"
        ),
        "actual_logical_cpu_allocation": os.cpu_count(),
        "python": sys.version,
        "platform": platform.platform(),
        "git_sha": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "deterministic_seeds": [19, 260601292, 260601293],
    }
    print(f"CAMPAIGN_METADATA_JSON={json.dumps(metadata, sort_keys=True)}", flush=True)

    for command in BASELINE_COMMANDS:
        run(command, env)

    claim_runners = sorted((ROOT / "repro" / "claims").glob("*/run.py"))
    print(
        f"DISCOVERED_CLAIM_RUNNERS_JSON={json.dumps([str(p.relative_to(ROOT)) for p in claim_runners])}",
        flush=True,
    )
    for runner in claim_runners:
        run([sys.executable, str(runner.relative_to(ROOT))], env)

    outputs = []
    for path in sorted((ROOT / "outputs").glob("*")):
        if path.is_file():
            outputs.append(
                {
                    "path": str(path.relative_to(ROOT)),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    runtime = time.perf_counter() - started
    summary = {
        "status": "passed",
        "runtime_s": round(runtime, 3),
        "actual_logical_cpu_allocation": os.cpu_count(),
        "max_rss_platform_units": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        "outputs": outputs,
    }
    print(f"CUMULATIVE_RESULT_JSON={json.dumps(summary, sort_keys=True)}", flush=True)


if __name__ == "__main__":
    main()
