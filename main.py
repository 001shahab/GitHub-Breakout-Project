#!/usr/bin/env python3
"""
GitHub Contribution Breakout
Copyright © 2024 3S Holding OÜ, Tartu, Estonia
Created by Prof. Shahab Anbarjafari
"""

import pygame
import sys
from game import BreakoutGame
from github_api import GitHubAPI
from config import Config
import os
from dotenv import load_dotenv

def main():
    """Main entry point for the game."""
    # Load environment variables
    load_dotenv()
    
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Set up display
    screen = pygame.display.set_mode((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))
    pygame.display.set_caption("GitHub Contribution Breakout")
    
    # Create clock for FPS control
    clock = pygame.time.Clock()
    
    # Get GitHub data
    print("Fetching your GitHub contributions...")
    github_username = os.getenv('GITHUB_USERNAME')
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_username:
        print("Error: GITHUB_USERNAME not set in .env file")
        sys.exit(1)
    
    github_api = GitHubAPI(github_username, github_token)
    contributions = github_api.get_contributions()
    
    if not contributions:
        print("Error: Could not fetch GitHub contributions")
        sys.exit(1)
    
    print(f"Successfully loaded {len(contributions)} days of contributions!")
    
    # Create game instance
    game = BreakoutGame(screen, contributions)
    
    # Game loop
    running = True
    while running:
        dt = clock.tick(Config.FPS) / 1000.0  # Delta time in seconds
        
        # Handle events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Update game
        game.update(dt, events)
        
        # Draw everything
        game.draw()
        
        # Update display
        pygame.display.flip()
    
    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()