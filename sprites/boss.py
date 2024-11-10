"""
Boss Sprite Module
----------------
Defines the boss enemy and its bullets.
"""

import random
import pygame
from . import BaseSprite
from config import *
from utils.error_handler import handle_sprite_error


class BossBullet(BaseSprite):
    """Boss bullet sprite."""

    @handle_sprite_error
    def __init__(self, x: int, y: int):
        """
        Initialize the boss bullet.

        Args:
            x: Starting x position
            y: Starting y position
        """
        super().__init__()
        self.create_surface((15, 25), RED)
        self.rect.centerx = x
        self.rect.top = y
        self.speed_y = 7

    @handle_sprite_error
    def update(self):
        """Update bullet position."""
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Boss(BaseSprite):
    """Boss enemy sprite with shooting capability."""

    @handle_sprite_error
    def __init__(self):
        """Initialize the boss sprite."""
        super().__init__()
        self.create_surface((100, 100), RED)
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.y = -self.rect.height
        self.speed_x = 3
        self.speed_y = 1
        self.health = 15
        self.direction = random.choice([1, -1])
        self.entry_phase = True
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1200

    @handle_sprite_error
    def update(self):
        """Update boss position and state."""
        if self.entry_phase:
            self.rect.y += self.speed_y
            if self.rect.top >= 50:
                self.entry_phase = False
        else:
            self.rect.x += self.speed_x * self.direction
            if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
                self.direction *= -1
