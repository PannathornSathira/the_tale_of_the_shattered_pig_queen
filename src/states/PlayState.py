import random, pygame, sys
from src.states.BaseState import BaseState
from src.constants import *
from src.Dependency import *
from src.Player import Player
from src.Level import Level
from src.bosses.MedusaBoss import MedusaBoss
#import src.CommonRender as CommonRender

class PlayState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.player = Player()
        self.level = Level(area=3)
        self.level.CreateMap()
        self.boss = MedusaBoss(x=1100, y=100)

    def Enter(self, params):
        pass
    

    def update(self,  dt, events):
        if self.player.alive:
            self.player.update(dt, events, self.level.platforms, self.boss)
        self.level.update(dt, events)
        if self.boss.alive:
            self.boss.update(dt, self.player)

    def Exit(self):
        pass

    def render(self):
        self.level.render(self.screen)
        self.player.render(self.screen)
        self.boss.render(self.screen)
        if self.player.alive:
            self.render_text(f"Player Health: {self.player.health}", 20, 20)
        if self.boss.alive:
            self.render_text(f"Boss Health: {self.boss.health}", 20, 60)
            
    def render_text(self, text, x, y):
        """Render text at a given position."""
        text_surface = self.font.render(text, True, (0, 0, 0))  # Render text in black color
        self.screen.blit(text_surface, (x, y))
    def CheckVictory(self):
        pass
