"""
Système d'items et de crafting pour le jeu MMO 2D
"""

from ui.inventory import Item, CraftingRecipe
from game.constants import COLORS

class ItemDatabase:
    """Base de données des items du jeu"""
    
    def __init__(self):
        self.items = create_items()
        self.recipes = create_recipes(self.items)
    
    def get_item(self, name):
        """Récupère un item par son nom"""
        return self.items.get(name)
    
    def get_recipe(self, item_name):
        """Récupère une recette par le nom de l'item produit"""
        for recipe in self.recipes:
            if recipe.output.name == item_name:
                return recipe
        return None
    
    def get_all_items(self):
        """Retourne tous les items"""
        return self.items
    
    def get_all_recipes(self):
        """Retourne toutes les recettes"""
        return self.recipes

def create_items():
    """Crée tous les items du jeu"""
    items = {
        # Ressources de base
        "wood": Item("Bois", "resource", "Matériau de base pour la construction", 99, COLORS["BROWN"], "wood"),
        "stone": Item("Pierre", "resource", "Matériau solide pour les constructions", 99, COLORS["GRAY"], "stone"),
        "iron_ore": Item("Minerai de fer", "resource", "Utilisé pour créer des outils", 99, COLORS["DARK_GRAY"], "iron_ore"),
        "gold_ore": Item("Minerai d'or", "resource", "Précieux minerai doré", 99, (255, 215, 0), "gold_ore"),
        "diamond_ore": Item("Minerai de diamant", "resource", "Le plus précieux des minerais", 99, (185, 242, 255), "diamond"),  # Le fichier s'appelle diamond.png
        "coal": Item("Charbon", "resource", "Combustible et matériau", 99, (36, 36, 36), "coal"),
        
        # Nourriture
        "apple": Item("Pomme", "food", "Restaure 10 points de vie", 10, COLORS["RED"], "apple"),
        "berry": Item("Baie", "food", "Restaure 5 points de vie", 20, (128, 0, 128), "berry"),
        "bread": Item("Pain", "food", "Restaure 20 points de vie", 5, (222, 184, 135), "bread"),
        "meat": Item("Viande", "food", "Restaure 15 points de vie", 8, (139, 69, 19), "meat"),
        
        # Matériaux raffinés
        "iron_ingot": Item("Lingot de fer", "material", "Fer purifié", 99, (169, 169, 169), "iron_ingot"),
        "gold_ingot": Item("Lingot d'or", "material", "Or purifié", 99, (255, 215, 0), "gold_ingot"),
        "diamond": Item("Diamant", "material", "Diamant taillé", 99, (185, 242, 255), "diamond"),
        
        # Outils
        "wooden_sword": Item("Épée en bois", "weapon", "Arme basique", 1, COLORS["BROWN"], "wooden_sword"),
        "iron_sword": Item("Épée en fer", "weapon", "Arme solide", 1, COLORS["DARK_GRAY"], "iron_sword"),
        "gold_sword": Item("Épée en or", "weapon", "Arme précieuse", 1, (255, 215, 0), "wooden_sword"),  # Pas de sprite spécifique, utiliser wooden_sword
        "diamond_sword": Item("Épée en diamant", "weapon", "L'arme ultime", 1, (185, 242, 255), "iron_sword"),  # Pas de sprite spécifique, utiliser iron_sword
        
        "wooden_pickaxe": Item("Pioche en bois", "tool", "Outil de minage basique", 1, COLORS["BROWN"], "wooden_pickaxe"),
        "iron_pickaxe": Item("Pioche en fer", "tool", "Outil de minage avancé", 1, COLORS["DARK_GRAY"], "wooden_pickaxe"),  # Pas de sprite spécifique, utiliser wooden_pickaxe
        
        # Armures
        "leather_armor": Item("Armure en cuir", "armor", "Protection basique", 1, (139, 69, 19), "leather_armor"),
        "iron_armor": Item("Armure en fer", "armor", "Protection solide", 1, COLORS["DARK_GRAY"], "iron_armor"),
    }
    return items

def create_recipes(items):
    """Crée toutes les recettes de crafting"""
    recipes = [
        # Raffinement
        CraftingRecipe("Lingot de fer", {"iron_ore": 2, "coal": 1}, items["iron_ingot"], 1),
        CraftingRecipe("Lingot d'or", {"gold_ore": 2, "coal": 1}, items["gold_ingot"], 1),
        CraftingRecipe("Diamant", {"diamond_ore": 1}, items["diamond"], 1),
        
        # Nourriture
        CraftingRecipe("Pain", {"wood": 2}, items["bread"], 1),  # Simplifié
        
        # Armes
        CraftingRecipe("Épée en bois", {"wood": 3, "stone": 1}, items["wooden_sword"], 1),
        CraftingRecipe("Épée en fer", {"iron_ingot": 2, "wood": 1}, items["iron_sword"], 1),
        CraftingRecipe("Épée en or", {"gold_ingot": 2, "wood": 1}, items["gold_sword"], 1),
        CraftingRecipe("Épée en diamant", {"diamond": 2, "wood": 1}, items["diamond_sword"], 1),
        
        # Outils
        CraftingRecipe("Pioche en bois", {"wood": 3, "stone": 2}, items["wooden_pickaxe"], 1),
        CraftingRecipe("Pioche en fer", {"iron_ingot": 3, "wood": 2}, items["iron_pickaxe"], 1),
        
        # Armures
        CraftingRecipe("Armure en cuir", {"wood": 8}, items["leather_armor"], 1),  # Simplifié
        CraftingRecipe("Armure en fer", {"iron_ingot": 8}, items["iron_armor"], 1),
    ]
    return recipes
