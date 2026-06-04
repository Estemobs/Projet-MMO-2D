# Structure du projet

## Vue globale

```text
Projet-MMO-2D/
├── main.py                # Lancement direct du jeu
├── launch.py              # Lancement avec options (--check, --check-only)
├── README.md
├── requirements.txt
├── assets/
│   └── sprites/
├── core/
│   ├── game_manager.py
│   └── items.py
├── game/
│   ├── gameplay_manager.py
│   ├── render_manager.py
│   ├── sound_manager.py
│   ├── day_night.py
│   ├── tutorial.py
│   ├── particles.py
│   ├── controls_hint.py
│   ├── transitions.py
│   └── ...
├── ui/
│   ├── menu.py
│   ├── inventory.py
│   └── pause_menu.py
├── systems/
│   ├── save_system.py
│   ├── update_checker.py
│   └── update_installer.py
├── scripts/
│   ├── launch.py
│   ├── generate_natural_sprites.py
│   ├── generate_missing_items.py
│   └── create_large_characters.py
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
- `game/`: logique de gameplay, carte, camera, rendu, entites, sons, particules.
- `ui/`: menus, inventaire, interface de pause.
- `systems/`: services techniques transverses (sauvegarde, mise a jour).
- `scripts/`: outils utilitaires, generation d'assets.
- `assets/`: ressources graphiques (sprites).
