from src.constants import *
import random, pygame, math
from src.bosses.BossBullet import BossBullet

class BeamAttack(BossBullet):
    def __init__(self, x, y, direction, width=BEAM_WIDTH, height=BEAM_HEIGHT):
        super().__init__(x, y, direction)
        self.width = width
        self.height = height
        self.rect.width = self.width
        self.rect.height = self.height
        self.active = True
        self.color = (0, 255, 0)
        self.speed = BEAM_SPEED
        
        # Adjust beam starting postition and rotation
        if self.direction == "right":
          self.x -= self.width
        elif self.direction == "left":
          pass
        elif self.direction == "up":
          pass
        elif self.direction == "down":
          self.y -= self.height

    def update(self, dt):
        super().update(dt)

    def render(self, screen):
        # Draw the bullet (just a simple rectangle for now)
        super().render(screen)
