#!/usr/bin/env python3
"""
Script de test de performance pour le jeu MMO 2D
"""

import time
import pygame
import psutil
import os
from main import Game

def test_performance():
    """Test les performances du jeu pendant 10 secondes"""
    print("🎮 Test de performance du jeu MMO 2D")
    print("=" * 50)
    
    # Initialiser le jeu
    game = Game()
    
    # Variables de test
    frame_count = 0
    start_time = time.time()
    test_duration = 10  # secondes
    fps_samples = []
    
    # Informations système
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    print(f"📊 Mémoire initiale: {initial_memory:.1f} MB")
    print(f"⏱️  Test pendant {test_duration} secondes...")
    print("🔄 Appuyez sur Échap ou fermez la fenêtre pour arrêter le test")
    print()
    
    # Boucle de test
    while game.running and (time.time() - start_time) < test_duration:
        dt = game.clock.tick(60) / 1000.0
        
        # Gestion des événements (permettre la fermeture)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.running = False
        
        # Mise à jour et rendu
        game.update(dt)
        game.draw()
        
        # Collecte des statistiques
        frame_count += 1
        current_fps = game.clock.get_fps()
        if current_fps > 0:
            fps_samples.append(current_fps)
        
        # Affichage des stats en temps réel (toutes les 60 frames)
        if frame_count % 60 == 0:
            current_memory = process.memory_info().rss / 1024 / 1024
            elapsed = time.time() - start_time
            avg_fps = frame_count / elapsed if elapsed > 0 else 0
            print(f"⏰ {elapsed:.1f}s | 🖼️  FPS: {current_fps:.1f} | 📊 Mémoire: {current_memory:.1f} MB")
    
    # Calcul des statistiques finales
    end_time = time.time()
    total_time = end_time - start_time
    final_memory = process.memory_info().rss / 1024 / 1024
    
    pygame.quit()
    
    # Affichage des résultats
    print("\n" + "=" * 50)
    print("📈 RÉSULTATS DU TEST")
    print("=" * 50)
    print(f"⏱️  Durée totale: {total_time:.2f} secondes")
    print(f"🖼️  Frames totales: {frame_count}")
    print(f"📊 FPS moyen: {frame_count / total_time:.1f}")
    
    if fps_samples:
        print(f"📊 FPS minimum: {min(fps_samples):.1f}")
        print(f"📊 FPS maximum: {max(fps_samples):.1f}")
        print(f"📊 FPS médian: {sorted(fps_samples)[len(fps_samples)//2]:.1f}")
    
    print(f"💾 Mémoire initiale: {initial_memory:.1f} MB")
    print(f"💾 Mémoire finale: {final_memory:.1f} MB")
    print(f"💾 Différence mémoire: {final_memory - initial_memory:+.1f} MB")
    
    # Évaluation des performances
    avg_fps = frame_count / total_time
    if avg_fps >= 55:
        performance_rating = "🟢 Excellente"
    elif avg_fps >= 45:
        performance_rating = "🟡 Bonne"
    elif avg_fps >= 30:
        performance_rating = "🟠 Correcte"
    else:
        performance_rating = "🔴 Faible"
    
    print(f"🎯 Performance globale: {performance_rating}")
    
    # Recommandations
    print("\n💡 RECOMMANDATIONS:")
    if avg_fps < 45:
        print("- Réduire la taille de la carte (MAP_WIDTH, MAP_HEIGHT)")
        print("- Réduire le nombre d'ennemis")
        print("- Optimiser le rendu (moins de détails visuels)")
    else:
        print("- Performance satisfaisante !")
        print("- Vous pouvez augmenter la complexité du jeu")

if __name__ == "__main__":
    try:
        test_performance()
    except KeyboardInterrupt:
        print("\n⏹️  Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur pendant le test: {e}")
