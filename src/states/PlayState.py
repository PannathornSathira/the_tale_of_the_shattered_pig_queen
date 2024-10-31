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
        self.level = None
        self.boss = MedusaBoss(x=1100, y=100)

    def Enter(self, params):
        self.level = params["level"]
        self.boss = params["boss"]
        self.player = params["player"]

    def update(self,  dt, events):
        if self.player.alive:
            self.player.update(dt, events, self.level.platforms, self.boss)
            
        self.level.update(dt, events)
        
        if self.boss.alive:
            self.boss.update(dt, self.player, self.level.platforms)  
        else:
            g_state_manager.Change("WORLD_MAP", {})

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    g_state_manager.Change("PAUSE", {
                        "level": self.level,
                        "boss": self.boss,
                        "player": self.player
                    })

    def Exit(self):
        pass

    def render(self,screen):
        self.level.render(screen)
        self.player.render(screen)
        self.boss.render(screen)
        if self.player.alive:
            self.render_text(f"Player Health: {self.player.health}", 20, 20, screen)
        if self.boss.alive:
            self.render_text(f"Boss Health: {self.boss.health}", 20, 60, screen)
            
    def render_text(self, text, x, y, screen):
        """Render text at a given position."""
        text_surface = self.font.render(text, True, (0, 0, 0))  # Render text in black color
        screen.blit(text_surface, (x, y))
    def CheckVictory(self):
        pass
