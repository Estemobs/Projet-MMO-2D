"""
Module core du jeu MMO 2D
"""

from .game_manager import GameManager
from .items import create_items, create_recipes

__all__ = ['GameManager', 'create_items', 'create_recipes']
