#!/usr/bin/env python3
"""Point d'entree racine: lancement direct du jeu."""

from core import GameManager


def main() -> None:
    game_manager = GameManager()
    game_manager.run()


if __name__ == "__main__":
    main()
