#!/usr/bin/env python3
"""Point d'entree racine: lancement direct du jeu."""

from pathlib import Path
import sys


def _check_updates_before_launch() -> bool:
    """Check for a release update before importing the game engine."""

    project_root = Path(__file__).parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    try:
        from systems.startup_updater import check_and_prompt_for_update
    except Exception as exc:
        print(f"⚠️  Vérification des mises à jour indisponible: {exc}")
        return True

    return check_and_prompt_for_update()


def main() -> None:
    if not _check_updates_before_launch():
        return

    from core import GameManager

    game_manager = GameManager()
    game_manager.run()


if __name__ == "__main__":
    main()
