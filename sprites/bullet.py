"""
Bullet Sprite Module
-----------------
Defines the player's bullet sprite.
"""

import math
from . import BaseSprite
from config import *
from utils.error_handler import handle_sprite_error


class Bullet(BaseSprite):
    """Player bullet sprite with directional movement."""

    @handle_sprite_error
    def __init__(self, x: int, y: int, angle: float):
        """
        Initialize the bullet.

        Args:
            x: Starting x position
            y: Starting y position
            angle: Firing angle in degrees
        """
        super().__init__()
        self.create_surface((10, 20), YELLOW)
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10
        self.angle = math.radians(angle)
        self.speed_x = -math.sin(self.angle) * self.speed
        self.speed_y = -math.cos(self.angle) * self.speed
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    @handle_sprite_error
    def update(self):
        """Update bullet position."""
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.kill()
