#!/usr/bin/env python3
"""Fail-closed evaluator-visible and historical-preservation audit."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import deque
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
JUDGED_REV = "39d8a32354134ce1777ce9adefe8f26e86ebc11b"
TEXT_SUFFIXES = {
    "",
    ".css",
    ".gitattributes",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".svg",
}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message: str) -> None:
    raise AssertionError(message)


logbook = json.loads((ROOT / "logbook.json").read_text())
slug_to_file = {
    node["slug"]: node["file"] for node in logbook["root"]["children"]
}

queue = deque(["README.md", "logbook.json", "pages/index.md"])
opened: set[str] = set()
broken: list[dict[str, str]] = []

while queue:
    rel = queue.popleft()
    rel = Path(rel).as_posix()
    if rel in opened:
        continue
    target = (ROOT / rel).resolve()
    if ROOT not in target.parents and target != ROOT:
        fail(f"path escaped candidate: {rel}")
    if not target.is_file():
        broken.append({"from": "<queue>", "target": rel})
        continue
    opened.add(rel)

    if rel == "logbook.json":
        queue.extend(slug_to_file.values())
        continue
    if target.suffix.lower() != ".md":
        continue

    for raw_link in LINK_RE.findall(target.read_text(errors="strict")):
        link = raw_link.strip().split(maxsplit=1)[0].strip("<>")
        if link.startswith(("http://", "https://", "mailto:")):
            continue
        if link.startswith("#/"):
            slug = link[2:].split("#", 1)[0]
            if slug not in slug_to_file:
                broken.append({"from": rel, "target": link})
            else:
                queue.append(slug_to_file[slug])
            continue
        link = unquote(link.split("#", 1)[0])
        if not link:
            continue
        child = (target.parent / link).resolve()
        try:
            child_rel = child.relative_to(ROOT).as_posix()
        except ValueError:
            broken.append({"from": rel, "target": link})
            continue
        if not child.is_file():
            broken.append({"from": rel, "target": child_rel})
        else:
            queue.append(child_rel)

if broken:
    fail(f"broken evaluator-visible links: {broken}")

required_by_claim = {
    "claim-1": [
        "pages/claim-1-geometric-decomposition/page.md",
        "evidence/claim-1/claim_contract.json",
        "evidence/claim-1/source_audit.md",
        "evidence/claim-1/distill_results.json",
        "evidence/claim-1/independent_verification.json",
        "repro/src/verify_transfer.py",
        "repro/src/verify_distill.py",
    ],
    "claim-2": [
        "pages/claim-2-kd-horizon/page.md",
        "evidence/claim-2/claim_contract.json",
        "evidence/claim-2/source_audit.md",
        "evidence/claim-2/exact_der_certificate.json",
        "evidence/claim-2/independent_checker.json",
        "repro/src/verify_theorem3_der_exact.py",
        "repro/src/audit_theorem3_der_exact.py",
    ],
    "claim-3": [
        "pages/claim-3-theorem4-exact/page.md",
        "evidence/claim-3/claim_contract.json",
        "evidence/claim-3/source_audit.md",
        "evidence/claim-3/exact_counterexample.json",
        "evidence/claim-3/independent_checker.json",
        "repro/claims/claim3_theorem4_quantifier/verify.py",
        "repro/claims/claim3_theorem4_quantifier/audit.py",
    ],
    "claim-4": [
        "pages/claim-4-theorem5-exact/page.md",
        "evidence/claim-4/claim_contract.json",
        "evidence/claim-4/source_audit.md",
        "evidence/claim-4/exact_rate_audit.json",
        "evidence/claim-4/independent_checker.json",
        "repro/claims/claim4_theorem5_rate/verify.py",
        "repro/claims/claim4_theorem5_rate/audit.py",
    ],
    "claim-5": [
        "pages/claim-5-real-architectures/page.md",
        "evidence/claim-5/claim_contract.json",
        "evidence/claim-5/source_audit.md",
        "evidence/claim-5/experiment_summary.json",
        "evidence/claim-5/test_predictions.csv",
        "evidence/claim-5/independent_checker.json",
        "repro/claims/claim5_real_architecture/experiment.py",
        "repro/claims/claim5_real_architecture/verify.py",
    ],
}
for claim, required in required_by_claim.items():
    missing = sorted(set(required) - opened)
    if missing:
        fail(f"{claim} is not reachable from canonical entrypoints: {missing}")

index_text = (ROOT / "pages/index.md").read_text()
if "| yes |" in index_text:
    fail("visibility matrix contains placeholder yes cells")
for verdict in ("VERIFIED", "FALSIFIED"):
    if verdict not in index_text:
        fail(f"missing current verdict in index: {verdict}")

manifest = ROOT / "audit/judged-manifest-relative.sha256"
old_rows = []
for line in manifest.read_text().splitlines():
    expected, rel = line.split("  ", 1)
    current = ROOT / rel
    if not current.is_file():
        fail(f"judged path missing from candidate: {rel}")
    current_exact = sha256(current) == expected
    archive = ROOT / f"historical/judged-{JUDGED_REV}" / rel
    archive_exact = archive.is_file() and sha256(archive) == expected
    if not current_exact and not archive_exact:
        fail(f"judged bytes neither current nor archived exactly: {rel}")
    old_rows.append(
        {
            "path": rel,
            "current_exact": current_exact,
            "archive_exact": archive_exact,
        }
    )

result = {
    "candidate_root": str(ROOT),
    "canonical_entrypoints": ["README.md", "logbook.json", "pages/index.md"],
    "opened_files": sorted(opened),
    "opened_file_count": len(opened),
    "broken_links": broken,
    "claim_required_files_reachable": {
        claim: True for claim in required_by_claim
    },
    "judged_old_file_count": len(old_rows),
    "judged_old_paths_subset": True,
    "judged_bytes_current_or_archived": True,
    "historical_checks": old_rows,
    "visibility_gate_passed": True,
}
print(json.dumps(result, indent=2))
