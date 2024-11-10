"""
Enemy Sprite Module
-----------------
Defines the basic enemy sprite.
"""

import random
from . import BaseSprite
from config import *
from utils.error_handler import handle_sprite_error


class Enemy(BaseSprite):
    """Basic enemy sprite that moves downward."""

    @handle_sprite_error
    def __init__(self):
        """Initialize the enemy sprite."""
        super().__init__()
        self.create_surface((50, 50), GRAY)
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 2)

    @handle_sprite_error
    def update(self):
        """Update enemy position."""
        self.rect.y += self.speed_y
