import pygame
from src.Dependency import *

class Brick:
    def __init__(self, x, y):
        self.tier=0   #n->0
        self.color=1  #5->1

        self.x=x
        self.y=y

        self.width = 96
        self.height = 48

        self.alive = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def Hit(self):
        gSounds['brick-hit2'].play()

        if self.tier > 0:
            if self.color == 1:
                self.tier = self.tier - 1
                self.color = 5
            else:
                self.color = self.color - 1

        else:
            if self.color == 1:
                self.alive = False
            else:
                self.color = self.color - 1

        if not self.alive:
            gSounds['brick-hit1'].play()

    def update(self, dt):
        pass

    def render(self, screen):
        if self.alive:
            screen.blit(brick_image_list[((self.color-1)*4)+self.tier], (self.rect.x, self.rect.y))