"""
Score Manager Module
------------------
Handles loading and saving of game scores using a simple text file.
"""

import os
import logging
from typing import Dict

SAVE_FILE = "game_scores.txt"

def load_scores() -> Dict[str, int]:
    """
    Load scores from the text file.
    
    Returns:
        Dict[str, int]: Dictionary of player names and their high scores.
    """
    scores = {}
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    try:
                        name, score = line.strip().split(':')
                        scores[name] = int(score)
                    except ValueError:
                        continue
    except Exception as e:
        logging.error(f"Error loading scores: {e}")
    return scores

def save_scores(scores: Dict[str, int]) -> None:
    """
    Save scores to the text file.
    
    Args:
        scores: Dictionary of player names and their high scores.
    """
    try:
        with open(SAVE_FILE, 'w') as f:
            for name, score in scores.items():
                f.write(f"{name}:{score}\n")
    except Exception as e:
        logging.error(f"Error saving scores: {e}")