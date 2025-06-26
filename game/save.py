import json

# Fonctions de sauvegarde/chargement génériques

def save_game_to_file(game, filename):
    save_data = {
        "world_map": [[tile.value for tile in row] for row in game.world_map],
        "player": {
            "x": game.player.x,
            "y": game.player.y,
            "health": game.player.health,
            "inventory": [
                {"name": slot.item.name, "quantity": slot.quantity}
                for slot in game.player.inventory.slots if slot
            ]
        },
        "enemies": [
            {"x": e.x, "y": e.y, "health": e.health} for e in game.enemies
        ]
    }
    with open(filename, "w") as f:
        json.dump(save_data, f, indent=2)

def load_game_from_file(game, filename, TileType, Player, Enemy):
    with open(filename, "r") as f:
        save_data = json.load(f)
    game.world_map = [[TileType(tile) for tile in row] for row in save_data["world_map"]]
    player_data = save_data["player"]
    game.player = Player(player_data["x"], player_data["y"])
    game.player.health = player_data["health"]
    for item_data in player_data["inventory"]:
        game.player.inventory.add_item(item_data["name"], item_data["quantity"])
    game.enemies = []
    for enemy_data in save_data["enemies"]:
        enemy = Enemy(enemy_data["x"], enemy_data["y"])
        enemy.health = enemy_data["health"]
        game.enemies.append(enemy)
