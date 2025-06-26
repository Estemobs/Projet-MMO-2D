# MMO 2D - Jeu de Survie en Python/Pygame

Un jeu 2D de survie et de construction en vue de dessus, développé avec Python et Pygame.

## 🚀 Installation et Lancement Rapide

### 1. Cloner le projet
```bash
git clone <url-du-repo>
cd "Projet MMO 2D"
```

### 2. Créer un environnement virtuel (recommandé)
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer le jeu
```bash
# Lancement simple
python launch.py

# Avec vérification d'intégrité
python launch.py --check

# Vérification seulement (sans lancer)
python launch.py --check-only
```

## 🎮 Contrôles

| Action | Touches |
|--------|---------|
| 🚶 Se déplacer | WASD ou flèches directionnelles |
| 🔨 Récolter/Construire | Clic gauche |
| 🏗️ Mode construction | B |
| 🧱 Fondation | 1 |
| 🏠 Mur | 2 |
| 🎒 Inventaire | I |
| 💾 Sauvegarder | F5 |
| 🏃 Quitter | Échap |

## ✨ Fonctionnalités
- Python 3.7 ou plus récent
- pip (gestionnaire de paquets Python)

### Installation
1. Clonez ou téléchargez le projet
2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

### Lancement
**Option 1 - Simple :**
```bash
python main.py
```

**Option 2 - Script de lancement (recommandé sur Linux) :**
```bash
./start_game.sh
```

**Option 3 - Script Python dédié :**
```bash
python launch.py
```

**Option 4 - Test avant lancement :**
```bash
python test_setup.py  # Vérifier que tout fonctionne
python main.py        # Lancer le jeu
```

## Contrôles

### Déplacement
- **WASD** ou **Flèches directionnelles** : Se déplacer dans les 4 directions
- Le joueur ne peut se déplacer que sur l'herbe (tiles vertes)

### Récolte de Ressources
- **Clic gauche** : Récolter une ressource (arbre, pierre, minerai)
- Le joueur doit être à proximité de la ressource (dans un rayon de 2 cases)
- Les ressources récoltées sont automatiquement ajoutées à l'inventaire

### Inventaire et Artisanat
- **Touche I** : Ouvrir/fermer l'inventaire
- **TAB** (dans l'inventaire) : Changer d'onglet (Inventaire/Artisanat/Équipement)
- **WASD** (dans l'inventaire) : Naviguer dans les menus
- **ENTER** (dans l'inventaire) : Crafter un objet ou équiper

### Construction
- **Touche B** : Activer/désactiver le mode construction
- **Touche 1** : Sélectionner les fondations (coût: 2 bois + 1 pierre)
- **Touche 2** : Sélectionner les murs (coût: 1 bois + 2 pierres)
- **Clic gauche** (en mode construction) : Placer une structure
- La portée de construction est de 3 cases

### Combat et Survie
- Les ennemis (cercles rouges) détectent le joueur dans un rayon de 3 cases
- Ils se dirigent automatiquement vers le joueur et l'attaquent au contact
- La santé du joueur diminue lors des attaques
- **Touche H** : Consommer de la nourriture pour récupérer de la santé

### Sauvegarde
- **F5** : Sauvegarder la partie en cours
- **Charger Partie** dans le menu : Reprendre la dernière sauvegarde
- Les sauvegardes incluent : position, inventaire, monde, ennemis

## Éléments du Jeu

### Types de Terrain
- 🟢 **Herbe** (vert) : Terrain traversable, zone de construction
- 🟤 **Arbres** (marron) : Source de bois
- ⚫ **Pierres** (gris) : Source de pierre
- ⚫ **Minerai de fer** (gris foncé) : Source de fer

### Structures Constructibles
- 🟡 **Fondations** (jaune) : Base de construction (2 bois + 1 pierre)
- 🟠 **Murs** (orange) : Structures défensives (1 bois + 2 pierres)

### Ennemis
- 🔴 **Ennemis hostiles** (cercles rouges) : 50 PV, 10 dégâts, détection à 3 cases

## Interface Utilisateur (HUD)

### Affichage en haut à gauche :
- **Barre de santé** : Santé actuelle / santé maximale (100)
- **Barre de santé visuelle** : Rouge/vert avec bordure blanche
- **Inventaire** : Quantités de bois, pierre et fer

### Instructions en bas de l'écran :
- Rappel des contrôles principaux

## Architecture du Code

### Classes principales :
- **`Game`** : Classe principale gérant la boucle de jeu
- **`Player`** : Gestion du joueur, inventaire, déplacement, récolte et construction
- **`Enemy`** : IA ennemie avec détection et attaque
- **`WorldGenerator`** : Génération procédurale de la carte
- **`Camera`** : Système de caméra suivant le joueur
- **`HUD`** : Interface utilisateur
- **`Building`** : Gestion des structures (préparé pour extensions futures)
- **`Faction`** : Système de factions (préparé pour extensions futures)

### Énumérations :
- **`TileType`** : Types de cases (herbe, arbre, pierre, minerai, mur, fondation)

## Compatibilité

Le jeu est testé et compatible avec :
- ✅ **Linux** (développé et testé)
- ✅ **Windows** (compatible via Pygame)
- ✅ **macOS** (compatible via Pygame)

## Extensions Possibles

### À court terme :
- Système de crafting plus avancé
- Plus de types d'ennemis
- Système de points de vie pour les structures
- Sauvegarde/chargement de partie

### À moyen terme :
- Multijoueur en réseau
- Système de quêtes
- Plus de ressources et recettes
- Système d'expérience et de compétences

### À long terme :
- Interface graphique améliorée avec sprites
- Système de commerce entre joueurs
- Cartes plus grandes avec biomes différents
- Système de guildes et alliances

## Dépendances

- **pygame** >= 2.5.0 : Moteur de jeu 2D
- **numpy** >= 1.21.0 : Calculs mathématiques (utilisé pour les futures extensions)

## Performance

- **FPS cible** : 60 FPS
- **Carte** : 100x100 cases (optimisé avec culling visuel)
- **Rendu** : Seules les cases visibles sont dessinées
- **Recommandations système** : Processeur moderne, 4GB RAM minimum

---

Développé avec ❤️ en Python et Pygame
