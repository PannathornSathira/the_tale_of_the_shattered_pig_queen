from src.constants import *
from src.resources import *
from src.platforms.BasePlatform import BasePlatform
import pygame
import time

class SpecialPlatform(BasePlatform):
    def __init__(self, x, y, area=1):
        super().__init__(x, y, area)
        
        self.flicker = False
        self.flicker_time = 0  # Tracks the total flicker time
        self.flicker_speed = 100  # Initial flicker speed in milliseconds
        self.hidden = False  # Track whether the platform is hidden
        self.disappearing = False  # Track if the platform is disappearing
        self.disappear_start_time = None  # Time when the platform started disappearing
        self.visible = True  # Track if the platform is currently visible
        self.fake = (area == 5)  # Determine if this is a fake platform

        # Set the platform color based on the area
        if self.area == 5:
            self.image = tile_dict["castle"]
        else:
            self.image = tile_dict["special"]

    def update(self, dt):
        # Update only if the platform is in the process of disappearing
        if self.disappearing:
            current_time = time.time()
            
            # Handle flickering effect
            if self.flicker:
                # Update flicker time and toggle visibility based on flicker speed
                self.flicker_time += dt * 1000  # Convert dt to milliseconds
                if self.flicker_time >= self.flicker_speed:
                    self.hidden = not self.hidden  # Toggle hidden state
                    self.flicker_time = 0  # Reset flicker time

            # Check if 3 seconds have passed since disappearing started
            if current_time - self.disappear_start_time >= 3:
                # Toggle visibility state every 3 seconds
                self.visible = not self.visible
                self.disappearing = not self.visible  # Stop disappearing if it reappears
                if self.visible:
                    # Reset flickering state when the platform reappears
                    self.flicker = False
                    self.hidden = False
                else:
                    # Start the next disappearance cycle
                    self.disappear_start_time = current_time

        # For fake platforms, disable the collision area
        if self.fake or not self.visible:
            # Make the collision area a zero-size rectangle if it's a fake platform
            self.rect = pygame.Rect(self.rect.x, self.rect.y, 0, 0)
        else:
            # Restore the actual size for other platforms
            self.rect = pygame.Rect(self.rect.x, self.rect.y, self.platform_length, self.platform_height)

    def trigger_effect(self, player):
        """Apply a special effect to the player based on the platform's area."""
        if self.area == 1:
                player.movement_speed = player.default_move_speed * 1.25
        elif self.area == 2:
                pass
        elif self.area == 3:
            # When player steps on a blue platform, make it disappear with flickering
            if not self.disappearing and self.visible:
                self.disappearing = True
                self.flicker = True  # Enable flickering effect
                self.disappear_start_time = time.time()
        elif self.area == 4:
                player.movement_speed = player.default_move_speed * 0.75
        elif self.area == 5:
            # No collision effect for fake platforms
            pass
        else:
            pass

    def render(self, screen):
        if not self.hidden and self.visible:
            super().render(screen)
