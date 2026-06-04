import pygame
from game.sound_manager import get_sound_manager
from game.constants import s

class Item:
    def __init__(self, name, item_type, description, stack_size=99, color=(255, 255, 255), sprite_name=None):
        self.name = name
        self.type = item_type  # "resource", "tool", "food", "weapon"
        self.description = description
        self.stack_size = stack_size
        self.color = color
        # Le nom du sprite correspond au nom de l'item par défaut
        self.sprite_name = sprite_name if sprite_name else name.lower().replace(" ", "_")

class ItemStack:
    def __init__(self, item, quantity=1):
        self.item = item
        self.quantity = quantity
    
    def can_stack_with(self, other_stack):
        return self.item.name == other_stack.item.name
    
    def add(self, quantity):
        """Ajoute une quantité à la pile. Retourne la quantité qui n'a pas pu être ajoutée."""
        max_add = self.item.stack_size - self.quantity
        actual_add = min(quantity, max_add)
        self.quantity += actual_add
        return quantity - actual_add

class Inventory:
    def __init__(self, size=36):
        self.size = size
        self.slots = [None] * size  # Liste de ItemStack ou None
        
        # Emplacement d'équipement (arme, armure, etc.)
        self.equipment = {
            "weapon": None,
            "armor": None,
            "tool": None
        }
    
    def add_item(self, item, quantity=1):
        """Ajoute un item à l'inventaire. Retourne la quantité qui n'a pas pu être ajoutée."""
        remaining = quantity
        
        # D'abord, essayer d'ajouter aux piles existantes
        for slot in self.slots:
            if slot and slot.can_stack_with(ItemStack(item)):
                remaining = slot.add(remaining)
                if remaining == 0:
                    return 0
        
        # Ensuite, créer de nouvelles piles dans les emplacements vides
        for i, slot in enumerate(self.slots):
            if slot is None and remaining > 0:
                take = min(remaining, item.stack_size)
                self.slots[i] = ItemStack(item, take)
                remaining -= take
        
        return remaining
    
    def remove_item(self, item_name, quantity=1):
        """Retire un item de l'inventaire. Retourne la quantité effectivement retirée."""
        removed = 0
        
        for i, slot in enumerate(self.slots):
            if slot and slot.item.name == item_name:
                take = min(quantity - removed, slot.quantity)
                slot.quantity -= take
                removed += take
                
                if slot.quantity == 0:
                    self.slots[i] = None
                
                if removed >= quantity:
                    break
        
        return removed
    
    def has_item(self, item_name, quantity=1):
        """Vérifie si l'inventaire contient assez d'un item."""
        total = 0
        for slot in self.slots:
            if slot and slot.item.name == item_name:
                total += slot.quantity
        return total >= quantity
    
    def get_item_count(self, item_name):
        """Retourne la quantité totale d'un item."""
        total = 0
        for slot in self.slots:
            if slot and slot.item.name == item_name:
                total += slot.quantity
        return total

class CraftingRecipe:
    def __init__(self, name, ingredients, result_item, result_quantity=1, description=""):
        self.name = name
        self.ingredients = ingredients  # {"item_name": quantity, ...}
        self.result_item = result_item
        self.result_quantity = result_quantity
        self.description = description
    
    def can_craft(self, inventory):
        """Vérifie si on peut crafter cette recette avec l'inventaire donné."""
        for item_name, needed_quantity in self.ingredients.items():
            if not inventory.has_item(item_name, needed_quantity):
                return False
        return True
    
    def craft(self, inventory):
        """Effectue le crafting si possible. Retourne True si réussi."""
        if not self.can_craft(inventory):
            return False
        
        # Retirer les ingrédients
        for item_name, needed_quantity in self.ingredients.items():
            inventory.remove_item(item_name, needed_quantity)
        
        # Ajouter le résultat
        inventory.add_item(self.result_item, self.result_quantity)
        return True

