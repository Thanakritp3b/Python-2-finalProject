"""
Main Game Module
--------------
Contains the main game loop and game state management.
"""

import pygame
import random
import logging
import sys
from typing import Dict, Optional
from config import *
from utils.error_handler import GameError, handle_pygame_error
from utils.score_manager import load_scores, save_scores
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.boss import Boss, BossBullet
from sprites.bullet import Bullet
from sprites.powerup import PowerUp

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='game_log.txt'
)


class Game:
    """Main game class that manages game state and loop."""

    def __init__(self):
        """Initialize the game state."""
        try:
            # Initialize pygame if not already initialized
            if not pygame.get_init():
                pygame.init()

            self.all_sprites = pygame.sprite.Group()
            self.enemies = pygame.sprite.Group()
            self.bullets = pygame.sprite.Group()
            self.boss_bullets = pygame.sprite.Group()
            self.powerups = pygame.sprite.Group()
            self.bosses = pygame.sprite.Group()

            self.game_active = False
            self.game_over = False
            self.score = 0
            self.enemies_defeated = 0
            self.boss_active = False
            self.scores = {}
            self.player_name = ""
            self.player = None

        except Exception as e:
            logging.critical(f"Failed to initialize game: {e}")
            pygame.quit()
            sys.exit(1)

    def get_player_name(self) -> bool:
        """Get player name and load scores."""
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            try:
                print(
                    "\n=== Once upon a time, I woke up on a jet plane to find that the world had fallen apart Game ===")
                self.player_name = input(
                    "Enter your name (1-20 characters): ").strip()

                if len(self.player_name) == 0:
                    print("Name cannot be empty. Please try again.")
                    attempts += 1
                    continue

                if len(self.player_name) > 20:
                    print("Name is too long (max 20 characters). Please try again.")
                    attempts += 1
                    continue

                # Load scores after valid name input
                try:
                    self.scores = load_scores()  # This now loads from text file
                    if self.player_name not in self.scores:
                        self.scores[self.player_name] = 0
                    return True
                except Exception as e:
                    logging.error(f"Error loading scores: {e}")
                    self.scores = {self.player_name: 0}
                    return True

            except (EOFError, KeyboardInterrupt):
                print("\nGame cancelled by user.")
                return False
            except Exception as e:
                logging.error(f"Error getting player name: {e}")
                attempts += 1

        print("Too many invalid attempts. Exiting game.")
        return False

    @handle_pygame_error
    def spawn_enemy(self) -> None:
        """Spawn a new enemy."""
        try:
            enemy = Enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
        except GameError as e:
            logging.error(f"Failed to spawn enemy: {e}")

    @handle_pygame_error
    def spawn_boss(self) -> None:
        """Spawn a boss enemy."""
        try:
            boss = Boss()
            self.all_sprites.add(boss)
            self.bosses.add(boss)
            self.boss_active = True
        except GameError as e:
            logging.error(f"Failed to spawn boss: {e}")

    @handle_pygame_error
    def handle_boss_shooting(self) -> None:
        """Handle boss shooting mechanics."""
        if self.boss_active:
            try:
                for boss in self.bosses:
                    if not boss.entry_phase and pygame.time.get_ticks() - boss.last_shot > boss.shoot_delay:
                        for offset in [-30, 0, 30]:
                            bullet = BossBullet(
                                boss.rect.centerx + offset, boss.rect.bottom)
                            self.all_sprites.add(bullet)
                            self.boss_bullets.add(bullet)
                        boss.last_shot = pygame.time.get_ticks()
            except GameError as e:
                logging.error(f"Error in boss shooting: {e}")

    @handle_pygame_error
    def handle_collisions(self) -> None:
        """Handle all game collisions."""
        try:
            # Player hit by boss bullets
            if pygame.sprite.spritecollide(self.player, self.boss_bullets, True):
                self.game_active = False
                self.game_over = True
                return

            # Bullet hits enemy
            hits = pygame.sprite.groupcollide(
                self.bullets, self.enemies, True, True)
            for hit in hits:
                self.score += 10
                self.enemies_defeated += 1

                if self.enemies_defeated % BOSS_SPAWN_INTERVAL == 0:
                    self.spawn_boss()
                elif not self.boss_active:
                    self.spawn_enemy()

            # Bullet hits boss
            boss_hits = pygame.sprite.groupcollide(
                self.bullets, self.bosses, True, False)
            for bullet, boss_list in boss_hits.items():
                for boss in boss_list:
                    boss.health -= 1
                    if boss.health <= 0:
                        boss.kill()
                        self.boss_active = False
                        self.score += 100
                        for _ in range(2):
                            self.spawn_enemy()

            # Player collects power-up
            powerup_hits = pygame.sprite.spritecollide(
                self.player, self.powerups, True)
            for powerup in powerup_hits:
                self.player.activate_triple_shot()

            # Enemy reaches bottom
            for enemy in self.enemies:
                if enemy.rect.top > SCREEN_HEIGHT:
                    self.game_active = False
                    self.game_over = True
                    break

        except Exception as e:
            logging.error(f"Error in collision handling: {e}")

    @handle_pygame_error
    def draw(self) -> None:
        """Draw the game screen."""
        try:
            screen.fill(BLACK)

            if not self.game_active:
                if self.game_over:
                    self.draw_game_over()
                else:
                    self.draw_start_screen()
            else:
                self.all_sprites.draw(screen)
                self.draw_hud()

            pygame.display.flip()
        except Exception as e:
            logging.error(f"Error drawing screen: {e}")

    @handle_pygame_error
    def draw_start_screen(self) -> None:
        """Draw the game start screen."""
        try:
            screen.fill(BLACK)
            title_text = font.render("Good luck", True, WHITE)
            player_text = font.render(
                f"Welcome, {self.player_name}!", True, GREEN)
            start_text = font.render("Press SPACE to Start", True, WHITE)

            screen.blit(title_text, (SCREEN_WIDTH//2 -
                        title_text.get_width()//2, SCREEN_HEIGHT//3))
            screen.blit(player_text, (SCREEN_WIDTH//2 -
                        player_text.get_width()//2, SCREEN_HEIGHT//2))
            screen.blit(start_text, (SCREEN_WIDTH//2 -
                        start_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
        except Exception as e:
            logging.error(f"Error drawing start screen: {e}")

    @handle_pygame_error
    def draw_game_over(self) -> None:
        """Draw the game over screen."""
        try:
            screen.fill(BLACK)
            y_position = 80

            game_over_text = font.render("Game Over", True, RED)
            player_text = font.render(
                f"Player: {self.player_name}", True, GREEN)
            score_text = font.render(f"Score: {self.score}", True, WHITE)
            high_score_text = font.render(
                f"High Score: {self.scores[self.player_name]}", True, YELLOW)
            restart_text = font.render(
                "Press SPACE to Play Again", True, WHITE)
            quit_text = small_font.render("Press Q to Quit", True, WHITE)

            screen.blit(game_over_text, (SCREEN_WIDTH//2 -
                        game_over_text.get_width()//2, y_position))
            screen.blit(player_text, (SCREEN_WIDTH//2 -
                        player_text.get_width()//2, y_position + 50))
            screen.blit(score_text, (SCREEN_WIDTH//2 -
                        score_text.get_width()//2, y_position + 100))
            screen.blit(high_score_text, (SCREEN_WIDTH//2 -
                        high_score_text.get_width()//2, y_position + 150))
            screen.blit(restart_text, (SCREEN_WIDTH//2 -
                        restart_text.get_width()//2, y_position + 200))
            screen.blit(quit_text, (SCREEN_WIDTH//2 -
                        quit_text.get_width()//2, y_position + 230))
        except Exception as e:
            logging.error(f"Error drawing game over screen: {e}")

    @handle_pygame_error
    def draw_hud(self) -> None:
        """Draw the heads-up display."""
        try:
            score_text = font.render(f"Score: {self.score}", True, WHITE)
            high_score_text = small_font.render(
                f"High Score: {self.scores[self.player_name]}", True, YELLOW)
            player_text = small_font.render(
                f"Player: {self.player_name}", True, GREEN)

            screen.blit(score_text, (10, 10))
            screen.blit(high_score_text, (10, 40))
            screen.blit(player_text, (10, 70))

            if self.boss_active:
                for boss in self.bosses:
                    health_text = font.render(
                        f"Boss HP: {boss.health}", True, RED)
                    screen.blit(health_text, (SCREEN_WIDTH - 200, 10))
        except Exception as e:
            logging.error(f"Error drawing HUD: {e}")

    @handle_pygame_error
    def handle_keypress(self, event: pygame.event.Event) -> None:
        """Handle keyboard input."""
        try:
            if event.key == pygame.K_q:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.key == pygame.K_SPACE:
                if self.game_active:
                    self.shoot()
                else:
                    self.reset_game()
        except Exception as e:
            logging.error(f"Error handling keypress: {e}")

    @handle_pygame_error
    def shoot(self) -> None:
        """Handle player shooting."""
        try:
            if self.player.triple_shot:
                for angle in [-30, 0, 30]:
                    bullet = Bullet(self.player.rect.centerx,
                                    self.player.rect.top, angle)
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)
            else:
                bullet = Bullet(self.player.rect.centerx,
                                self.player.rect.top, 0)
                self.all_sprites.add(bullet)
                self.bullets.add(bullet)
        except GameError as e:
            logging.error(f"Error shooting: {e}")

    @handle_pygame_error
    def update(self) -> None:
        """Update game state."""
        try:
            # Spawn power-ups
            if random.random() < ENEMY_SPAWN_RATE:
                try:
                    powerup = PowerUp()
                    self.all_sprites.add(powerup)
                    self.powerups.add(powerup)
                except GameError as e:
                    logging.error(f"Failed to spawn power-up: {e}")

            self.all_sprites.update()
            self.handle_boss_shooting()
            self.handle_collisions()

            # Update high score
            if self.score > self.scores.get(self.player_name, 0):
                self.scores[self.player_name] = self.score
                # Save immediately when high score is broken
                save_scores(self.scores)

        except Exception as e:
            logging.error(f"Error updating game state: {e}")

    @handle_pygame_error
    def reset_game(self) -> None:
        """Reset the game state."""
        try:
            self.game_active = True
            self.game_over = False
            self.score = 0
            self.enemies_defeated = 0
            self.boss_active = False

            self.all_sprites.empty()
            self.enemies.empty()
            self.bullets.empty()
            self.boss_bullets.empty()
            self.powerups.empty()
            self.bosses.empty()

            self.player = Player()
            self.all_sprites.add(self.player)

            for _ in range(2):
                self.spawn_enemy()

        except GameError as e:
            logging.error(f"Failed to reset game: {e}")
            self.game_active = False
            self.game_over = True

    def run(self):
        """Main game loop."""
        try:
            # Get player name first
            if not self.get_player_name():
                pygame.quit()
                return

            # Initialize player and enemies
            try:
                self.player = Player()
                self.all_sprites.add(self.player)

                for _ in range(2):
                    enemy = Enemy()
                    self.all_sprites.add(enemy)
                    self.enemies.add(enemy)
            except GameError as e:
                logging.error(f"Failed to initialize sprites: {e}")
                return

            # Main game loop
            running = True
            while running:
                try:
                    clock.tick(FPS)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN:
                            self.handle_keypress(event)

                    if self.game_active:
                        self.update()

                    self.draw()

                except Exception as e:
                    logging.error(f"Error in game loop: {e}")
                    continue

        except Exception as e:
            logging.critical(f"Critical game error: {e}")
        finally:
            try:
                save_scores(self.scores)  # Final save before quitting
            except Exception as e:
                logging.error(f"Error saving scores: {e}")
            pygame.quit()


if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        logging.critical(f"Fatal error: {e}")
        pygame.quit()
        sys.exit(1)
