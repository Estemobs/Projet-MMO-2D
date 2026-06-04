"""
Game Manager - Battle Royale
"""

import pygame

from ui.inventory import InventoryUI
from ui.menu import Menu
from ui.pause_menu import PauseMenu
from game.constants import COLORS, TARGET_FPS, update_scale
from game.hud import HUD
from game.render_manager import RenderManager
from game.gameplay_manager import GameplayManager
from game.minimap import MiniMap
from game.sprite_manager import get_sprite_manager
from game.sound_manager import get_sound_manager
from game.transitions import ScreenTransition
from game.controls_hint import ControlsHint
from core.items import create_items

pygame.init()


class GameManager:
    def __init__(self):
        self.state = "menu"

        temp_screen = pygame.display.set_mode((800, 600))
        temp_font = pygame.font.Font(None, 24)
        temp_menu = Menu(temp_screen, temp_font)

        if temp_menu.fullscreen:
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
        else:
            resolution = temp_menu.get_resolution()
            self.screen = pygame.display.set_mode(resolution)

        pygame.display.set_caption("Battle Royale - Dernier en vie")
        update_scale(self.screen.get_width(), self.screen.get_height())
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

        self.items = create_items()

        self.sprite_manager = get_sprite_manager()
        self.sound_manager = get_sound_manager()
        self.transitions = ScreenTransition(self.screen.get_width(), self.screen.get_height())

        self.menu = Menu(self.screen, self.font)
        self.inventory_ui = InventoryUI(self.screen, self.font, self.sprite_manager)
        self.pause_menu = PauseMenu(self.screen, self.font)

        self.render_manager = RenderManager(self.screen)
        self.gameplay_manager = GameplayManager()
        self.minimap = MiniMap(self.screen.get_width(), self.screen.get_height())

        self.controls_hint = ControlsHint(self.screen.get_width(), self.screen.get_height())

        self.world_map = None
        self.player = None
        self.camera = None
        self.hud = None

        self.running = True

    def init_game(self):
        self.gameplay_manager.init_new_game(self.screen.get_width(), self.screen.get_height())

        self.world_map = self.gameplay_manager.world_map
        self.player = self.gameplay_manager.player
        self.camera = self.gameplay_manager.camera

        self.hud = HUD(self.font)
        self.minimap.generate_world_minimap(self.world_map)

        self._give_starting_items()
        self.state = "playing"

    def _give_starting_items(self):
        self.player.inventory.add_item(self.items["bandage"], 2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.state == "menu":
                self._handle_menu_events(event)
            elif self.state == "playing":
                self._handle_game_events(event)

    def _handle_menu_events(self, event):
        action = self.menu.handle_event(event)
        if action == "new_game":
            self.init_game()
        elif action == "options":
            self.menu.current_menu = "options"
            self.menu.selected_button = 0
        elif action == "quit":
            self.running = False
        elif action == "toggle_fullscreen":
            self._toggle_fullscreen()
        elif action and action.startswith("remap_control_"):
            control_key = action.split("remap_control_")[-1]
            self._remap_control(control_key)

    def _handle_game_events(self, event):
        if self.pause_menu.visible:
            action = self.pause_menu.handle_event(event)
            if action == "resume":
                self.pause_menu.hide()
            elif action == "menu":
                self.pause_menu.hide()
                self.state = "menu"
                self.menu.current_menu = "main"
            elif action == "quit":
                self.running = False
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pause_menu.show()
            elif event.key == pygame.K_i:
                self.inventory_ui.toggle_visibility()
            elif event.key == pygame.K_f:
                if self.player:
                    result = self.player.eat_best_food()
                    if result:
                        food_name, heal = result

        if self.inventory_ui.visible:
            self.inventory_ui.handle_event(event, self.player.inventory, None)

    def update(self, dt):
        if self.state == "playing":
            keys = pygame.key.get_pressed()
            mouse_buttons = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()

            self.gameplay_manager.update(keys, mouse_buttons, mouse_pos, dt, self.menu.controls, self.camera, self.items)
            self.render_manager.update_time(dt)

            if self.hud:
                self.hud.update(dt)

            self.player = self.gameplay_manager.player

    def draw(self):
        self.screen.fill(COLORS["BLACK"])
        if self.state == "menu":
            self.menu.draw()
        elif self.state == "playing":
            self._draw_game()
        pygame.display.flip()

    def _draw_game(self):
        self.render_manager.draw_world(self.world_map, self.camera)
        self.render_manager.draw_entities(
            self.player, self.gameplay_manager.enemies, self.gameplay_manager.death_markers,
            self.camera, self.gameplay_manager.item_manager
        )

        if hasattr(self.gameplay_manager, 'particle_manager'):
            self.gameplay_manager.particle_manager.draw(self.screen, self.camera)

        self.minimap.draw(self.screen, self.player, self.gameplay_manager.enemies, self.camera, self.gameplay_manager.death_markers)
        self.hud.draw(self.screen, self.player, self)

        if self.player.attack_feedback:
            self._draw_attack_feedback()

        if self.gameplay_manager.show_death_message:
            self._draw_death_message()

        self.inventory_ui.draw(self.player.inventory, None)
        self.pause_menu.draw()
        self.controls_hint.draw(self.screen, self.player, self.menu.controls)

    def _draw_attack_feedback(self):
        text, _ = self.player.attack_feedback
        big_font = pygame.font.Font(None, 40)
        surf = big_font.render(text, True, COLORS["RED"])
        x = self.screen.get_width() // 2 - surf.get_width() // 2
        y = self.screen.get_height() // 2 - 60
        self.screen.blit(surf, (x, y))

    def _draw_death_message(self):
        big_font = pygame.font.Font(None, 48)
        lines = ["Vous etes mort!", "Votre inventaire est sur la map.", "Allez le recuperer."]
        for i, line in enumerate(lines):
            surf = big_font.render(line, True, COLORS["RED"])
            x = self.screen.get_width() // 2 - surf.get_width() // 2
            y = self.screen.get_height() // 3 + i * 50
            self.screen.blit(surf, (x, y))

    def _toggle_fullscreen(self):
        try:
            if self.menu.is_fullscreen():
                info = pygame.display.Info()
                self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            else:
                current_resolution = self.menu.get_resolution()
                self.screen = pygame.display.set_mode(current_resolution)

            update_scale(self.screen.get_width(), self.screen.get_height())
            self.menu.screen = self.screen

            if self.state == "playing":
                if hasattr(self, 'hud') and self.hud:
                    self.hud.screen = self.screen
                if hasattr(self, 'camera') and self.camera:
                    self.camera.update_screen_size(self.screen.get_width(), self.screen.get_height())
                if hasattr(self, 'minimap') and self.minimap:
                    self.minimap.update_screen_size(self.screen.get_width(), self.screen.get_height())
                if hasattr(self, 'controls_hint') and self.controls_hint:
                    self.controls_hint.update_screen_size(self.screen.get_width(), self.screen.get_height())
                if hasattr(self, 'transitions') and self.transitions:
                    self.transitions.update_screen_size(self.screen.get_width(), self.screen.get_height())
        except Exception as e:
            print(f"Erreur fullscreen: {e}")

    def _remap_control(self, control_key):
        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    else:
                        self.menu.controls[control_key] = event.key
                        self.menu.save_settings()
                        waiting_for_key = False

            self.menu.draw()
            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            dw, dh = 500, 150
            dx = (self.screen.get_width() - dw) // 2
            dy = (self.screen.get_height() - dh) // 2
            pygame.draw.rect(self.screen, (40, 40, 40), (dx, dy, dw, dh))
            pygame.draw.rect(self.screen, (255, 255, 255), (dx, dy, dw, dh), 3)

            control_names = {
                "move_up": "Monter", "move_down": "Descendre",
                "move_left": "Gauche", "move_right": "Droite",
                "inventory": "Inventaire",
            }
            title_surf = self.font.render(f"Modifier: {control_names.get(control_key, control_key)}", True, (255, 255, 255))
            self.screen.blit(title_surf, title_surf.get_rect(center=(dx + dw // 2, dy + 40)))
            wait_surf = self.font.render("Appuyez sur une touche...", True, (255, 255, 0))
            self.screen.blit(wait_surf, wait_surf.get_rect(center=(dx + dw // 2, dy + 80)))
            cancel_surf = self.font.render("(Echap pour annuler)", True, (200, 200, 200))
            self.screen.blit(cancel_surf, cancel_surf.get_rect(center=(dx + dw // 2, dy + 110)))

            pygame.display.flip()
            self.clock.tick(30)

    def run(self):
        while self.running:
            dt = self.clock.tick(TARGET_FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
            self.transitions.update()
        pygame.quit()
