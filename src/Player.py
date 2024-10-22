from src.constants import *
from src.Util import SpriteManager
import pygame


class Player:
    def __init__(self):
        self.character_x = WIDTH / 2 - (CHARACTER_WIDTH) / 2
        self.character_y = (5 * TILE_SIZE - CHARACTER_HEIGHT) * 3
        self.direction = "front"  # left right front
        self.sprite_collection = SpriteManager().spriteCollection
        self.animation = self.sprite_collection["character_front"].animation

    def update(self, dt, events):
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_LEFT]:
            self.direction = "left"
            self.animation = self.sprite_collection["character_walk_right"].animation
        elif pressedKeys[pygame.K_RIGHT]:
            self.direction = "right"
            self.animation = self.sprite_collection["character_walk_right"].animation
        else:
            self.direction = "front"
            self.animation = self.sprite_collection["character_front"].animation

        if self.direction == "left":
            self.character_x -= CHARACTER_MOVE_SPEED * dt
        elif self.direction == "right":
            self.character_x += CHARACTER_MOVE_SPEED * dt

        self.animation.update(dt)

    def render(self, screen):
        char_img = self.animation.image
        if self.direction == "left":
            char_img = pygame.transform.flip(char_img, True, False)
        screen.blit(char_img, (self.character_x, self.character_y))
