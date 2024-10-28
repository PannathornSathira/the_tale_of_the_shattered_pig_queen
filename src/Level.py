import random
import pygame
from src.Util import GenerateTiles
from src.constants import *
from src.platforms.BasePlatform import BasePlatform
from src.platforms.SpecialPlatform import SpecialPlatform


class Level:
    def __init__(self, area=0):
        self.tilemaps = GenerateTiles('./graphics/tiles.png', TILE_SIZE, TILE_SIZE, colorkey=-1, scale=3)
        self.tiles = []
        self.platforms = [[None for _ in range(8)] for _ in range(3)]  # 3x8 matrix for platforms
        self.map_width = WIDTH // (TILE_SIZE * 3) + 1
        self.map_height = HEIGHT // (TILE_SIZE * 3) + 1
        if area == 0:
            self.area = random.randint(1,5)
        else:
            self.area = area
            
    def update(self, dt, events):
        for platform_row in self.platforms:
            for platform in platform_row:
                if platform:
                    platform.update(dt)

    def CreateMap(self):
        for y in range(self.map_height):
            self.tiles.append([])
            for x in range(self.map_width):
                if y < 5:
                    self.tiles[y].append(SKY)
                elif y == 5:
                    self.tiles[y].append(GRASS)
                elif y == 6:
                    self.tiles[y].append(GROUND_BOUNDARY)
                else:
                    self.tiles[y].append(GROUND)
        self.GeneratePlatforms()

    def GeneratePlatforms(self):
        platform_length = WIDTH // (NUM_COL)  # Platform length in pixels
        row_y_positions = [1 * TILE_SIZE * 4 + 50, 2 * TILE_SIZE * 4 + 50, 3 * TILE_SIZE * 4 + 50]  # Y-positions for each row
        platform_counts = [2, 4, 6]  # Number of platforms per row

        for row in range(NUM_ROW):  # Loop through each row
            row_y = row_y_positions[row]
            cols = random.sample(range(NUM_COL), platform_counts[row])

            # Ensure at least one "normal" platform
            normal_col = random.choice(cols)
            platform = BasePlatform((normal_col) * platform_length, row_y, self.area)
            self.platforms[row][normal_col] = platform

            # Ensure at least one "special" platform
            special_col = random.choice([col for col in cols if col != normal_col])
            platform = SpecialPlatform((special_col) * platform_length, row_y, self.area)
            self.platforms[row][special_col] = platform

            # Fill in the remaining platforms randomly
            for col in cols:
                if col == normal_col or col == special_col:
                    continue  # Skip the already placed platforms

                platform_type = random.choice(["normal", "special"])
                if platform_type == "normal":
                    platform = BasePlatform((col) * platform_length, row_y, self.area)
                else:
                    platform = SpecialPlatform((col) * platform_length, row_y, self.area)

                # Store the platform in the matrix
                self.platforms[row][col] = platform



    def render(self, screen):
        for y in range(self.map_height):
            for x in range(self.map_width):
                id = self.tiles[y][x]
                screen.blit(self.tilemaps[id], (x * TILE_SIZE * 3, y * TILE_SIZE * 3))

        # Draw platforms
        for row in range(NUM_ROW):
            for col in range(NUM_COL):
                platform = self.platforms[row][col]
                if platform:
                    platform.render(screen)
