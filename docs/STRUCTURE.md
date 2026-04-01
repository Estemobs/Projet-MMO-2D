# Structure du projet

## Vue globale

```text
Projet-MMO-2D/
├── main.py                # Lancement direct du jeu
├── launch.py              # Lancement avec options (--check, --check-only)
├── check.py               # Verification integrite uniquement
├── README.md
├── requirements.txt
├── settings.json
├── assets/
│   └── sprites/
├── core/
│   ├── game_manager.py
│   └── items.py
├── game/
│   ├── core.py
│   ├── gameplay_manager.py
│   ├── render_manager.py
│   └── ...
├── ui/
│   ├── menu.py
│   ├── inventory.py
│   └── pause_menu.py
├── systems/
│   └── save_system.py
├── data/
│   ├── config.py
│   └── savegame.json
├── scripts/
│   ├── launch.py
│   ├── test_performance.py
│   └── ...
└── docs/
	└── STRUCTURE.md
```

## Points d'entree recommandes

```bash
python launch.py --check
```

Alternative rapide:

```bash
python main.py
```

## Role des repertoires

- `core/`: orchestration centrale de l'application.
- `game/`: logique de gameplay, carte, camera, rendu, entites.
- `ui/`: menus, inventaire, interface de pause.
- `systems/`: services techniques transverses (sauvegarde).
- `scripts/`: outils utilitaires, generation assets, tests manuels.
- `assets/`: ressources graphiques.
- `data/`: configuration locale et donnees de session.
