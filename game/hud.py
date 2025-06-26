import pygame
from .constants import WHITE, RED, GREEN, YELLOW

class HUD:
    def __init__(self, font):
        self.font = font
    
    def draw(self, screen, player, game_instance=None):
        # Afficher la santé
        health_text = self.font.render(f"Santé: {int(player.health)}/{player.max_health}", True, WHITE)
        screen.blit(health_text, (10, 10))
        
        # Barre de santé
        health_bar_width = 200
        health_bar_height = 20
        health_ratio = player.health / player.max_health
        
        pygame.draw.rect(screen, RED, (10, 35, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, GREEN, (10, 35, health_bar_width * health_ratio, health_bar_height))
        pygame.draw.rect(screen, WHITE, (10, 35, health_bar_width, health_bar_height), 2)
        
        # Afficher la faim
        hunger_text = self.font.render(f"Faim: {int(player.hunger)}/{player.max_hunger}", True, WHITE)
        screen.blit(hunger_text, (220, 10))
        
        # Barre de faim
        hunger_ratio = player.hunger / player.max_hunger
        hunger_color = GREEN if player.hunger > 30 else (YELLOW if player.hunger > 10 else RED)
        
        pygame.draw.rect(screen, RED, (220, 35, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, hunger_color, (220, 35, health_bar_width * hunger_ratio, health_bar_height))
        pygame.draw.rect(screen, WHITE, (220, 35, health_bar_width, health_bar_height), 2)
        
        # Afficher les ressources importantes derrière les barres de vie
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
            screen.blit(mode_text, (450, 10))
