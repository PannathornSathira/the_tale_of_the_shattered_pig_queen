import random, pygame, math
from src.Util import GenerateTiles
from src.constants import *

#patterns
NONE = 1
SINGLE_PYRAMID = 2
MULTI_PYRAMID = 3

SOLID = 1            # all colors the same in this row
ALTERNATE = 2        # alternative colors
SKIP = 3             # skip every other brick
NONE = 4             # no block this row
class Level:
    def __init__(self):
        self.tilemaps = GenerateTiles('./graphics/tiles.png', TILE_SIZE, TILE_SIZE, colorkey=-1, scale=3)
        self.tiles = []
        self.platforms = []
        self.map_width = WIDTH // (TILE_SIZE*3) + 1
        self.map_height = HEIGHT // (TILE_SIZE*3) + 1

    def CreateMap(self):
        for y in range(self.map_height):
            self.tiles.append([])
            for x in range(self.map_width):
                if y < 4:
                    self.tiles[y].append(SKY)
                elif y == 4:
                    self.tiles[y].append(GRASS)
                elif y == 5:
                    self.tiles[y].append(GROUND_BOUNDARY)
                else:
                    self.tiles[y].append(GROUND)
        self.GeneratePlatforms()
    def GeneratePlatforms(self):
        platform_color = (0, 0, 0)  
        min_height = 2
        max_height = 4
        platform_count = 5
        platform_width = 1.5 * TILE_SIZE * 3  # Width of the platform in pixels
        platform_height = TILE_SIZE * 0.5  # Height of the platform in pixels

        for _ in range(platform_count):
            platform_x = random.randint(2 * TILE_SIZE * 3, (self.map_width - 2) * TILE_SIZE * 3)
            platform_y = random.randint(min_height * TILE_SIZE * 3, max_height * TILE_SIZE * 3)
            platform_rect = pygame.Rect(platform_x, platform_y, platform_width, platform_height)
            self.platforms.append((platform_rect, platform_color)) 
                   
    def render(self, screen):
        for y in range(self.map_height):
            for x in range(self.map_width):
                id = self.tiles[y][x]
                screen.blit(self.tilemaps[id], (x * TILE_SIZE * 3, y * TILE_SIZE * 3))
            for platform_rect, platform_color in self.platforms:
                pygame.draw.rect(screen, platform_color, platform_rect)