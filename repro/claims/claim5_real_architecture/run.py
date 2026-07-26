#!/usr/bin/env python3
"""Run the real-architecture experiment and its independent checker."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

for script in ("experiment.py", "verify.py"):
    subprocess.run([sys.executable, str(HERE / script)], cwd=ROOT, check=True)
