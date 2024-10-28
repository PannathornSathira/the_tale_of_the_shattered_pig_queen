import pygame
from src.constants import *

class BossBullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # Typically downwards towards the player
        self.speed = 300  # Speed of the boss bullet
        self.width = 10
        self.height = 10
        self.active = True  # If the bullet is still active

    def update(self, dt):
        # Move the bullet downwards
        if self.direction == "right":
            self.x += self.speed * dt
        elif self.direction == "left":
            self.x -= self.speed * dt
        
        # If the bullet moves off-screen, deactivate it
        if self.x < 0 or self.x > WIDTH:
            self.active = False

    def render(self, screen):
        # Draw the bullet (just a simple rectangle for now)
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))
