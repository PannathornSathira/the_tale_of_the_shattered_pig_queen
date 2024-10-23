from src.constants import *
import random, pygame, math
class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # "left" or "right"
        self.speed = 500  # Bullet speed
        self.width = 10
        self.height = 5
        self.active = True  # If the bullet is still on the screen

    def update(self, dt):
        # Move the bullet in the correct direction
        if self.direction == "right":
            self.x += self.speed * dt
        elif self.direction == "left":
            self.x -= self.speed * dt
        
        # If the bullet moves off-screen, deactivate it
        if self.x < 0 or self.x > WIDTH:
            self.active = False

    def render(self, screen):
        # Draw the bullet (just a simple rectangle for now)
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
