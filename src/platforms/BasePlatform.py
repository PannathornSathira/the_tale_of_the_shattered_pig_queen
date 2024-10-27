from src.constants import *
import pygame

class BasePlatform:
  def __init__(self, x, y, area=1):
    self.x = x
    self.y = y
    self.color = (0,0,0)
    self.area = area
    self.platform_length = WIDTH // (NUM_COL + 2)  # Platform length in pixels
    self.platform_height = TILE_SIZE * 0.5  # Platform height in pixels
    
    self.rect = pygame.Rect(x, y, self.platform_length, self.platform_height)
    
  def update(self, dt):
    pass
  
  def trigger_effect(self, player):
    player.revert_to_default()
    
  def render(self, screen):
    pygame.draw.rect(screen, self.color, self.rect)