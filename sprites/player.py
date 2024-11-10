"""
Player Sprite Module
-----------------
Defines the player character sprite.
"""

from . import BaseSprite
from config import *
from utils.error_handler import handle_sprite_error


class Player(BaseSprite):
    """Player sprite class with movement and shooting capabilities."""

    @handle_sprite_error
    def __init__(self):
        """Initialize the player sprite."""
        super().__init__()
        self.create_surface((50, 50), PINK)
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        self.triple_shot = False
        self.triple_shot_timer = 0
        self.triple_shot_duration = TRIPLE_SHOT_DURATION

    @handle_sprite_error
    def update(self):
        """Update player position and state."""
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5

        self.rect.x += self.speed_x

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.triple_shot:
            current_time = pygame.time.get_ticks()
            if current_time - self.triple_shot_timer > self.triple_shot_duration:
                self.triple_shot = False

    @handle_sprite_error
    def activate_triple_shot(self):
        """Activate triple shot power-up."""
        self.triple_shot = True
        self.triple_shot_timer = pygame.time.get_ticks()
