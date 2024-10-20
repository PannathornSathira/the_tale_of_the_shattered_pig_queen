import pygame
from src.constants import *
from src.Dependency import *

class Ball:
    def __init__(self, skin=1):
        self.width = 24
        self.height = 24

        self.dx = 0
        self.dy = 0

        self.Reset()

        self.skin = skin
        self.image = ball_image_list[self.skin]
        #self.rect = pygame.Rect(self.x, self.y, self.width, self.height)



    def Collides(self, target):
        if self.rect.x > target.rect.x + target.width or target.rect.x >self.rect.x + self.width:
            return False

        if self.rect.y > target.rect.y + target.height or target.rect.y > self.rect.y + self.height:
            return False

        return True

    def Reset(self):
        self.x = WIDTH/2 - 6
        self.y = HEIGHT/2 - 6
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.dx = 0
        self.dy = 0


    def update(self, dt):
        self.rect.x += self.dx * dt
        self.rect.y += self.dy * dt

        #A ball hits a left wall
        if self.rect.x <= 0:
            self.rect.x = 0
            self.dx = -self.dx
            gSounds['wall-hit'].play()

        # A ball hits a right wall
        if self.rect.x >= WIDTH - 24:
            self.rect.x = WIDTH - 24
            self.dx = -self.dx
            gSounds['wall-hit'].play()

        # A ball hits a upper wall
        if self.rect.y <= 0:
            self.rect.y = 0
            self.dy = -self.dy
            gSounds['wall-hit'].play()

    def render(self, screen):
        # rect.x rect.y is center?? or is it square box
        # rect = self.image.get_rect()
        # rect.center = (self.rect.x, self.rect.y)
        screen.blit(self.image, (self.rect.x, self.rect.y))
