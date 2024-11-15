from src.constants import *
from src.resources import *
import pygame

class BasePlatform:
  def __init__(self, x, y, area=1):
    self.x = x
    self.y = y
    self.color = (0,0,0)
    self.area = area
    self.platform_length = WIDTH // (NUM_COL)  # Platform length in pixels
    self.platform_height = TILE_SIZE * 0.5  # Platform height in pixels
    
    if area == 3:
        self.image = tile_dict["sea"]
    elif area == 2:
        self.image = tile_dict["forest"]
    elif area == 1:
        self.image = tile_dict["sky"]
    elif area == 4:
        self.image = tile_dict["sand"]
    elif area == 5:
        self.image = tile_dict["castle"]
    else:
        self.image = tile_dict["castle"]
    
    self.rect = pygame.Rect(x, y, self.platform_length, self.platform_height)
    
  def update(self, dt):
    pass
  
  def trigger_effect(self, player):
    player.revert_to_default()
    
  def render(self, screen):
    img = self.image
    img = pygame.transform.scale(img, (self.platform_length, self.platform_height))
    screen.blit(img, (self.rect.x, self.rect.y))