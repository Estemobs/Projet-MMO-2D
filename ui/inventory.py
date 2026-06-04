"""
Inventaire et équipement - Style survivor moderne
"""

import pygame
from game.sound_manager import get_sound_manager
from game.constants import s


class Item:
    def __init__(self, name, item_type, description, stack_size=99, color=(255, 255, 255), sprite_name=None):
        self.name = name
        self.type = item_type
        self.description = description
        self.stack_size = stack_size
        self.color = color
        self.sprite_name = sprite_name if sprite_name else name.lower().replace(" ", "_")


class ItemStack:
    def __init__(self, item, quantity=1):
        self.item = item
        self.quantity = quantity

    def can_stack_with(self, other_stack):
        return self.item.name == other_stack.item.name

    def add(self, quantity):
        max_add = self.item.stack_size - self.quantity
        actual_add = min(quantity, max_add)
        self.quantity += actual_add
        return quantity - actual_add


class Inventory:
    def __init__(self, size=24):
        self.size = size
        self.slots = [None] * size
        self.equipment = {"weapon": None, "armor": None, "tool": None}

    def add_item(self, item, quantity=1):
        remaining = quantity
        for slot in self.slots:
            if slot and slot.can_stack_with(ItemStack(item)):
                remaining = slot.add(remaining)
                if remaining == 0:
                    return 0
        for i, slot in enumerate(self.slots):
            if slot is None and remaining > 0:
                take = min(remaining, item.stack_size)
                self.slots[i] = ItemStack(item, take)
                remaining -= take
        return remaining

    def remove_item(self, item_name, quantity=1):
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
        total = 0
        for slot in self.slots:
            if slot and slot.item.name == item_name:
                total += slot.quantity
        return total >= quantity

    def get_item_count(self, item_name):
        total = 0
        for slot in self.slots:
            if slot and slot.item.name == item_name:
                total += slot.quantity
        return total


class CraftingRecipe:
    def __init__(self, name, ingredients, result_item, result_quantity=1, description=""):
        self.name = name
        self.ingredients = ingredients
        self.result_item = result_item
        self.result_quantity = result_quantity
        self.description = description

    def can_craft(self, inventory):
        for item_name, needed_quantity in self.ingredients.items():
            if not inventory.has_item(item_name, needed_quantity):
                return False
        return True

    def craft(self, inventory):
        if not self.can_craft(inventory):
            return False
        for item_name, needed_quantity in self.ingredients.items():
            inventory.remove_item(item_name, needed_quantity)
        inventory.add_item(self.result_item, self.result_quantity)
        return True


