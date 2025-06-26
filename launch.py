#!/usr/bin/env python3
"""
Script de lancement du jeu MMO 2D
"""

import sys
import os

def main():
    """Lance le jeu MMO 2D"""
    print("🎮 Lancement du jeu MMO 2D...")
    print("=" * 40)
    
    try:
        # Importer et lancer le jeu
        from main import Game
        
        print("✅ Modules chargés avec succès")
        print("🚀 Initialisation du jeu...")
        
        game = Game()
        print("🎯 Jeu initialisé, démarrage...")
        print("\n🎮 CONTRÔLES:")
        print("  • WASD / Flèches : Se déplacer")
        print("  • Clic gauche : Récolter/Construire")
        print("  • B : Mode construction")
        print("  • 1 : Fondation, 2 : Mur")
        print("  • Échap : Quitter")
        print("\n🎯 Amusez-vous bien !")
        print("=" * 40)
        
        game.run()
        
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        print("💡 Assurez-vous d'avoir installé les dépendances:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        sys.exit(1)
    
    print("\n👋 Merci d'avoir joué !")

if __name__ == "__main__":
    main()
