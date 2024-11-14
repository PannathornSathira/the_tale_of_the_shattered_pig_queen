from abc import ABC, abstractmethod
from src.constants import *
import pygame
from src.Dependency import *
from src.resources import *
from src.Util import *

class MainMenuState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 80)  # Set font size to 48
        self.start_game = False
        self.bg_image = pygame.image.load("./graphics/main_menu_temp.png")
        #self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH + 5, HEIGHT + 5))
        
    def Enter(self, params):
        gMusic["main"].play(-1)

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # g_state_manager.Change("WORLD_MAP", {
                #     "completed_level": None
                # })
                g_state_manager.Change("START_STORY", {
                    "play_check": True,
                })
                #g_state_manager.Change("SHOP", {})
            if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                g_state_manager.Change("END", {
                    "play_check": True,
                })    
    def Exit(self):
        gMusic["main"].stop()

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))
        text_surface = self.font.render("Press Enter to Start", True, (0, 0, 0))  # Black color
        text_rect = text_surface.get_rect(center=(screen.get_width() / 2 - 320, screen.get_height() / 2- 290))
        screen.blit(text_surface, text_rect)
