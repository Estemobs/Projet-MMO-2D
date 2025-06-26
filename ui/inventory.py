import pygame
import json

class Item:
    def __init__(self, name, item_type, description, stack_size=99, color=(255, 255, 255)):
        self.name = name
        self.type = item_type  # "resource", "tool", "food", "weapon"
        self.description = description
        self.stack_size = stack_size
        self.color = color

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
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.small_font = pygame.font.Font(None, 16)
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.DARK_GRAY = (64, 64, 64)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 100, 255)
        self.BROWN = (139, 69, 19)
        
        self.slot_size = 40
        self.slot_padding = 5
        self.visible = False
        self.selected_slot = 0
        
        # Modes d'affichage
        self.current_tab = "inventory"  # "inventory", "crafting", "equipment"
    
    def draw_slot(self, x, y, item_stack, selected=False):
        """Dessine un emplacement d'inventaire."""
        # Fond de l'emplacement
        color = self.BLUE if selected else self.GRAY
        pygame.draw.rect(self.screen, color, (x, y, self.slot_size, self.slot_size))
        pygame.draw.rect(self.screen, self.WHITE, (x, y, self.slot_size, self.slot_size), 2)
        
        if item_stack:
            # Couleur de l'item
            item_color = item_stack.item.color
            pygame.draw.rect(self.screen, item_color, 
                           (x + 5, y + 5, self.slot_size - 10, self.slot_size - 10))
            
            # Quantité
            if item_stack.quantity > 1:
                qty_text = self.small_font.render(str(item_stack.quantity), True, self.WHITE)
                self.screen.blit(qty_text, (x + self.slot_size - 15, y + self.slot_size - 15))
    
    def draw_inventory_tab(self, inventory):
        """Dessine l'onglet inventaire."""
        start_x = 50
        start_y = 100
        cols = 9
        rows = 4
        
        for i in range(min(inventory.size, cols * rows)):
            row = i // cols
            col = i % cols
            
            x = start_x + col * (self.slot_size + self.slot_padding)
            y = start_y + row * (self.slot_size + self.slot_padding)
            
            selected = (i == self.selected_slot and self.current_tab == "inventory")
            self.draw_slot(x, y, inventory.slots[i], selected)
    
    def draw_crafting_tab(self, recipes, inventory):
        """Dessine l'onglet crafting."""
        start_x = 50
        start_y = 100
        
        # Liste des recettes
        for i, recipe in enumerate(recipes[:10]):  # Limiter à 10 recettes visibles
            y = start_y + i * 60
            
            # Fond de la recette
            can_craft = recipe.can_craft(inventory)
            color = self.GREEN if can_craft else self.DARK_GRAY
            pygame.draw.rect(self.screen, color, (start_x, y, 400, 50))
            pygame.draw.rect(self.screen, self.WHITE, (start_x, y, 400, 50), 2)
            
            # Nom de la recette
            name_text = self.font.render(recipe.name, True, self.WHITE)
            self.screen.blit(name_text, (start_x + 10, y + 5))
            
            # Ingrédients
            ingredients_text = ", ".join([f"{qty} {name}" for name, qty in recipe.ingredients.items()])
            ing_text = self.small_font.render(f"Requis: {ingredients_text}", True, self.WHITE)
            self.screen.blit(ing_text, (start_x + 10, y + 25))
    
    def draw_equipment_tab(self, inventory):
        """Dessine l'onglet équipement."""
        start_x = 200
        start_y = 150
        
        equipment_slots = ["weapon", "armor", "tool"]
        slot_names = ["Arme", "Armure", "Outil"]
        
        for i, (slot_name, display_name) in enumerate(zip(equipment_slots, slot_names)):
            x = start_x
            y = start_y + i * 80
            
            # Nom de l'emplacement
            name_text = self.font.render(display_name + ":", True, self.WHITE)
            self.screen.blit(name_text, (x - 100, y + 10))
            
            # Emplacement
            selected = (slot_name == equipment_slots[self.selected_slot] and self.current_tab == "equipment")
            self.draw_slot(x, y, inventory.equipment[slot_name], selected)
    
    def draw(self, inventory, recipes):
        """Dessine l'interface d'inventaire."""
        if not self.visible:
            return
        
        # Fond semi-transparent
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(180)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Titre
        title_text = "Inventaire et Artisanat"
        title = self.font.render(title_text, True, self.WHITE)
        title_rect = title.get_rect(center=(self.screen.get_width()//2, 30))
        self.screen.blit(title, title_rect)
        
        # Onglets
        tab_width = 120
        tab_height = 30
        tab_y = 60
        tabs = [("inventory", "Inventaire"), ("crafting", "Artisanat"), ("equipment", "Équipement")]
        
        for i, (tab_id, tab_name) in enumerate(tabs):
            x = 50 + i * (tab_width + 10)
            color = self.BLUE if tab_id == self.current_tab else self.GRAY
            
            pygame.draw.rect(self.screen, color, (x, tab_y, tab_width, tab_height))
            pygame.draw.rect(self.screen, self.WHITE, (x, tab_y, tab_width, tab_height), 2)
            
            tab_text = self.small_font.render(tab_name, True, self.WHITE)
            text_rect = tab_text.get_rect(center=(x + tab_width//2, tab_y + tab_height//2))
            self.screen.blit(tab_text, text_rect)
        
        # Contenu de l'onglet
        if self.current_tab == "inventory":
            self.draw_inventory_tab(inventory)
        elif self.current_tab == "crafting":
            self.draw_crafting_tab(recipes, inventory)
        elif self.current_tab == "equipment":
            self.draw_equipment_tab(inventory)
        
        # Instructions
        instructions = [
            "TAB: Changer d'onglet",
            "WASD: Naviguer",
            "ENTER: Utiliser/Équiper",
            "I: Fermer inventaire"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.small_font.render(instruction, True, self.WHITE)
            self.screen.blit(inst_text, (self.screen.get_width() - 200, 100 + i * 20))
    
    def handle_event(self, event, inventory, recipes):
        """Gère les événements de l'interface d'inventaire."""
        if not self.visible:
            return
        
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
