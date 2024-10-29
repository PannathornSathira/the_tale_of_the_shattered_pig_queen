from src.constants import *
import random, pygame, math
class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # "left" or "right"
        self.speed = BULLET_SPEED  # Bullet speed
        if direction == "right" or direction == "left":
            self.width = BULLET_LENGTH
            self.height = BULLET_WIDTH
        else:
            self.width = BULLET_WIDTH
            self.height = BULLET_LENGTH
        self.active = True  # If the bullet is still on the screen
        self.color = (128, 0, 128)
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, dt):
        # Move the bullet in the correct direction
        if self.direction == "right":
            self.x += self.speed * dt
        elif self.direction == "left":
            self.x -= self.speed * dt
        elif self.direction == "up":
            self.y -= self.speed * dt
        elif self.direction == "down":
            self.y += self.speed * dt
        
        # If the bullet moves off-screen, deactivate it
        if self.x + self.width < 0 or self.x > WIDTH or self.y + self.height < 0 or self.y > HEIGHT:
            self.active = False
            
        self.rect.x = self.x
        self.rect.y = self.y

    def render(self, screen):
        # Draw the bullet (just a simple rectangle for now)
        pygame.draw.rect(screen, self.color, self.rect)
