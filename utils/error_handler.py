"""
Error Handler Module
------------------
Provides custom exceptions and error handling utilities.
"""

import logging
from typing import Callable, Any
from functools import wraps

class GameError(Exception):
    """Base exception class for game-specific errors."""
    pass

def handle_sprite_error(func: Callable) -> Callable:
    """
    Decorator for handling sprite-related errors.
    
    Args:
        func: The function to wrap with error handling.
        
    Returns:
        Callable: The wrapped function with error handling.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Sprite error in {func.__name__}: {e}")
            raise GameError(f"Sprite error: {e}")
    return wrapper

def handle_pygame_error(func: Callable) -> Callable:
    """
    Decorator for handling pygame-specific errors.
    
    Args:
        func: The function to wrap with error handling.
        
    Returns:
        Callable: The wrapped function with error handling.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Pygame error in {func.__name__}: {e}")
            return None
    return wrapper