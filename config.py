"""
Game Configuration Module
------------------------
Contains all game constants and settings.
"""

import pygame
import logging
import sys
from typing import Tuple

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='game_log.txt'
)

# Screen settings
SCREEN_WIDTH: int = 600
SCREEN_HEIGHT: int = 400
FPS: int = 60

# Colors
WHITE: Tuple[int, int, int] = (255, 255, 255)
RED: Tuple[int, int, int] = (255, 0, 0)
BLACK: Tuple[int, int, int] = (0, 0, 0)
GRAY: Tuple[int, int, int] = (169, 169, 169)
PINK: Tuple[int, int, int] = (255, 0, 255)
YELLOW: Tuple[int, int, int] = (253, 208, 23)
BLUE: Tuple[int, int, int] = (0, 191, 255)
GREEN: Tuple[int, int, int] = (0, 255, 0)
ORANGE: Tuple[int, int, int] = (255, 165, 0)

# File paths
SAVE_FILE: str = "assets/game_data.json"

# Game settings
ENEMY_SPAWN_RATE: float = 0.0004
BOSS_SPAWN_INTERVAL: int = 15
TRIPLE_SHOT_DURATION: int = 3600

try:
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Airforce")
    clock = pygame.time.Clock()

    # Initialize fonts
    font = pygame.font.SysFont("Arial", 30)
    small_font = pygame.font.SysFont("Arial", 20)
except pygame.error as e:
    logging.critical(f"Failed to initialize pygame: {e}")
    sys.exit(1)