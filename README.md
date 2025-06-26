# 🎮 MMO 2D - Jeu de Survie

Un jeu 2D de survie et construction en vue de dessus, développé avec Python et Pygame.

## 🚀 Installation et Lancement

### Prérequis
- Python 3.8 ou plus récent
- pip (gestionnaire de paquets Python)

### Installation rapide
```bash
# Cloner ou télécharger le projet
# Installer les dépendances
pip install -r requirements.txt

# Lancer le jeu
python launch.py
```

## 🎮 Contrôles

| Action | Touches |
|--------|---------|
| **Déplacement** | WASD ou flèches directionnelles |
| **Récolter/Construire** | Clic gauche |
| **Mode construction** | B |
| **Sélectionner fondation** | 1 |
| **Sélectionner mur** | 2 |
| **Inventaire** | I |
| **Manger** | H |
| **Sauvegarder** | F5 |
| **Menu principal** | Échap |

## 🌍 Éléments du Jeu

- 🟢 **Herbe** : Terrain traversable
- 🟤 **Arbres** : Source de bois
- ⚫ **Pierres** : Source de pierre
- ⚫ **Minerai de fer** : Source de fer
- 🟡 **Fondations** : Base de construction (2 bois + 1 pierre)
- 🟠 **Murs** : Structures défensives (1 bois + 2 pierres)
- 🔴 **Ennemis** : 50 PV, 10 dégâts, détection à 3 cases

## 📁 Structure du Projet

```
MMO 2D/
├── core/                   # Logique principale
│   ├── game_manager.py     # Gestionnaire principal
│   └── items.py           # Système d'objets
├── systems/               # Systèmes annexes
│   └── save_system.py     # Sauvegarde/chargement
├── ui/                    # Interface utilisateur
│   ├── menu.py           # Menus
│   └── inventory.py       # Inventaire et crafting
├── game/                  # Composants de jeu
│   ├── core.py           # Ancienne classe principale
│   ├── player.py         # Logique du joueur
│   ├── enemy.py          # IA des ennemis
│   ├── world.py          # Génération du monde
│   └── ...
├── launch.py             # Script de lancement avec vérifications
├── main.py               # Point d'entrée simplifié
└── config.py             # Configuration du jeu
```

## 🛠️ Développement

### Scripts disponibles
- `python launch.py` - Lance avec vérifications d'intégrité
- `python launch.py --check` - Vérifie avant de lancer
- `python launch.py --check-only` - Vérifications seulement
- `python main.py` - Lancement direct
- `python test_performance.py` - Test de performance

### Extensions possibles
- Multijoueur en réseau
- Plus de biomes
- Système de quêtes
- Commerce entre joueurs
- Magie et sorts

## 📊 Performance

Le jeu vise 60 FPS. Utilisez `test_performance.py` pour tester votre système.

## 📝 License

Projet éducatif open source.
