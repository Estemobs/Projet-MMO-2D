#!/usr/bin/env python3
"""
Test complet simulation d'utilisation en jeu
"""

import sys
import os
import pygame

# Ajouter le répertoire parent au path pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

def simulate_f5_save():
    """Simule une sauvegarde F5 en jeu"""
    print("🔍 Simulation sauvegarde F5...")
    
    try:
        pygame.init()
        
        from core import GameManager
        
        # Créer le jeu
        game_manager = GameManager()
        game_manager.init_game()
        
        # Modifier quelques valeurs pour tester
        original_health = game_manager.player.health
        game_manager.player.health = 85
        game_manager.player.x = 123
        game_manager.player.y = 456
        
        print(f"🎮 Joueur: Santé={game_manager.player.health}, Pos=({game_manager.player.x}, {game_manager.player.y})")
        
        # Simuler F5 (sauvegarde par défaut slot 0)
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F5)
        game_manager._handle_game_events(event)
        
        print("✅ F5 pressé - sauvegarde effectuée")
        
        # Vérifier le fichier
        save_path = "saves/save_slot_0.json"
        if os.path.exists(save_path):
            print("✅ Fichier sauvegarde créé")
            
            # Restaurer la santé originale pour tester le chargement
            game_manager.player.health = original_health
            game_manager.player.x = 0
            game_manager.player.y = 0
            
            # Simuler Échap pour aller au menu
            game_manager.state = "menu"
            game_manager.menu.current_menu = "load_menu"
            game_manager.menu.load_save_slots_info()
            
            print("📋 Menu chargement ouvert")
            
            # Vérifier que le slot 0 est visible
            slot_0 = game_manager.menu.save_slots[0]
            if slot_0 and slot_0.get("exists", False):
                print("✅ Slot 0 visible dans le menu")
                print(f"   Info: {slot_0}")
                
                # Simuler le chargement du slot 0
                if game_manager.load_game(0):
                    print("✅ Chargement réussi")
                    print(f"🎮 Joueur restauré: Santé={game_manager.player.health}, Pos=({game_manager.player.x}, {game_manager.player.y})")
                    
                    if game_manager.player.health == 85:
                        print("✅ Données correctement restaurées")
                        return True
                    else:
                        print(f"❌ Santé incorrecte: {game_manager.player.health} (attendu: 85)")
                        return False
                else:
                    print("❌ Chargement échoué")
                    return False
            else:
                print("❌ Slot 0 non visible dans le menu")
                return False
        else:
            print("❌ Fichier sauvegarde non créé")
            return False
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def simulate_menu_save():
    """Simule une sauvegarde via le menu"""
    print("\n🔍 Simulation sauvegarde via menu...")
    
    try:
        pygame.init()
        
        from core import GameManager
        
        # Créer le jeu
        game_manager = GameManager()
        game_manager.init_game()
        
        # Modifier des valeurs
        game_manager.player.health = 77
        
        # Aller au menu sauvegarde
        game_manager.state = "menu"
        game_manager.menu.current_menu = "save_menu"
        game_manager.menu.load_save_slots_info()
        
        # Simuler sauvegarde dans slot 1
        action = "save_slot_1"
        if action.startswith("save_slot_"):
            slot_number = int(action.split("_")[-1])
            if game_manager.save_game(slot_number):
                print(f"✅ Sauvegarde menu slot {slot_number} réussie")
                
                # Vérifier que le fichier existe
                save_path = f"saves/save_slot_{slot_number}.json"
                if os.path.exists(save_path):
                    print("✅ Fichier créé")
                    
                    # Actualiser et vérifier le menu
                    game_manager.menu.load_save_slots_info()
                    slot_info = game_manager.menu.save_slots[slot_number]
                    
                    if slot_info and slot_info.get("exists", False):
                        print("✅ Sauvegarde visible dans le menu")
                        return True
                    else:
                        print("❌ Sauvegarde non visible dans le menu")
                        return False
                else:
                    print("❌ Fichier non créé")
                    return False
            else:
                print("❌ Sauvegarde échouée")
                return False
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🎮 SIMULATION COMPLÈTE D'UTILISATION")
    print("=" * 40)
    
    test1 = simulate_f5_save()
    test2 = simulate_menu_save()
    
    print("\n📊 RÉSULTATS")
    print("=" * 12)
    print(f"Sauvegarde F5:    {'✅ OK' if test1 else '❌ ÉCHEC'}")
    print(f"Sauvegarde menu:  {'✅ OK' if test2 else '❌ ÉCHEC'}")
    
    if test1 and test2:
        print("\n🎉 TOUS LES PROBLÈMES SONT CORRIGÉS !")
        print("✅ F5 fonctionne et apparaît dans le menu")
        print("✅ Sauvegarde via menu fonctionne")
        print("✅ Chargement fonctionne")
    else:
        print("\n⚠️ Des problèmes persistent")

if __name__ == "__main__":
    main()
