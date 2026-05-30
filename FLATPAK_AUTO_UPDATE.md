# 🚀 Système de Mise à Jour Automatique Flatpak

## 📋 Vue d'Ensemble

Le jeu MMO 2D utilise maintenant un **système de mise à jour automatique** qui :
- ✅ Reconstruit le flatpak **à chaque commit sur la branche main**
- ✅ Publie les builds **nightly** sur GitHub Releases
- ✅ Vérifie automatiquement les mises à jour **au démarrage du jeu**
- ✅ Télécharge et installe les mises à jour **sans intervention**

---

## 🔄 Comment Ça Marche

### 1. **Commit → Build Automatique**

```
git push origin main
    ↓
GitHub Actions déclenche le workflow
    ↓
Compile Windows .exe
Compile Linux Flatpak
    ↓
Publie le Flatpak dans GitHub Releases (tag: "nightly")
```

### 2. **Au Démarrage du Jeu**

```
Lance le jeu (main.py)
    ↓
Vérification des mises à jour sur GitHub
    ↓
Si une nouvelle version disponible :
  → Affiche une fenêtre de dialog
  → Montre les notes de version
  → Propose de mettre à jour maintenant ou plus tard
    ↓
Si mise à jour acceptée :
  → Télécharge le nouveau flatpak
  → Remplace le fichier existant
  → Propose de relancer le jeu
```

---

## 📦 Structure du Système

### **GitHub Workflow** (`.github/workflows/release.yml`)

```yaml
on:
  push:
    tags:
      - 'v[0-9]+.[0-9]+.[0-9]+'  # Versions stables
    branches:
      - main                      # Builds nightly
```

**3 jobs disponibles :**

| Job | Déclenchement | Résultat |
|-----|--|--|
| `build-windows` | Tags + main push | Génère `ProjetMMO2D.exe` |
| `build-flatpak` | Tags + main push | Génère `ProjetMMO2D.flatpak` |
| `release` | **Tags seulement** | Publie release stables |
| `publish-flatpak-nightly` | **Main seulement** | Publie nightly sur tag `nightly` |

### **Manifest Flatpak** (`packaging/io.github.Estemobs.ProjetMMO2D.yml`)

```yaml
modules:
  - name: projet-mmo-2d
    sources:
      - type: git                              # ← Utilise le repo GitHub
        url: https://github.com/Estemobs/Projet-MMO-2D.git
        branch: main                           # ← Clone toujours depuis main
        commit: HEAD
```

**Avantage :** Le flatpak est construit directement depuis le repo, sans fichiers locaux.

### **Système de Vérification** (`systems/update_checker.py`)

```python
# Cherche les mises à jour
checker = UpdateChecker(check_nightly=True)
checker.check()

# Retourne :
# - has_update: bool - Y a-t-il une MAJ disponible ?
# - latest_release: dict - Infos de la release
# - is_nightly: bool - Est-ce une nightly build ?
```

---

## 🎯 Cas d'Usage

### **Scenario 1: Fix un bug sur main**

```bash
git add .
git commit -m "fix: corriger le bug de collision"
git push origin main
```

↓ **Immédiatement** (en ~5 min):
- Le flatpak est construit
- Disponible comme "nightly" sur GitHub Releases
- Au prochain lancement : le jeu propose la mise à jour

### **Scenario 2: Nouvelle version stable**

```bash
git tag v1.2.0
git push origin v1.2.0
```

↓ **Immédiatement** :
- Builds Windows .exe **ET** Linux Flatpak
- Crée une **GitHub Release v1.2.0** officielle
- Marque comme "Stable" (pas prerelease)
- Les utilisateurs voient "v1.2.0" comme nouvelle version

---

## 🔍 Vérifier les Builds

### **Voir les workflows GitHub**

```bash
gh run list --workflow=release.yml
```

### **Télécharger le nightly manuellement**

```bash
gh release download nightly --pattern "*.flatpak"
```

### **Checker les releases**

```bash
gh release list
```

---

## 📱 Versions Disponibles sur Releases

