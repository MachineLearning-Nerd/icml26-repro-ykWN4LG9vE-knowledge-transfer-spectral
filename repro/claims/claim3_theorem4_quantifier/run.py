#!/usr/bin/env python3
"""Run the primary and independent Claim 3 certificates."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

for script in ("verify.py", "audit.py"):
    subprocess.run([sys.executable, str(HERE / script)], cwd=ROOT, check=True)
