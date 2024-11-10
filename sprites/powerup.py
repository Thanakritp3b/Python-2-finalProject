"""
Power-up Sprite Module
-------------------
Defines the power-up sprite.
"""

import random
from . import BaseSprite
from config import *
from utils.error_handler import handle_sprite_error


class PowerUp(BaseSprite):
    """Power-up sprite that grants triple shot capability."""

    @handle_sprite_error
    def __init__(self):
        """Initialize the power-up sprite."""
        super().__init__()
        self.create_surface((30, 30), BLUE)
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = 2

    @handle_sprite_error
    def update(self):
        """Update power-up position."""
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
