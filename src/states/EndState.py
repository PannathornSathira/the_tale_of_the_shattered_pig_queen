from abc import ABC, abstractmethod
from src.constants import *
import pygame
from src.Dependency import *
from src.resources import *
from src.Util import *


class EndState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        # self.bg_image = pygame.image.load("./graphics/main_menu_temp.png")
        self.bg_image = pygame.Surface((WIDTH, HEIGHT))
        self.bg_image.fill((0, 0, 0))

    def Enter(self, params):
        pass

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # g_state_manager.Change("WORLD_MAP", {
                #     "completed_level": None
                # })
                g_state_manager.Change("MAIN_MENU", {})

    def Exit(self):
        pass

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))
        text_surface = self.font.render(
            "The End. Press Enter to Continue", True, (255, 255, 255)
        )  # Black color
        text_rect = text_surface.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2)
        )
        screen.blit(text_surface, text_rect)
