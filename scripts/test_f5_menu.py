#!/usr/bin/env python3
"""
Test de sauvegarde F5 et affichage dans le menu
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

def test_save_and_menu():
    """Test que la sauvegarde F5 apparaît dans le menu"""
    print("🔍 Test sauvegarde F5 et affichage menu...")
    
    try:
        import pygame
        pygame.init()
        
        from core import GameManager
        
        # Créer et initialiser le jeu
        game_manager = GameManager()
        game_manager.init_game()
        
        print("✅ Jeu initialisé")
        
        # Simuler une sauvegarde F5 (slot 0 par défaut)
        result = game_manager.save_game(0)
        if result:
            print("✅ Sauvegarde F5 (slot 0) créée")
        else:
            print("❌ Échec sauvegarde F5")
            return False
        
        # Vérifier que le fichier existe
        save_path = "saves/save_slot_0.json"
        if os.path.exists(save_path):
            print("✅ Fichier de sauvegarde créé")
        else:
            print("❌ Fichier de sauvegarde introuvable")
            return False
        
        # Tester le menu
        game_manager.menu.load_save_slots_info()
        
        # Vérifier que le slot 0 est détecté
        if game_manager.menu.save_slots[0] and game_manager.menu.save_slots[0].get("exists", False):
            print("✅ Sauvegarde détectée dans le menu slot 0")
        else:
            print("❌ Sauvegarde NON détectée dans le menu")
            print(f"   Slot 0: {game_manager.menu.save_slots[0]}")
            return False
        
        # Test de chargement
        if game_manager.load_game(0):
            print("✅ Chargement depuis slot 0 réussi")
        else:
            print("❌ Échec du chargement")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🎮 TEST SAUVEGARDE F5 + MENU")
    print("=" * 30)
    
    if test_save_and_menu():
        print("\n🎉 TOUT FONCTIONNE !")
        print("✅ F5 sauvegarde correctement")
        print("✅ Les sauvegardes apparaissent dans le menu")
        print("✅ Le chargement fonctionne")
    else:
        print("\n❌ DES PROBLÈMES DÉTECTÉS")
        print("Vérifiez les messages d'erreur ci-dessus")

if __name__ == "__main__":
    main()