| Tag | Type | Build | Éditable |
|-----|------|-------|----------|
| `nightly` | Build auto | À chaque commit main | ✅ Auto |
| `v1.2.0` | Stable | Créé lors du tag | ❌ Manuel |

---

## ⚠️ Points Importants

### **Les utilisateurs reçoivent les updates de deux façons :**

1. **Au démarrage du jeu** (recommandé)
   - Vérification auto avant chaque lancement
   - Dialog GUI pour accepter/refuser
   - Télécharge et installe automatiquement

2. **Manuellement**
   - Ils peuvent télécharger le nightly depuis Releases
   - Remplacer le fichier `.flatpak` manuellement

### **Versions nightly vs Stables**

- **Nightly** (`tag: nightly`)
  - Dernier code de `main`
  - Peut contenir des bugs
  - Marqé comme "prerelease"
  - Mis à jour à chaque commit

- **Stable** (`tag: v1.2.0`)
  - Code testé et validé
  - Avec release notes officielles
  - Marqué comme release stable
  - Créé manuellement avec un tag

---

## 🛠️ Configuration Avancée

### **Désactiver les checks nightly**

Dans `main.py` ou `core/game_manager.py` :

```python
# Chercher seulement les versions stables
checker = UpdateChecker(check_nightly=False)
```

### **Forcer une vérification manuelle**

```python
from systems.update_checker import check_for_updates_sync

checker = check_for_updates_sync(check_nightly=True)
if checker.has_update:
    print(f"Nouvelle version: {checker.get_latest_version()}")
    print(checker.get_release_notes())
```

---

## 📊 Diagramme du Flux Complet

```
┌─────────────────────────────────────────────────────────┐
│         USER COMMITS & PUSHES CODE TO MAIN             │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    ┌────▼────┐            ┌─────▼─────┐
    │ WINDOWS │            │   LINUX   │
    │ BUILD   │            │  FLATPAK  │
    └────┬────┘            └─────┬─────┘
         │                       │
    ┌────▼──────────────────────▼────┐
    │ PUBLISH TO GITHUB RELEASES     │
    │ Tag: "nightly" (prerelease)    │
    └────────────┬────────────────────┘
                 │
    ┌────────────▼────────────┐
    │  USER LAUNCHES GAME     │
    └────────────┬────────────┘
                 │
    ┌────────────▼──────────────────┐
    │  CHECK FOR UPDATES AT STARTUP │
    │  (queries GitHub API)         │
    └────────────┬──────────────────┘
                 │
         ┌───────┴───────┐
         │               │
    ┌────▼────┐    ┌─────▼─────┐
    │ UPDATE  │    │   LAUNCH  │
    │ FOUND?  │    │  NORMALLY │
    └────┬────┘    └───────────┘
         │
    ┌────▼──────────────────────┐
    │ SHOW UPDATE DIALOG        │
    │ WITH RELEASE NOTES        │
    └────┬───────────┬──────────┘
         │           │
    ┌────▼────┐ ┌────▼─────┐
    │ACCEPT   │ │ DECLINE  │
    │UPDATE   │ │ UPDATE   │
    └────┬────┘ └────┬─────┘
         │           │
    ┌────▼────┐ ┌────▼─────────┐
    │DOWNLOAD │ │ LAUNCH GAME  │
    │& INSTALL│ │ AS-IS        │
    └────┬────┘ └──────────────┘
         │
    ┌────▼──────────────────┐
    │ RESTART GAME PROMPT   │
    │ (new version applied) │
    └───────────────────────┘
```

---

## 🚀 Résumé des Bénéfices

✅ **Automatique** - Les utilisateurs reçoivent les mises à jour sans action manuelle  
✅ **Rapide** - Les builds commencent immédiatement après un push  
✅ **Transparent** - Interface graphique pour accepter/refuser les mises à jour  
✅ **Sûr** - Récupère depuis le repo officiel, pas de fichiers locaux  
✅ **Flexible** - Support des versions nightly ET stables  

---

**Dernière mise à jour:** Mai 2025
