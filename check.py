#!/usr/bin/env python3
"""Point d'entree racine: verification d'integrite uniquement."""

import sys
from pathlib import Path
import runpy


if __name__ == "__main__":
    script_path = Path(__file__).parent / "scripts" / "launch.py"
    original_argv = sys.argv[:]
    try:
        sys.argv = [str(script_path), "--check-only"]
        runpy.run_path(str(script_path), run_name="__main__")
    finally:
        sys.argv = original_argv
