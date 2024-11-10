from src.Bullet import Bullet
from src.constants import *
from src.resources import *
import pygame
import math


class BossBullet(Bullet):

    def __init__(self, x, y, direction, dy=0, general_speed=(0, 0), damage=10, scaling=1):
        super().__init__(x, y, direction, general_speed, damage=damage)
        self.scaling = scaling
        self.speed_y = dy * self.scaling
        self.color = (255, 0, 0)
        self.damage = 10
        self.image = sprite_collection["sandworm_bullet"].image
        #self.scaling = scaling
        self.angle = self.calculate_angle()
        self.rotated_image = pygame.transform.rotate(self.image, -self.angle)
        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))
        
    def re_initialize(self):
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.angle = self.calculate_angle()
        self.rotated_image = pygame.transform.rotate(self.image, -self.angle)
        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))
        print(self.angle)
        
    def calculate_angle(self):
        """Calculate the rotation angle based on dx and dy speeds."""
        angle_radians = math.atan2(-self.speed_y, self.speed)  # Negative dy to adjust for screen coordinates
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees

    def update(self, dt):
        super().update(dt)
        #self.speed_y = self.speed_y * self.scaling
        if self.direction == "left" or self.direction == "right":
            self.y += self.speed_y * dt

    def render(self, screen):
        screen.blit(self.rotated_image, self.rect)