class InventoryUI:
    def __init__(self, screen, font, sprite_manager=None):
        self.screen = screen
        self.font = font
        self.small_font = pygame.font.Font(None, 16)
        self.tooltip_font = pygame.font.Font(None, 18)
        self.sprite_manager = sprite_manager
        
        # Couleurs modernes
        self.WHITE = (245, 247, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (132, 144, 170)
        self.DARK_GRAY = (36, 44, 68)
        self.GREEN = (84, 214, 125)
        self.BLUE = (88, 138, 255)
        self.RED = (245, 98, 98)
        self.ORANGE = (255, 165, 0)
        self.PURPLE = (200, 120, 255)
        self.YELLOW = (255, 221, 129)
        
        self.slot_size = 44
        self.slot_padding = 4
        self.visible = False
        self.selected_slot = 0
        self.hover_slot = -1
        
        # Sound manager
        self.sound_manager = get_sound_manager()
        
        # Craft feedback
        self.craft_feedback = ""
        self.craft_feedback_timer = 0.0
        
        # Modes d'affichage
        self.current_tab = "inventory"
        
        # Couleurs par catégorie d'item
        self.category_colors = {
            "resource": (84, 180, 120),   # Vert ressource
            "food": (220, 140, 60),       # Orange nourriture
            "weapon": (220, 80, 80),      # Rouge arme
            "tool": (140, 160, 200),      # Bleu outil
            "armor": (180, 140, 200),     # Violet armure
            "material": (180, 170, 120),  # Jaune matériau
        }

    def _get_category_color(self, item_type):
        """Retourne la couleur de bordure selon le type d'item."""
        return self.category_colors.get(item_type, (117, 171, 255))

    def draw_slot(self, x, y, item_stack, selected=False):
        """Dessine un emplacement d'inventaire avec style amélioré."""
        # Couleur de bordure selon la catégorie
        if item_stack:
            base_color = self._get_category_color(item_stack.item.type)
        else:
            base_color = (60, 70, 100)
        
        border_color = (255, 220, 120) if selected else base_color
        border_width = 3 if selected else 2

        # Fond du slot
        slot_surface = pygame.Surface((self.slot_size, self.slot_size), pygame.SRCALPHA)
        # Dégradé vertical subtil
        for i in range(self.slot_size):
            t = i / self.slot_size
            r = int(25 + t * 10)
            g = int(30 + t * 10)
            b = int(50 + t * 15)
            pygame.draw.line(slot_surface, (r, g, b, 210), (0, i), (self.slot_size, i))
        # Bordure
        pygame.draw.rect(slot_surface, border_color, slot_surface.get_rect(), border_width, border_radius=5)
        self.screen.blit(slot_surface, (x, y))

        if item_stack:
            # Dessiner le sprite
            sprite_drawn = False
            if self.sprite_manager:
                sprite = self.sprite_manager.get_item_sprite(item_stack.item.sprite_name)
                if sprite:
                    item_size = self.slot_size - 8
                    sprite_scaled = pygame.transform.smoothscale(sprite, (item_size, item_size))
                    self.screen.blit(sprite_scaled, (x + 4, y + 4))
                    sprite_drawn = True

            if not sprite_drawn:
                # Fallback : rectangle coloré avec icône
                color = self._get_category_color(item_stack.item.type)
                pygame.draw.rect(self.screen, color,
                               (x + 6, y + 6, self.slot_size - 12, self.slot_size - 12), border_radius=4)

            # Quantité avec fond
            if item_stack.quantity > 1:
                qty_text = self.small_font.render(str(item_stack.quantity), True, self.WHITE)
                text_rect = qty_text.get_rect()
                text_rect.bottomright = (x + self.slot_size - 2, y + self.slot_size - 1)
                bg_rect = text_rect.inflate(4, 2)
                bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(bg_surf, (0, 0, 0, 180), bg_surf.get_rect(), border_radius=2)
                self.screen.blit(bg_surf, bg_rect.topleft)
                self.screen.blit(qty_text, text_rect)
                qty_text = self.small_font.render(str(item_stack.quantity), True, self.WHITE)
                text_rect = qty_text.get_rect()
                text_rect.bottomright = (x + self.slot_size - 2, y + self.slot_size - 1)
                bg_rect = text_rect.inflate(4, 2)
                pygame.draw.rect(self.screen, (0, 0, 0, 150), bg_rect, border_radius=2)
                self.screen.blit(qty_text, text_rect)
    
    def draw_inventory_tab(self, inventory):
        """Dessine l'onglet inventaire."""
        start_x = 50
        start_y = 100
        cols = 9
        rows = 4
        
        # Stocker les positions des slots pour les clics
        self.inventory_slots_rects = []
        
        for i in range(min(inventory.size, cols * rows)):
            row = i // cols
            col = i % cols
            
            x = start_x + col * (self.slot_size + self.slot_padding)
            y = start_y + row * (self.slot_size + self.slot_padding)
            
            # Stocker le rectangle pour les clics
            slot_rect = pygame.Rect(x, y, self.slot_size, self.slot_size)
            self.inventory_slots_rects.append((i, slot_rect))
            
            selected = (i == self.selected_slot and self.current_tab == "inventory")
            self.draw_slot(x, y, inventory.slots[i], selected)
    
    def draw_crafting_tab(self, recipes, inventory):
        """Dessine l'onglet crafting."""
        start_x = 50
        start_y = 110
        self.crafting_rects = []

        for i, recipe in enumerate(recipes[:10]):
            y = start_y + i * 65
            can_craft = recipe.can_craft(inventory)
            recipe_rect = pygame.Rect(start_x, y, 450, 55)

            self.crafting_rects.append((i, recipe_rect, can_craft))
            selected = (i == self.selected_slot and self.current_tab == "crafting")

            recipe_surface = pygame.Surface((450, 55), pygame.SRCALPHA)
            if can_craft:
                bg_color = (50, 100, 80, 150) if selected else (40, 80, 60, 120)
                border_color = (100, 255, 150) if selected else (80, 200, 120)
            else:
                bg_color = (80, 40, 40, 100)
                border_color = (180, 100, 100)

            border_width = 3 if selected else 2
            pygame.draw.rect(recipe_surface, bg_color, recipe_surface.get_rect(), border_radius=6)
            pygame.draw.rect(recipe_surface, border_color, recipe_surface.get_rect(), border_width, border_radius=6)

            self.screen.blit(recipe_surface, recipe_rect)

            name_text = self.font.render(f"🔨 {recipe.name}", True, (245, 247, 255) if can_craft else (180, 100, 100))
            self.screen.blit(name_text, (start_x + 15, y + 5))

            ingredients_text = ", ".join([f"{qty}× {name[:10]}" for name, qty in recipe.ingredients.items()])
            ing_color = (200, 230, 200) if can_craft else (200, 100, 100)
            ing_text = self.small_font.render(f"Requis: {ingredients_text}", True, ing_color)
            self.screen.blit(ing_text, (start_x + 15, y + 28))
    
    def draw_equipment_tab(self, inventory):
        """Dessine l'onglet équipement."""
        start_x = 200
        start_y = 150
        
        # Stocker les positions des équipements pour les clics
        self.equipment_rects = []
        
        equipment_slots = ["weapon", "armor", "tool"]
        slot_names = ["Arme", "Armure", "Outil"]
        
        for i, (slot_name, display_name) in enumerate(zip(equipment_slots, slot_names)):
            x = start_x
            y = start_y + i * 80
            
            # Nom de l'emplacement
            name_text = self.font.render(display_name + ":", True, self.WHITE)
            self.screen.blit(name_text, (x - 100, y + 10))
            
            # Stocker le rectangle pour les clics
            slot_rect = pygame.Rect(x, y, self.slot_size, self.slot_size)
            self.equipment_rects.append((slot_name, slot_rect))
            
            # Emplacement
            selected = (i == self.selected_slot and self.current_tab == "equipment")
            self.draw_slot(x, y, inventory.equipment[slot_name], selected)
    
    def draw(self, inventory, recipes):
        """Dessine l'interface d'inventaire."""
        if not self.visible:
            return

        # Mettre à jour le timer de feedback
        if self.craft_feedback_timer > 0:
            self.craft_feedback_timer -= 1/60  # ~60fps

        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))

        title_text = "📦 Inventaire et Artisanat"
        title = self.font.render(title_text, True, (245, 247, 255))
        title_rect = title.get_rect(center=(self.screen.get_width()//2, 20))
        self.screen.blit(title, title_rect)

        # Onglets modernes
        tab_width = 140
        tab_height = 35
        tab_y = 50
        tabs = [("inventory", "📋 Inventaire"), ("crafting", "🔨 Artisanat"), ("equipment", "⚔ Équipement")]

        self.tab_rects = []

        for i, (tab_id, tab_name) in enumerate(tabs):
            x = 50 + i * (tab_width + 15)
            is_active = tab_id == self.current_tab

            tab_rect = pygame.Rect(x, tab_y, tab_width, tab_height)
            self.tab_rects.append((tab_id, tab_rect))

            tab_surface = pygame.Surface((tab_width, tab_height), pygame.SRCALPHA)
            if is_active:
                pygame.draw.rect(tab_surface, (112, 165, 255, 220), tab_surface.get_rect(), border_radius=6)
                pygame.draw.rect(tab_surface, (189, 214, 255), tab_surface.get_rect(), 2, border_radius=6)
                text_color = (255, 255, 255)
            else:
                pygame.draw.rect(tab_surface, (50, 60, 100, 150), tab_surface.get_rect(), border_radius=6)
                pygame.draw.rect(tab_surface, (100, 120, 180), tab_surface.get_rect(), 1, border_radius=6)
                text_color = (180, 190, 220)

            self.screen.blit(tab_surface, tab_rect)

            tab_text = self.small_font.render(tab_name, True, text_color)
            text_rect = tab_text.get_rect(center=(x + tab_width//2, tab_y + tab_height//2))
            self.screen.blit(tab_text, text_rect)

        if self.current_tab == "inventory":
            self.draw_inventory_tab(inventory)
        elif self.current_tab == "crafting":
            self.draw_crafting_tab(recipes, inventory)
        elif self.current_tab == "equipment":
            self.draw_equipment_tab(inventory)

        # Instructions en bas
        instructions = [
            "Clic: Sélectionner / Utiliser",
            "TAB: Onglets",
            "I: Fermer"
        ]

        info_y = self.screen.get_height() - 70
        for i, instruction in enumerate(instructions):
            inst_text = self.small_font.render(instruction, True, (140, 160, 200))
            self.screen.blit(inst_text, (20 + i * 220, info_y))

        # Craft feedback
        if self.craft_feedback_timer > 0:
            feedback_text = self.font.render(self.craft_feedback, True, (84, 214, 125))
            feedback_rect = feedback_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height() - 100))
            # Fond semi-transparent
            bg_rect = feedback_rect.inflate(20, 10)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((30, 60, 40, 200))
            self.screen.blit(bg_surface, bg_rect)
            self.screen.blit(feedback_text, feedback_rect)

        # Tooltip au survol
        self._draw_tooltip(inventory)

    def _draw_tooltip(self, inventory):
        """Dessine un tooltip si on survole un slot avec un item."""
        mouse_pos = pygame.mouse.get_pos()
        
        if self.current_tab == "inventory" and hasattr(self, 'inventory_slots_rects'):
            for slot_index, slot_rect in self.inventory_slots_rects:
                if slot_rect.collidepoint(mouse_pos) and inventory.slots[slot_index]:
                    item_stack = inventory.slots[slot_index]
                    item = item_stack.item
                    
                    # Construire le texte du tooltip
                    lines = [item.name]
                    if hasattr(item, 'description') and item.description:
                        lines.append(item.description)
                    
                    # Catégorie
                    cat_names = {
                        "resource": "Ressource",
                        "food": "Nourriture",
                        "weapon": "Arme",
                        "tool": "Outil",
                        "armor": "Armure",
                        "material": "Matériau",
                    }
                    cat = cat_names.get(item.type, item.type)
                    lines.append(f"Type: {cat}")
                    
                    # Quantité
                    if item_stack.quantity > 1:
                        lines.append(f"Quantité: {item_stack.quantity}")
                    
                    # Dessiner le tooltip
                    self._render_tooltip(mouse_pos[0] + 15, mouse_pos[1] + 15, lines, item.type)
                    break

    def _render_tooltip(self, x, y, lines, item_type="resource"):
        """Dessine un tooltip stylisé."""
        padding = 8
        line_height = 18
        width = max(self.tooltip_font.size(line)[0] for line in lines) + padding * 2
        height = len(lines) * line_height + padding * 2

        # Ajuster pour ne pas dépasser l'écran
        if x + width > self.screen.get_width():
            x = self.screen.get_width() - width - 5
        if y + height > self.screen.get_height():
            y = self.screen.get_height() - height - 5

        # Fond du tooltip
        tooltip_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(tooltip_surf, (15, 20, 35, 230), (0, 0, width, height), border_radius=6)
        
        # Bordure colorée selon la catégorie
        cat_color = self._get_category_color(item_type)
        pygame.draw.rect(tooltip_surf, cat_color, (0, 0, width, height), 1, border_radius=6)
        
        self.screen.blit(tooltip_surf, (x, y))

        # Texte
        for i, line in enumerate(lines):
            if i == 0:
                # Titre : blanc gras
                color = self.WHITE
            elif "Type:" in line:
                color = self._get_category_color(item_type)
            else:
                color = self.GRAY
            
            text_surf = self.tooltip_font.render(line, True, color)
            self.screen.blit(text_surf, (x + padding, y + padding + i * line_height))
    
    def handle_event(self, event, inventory, recipes):
        """Gère les événements de l'interface d'inventaire."""
        if not self.visible:
            return
        
        # Gestion des clics de souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                mouse_pos = pygame.mouse.get_pos()
                
                # Vérifier les clics sur les onglets
                if hasattr(self, 'tab_rects'):
                    for tab_id, tab_rect in self.tab_rects:
                        if tab_rect.collidepoint(mouse_pos):
                            self.current_tab = tab_id
                            self.selected_slot = 0
                            return
                
                # Vérifier les clics selon l'onglet actuel
                if self.current_tab == "inventory" and hasattr(self, 'inventory_slots_rects'):
                    for slot_index, slot_rect in self.inventory_slots_rects:
                        if slot_rect.collidepoint(mouse_pos):
                            self.selected_slot = slot_index
                            return
                
                elif self.current_tab == "crafting" and hasattr(self, 'crafting_rects'):
                    for recipe_index, recipe_rect, can_craft in self.crafting_rects:
                        if recipe_rect.collidepoint(mouse_pos):
                            self.selected_slot = recipe_index
                            # Crafting direct si possible
                            if can_craft and recipe_index < len(recipes):
                                recipe = recipes[recipe_index]
                                if recipe.craft(inventory):
                                    self.sound_manager.play('craft')
                                    self.craft_feedback = f"Crafté: {recipe.name}"
                                    self.craft_feedback_timer = 2.0
                                    print(f"Crafté: {recipe.name}")
                                else:
                                    self.sound_manager.play('craft_fail')
                                    print("Pas assez de ressources!")
                            return
                
                elif self.current_tab == "equipment" and hasattr(self, 'equipment_rects'):
                    for slot_name, slot_rect in self.equipment_rects:
                        if slot_rect.collidepoint(mouse_pos):
                            equipment_slots = ["weapon", "armor", "tool"]
                            if slot_name in equipment_slots:
                                self.selected_slot = equipment_slots.index(slot_name)
                            return
            
            elif event.button == 3:  # Clic droit - Manger de la nourriture
                mouse_pos = pygame.mouse.get_pos()
                if self.current_tab == "inventory" and hasattr(self, 'inventory_slots_rects'):
                    for slot_index, slot_rect in self.inventory_slots_rects:
                        if slot_rect.collidepoint(mouse_pos):
                            if inventory.slots[slot_index]:
                                item = inventory.slots[slot_index].item
                                if item.type == "food":
                                    # Retirer l'item de l'inventaire
                                    inventory.remove_item(item.name, 1)
                                    self.sound_manager.play('pickup')
                                    self.craft_feedback = f"Mangé: {item.name}"
                                    self.craft_feedback_timer = 2.0
                                    print(f"Consommé: {item.name}")
                            return
        
        # Gestion du clavier (optionnelle)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                tabs = ["inventory", "crafting", "equipment"]
                current_index = tabs.index(self.current_tab)
                self.current_tab = tabs[(current_index + 1) % len(tabs)]
                self.selected_slot = 0
            
            elif event.key == pygame.K_w:
                if self.current_tab == "inventory":
                    self.selected_slot = max(0, self.selected_slot - 9)
                elif self.current_tab == "crafting":
                    self.selected_slot = max(0, self.selected_slot - 1)
                elif self.current_tab == "equipment":
                    self.selected_slot = max(0, self.selected_slot - 1)
            
            elif event.key == pygame.K_s:
                if self.current_tab == "inventory":
                    self.selected_slot = min(inventory.size - 1, self.selected_slot + 9)
                elif self.current_tab == "crafting":
                    self.selected_slot = min(len(recipes) - 1, self.selected_slot + 1)
                elif self.current_tab == "equipment":
                    self.selected_slot = min(2, self.selected_slot + 1)
            
            elif event.key == pygame.K_a:
                if self.current_tab == "inventory":
                    self.selected_slot = max(0, self.selected_slot - 1)
            
            elif event.key == pygame.K_d:
                if self.current_tab == "inventory":
                    self.selected_slot = min(inventory.size - 1, self.selected_slot + 1)
            
            elif event.key == pygame.K_RETURN:
                if self.current_tab == "crafting" and self.selected_slot < len(recipes):
                    recipe = recipes[self.selected_slot]
                    if recipe.craft(inventory):
                        print(f"Crafté: {recipe.name}")
                    else:
                        print("Pas assez de ressources!")
    
    def toggle_visibility(self):
        """Bascule la visibilité de l'inventaire."""
        self.visible = not self.visible
        if self.visible:
            self.selected_slot = 0
