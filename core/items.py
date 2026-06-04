"""
Items Battle Royale - Armes, Armures, Soins
"""

from ui.inventory import Item, CraftingRecipe
from game.constants import COLORS


def create_items():
    items = {
        # Armes
        "pistol": Item("Pistolet", "weapon", "15 degats, tir rapide", 1, (180, 180, 180), "wooden_sword"),
        "shotgun": Item("Shotgun", "weapon", "40 degats, portee courte", 1, (140, 100, 60), "iron_sword"),
        "rifle": Item("Fusil", "weapon", "25 degats, portee longue", 1, (80, 80, 90), "iron_sword"),
        "sniper": Item("Sniper", "weapon", "60 degats, tres longue portee", 1, (60, 60, 70), "diamond_sword"),
        "smg": Item("SMG", "weapon", "10 degats, tres rapide", 1, (100, 100, 110), "wooden_sword"),
        "katana": Item("Katana", "weapon", "35 degats, melee", 1, (200, 200, 220), "iron_sword"),
        "axe": Item("Hache", "weapon", "20 degats, melee", 1, (139, 69, 19), "wooden_sword"),

        # Armures
        "vest_1": Item("Gilet Lv1", "armor", "+20 PV max", 1, (100, 120, 80), "leather_armor"),
        "vest_2": Item("Gilet Lv2", "armor", "+40 PV max", 1, (80, 100, 120), "iron_armor"),
        "vest_3": Item("Gilet Lv3", "armor", "+60 PV max", 1, (120, 100, 140), "iron_armor"),

        # Soins
        "bandage": Item("Bandage", "heal", "Soigne 25 PV", 5, (220, 220, 220), "apple"),
        "medkit": Item("Medkit", "heal", "Soigne 75 PV", 3, (220, 50, 50), "apple"),
        "potion": Item("Potion", "heal", "Soigne 50 PV", 3, (100, 180, 255), "berry"),

        # Munitions
        "ammo": Item("Munitions", "ammo", "Pour les armes a feu", 30, (255, 200, 50), "coal"),
    }
    return items


def create_recipes(items):
    return []
