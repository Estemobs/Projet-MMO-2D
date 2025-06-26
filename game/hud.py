import pygame
from .constants import WINDOW_WIDTH, BLACK, WHITE, RED, GREEN, YELLOW

class HUD:
    def __init__(self, font):
        self.font = font
    
    def draw(self, screen, player, game_instance=None):
        # Fond semi-transparent pour le HUD
        hud_surface = pygame.Surface((WINDOW_WIDTH, 100))
        hud_surface.set_alpha(180)
        hud_surface.fill(BLACK)
        screen.blit(hud_surface, (0, 0))
        
        # Afficher la santé
        health_text = self.font.render(f"Santé: {player.health}/{player.max_health}", True, WHITE)
        screen.blit(health_text, (10, 10))
        
        # Barre de santé
        health_bar_width = 200
        health_bar_height = 20
        health_ratio = player.health / player.max_health
        
        pygame.draw.rect(screen, RED, (10, 35, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, GREEN, (10, 35, health_bar_width * health_ratio, health_bar_height))
        pygame.draw.rect(screen, WHITE, (10, 35, health_bar_width, health_bar_height), 2)
        
        # Afficher quelques ressources importantes
        inventory_y = 60
        wood_count = player.inventory.get_item_count("wood")
        stone_count = player.inventory.get_item_count("stone")
        iron_count = player.inventory.get_item_count("iron_ore")
        
        wood_text = self.font.render(f"Bois: {wood_count}", True, WHITE)
        stone_text = self.font.render(f"Pierre: {stone_count}", True, WHITE)
        iron_text = self.font.render(f"Fer: {iron_count}", True, WHITE)
        
        screen.blit(wood_text, (10, inventory_y))
        screen.blit(stone_text, (120, inventory_y))
        screen.blit(iron_text, (250, inventory_y))
        
        # Mode de construction
        if player.build_mode:
            mode_text = self.font.render(f"MODE CONSTRUCTION: {player.selected_building}", True, YELLOW)
            screen.blit(mode_text, (400, 10))
        
        # Temps de jeu
        if game_instance:
            playtime_text = self.font.render(f"Temps de jeu: {game_instance.get_playtime()}", True, WHITE)
            screen.blit(playtime_text, (800, 10))
