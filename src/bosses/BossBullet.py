from src.Bullet import Bullet
from src.constants import *
from src.resources import *
import pygame
import math


class BossBullet(Bullet):

    def __init__(self, x, y, direction, dy=0, general_speed=(0, 0), damage=10):
        super().__init__(x, y, direction, general_speed, damage=damage)
        self.speed_y = dy
        self.color = (255, 0, 0)
        self.damage = 10
        self.image = pygame.Surface(
            (self.width, self.height)
        )
        self.image.fill((255, 0, 0))
        self.original_image = self.image.copy()
        self.angle = self.calculate_angle()
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
    def re_initialize(self):
        self.angle = self.calculate_angle()
        self.image = pygame.transform.rotate(pygame.transform.scale(self.original_image, (self.width, self.height)), -self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def set_image(self, image):
        self.original_image = image
        self.angle = self.calculate_angle()
        self.image = pygame.transform.rotate(pygame.transform.scale(self.original_image, (self.width, self.height)), -self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
    def calculate_angle(self):
        """Calculate the rotation angle based on dx and dy speeds."""
        if self.dx != 0 or self.dy != 0:
            angle_radians = math.atan2(self.dy, self.dx) + math.pi
        else:
            angle_radians = math.atan2(-self.speed_y, self.speed)  # Negative dy to adjust for screen coordinates
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees

    def update(self, dt):
        super().update(dt)
        if self.direction == "left" or self.direction == "right":
            self.y += self.speed_y * dt

    def render(self, screen):
        screen.blit(self.image, self.rect)
