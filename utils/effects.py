"""
Visual effects for the game
"""

import pygame
import random
import math

class Particle:
    def __init__(self, x, y, vx, vy, color, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 4)
        
    def update(self, dt):
        """Update particle position and lifetime."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 200 * dt  # Gravity
        self.lifetime -= dt
        
    def draw(self, screen):
        """Draw particle with fading effect."""
        if self.lifetime > 0:
            alpha = self.lifetime / self.max_lifetime
            size = int(self.size * alpha)
            if size > 0:
                # Create a surface for the particle with alpha
                particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                color_with_alpha = (*self.color, int(255 * alpha))
                pygame.draw.circle(particle_surface, color_with_alpha, (size, size), size)
                screen.blit(particle_surface, (int(self.x - size), int(self.y - size)))

class Effects:
    particles = []
    
    @classmethod
    def create_spark(cls, x, y):
        """Create spark effect at position."""
        for _ in range(5):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = (255, 255, 255)
            lifetime = random.uniform(0.2, 0.4)
            cls.particles.append(Particle(x, y, vx, vy, color, lifetime))
    
    @classmethod
    def create_explosion(cls, x, y, color):
        """Create explosion effect with given color."""
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 300)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            lifetime = random.uniform(0.3, 0.6)
            cls.particles.append(Particle(x, y, vx, vy, color, lifetime))
    
    @classmethod
    def update(cls, dt):
        """Update all particles."""
        cls.particles = [p for p in cls.particles if p.lifetime > 0]
        for particle in cls.particles:
            particle.update(dt)
    
    @classmethod
    def draw(cls, screen):
        """Draw all particles."""
        for particle in cls.particles:
            particle.draw(screen)