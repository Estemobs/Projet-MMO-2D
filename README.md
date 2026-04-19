# MMO 2D - Jeu de Survie

Jeu 2D de survie/construction en vue de dessus, developpe avec Python et Pygame.

## Demarrage rapide

### 1. Prerequis
- Python 3.8+
- `pip`

### 2. Installer l'environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Lancer le projet

```bash
# Lancement recommande (verification + jeu)
python launch.py --check

# Lancement direct
python main.py
```

## Fichiers de lancement a la racine

- `main.py`: lance le jeu directement.
- `launch.py`: lance le gestionnaire complet (options `--check`, `--check-only`).
- `check.py`: execute uniquement les verifications d'integrite.

## Commandes utiles

```bash
# Verifier l'installation
python check.py

# Verifier puis lancer
python launch.py --check

# Test performance
python scripts/test_performance.py
```

## Release automatique (.exe + .flatpak)

Le workflow GitHub Actions `.github/workflows/release.yml` construit automatiquement:
- `ProjetMMO2D.exe` (Windows, autonome)
- `ProjetMMO2D.flatpak` (Linux, autonome)

### Comment ça marche

1. Le workflow se lance automatiquement quand un tag `vX.Y.Z` est push (ex: `v1.2.0`).
2. Deux builds sont exécutés:
   - Windows: build PyInstaller du `.exe`
   - Linux: build Flatpak du bundle `.flatpak`
3. Les deux fichiers sont publiés automatiquement dans la GitHub Release du tag.

### Générer une release

```bash
git tag v1.2.0
git push origin v1.2.0
```

Ensuite, GitHub Actions:
- compile les binaires
- crée/alimente la release
- attache les artefacts `.exe` et `.flatpak`

### Build manuel (sans publier de release)

Le workflow peut aussi être lancé à la main via l'onglet **Actions** (`workflow_dispatch`) pour générer les artefacts de build, sans étape de publication.

## Controles en jeu

| Action | Touches |
|--------|---------|
| Deplacement | WASD ou fleches |
| Interagir / Construire | Clic gauche |
| Mode construction | B |
| Fondation | 1 |
| Mur | 2 |
| Inventaire | I |
| Manger | H |
| Sauvegarder | F5 |
| Pause / Menu | Echap |

## Structure du projet

```text
.
├── main.py
├── launch.py
├── check.py
├── requirements.txt
├── core/          # Orchestration principale (GameManager, items)
├── game/          # Gameplay, monde, rendu, entites
├── ui/            # Inventaire, menus, pause
├── systems/       # Sauvegarde / chargement
├── data/          # Config et donnees de sauvegarde
├── assets/        # Sprites et ressources
├── scripts/       # Outils de maintenance, generation et tests
└── docs/          # Documentation technique
```

## Notes de maintenance

- Les scripts de `scripts/` ne sont pas tous requis pour jouer: ils servent au debug, aux tests et a la generation d'assets.
- En cas de probleme de dependances, reactiver le venv puis relancer `pip install -r requirements.txt`.
