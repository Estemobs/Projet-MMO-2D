#!/bin/bash
# Script de lancement pour le jeu MMO 2D

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎮 Lancement du jeu MMO 2D...${NC}"
echo "========================================"

# Aller dans le répertoire du jeu
cd "$(dirname "$0")"

# Vérifier que l'environnement virtuel existe
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Environnement virtuel non trouvé. Création...${NC}"
    python3 -m venv .venv
fi

# Activer l'environnement virtuel
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo -e "${GREEN}✅ Environnement virtuel activé${NC}"
else
    echo -e "${RED}❌ Impossible d'activer l'environnement virtuel${NC}"
    exit 1
fi

# Vérifier et installer les dépendances
echo -e "${BLUE}📦 Vérification des dépendances...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Dépendances installées${NC}"
    else
        echo -e "${RED}❌ Erreur lors de l'installation des dépendances${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  Fichier requirements.txt non trouvé${NC}"
fi

echo -e "${BLUE}🚀 Démarrage du jeu...${NC}"
echo ""
echo -e "${GREEN}🎮 CONTRÔLES RAPIDES:${NC}"
echo "  • WASD / Flèches : Se déplacer"
echo "  • Clic gauche : Récolter/Construire"
echo "  • B : Mode construction"
echo "  • I : Inventaire"
echo "  • F5 : Sauvegarder"
echo "  • Échap : Menu principal"
echo ""
echo -e "${BLUE}🎯 Bon jeu !${NC}"
echo "========================================"

# Lancer le jeu
python main.py

# Désactiver l'environnement virtuel
deactivate

echo ""
echo -e "${BLUE}👋 Merci d'avoir joué !${NC}"
