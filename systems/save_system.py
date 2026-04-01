"""
Système de sauvegarde pour le jeu MMO 2D
"""

import json
import os
import time
from datetime import datetime
from game.save import GameSave

class SaveSystem:
    """Gestionnaire des sauvegardes"""
    
    def __init__(self):
        self.save_directory = "saves"
        self.ensure_save_directory()
    
    def ensure_save_directory(self):
        """S'assure que le dossier de sauvegarde existe"""
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
    
    def get_save_path(self, slot_number):
        """Retourne le chemin du fichier de sauvegarde"""
        return os.path.join(self.save_directory, f"save_slot_{slot_number}.json")
    
    def save_game(self, slot_number, player, world_map, enemies, playtime):
        """Sauvegarde une partie"""
        try:
            save_data = {
                "timestamp": datetime.now().isoformat(),
                "playtime": playtime,
                "player": {
                    "x": player.x,
                    "y": player.y,
                    "health": player.health,
                    "hunger": player.hunger,
                    "level": player.level,
                    "xp": player.xp,
                    "inventory": self._serialize_inventory(player.inventory)
                },
                "world_map": self._serialize_world_map(world_map),
                "enemies": [
                    {
                        "x": enemy.x,
                        "y": enemy.y,
                        "health": enemy.health
                    }
                    for enemy in enemies
                ]
            }
            
            save_path = self.get_save_path(slot_number)
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return False
    
    def load_game(self, slot_number):
        """Charge une partie"""
        save_path = self.get_save_path(slot_number)
        
        if not os.path.exists(save_path):
            return None
        
        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # Désérialiser les données
            save_data["world_map"] = self._deserialize_world_map(save_data["world_map"])
            save_data["player"]["inventory"] = self._deserialize_inventory(save_data["player"]["inventory"])
            
            return save_data
            
        except Exception as e:
            print(f"Erreur lors du chargement: {e}")
            return None
    
    def get_save_info(self, slot_number):
        """Récupère les informations d'une sauvegarde"""
        save_path = self.get_save_path(slot_number)
        
        if not os.path.exists(save_path):
            return None
        
        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            timestamp = datetime.fromisoformat(save_data["timestamp"])
            playtime_str = self._format_playtime(save_data["playtime"])
            
            return {
                "timestamp": timestamp.strftime("%d/%m/%Y %H:%M"),
                "playtime": playtime_str
            }
            
        except Exception as e:
            print(f"Erreur lors de la lecture des infos: {e}")
            return None
    
    def delete_save(self, slot_number):
        """Supprime une sauvegarde"""
        save_path = self.get_save_path(slot_number)
        
        if os.path.exists(save_path):
            try:
                os.remove(save_path)
                return True
            except Exception as e:
                print(f"Erreur lors de la suppression: {e}")
                return False
        
        return False
    
    def _serialize_inventory(self, inventory):
        """Sérialise un inventaire"""
        serialized_slots = []
        for slot in inventory.slots:
            if slot:
                serialized_slots.append({
                    "item_name": slot.item.name,
                    "quantity": slot.quantity
                })
            else:
                serialized_slots.append(None)
        
        serialized_equipment = {}
        for slot_name, equipment in inventory.equipment.items():
            if equipment:
                serialized_equipment[slot_name] = {
                    "item_name": equipment.item.name,
                    "quantity": equipment.quantity
                }
            else:
                serialized_equipment[slot_name] = None
        
        return {
            "slots": serialized_slots,
            "equipment": serialized_equipment
        }
    
    def _deserialize_inventory(self, inventory_data):
        """Désérialise un inventaire"""
        from ui.inventory import Inventory, ItemStack
        from core.items import ItemDatabase
        
        inventory = Inventory()
        item_db = ItemDatabase()
        
        # Restaurer les slots
        for i, slot_data in enumerate(inventory_data.get("slots", [])):
            if slot_data and i < len(inventory.slots):
                item = item_db.get_item(slot_data["item_name"])
                if item:
                    inventory.slots[i] = ItemStack(item, slot_data["quantity"])
        
        # Restaurer l'équipement
        for slot_name, equipment_data in inventory_data.get("equipment", {}).items():
            if equipment_data and slot_name in inventory.equipment:
                item = item_db.get_item(equipment_data["item_name"])
                if item:
                    inventory.equipment[slot_name] = ItemStack(item, equipment_data["quantity"])
        
        return inventory
    
    def _serialize_world_map(self, world_map):
        """Sérialise la carte du monde"""
        return [[tile.value if hasattr(tile, 'value') else int(tile) for tile in row] for row in world_map]
    
    def _deserialize_world_map(self, world_map_data):
        """Désérialise la carte du monde"""
        from game.tiletype import TileType
        return [[TileType(tile) for tile in row] for row in world_map_data]
    
    def _format_playtime(self, seconds):
        """Formate le temps de jeu en heures:minutes"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours:02d}:{minutes:02d}"
