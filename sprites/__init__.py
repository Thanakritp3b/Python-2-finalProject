"""
Base Sprite Module
----------------
Provides base sprite class with error handling.
"""

import pygame
from utils.error_handler import handle_sprite_error
from typing import Tuple


class BaseSprite(pygame.sprite.Sprite):
    """Base class for all game sprites with error handling."""

    @handle_sprite_error
    def __init__(self):
        """Initialize the base sprite."""
        super().__init__()

    @handle_sprite_error
    def create_surface(self, size: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """
        Create a surface for the sprite.

        Args:
            size: Tuple of width and height.
            color: Tuple of RGB values.
        """
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
