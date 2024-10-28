from src.Bullet import Bullet
from src.constants import *

class BossBullet(Bullet):
  
  def __init__(self, x, y, direction, dy=0):
    super().__init__(x, y, direction)
    self.speed_y = dy
    self.color = (255, 0, 0)
  
  def update(self, dt):
    super().update(dt)
    if self.direction == "left" or self.direction == "right":
      self.y += self.speed_y * dt

  def render(self, screen):
    super().render(screen)