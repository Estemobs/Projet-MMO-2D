import pygame
from .constants import WHITE, RED, GREEN, YELLOW

class HUD:
    def __init__(self, font):
        self.font = font
        self.small_font = pygame.font.Font(None, 18)
    
    def draw(self, screen, player, game_instance=None):
        bar_width = 200
        bar_height = 20

        # ── Background panel ──────────────────────────────────────────────
        hud_background_rect = pygame.Rect(5, 5, 450, 90)
        pygame.draw.rect(screen, (0, 0, 0), hud_background_rect)
        pygame.draw.rect(screen, WHITE, hud_background_rect, 2)

        # ── Health ────────────────────────────────────────────────────────
        health_text = self.font.render(
            f"Santé: {int(player.health)}/{player.max_health}", True, WHITE)
        screen.blit(health_text, (10, 10))

        health_ratio = max(0, player.health / player.max_health)
        pygame.draw.rect(screen, RED,   (10, 35, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (10, 35, int(bar_width * health_ratio), bar_height))
        pygame.draw.rect(screen, WHITE, (10, 35, bar_width, bar_height), 2)

        # ── Hunger ────────────────────────────────────────────────────────
        hunger_text = self.font.render(
            f"Faim: {int(player.hunger)}/{player.max_hunger}", True, WHITE)
        screen.blit(hunger_text, (220, 10))

        hunger_ratio = max(0, player.hunger / player.max_hunger)
        hunger_color = GREEN if player.hunger > 30 else (YELLOW if player.hunger > 10 else RED)
        pygame.draw.rect(screen, RED,          (220, 35, bar_width, bar_height))
        pygame.draw.rect(screen, hunger_color, (220, 35, int(bar_width * hunger_ratio), bar_height))
        pygame.draw.rect(screen, WHITE,        (220, 35, bar_width, bar_height), 2)

        # ── Level / XP ────────────────────────────────────────────────────
        level = getattr(player, 'level', 1)
        xp = getattr(player, 'xp', 0)
        xp_needed = level * 100
        xp_ratio = min(1.0, xp / xp_needed)
        level_text = self.font.render(f"Niv.{level}  XP:{xp}/{xp_needed}", True, WHITE)
        screen.blit(level_text, (10, 60))
        pygame.draw.rect(screen, (50, 50, 200), (180, 60, 120, 14))
        pygame.draw.rect(screen, (100, 100, 255), (180, 60, int(120 * xp_ratio), 14))
        pygame.draw.rect(screen, WHITE, (180, 60, 120, 14), 1)

        # ── Weapon indicator ─────────────────────────────────────────────
        weapon_name = "Mains nues"
        dmg = player.BARE_HANDS_DAMAGE
        for slot in player.inventory.slots:
            if slot and slot.item.type in ("weapon", "tool"):
                weapon_name = slot.item.name
                dmg = player.WEAPON_DAMAGE.get(slot.item.name, player.BARE_HANDS_DAMAGE)
                break
        weapon_text = self.small_font.render(
            f"Arme: {weapon_name}  ({dmg} dégâts)", True, (200, 200, 200))
        screen.blit(weapon_text, (310, 62))

        # ── Build mode indicator ──────────────────────────────────────────
        if player.build_mode:
            mode_text = self.font.render(
                f"🏗 MODE CONSTRUCTION: {player.selected_building.upper()}", True, YELLOW)
            screen.blit(mode_text, (450, 10))

