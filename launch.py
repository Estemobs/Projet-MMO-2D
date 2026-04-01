#!/usr/bin/env python3
"""Point d'entree racine: delegue au lanceur complet."""

from pathlib import Path
import runpy


if __name__ == "__main__":
    script_path = Path(__file__).parent / "scripts" / "launch.py"
    runpy.run_path(str(script_path), run_name="__main__")
