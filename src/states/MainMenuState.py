from abc import ABC, abstractmethod
from src.constants import *
import pygame
from src.Dependency import *
from src.resources import *
from src.Util import *

class MainMenuState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
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
                g_state_manager.Change("SHOP", {})
                
    def Exit(self):
        pass

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))
        text_surface = self.font.render("Press Enter to Start", True, (0, 0, 0))  # Black color
        text_rect = text_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(text_surface, text_rect)
