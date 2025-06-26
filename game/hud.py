import pygame
from .constants import WHITE, RED, GREEN, YELLOW

class HUD:
    def __init__(self, font):
        self.font = font
    
    def draw(self, screen, player, game_instance=None):
        # Afficher la santé (sans fond noir)
        health_text = self.font.render(f"Santé: {player.health}/{player.max_health}", True, WHITE)
        screen.blit(health_text, (10, 10))
        
        # Barre de santé
        health_bar_width = 200
        health_bar_height = 20
        health_ratio = player.health / player.max_health
        
        pygame.draw.rect(screen, RED, (10, 35, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, GREEN, (10, 35, health_bar_width * health_ratio, health_bar_height))
        pygame.draw.rect(screen, WHITE, (10, 35, health_bar_width, health_bar_height), 2)
        
        # Mode de construction
        if player.build_mode:
            mode_text = self.font.render(f"MODE CONSTRUCTION: {player.selected_building}", True, YELLOW)
            screen.blit(mode_text, (400, 10))
