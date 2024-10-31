import pygame
from src.Dependency import *

class PauseState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.options = ["Resume"]
        self.selected_option_index = 0
        
        self.level = None
        self.boss = None
        self.player = None

    def Exit(self):
        pass

    def Enter(self, params):
        self.level = params["level"]
        self.boss = params["boss"]
        self.player = params["player"]

    def update(self, dt, events):
        # Handle player input for selecting options
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option_index = (self.selected_option_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option_index = (self.selected_option_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option_index == 0:
                        g_state_manager.Change("PLAY", {
                            "level": self.level,
                            "boss": self.boss,
                            "player": self.player
                        })
                    elif self.selected_option_index == 1:
                        g_state_manager.Change("MAIN_MENU", {})
        return None, None

    def render(self, screen):
        # Fill the screen with a semi-transparent overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with transparency
        screen.blit(overlay, (0, 0))

        # Render pause menu options
        for index, option in enumerate(self.options):
            color = (255, 255, 255) if index == self.selected_option_index else (100, 100, 100)
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2, 200 + index * 50))
            screen.blit(text_surface, text_rect)

        # Update the display
        pygame.display.update()
