from src.constants import *
from src.Util import SpriteManager
import pygame
import time

class Player:
    def __init__(self):
        self.character_x = WIDTH / 2 - (CHARACTER_WIDTH) / 2
        self.character_y = (5 * TILE_SIZE - CHARACTER_HEIGHT) * 3
        self.direction = "front"  # left right front
        self.sprite_collection = SpriteManager().spriteCollection
        self.animation = self.sprite_collection["character_front"].animation
        
        self.velocity_y = 0  # Vertical speed (used for jumping/falling)
        self.is_jumping = False  # Track if the player is in the air
        self.on_ground = True
        self.jump_force = -800  # Force applied when jumping
        self.gravity = 1500  # Gravity that pulls the player down
        self.ground_y = self.character_y  # Starting ground level
        #self.store_veloy = 0

    def update(self, dt, events, platforms):
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_LEFT]:
            self.direction = "left"
            self.animation = self.sprite_collection["character_walk_right"].animation
            self.character_x -= CHARACTER_MOVE_SPEED * dt
        elif pressedKeys[pygame.K_RIGHT]:
            self.direction = "right"
            self.animation = self.sprite_collection["character_walk_right"].animation
            self.character_x += CHARACTER_MOVE_SPEED * dt
        elif pressedKeys[pygame.K_SPACE] and self.on_ground:
            self.is_jumping = True
            self.velocity_y = self.jump_force
            self.on_ground = False
            self.animation = self.sprite_collection["character_walk_right"].animation
        else:
            self.direction = "front"
            self.animation = self.sprite_collection["character_front"].animation
            
        if pressedKeys[pygame.K_SPACE] and pressedKeys[pygame.K_RIGHT] and self.on_ground:
            self.is_jumping = True
            self.velocity_y = self.jump_force  # Apply the jump force
            self.on_ground = False
            self.direction = "right"
            self.animation = self.sprite_collection["character_walk_right"].animation
            self.character_x += CHARACTER_MOVE_SPEED * dt  # Move right while jumping
        
        if pressedKeys[pygame.K_SPACE] and pressedKeys[pygame.K_LEFT] and self.on_ground:
            self.is_jumping = True
            self.velocity_y = self.jump_force  # Apply the jump force
            self.on_ground = False
            self.direction = "left"
            self.animation = self.sprite_collection["character_walk_right"].animation
            self.character_x -= CHARACTER_MOVE_SPEED * dt  # Move right while jumping

        # Apply gravity
        if not self.on_ground:
            self.velocity_y += self.gravity * dt
            self.character_y += self.velocity_y * dt
        
        if self.character_y >= self.ground_y:
            self.character_y = self.ground_y
            self.velocity_y = 0
            self.on_ground = True
            self.is_jumping = False

        #self.check_platform_collision(platforms)
        colli,rec_top = self.check_platform_collision(platforms)
        if not colli:
            # No platform collision, apply gravity as player is in the air
            if self.character_y == (5 * TILE_SIZE - CHARACTER_HEIGHT* 2.5) * 3:
                pass
            elif self.character_y < (5 * TILE_SIZE - CHARACTER_HEIGHT* 2.5) * 3:
                self.on_ground = False
        else:
            # Collided with a platform
            self.character_y = rec_top - CHARACTER_HEIGHT * 2.5
            self.on_ground = True
            self.is_jumping = False
            self.velocity_y = 0 
        self.animation.update(dt)
        
        
    def check_platform_collision(self, platforms):
            # Create a rectangle for the player's current position
            player_rect = pygame.Rect(self.character_x, self.character_y, CHARACTER_WIDTH, CHARACTER_HEIGHT * 2.5)
            for platform_rect, _ in platforms:
                if player_rect.colliderect(platform_rect) and self.velocity_y > 0:
                    # Collision with the top of a platform while falling
                    #self.character_y = platform_rect.top - CHARACTER_HEIGHT * 2.5
                    #self.store_veloy = self.velocity_y
                    #self.velocity_y = 0
                    #self.on_ground = True
                    #self.is_jumping = False
                    return True, platform_rect.top
            
            return False, platform_rect.top
    def render(self, screen):
        char_img = self.animation.image
        if self.direction == "left":
            char_img = pygame.transform.flip(char_img, True, False)
        screen.blit(char_img, (self.character_x, self.character_y))
