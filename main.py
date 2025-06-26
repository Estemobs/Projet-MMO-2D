#!/usr/bin/env python3
"""
Fichier principal simplifié du jeu MMO 2D
"""

import pygame
import sys
import os

# Ajouter le répertoire du projet au path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from core import GameManager

def main():
    """Point d'entrée principal du jeu"""
    try:
        # Créer le gestionnaire de jeu
        game_manager = GameManager()
        
        # Lancer la boucle principale
        game_manager.run()
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        sys.exit(1)
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
