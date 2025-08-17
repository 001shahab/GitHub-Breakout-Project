"""
Main game logic for GitHub Contribution Breakout
"""

import pygame
import math
from config import Config
from utils.colors import Colors
from utils.effects import Effects

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = Config.PADDLE_WIDTH
        self.height = Config.PADDLE_HEIGHT
        self.speed = Config.PADDLE_SPEED
        self.color = Colors.PADDLE
        
    def update(self, dt, keys):
        """Update paddle position based on input."""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x = max(0, self.x - self.speed * dt)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x = min(Config.WINDOW_WIDTH - self.width, self.x + self.speed * dt)
    
    def draw(self, screen):
        """Draw paddle with rounded corners."""
        pygame.draw.rect(screen, self.color, 
                        (self.x, self.y, self.width, self.height),
                        border_radius=Config.PADDLE_RADIUS)
        # Add subtle highlight
        highlight = pygame.Surface((self.width - 4, 2))
        highlight.set_alpha(100)
        highlight.fill((255, 255, 255))
        screen.blit(highlight, (self.x + 2, self.y + 2))

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = Config.BALL_RADIUS
        self.vx = Config.BALL_SPEED
        self.vy = -Config.BALL_SPEED
        self.color = Colors.BALL
        self.attached = True
        self.trail = []
        
    def update(self, dt, paddle):
        """Update ball position and handle collisions."""
        if self.attached:
            self.x = paddle.x + paddle.width // 2
            self.y = paddle.y - self.radius - 1
            return
        
        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)
        
        # Move ball
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Wall collisions
        if self.x <= self.radius or self.x >= Config.WINDOW_WIDTH - self.radius:
            self.vx = -self.vx
            Effects.create_spark(self.x, self.y)
            
        if self.y <= self.radius:
            self.vy = -self.vy
            Effects.create_spark(self.x, self.y)
            
        # Paddle collision
        if (self.y + self.radius >= paddle.y and 
            self.y - self.radius <= paddle.y + paddle.height and
            self.x >= paddle.x and 
            self.x <= paddle.x + paddle.width):
            
            # Calculate bounce angle based on hit position
            hit_pos = (self.x - paddle.x) / paddle.width
            angle = math.pi * (0.125 + 0.75 * hit_pos)
            
            speed = math.sqrt(self.vx**2 + self.vy**2)
            self.vx = speed * math.cos(angle)
            self.vy = -abs(speed * math.sin(angle))
            
            Effects.create_spark(self.x, self.y)
    
    def launch(self):
        """Launch ball from paddle."""
        self.attached = False
        
    def draw(self, screen):
        """Draw ball with glow effect."""
        # Draw trail
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)) * 0.3)
            color = (*self.color, alpha)
            pygame.draw.circle(screen, color[:3], (int(pos[0]), int(pos[1])), 
                             self.radius * (i / len(self.trail)))
        
        # Draw ball
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Add highlight
        highlight_pos = (int(self.x - self.radius * 0.3), int(self.y - self.radius * 0.3))
        pygame.draw.circle(screen, (255, 255, 255), highlight_pos, self.radius // 3)

class Block:
    def __init__(self, x, y, contribution_count):
        self.x = x
        self.y = y
        self.width = Config.BLOCK_WIDTH
        self.height = Config.BLOCK_HEIGHT
        self.contribution_count = contribution_count
        self.color = self._get_color(contribution_count)
        self.destroyed = False
        self.destroy_animation = 0
        
    def _get_color(self, count):
        """Get color based on contribution count."""
        if count == 0:
            return Colors.CONTRIB_NONE
        elif count <= 3:
            return Colors.CONTRIB_LOW
        elif count <= 6:
            return Colors.CONTRIB_MEDIUM
        elif count <= 9:
            return Colors.CONTRIB_HIGH
        else:
            return Colors.CONTRIB_MAX
    
    def hit(self):
        """Handle block being hit."""
        if not self.destroyed:
            self.destroyed = True
            self.destroy_animation = 1.0
            Effects.create_explosion(self.x + self.width // 2, 
                                   self.y + self.height // 2, 
                                   self.color)
            return True
        return False
    
    def update(self, dt):
        """Update block animation."""
        if self.destroyed and self.destroy_animation > 0:
            self.destroy_animation -= dt * 3
    
    def draw(self, screen):
        """Draw block with effects."""
        if self.destroyed and self.destroy_animation <= 0:
            return
            
        if self.destroyed:
            # Destruction animation
            scale = self.destroy_animation
            w = int(self.width * scale)
            h = int(self.height * scale)
            x = self.x + (self.width - w) // 2
            y = self.y + (self.height - h) // 2
            
            alpha = int(255 * self.destroy_animation)
            color = (*self.color, alpha)
            
            pygame.draw.rect(screen, color[:3], (x, y, w, h), 
                           border_radius=Config.BLOCK_RADIUS)
        else:
            # Normal draw
            pygame.draw.rect(screen, self.color, 
                           (self.x, self.y, self.width, self.height),
                           border_radius=Config.BLOCK_RADIUS)
            
            # Add subtle gradient effect
            if self.contribution_count > 0:
                highlight = pygame.Surface((self.width - 2, self.height // 2))
                highlight.set_alpha(30)
                highlight.fill((255, 255, 255))
                screen.blit(highlight, (self.x + 1, self.y + 1))

class BreakoutGame:
    def __init__(self, screen, contributions):
        self.screen = screen
        self.contributions = contributions
        self.dark_mode = Config.DARK_MODE
        
        # Game objects
        self.paddle = Paddle(Config.WINDOW_WIDTH // 2 - Config.PADDLE_WIDTH // 2,
                           Config.WINDOW_HEIGHT - 100)
        self.ball = Ball(self.paddle.x + self.paddle.width // 2,
                        self.paddle.y - Config.BALL_RADIUS)
        self.blocks = self._create_blocks()
        
        # Game state
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.paused = False
        
        # UI
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def _create_blocks(self):
        """Create blocks from GitHub contributions."""
        blocks = []
        
        # Calculate grid dimensions
        days_in_week = 7
        weeks = len(self.contributions) // days_in_week
        
        # Starting position
        start_x = (Config.WINDOW_WIDTH - (weeks * (Config.BLOCK_WIDTH + Config.BLOCK_SPACING))) // 2
        start_y = 100
        
        for week in range(weeks):
            for day in range(days_in_week):
                idx = week * days_in_week + day
                if idx < len(self.contributions):
                    contribution = self.contributions[idx]
                    
                    x = start_x + week * (Config.BLOCK_WIDTH + Config.BLOCK_SPACING)
                    y = start_y + day * (Config.BLOCK_HEIGHT + Config.BLOCK_SPACING)
                    
                    # Only create blocks for days with contributions
                    if contribution['count'] > 0:
                        blocks.append(Block(x, y, contribution['count']))
        
        return blocks
    
    def update(self, dt, events):
        """Update game state."""
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.ball.attached:
                    self.ball.launch()
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_t:
                    self.dark_mode = not self.dark_mode
                    Colors.update_theme(self.dark_mode)
        
        if self.paused or self.game_over:
            return
        
        # Get keys
        keys = pygame.key.get_pressed()
        
        # Update game objects
        self.paddle.update(dt, keys)
        self.ball.update(dt, self.paddle)
        
        # Update blocks
        for block in self.blocks:
            block.update(dt)
        
        # Check ball-block collisions
        for block in self.blocks:
            if not block.destroyed:
                if (self.ball.x + self.ball.radius >= block.x and
                    self.ball.x - self.ball.radius <= block.x + block.width and
                    self.ball.y + self.ball.radius >= block.y and
                    self.ball.y - self.ball.radius <= block.y + block.height):
                    
                    if block.hit():
                        self.score += block.contribution_count * 10
                        self.ball.vy = -self.ball.vy
        
        # Check if ball is out of bounds
        if self.ball.y > Config.WINDOW_HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                # Reset ball
                self.ball = Ball(self.paddle.x + self.paddle.width // 2,
                               self.paddle.y - Config.BALL_RADIUS)
        
        # Check win condition
        if all(block.destroyed for block in self.blocks if block.contribution_count > 0):
            self.game_over = True
        
        # Update effects
        Effects.update(dt)
    
    def draw(self):
        """Draw everything."""
        # Clear screen
        self.screen.fill(Colors.BACKGROUND)
        
        # Draw grid pattern (subtle)
        for x in range(0, Config.WINDOW_WIDTH, 50):
            pygame.draw.line(self.screen, Colors.GRID_LINE, (x, 0), (x, Config.WINDOW_HEIGHT))
        for y in range(0, Config.WINDOW_HEIGHT, 50):
            pygame.draw.line(self.screen, Colors.GRID_LINE, (0, y), (Config.WINDOW_WIDTH, y))
        
        # Draw game objects
        for block in self.blocks:
            block.draw(self.screen)
        
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        
        # Draw effects
        Effects.draw(self.screen)
        
        # Draw UI
        self._draw_ui()
        
        # Draw pause overlay
        if self.paused:
            self._draw_pause_overlay()
        
        # Draw game over
        if self.game_over:
            self._draw_game_over()
    
    def _draw_ui(self):
        """Draw UI elements."""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, Colors.TEXT)
        self.screen.blit(score_text, (20, 20))
        
        # Lives
        lives_text = self.font.render(f"Lives: {self.lives}", True, Colors.TEXT)
        self.screen.blit(lives_text, (Config.WINDOW_WIDTH - 150, 20))
        
        # Instructions
        if self.ball.attached:
            inst_text = self.small_font.render("Press SPACE to launch", True, Colors.TEXT_SECONDARY)
            text_rect = inst_text.get_rect(center=(Config.WINDOW_WIDTH // 2, Config.WINDOW_HEIGHT - 50))
            self.screen.blit(inst_text, text_rect)
    
    def _draw_pause_overlay(self):
        """Draw pause screen overlay."""
        overlay = pygame.Surface((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font.render("PAUSED", True, Colors.TEXT)
        text_rect = pause_text.get_rect(center=(Config.WINDOW_WIDTH // 2, Config.WINDOW_HEIGHT // 2))
        self.screen.blit(pause_text, text_rect)
        
        inst_text = self.small_font.render("Press P to resume", True, Colors.TEXT_SECONDARY)
        inst_rect = inst_text.get_rect(center=(Config.WINDOW_WIDTH // 2, Config.WINDOW_HEIGHT // 2 + 40))
        self.screen.blit(inst_text, inst_rect)
    
    def _draw_game_over(self):
        """Draw game over screen."""
        overlay = pygame.Surface((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))
        overlay.set_alpha(192)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        if self.lives <= 0:
            text = "GAME OVER"
            color = Colors.CONTRIB_MAX
        else:
            text = "YOU WIN!"
            color = Colors.CONTRIB_HIGH
        
        game_over_text = self.font.render(text, True, color)
        text_rect = game_over_text.get_rect(center=(Config.WINDOW_WIDTH // 2, Config.WINDOW_HEIGHT // 2 - 40))
        self.screen.blit(game_over_text, text_rect)
        
        score_text = self.font.render(f"Final Score: {self.score}", True, Colors.TEXT)
        score_rect = score_text.get_rect(center=(Config.WINDOW_WIDTH // 2, Config.WINDOW_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        inst_text = self.small_font.render("Press ESC to exit", True, Colors.TEXT_SECONDARY)
        inst_rect = inst_text.get_rect(center=(Config.WINDOW_WIDTH // 2, Config.WINDOW_HEIGHT // 2 + 40))
        self.screen.blit(inst_text, inst_rect)