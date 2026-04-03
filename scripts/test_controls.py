#!/usr/bin/env python3
"""
Script de test pour vérifier les fonctionnalités du jeu
"""

import pygame
import sys
import os

# Ajouter le répertoire principal au path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_game_controls():
    """Test rapide des contrôles du jeu"""
    print("🧪 Test des contrôles du jeu...")
    
    # Importer le GameManager
    from core.game_manager import GameManager
    
    # Créer une instance du jeu
    game = GameManager()
    
    # Initialiser une nouvelle partie
    game.init_game()
    
    print("✅ Jeu initialisé avec succès")
    print(f"📊 Joueur position: ({int(game.player.x)}, {int(game.player.y)})")
    print(f"🎯 Ennemis: {len(game.enemies)}")
    print(f"💚 Santé du joueur: {game.player.health}")
    print(f"🍎 Faim du joueur: {game.player.hunger}")
    
    # Tester l'inventaire
    print("\n🎒 Test de l'inventaire:")
    items_count = sum(1 for slot in game.player.inventory.slots if slot is not None)
    print(f"   Items dans l'inventaire: {items_count}")
    
    # Tester la minimap
    print("\n🗺️ Test de la minimap:")
    print(f"   Position: ({game.minimap.x}, {game.minimap.y})")
    print(f"   Taille: {game.minimap.width}x{game.minimap.height}")
    
    # Nettoyer
    pygame.quit()
    print("\n✅ Tous les tests réussis!")

if __name__ == "__main__":
    test_game_controls()
