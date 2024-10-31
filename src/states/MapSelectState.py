from src.constants import *
from src.Dependency import *
from src.Level import Level
from src.Player import Player
from src.bosses.KrakenBoss import KrakenBoss
from src.bosses.GreatSharkBoss import GreatSharkBoss
from src.bosses.BlackWidowBoss import BlackWidowBoss
from src.bosses.MedusaBoss import MedusaBoss
from src.bosses.BlueDragonBoss import BlueDragonBoss
from src.bosses.TornadoFiendBoss import TornadoFiendBoss
from src.bosses.KingMummyBoss import KingMummyBoss
from src.bosses.SandWormBoss import SandWormBoss
from src.bosses.WraithBoss import WraithBoss
import pygame, random

class MapSelectState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.map_areas = [
            pygame.Rect(100, 100, 200, 150),  # Area 1
            pygame.Rect(400, 100, 200, 150),  # Area 2
            pygame.Rect(100, 300, 200, 150),  # Area 3
            pygame.Rect(400, 300, 200, 150),  # Area 4
            pygame.Rect(100, 500, 200, 150),  # Area 5 (Final Boss)
            pygame.Rect(700, 300, 200, 150,)# Shop
        ]
        self.start_game = False
        self.go_to_shop = False
        self.selected_area_index = None
        
        self.boss_spawn_x = 1100
        self.boss_spawn_y = 100

    def Exit(self):
        pass

    def Enter(self, params):
        pass

    def update(self, dt, events):

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check if player collides with any area
        for index, area in enumerate(self.map_areas):
            if area.collidepoint(mouse_pos):
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if index < 5:
                                level = Level(area=index+1)
                                level.CreateMap()
                                player = Player()
                                boss = self.spawn_boss(area=index+1)
                                g_state_manager.Change("PLAY", {
                                    "level": level,
                                    "boss": boss,
                                    "player": player
                                })
                            else:
                                g_state_manager.Change("SHOP", {
                                    
                                })
                self.selected_area_index = index
                break
        else:
            self.selected_area_index = None
            
    def spawn_boss(self, area):
        if area == 1:
            return random.choice([KrakenBoss(self.boss_spawn_x, self.boss_spawn_y), GreatSharkBoss(self.boss_spawn_x, self.boss_spawn_y)])
        elif area == 2:
            # return random.choice([BlackWidowBoss(self.boss_spawn_x, self.boss_spawn_y), MedusaBoss(self.boss_spawn_x, self.boss_spawn_y)])
            return random.choice([BlackWidowBoss(self.boss_spawn_x, self.boss_spawn_y)])
        elif area == 3:
            return random.choice([BlueDragonBoss(self.boss_spawn_x, self.boss_spawn_y), TornadoFiendBoss(self.boss_spawn_x, self.boss_spawn_y)])
        elif area == 4:
            return random.choice([KingMummyBoss(self.boss_spawn_x, self.boss_spawn_y), SandWormBoss(self.boss_spawn_x, self.boss_spawn_y)])
        elif area == 5:
            return WraithBoss(self.boss_spawn_x, self.boss_spawn_y)

    def render(self, screen):
        # Fill the screen with a background color
        screen.fill((173, 216, 230))  # Light blue color

        # Draw each map area as a rectangle
        for index, area in enumerate(self.map_areas):
            color = (0, 255, 0) if index == self.selected_area_index else (255, 0, 0)
            pygame.draw.rect(screen, color, area)

            # Draw area number
            area_name = f"Area {index + 1}" if index < 5 else "Shop"
            text_surface = self.font.render(area_name, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=area.center)
            screen.blit(text_surface, text_rect)

        # Update the display
        pygame.display.update()
