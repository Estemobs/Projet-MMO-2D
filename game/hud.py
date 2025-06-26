import pygame
from .constants import WHITE, RED, GREEN, YELLOW, BLACK

class HUD:
    def __init__(self, font):
        self.font = font
        self.small_font = pygame.font.Font(None, 18)
    
    def draw(self, screen, player, game_instance=None):
        # Fond pour les barres et informations
        hud_background_rect = pygame.Rect(5, 5, 450, 65)  # Réduit la hauteur
        pygame.draw.rect(screen, (0, 0, 0, 128), hud_background_rect)  # Fond semi-transparent
        pygame.draw.rect(screen, WHITE, hud_background_rect, 2)  # Bordure blanche
        
        # Afficher la santé
        health_text = self.font.render(f"Santé: {int(player.health)}/{player.max_health}", True, WHITE)
        screen.blit(health_text, (10, 10))
        
        # Barre de santé avec fond
        health_bar_width = 200
        health_bar_height = 20
        health_ratio = player.health / player.max_health
        
        # Fond de la barre de santé
        pygame.draw.rect(screen, BLACK, (10, 35, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, RED, (10, 35, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, GREEN, (10, 35, health_bar_width * health_ratio, health_bar_height))
        pygame.draw.rect(screen, WHITE, (10, 35, health_bar_width, health_bar_height), 2)
        
        # Afficher la faim
        hunger_text = self.font.render(f"Faim: {int(player.hunger)}/{player.max_hunger}", True, WHITE)
        screen.blit(hunger_text, (220, 10))
        
        # Barre de faim avec fond
        hunger_ratio = player.hunger / player.max_hunger
        hunger_color = GREEN if player.hunger > 30 else (YELLOW if player.hunger > 10 else RED)
        
        # Fond de la barre de faim
        pygame.draw.rect(screen, BLACK, (220, 35, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, RED, (220, 35, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, hunger_color, (220, 35, health_bar_width * hunger_ratio, health_bar_height))
        pygame.draw.rect(screen, WHITE, (220, 35, health_bar_width, health_bar_height), 2)
        
        # Mode de construction
        if player.build_mode:
            mode_text = self.font.render(f"MODE CONSTRUCTION: {player.selected_building}", True, YELLOW)
            screen.blit(mode_text, (10, screen.get_height() - 30))
            screen.blit(mode_text, (450, 10))