class InventoryUI:
    def __init__(self, screen, font, sprite_manager=None):
        self.screen = screen
        self.font = font
        self.tooltip_font = pygame.font.Font(None, max(14, int(screen.get_height() * 0.02)))
        self.sprite_manager = sprite_manager

        self.WHITE = (240, 242, 250)
        self.BLACK = (0, 0, 0)
        self.GRAY = (120, 130, 155)
        self.DARK_BG = (14, 18, 30)
        self.GREEN = (80, 210, 120)
        self.BLUE = (90, 140, 255)
        self.RED = (240, 85, 85)
        self.ORANGE = (255, 165, 0)
        self.PURPLE = (200, 120, 255)
        self.YELLOW = (255, 215, 110)
        self.ACCENT = (100, 150, 255)

        self.visible = False
        self.selected_slot = 0
        self.current_tab = "inventory"

        self.sound_manager = get_sound_manager()
        self.feedback_text = ""
        self.feedback_timer = 0.0

        self.category_colors = {
            "resource": (84, 180, 120),
            "food": (220, 140, 60),
            "weapon": (220, 80, 80),
            "tool": (140, 160, 200),
            "armor": (180, 140, 200),
        }

    def toggle_visibility(self):
        self.visible = not self.visible
        if self.visible:
            self.selected_slot = 0

    def _slot_size(self):
        return s(48)

    def _cat_color(self, item_type):
        return self.category_colors.get(item_type, (100, 120, 160))

    def _draw_slot(self, x, y, item_stack, selected=False):
        sz = self._slot_size()
        bg = pygame.Surface((sz, sz), pygame.SRCALPHA)

        if selected:
            pulse = int(abs(pygame.time.get_ticks() / 300 % 6.28) * 8) + 60
            glow = pygame.Surface((sz + 8, sz + 8), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*self.ACCENT, pulse), (0, 0, sz + 8, sz + 8), border_radius=8)
            self.screen.blit(glow, (x - 4, y - 4))

        for i in range(sz):
            t = i / max(1, sz)
            r, g, b = int(22 + t * 6), int(26 + t * 6), int(40 + t * 8)
            pygame.draw.line(bg, (r, g, b, 220), (0, i), (sz, i))

        bc = self.ACCENT if selected else (50, 58, 80)
        pygame.draw.rect(bg, (*bc, 200), (0, 0, sz, sz), 2, border_radius=6)
        self.screen.blit(bg, (x, y))

        if item_stack:
            drawn = False
            if self.sprite_manager:
                sprite = self.sprite_manager.get_item_sprite(item_stack.item.sprite_name)
                if sprite:
                    isz = sz - s(10)
                    scaled = pygame.transform.smoothscale(sprite, (isz, isz))
                    self.screen.blit(scaled, (x + s(5), y + s(5)))
                    drawn = True
            if not drawn:
                cc = self._cat_color(item_stack.item.type)
                pygame.draw.rect(self.screen, cc, (x + s(8), y + s(8), sz - s(16), sz - s(16)), border_radius=4)

            if item_stack.quantity > 1:
                sf = pygame.font.Font(None, s(16))
                qt = sf.render(str(item_stack.quantity), True, self.WHITE)
                qr = qt.get_rect(bottomright=(x + sz - 2, y + sz - 1))
                bg2 = pygame.Surface((qr.width + 4, qr.height + 2), pygame.SRCALPHA)
                pygame.draw.rect(bg2, (0, 0, 0, 180), bg2.get_rect(), border_radius=2)
                self.screen.blit(bg2, (qr.x - 2, qr.y - 1))
                self.screen.blit(qt, qr)

    def draw(self, inventory, recipes):
        if not self.visible:
            return

        w, h = self.screen.get_size()

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        pw = int(w * 0.45)
        ph = int(h * 0.65)
        px = (w - pw) // 2
        py = (h - ph) // 2

        panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        for i in range(ph):
            t = i / max(1, ph)
            r, g, b = int(14 + t * 4), int(18 + t * 4), int(28 + t * 6)
            pygame.draw.line(panel, (r, g, b, 230), (0, i), (pw, i))
        pygame.draw.rect(panel, (*self.ACCENT, 120), (0, 0, pw, ph), 1, border_radius=12)
        self.screen.blit(panel, (px, py))

        title_font = pygame.font.Font(None, max(20, int(h * 0.03)))
        title = title_font.render("Inventaire", True, self.WHITE)
        self.screen.blit(title, title.get_rect(center=(px + pw // 2, py + 20)))

        tabs = [("inventory", "Items"), ("equipment", "Equipement")]
        tab_w = int(pw * 0.2)
        tab_h = s(28)
        tab_y = py + 40
        self.tab_rects = []

        for i, (tid, tname) in enumerate(tabs):
            tx = px + int(pw * 0.15) + i * (tab_w + s(10))
            is_active = tid == self.current_tab
            tr = pygame.Rect(tx, tab_y, tab_w, tab_h)
            self.tab_rects.append((tid, tr))

            ts = pygame.Surface((tab_w, tab_h), pygame.SRCALPHA)
            if is_active:
                pygame.draw.rect(ts, (*self.ACCENT, 200), (0, 0, tab_w, tab_h), border_radius=6)
            else:
                pygame.draw.rect(ts, (40, 48, 70, 150), (0, 0, tab_w, tab_h), border_radius=6)
                pygame.draw.rect(ts, (60, 70, 100, 100), (0, 0, tab_w, tab_h), 1, border_radius=6)
            self.screen.blit(ts, (tx, tab_y))

            tf = pygame.font.Font(None, s(16))
            tt = tf.render(tname, True, (255, 255, 255) if is_active else (140, 150, 175))
            self.screen.blit(tt, tt.get_rect(center=(tx + tab_w // 2, tab_y + tab_h // 2)))

        if self.current_tab == "inventory":
            self._draw_inventory_tab(inventory, px, py, pw, ph)
        elif self.current_tab == "equipment":
            self._draw_equipment_tab(inventory, px, py, pw, ph)

        inst = pygame.font.Font(None, s(14))
        self.screen.blit(inst.render("I: Fermer  |  Clic droit: Utiliser", True, (90, 100, 130)), (px + 10, py + ph - 20))

        if self.feedback_timer > 0:
            self.feedback_timer -= 1 / 60
            ff = pygame.font.Font(None, s(20))
            ft = ff.render(self.feedback_text, True, self.GREEN)
            self.screen.blit(ft, ft.get_rect(center=(w // 2, py + ph + 20)))

        self._draw_tooltip(inventory)

    def _draw_inventory_tab(self, inventory, px, py, pw, ph):
        cols = 6
        sz = self._slot_size()
        pad = s(6)
        start_x = px + (pw - cols * (sz + pad)) // 2
        start_y = py + 80
        self.inventory_rects = []

        for i in range(min(inventory.size, cols * 4)):
            row = i // cols
            col = i % cols
            x = start_x + col * (sz + pad)
            y = start_y + row * (sz + pad)
            self.inventory_rects.append((i, pygame.Rect(x, y, sz, sz)))
            self._draw_slot(x, y, inventory.slots[i], i == self.selected_slot and self.current_tab == "inventory")

    def _draw_equipment_tab(self, inventory, px, py, pw, ph):
        cx = px + pw // 2
        sz = self._slot_size()
        self.equipment_rects = []

        eq = [("weapon", "Arme"), ("armor", "Armure"), ("tool", "Outil")]
        for i, (slot_name, label) in enumerate(eq):
            y = py + 90 + i * (sz + s(20))

            lf = pygame.font.Font(None, s(18))
            lt = lf.render(label, True, self.GRAY)
            self.screen.blit(lt, lt.get_rect(center=(cx - sz - s(30), y + sz // 2)))

            sx = cx - sz // 2
            self.equipment_rects.append((slot_name, pygame.Rect(sx, y, sz, sz)))
            self._draw_slot(sx, y, inventory.equipment.get(slot_name), False)

            equipped = inventory.equipment.get(slot_name)
            if equipped:
                nf = pygame.font.Font(None, s(16))
                nt = nf.render(equipped.item.name, True, self.WHITE)
                self.screen.blit(nt, (cx + sz // 2 + s(10), y + sz // 2 - 8))
            else:
                nf = pygame.font.Font(None, s(14))
                nt = nf.render("Vide", True, (80, 90, 115))
                self.screen.blit(nt, (cx + sz // 2 + s(10), y + sz // 2 - 6))

    def _draw_tooltip(self, inventory):
        mouse_pos = pygame.mouse.get_pos()

        if self.current_tab == "inventory" and hasattr(self, 'inventory_rects'):
            for idx, rect in self.inventory_rects:
                if rect.collidepoint(mouse_pos) and inventory.slots[idx]:
                    item = inventory.slots[idx].item
                    lines = [item.name]
                    if item.description:
                        lines.append(item.description)
                    cat_names = {"resource": "Ressource", "food": "Nourriture", "weapon": "Arme", "tool": "Outil", "armor": "Armure"}
                    lines.append(cat_names.get(item.type, item.type))
                    if inventory.slots[idx].quantity > 1:
                        lines.append(f"x{inventory.slots[idx].quantity}")
                    self._render_tooltip(mouse_pos[0] + 15, mouse_pos[1] + 15, lines, item.type)
                    break

    def _render_tooltip(self, x, y, lines, item_type="resource"):
        pad = 8
        lh = 18
        w = max(self.tooltip_font.size(line)[0] for line in lines) + pad * 2
        h = len(lines) * lh + pad * 2

        sw, sh = self.screen.get_size()
        if x + w > sw:
            x = sw - w - 5
        if y + h > sh:
            y = sh - h - 5

        ts = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(ts, (12, 16, 28, 230), (0, 0, w, h), border_radius=6)
        cc = self._cat_color(item_type)
        pygame.draw.rect(ts, (*cc, 150), (0, 0, w, h), 1, border_radius=6)
        self.screen.blit(ts, (x, y))

        for i, line in enumerate(lines):
            color = self.WHITE if i == 0 else (cc if i == 1 and line in ["Ressource", "Nourriture", "Arme", "Outil", "Armure"] else self.GRAY)
            st = self.tooltip_font.render(line, True, color)
            self.screen.blit(st, (x + pad, y + pad + i * lh))

    def handle_event(self, event, inventory, recipes):
        if not self.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if hasattr(self, 'tab_rects'):
                for tid, tr in self.tab_rects:
                    if tr.collidepoint((mx, my)):
                        self.current_tab = tid
                        self.selected_slot = 0
                        return

            if self.current_tab == "inventory" and hasattr(self, 'inventory_rects'):
                for idx, rect in self.inventory_rects:
                    if rect.collidepoint((mx, my)):
                        self.selected_slot = idx
                        if event.button == 3 and inventory.slots[idx]:
                            item = inventory.slots[idx].item
                            if item.type == "food":
                                inventory.remove_item(item.name, 1)
                                self.sound_manager.play('pickup')
                                self.feedback_text = f"+{item.name}"
                                self.feedback_timer = 1.5
                        return

            if self.current_tab == "equipment" and hasattr(self, 'equipment_rects'):
                for slot_name, rect in self.equipment_rects:
                    if rect.collidepoint((mx, my)):
                        if event.button == 1:
                            self._try_equip(inventory, slot_name)
                        return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                tabs = ["inventory", "equipment"]
                ci = tabs.index(self.current_tab)
                self.current_tab = tabs[(ci + 1) % len(tabs)]
                self.selected_slot = 0
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected_slot = max(0, self.selected_slot - 6)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_slot = min(inventory.size - 1, self.selected_slot + 6)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.selected_slot = max(0, self.selected_slot - 1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.selected_slot = min(inventory.size - 1, self.selected_slot + 1)

    def _try_equip(self, inventory, slot_name):
        if self.selected_slot < inventory.size and inventory.slots[self.selected_slot]:
            item = inventory.slots[self.selected_slot].item
            equip_map = {"weapon": ["weapon"], "armor": ["armor"], "tool": ["tool"]}
            if item.type in equip_map.get(slot_name, []):
                old = inventory.equipment.get(slot_name)
                inventory.equipment[slot_name] = inventory.slots[self.selected_slot]
                inventory.slots[self.selected_slot] = old
                self.sound_manager.play('equip')
                self.feedback_text = f"Equipe: {item.name}"
                self.feedback_timer = 1.5
