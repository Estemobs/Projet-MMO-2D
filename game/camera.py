from .constants import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE

class Camera:
    def __init__(self, screen_width=800, screen_height=600):
        self.x = 0
        self.y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def update(self, player_x, player_y):
        # Centrer la caméra sur le joueur
        self.x = player_x - self.screen_width // 2
        self.y = player_y - self.screen_height // 2
        
        # Limiter la caméra aux bordures de la carte
        self.x = max(0, min(self.x, MAP_WIDTH * TILE_SIZE - self.screen_width))
        self.y = max(0, min(self.y, MAP_HEIGHT * TILE_SIZE - self.screen_height))

    def follow_player(self, player):
        """Fait suivre la caméra au joueur"""
        self.update(player.x, player.y)
    
    def update_screen_size(self, screen_width, screen_height):
        """Met à jour la taille de l'écran pour la caméra"""
        self.screen_width = screen_width
        self.screen_height = screen_height
