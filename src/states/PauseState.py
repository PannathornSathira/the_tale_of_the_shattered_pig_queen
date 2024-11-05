import pygame
from src.Dependency import *
from src.resources import *
from src.Util import *

class PauseState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.options = ["Resume", "End this journey"]
        self.selected_option_index = 0
        
        self.level = None
        self.boss = None
        self.player = None
        self.total_coins = 0
        

    def Exit(self):
        pass

    def Enter(self, params):
        self.level = params["level"]
        self.boss = params["boss"]
        self.player = params["player"]
        self.total_coins = params["total_coins"]
        self.difficulty = params["difficulty"]
        self.damage_potions = params['damage_potions']
        self.health_potions = params.get("health_potions")
        self.swiftness_potions = params.get("swiftness_potions")

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
                            "player": self.player,
                            "total_coins": self.total_coins,
                            "difficulty": self.difficulty,
                            "damage_potions": self.damage_potions,
                            "health_potions": self.health_potions,
                            "swiftness_potions": self.swiftness_potions
                            
                        })
                    elif self.selected_option_index == 1:
                        save_values({
                            "total_coins": self.total_coins,
                            "damage_potions": self.damage_potions,
                            "health_potions": self.health_potions,
                            "swiftness_potions": self.swiftness_potions
                        })
                        g_state_manager.Change("SHOP", {})
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
