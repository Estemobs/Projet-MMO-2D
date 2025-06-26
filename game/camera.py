from .constants import WINDOW_WIDTH, WINDOW_HEIGHT, MAP_WIDTH, MAP_HEIGHT, TILE_SIZE

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def update(self, player_x, player_y):
        # Centrer la caméra sur le joueur
        self.x = player_x - WINDOW_WIDTH // 2
        self.y = player_y - WINDOW_HEIGHT // 2
        
        # Limiter la caméra aux bordures de la carte
        self.x = max(0, min(self.x, MAP_WIDTH * TILE_SIZE - WINDOW_WIDTH))
        self.y = max(0, min(self.y, MAP_HEIGHT * TILE_SIZE - WINDOW_HEIGHT))
