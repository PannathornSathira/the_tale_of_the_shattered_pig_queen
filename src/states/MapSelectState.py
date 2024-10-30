from src.states.BaseState import BaseState
from src.constants import *
from src.Dependency import *
import pygame

class MapSelectState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.map_areas = [
            pygame.Rect(100, 100, 200, 150),  # Area 1
            pygame.Rect(400, 100, 200, 150),  # Area 2
            pygame.Rect(100, 300, 200, 150),  # Area 3
            pygame.Rect(400, 300, 200, 150),  # Area 4
            pygame.Rect(700, 300, 200, 150,)# Shop
        ]
        self.selected_area_index = None
        self.start_game = False
        self.go_to_shop = False

    def Exit(self):
        pass

    def Enter(self, params):
        pass

    def update(self, dt, events):
        # Get player input
        pressed_keys = pygame.key.get_pressed()

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check if player collides with any area
        for index, area in enumerate(self.map_areas):
            if area.collidepoint(mouse_pos):
                self.selected_area_index = index
                break
        else:
            self.selected_area_index = None

        # Check if ENTER key is pressed while hovering over an area
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.selected_area_index is not None:
                if self.selected_area_index == 4:  # Shop area
                    self.go_to_shop = True
                else:
                    self.start_game = True

        return None, None

    def render(self):
        # Fill the screen with a background color
        self.screen.fill((173, 216, 230))  # Light blue color

        # Draw each map area as a rectangle
        for index, area in enumerate(self.map_areas):
            color = (0, 255, 0) if index == self.selected_area_index else (255, 0, 0)
            pygame.draw.rect(self.screen, color, area)

            # Draw area number
            area_name = f"Area {index + 1}" if index < 4 else "Shop"
            text_surface = self.font.render(area_name, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=area.center)
            self.screen.blit(text_surface, text_rect)

        # Update the display
        pygame.display.update()
