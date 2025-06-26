# 📁 Structure du Projet

## Organisation des dossiers

```
📁 Projet MMO 2D/
├── 📁 core/           # Modules principaux du moteur de jeu
├── 📁 game/           # Logique spécifique du jeu
├── 📁 ui/             # Interface utilisateur
├── 📁 systems/        # Systèmes transversaux
├── 📁 scripts/        # Scripts utilitaires et de lancement
├── 📁 data/           # Configuration et sauvegardes
├── 📁 docs/           # Documentation (vide pour l'instant)
├── 📄 main.py         # Point d'entrée principal
├── 📄 README.md       # Documentation principale
└── 📄 requirements.txt # Dépendances Python
```

## Point d'entrée

Lancez le jeu avec :
```bash
python main.py
```

Ou directement avec le script complet :
```bash
python scripts/launch.py
```

## Scripts disponibles

- `scripts/launch.py` : Script de lancement avec vérifications
- `scripts/test_performance.py` : Tests de performance

## Configuration et données

- `data/config.py` : Configuration du jeu
- `data/savegame.json` : Fichier de sauvegarde
