# import random, pygame, sys
# from src.constants import *
from src.Dependency import *
# from src.Player import Player
# from src.Level import Level
# from src.bosses.MedusaBoss import MedusaBoss
# import json
# from src.Util import *
#import src.CommonRender as CommonRender

class PlayState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.player = Player()
        self.level = None
        self.boss = None
        self.total_coins = 0
        self.boss_health = 0
        self.coin_scaling = 0

    def Enter(self, params):
        self.level = params["level"]
        self.boss = params["boss"]
        self.player = params["player"]
        self.total_coins = params["total_coins"]
        difficulty = params["difficulty"]
        if difficulty == 1:
            self.coin_scaling = 10
        elif difficulty == 2:
            self.coin_scaling = 20
        elif difficulty == 3:
            self.coin_scaling = 50
        elif difficulty == 4:
            self.coin_scaling = 100
        elif difficulty == 5:
            self.coin_scaling = 200
        self.boss_health = self.boss.health

    def update(self, dt, events):
        if self.player.alive:
            self.player.update(dt, events, self.level.platforms, self.boss)
        else:
            self.save_coins()
            g_state_manager.Change("MAIN_MENU", {})

        if self.boss.alive:
            self.boss.update(dt, self.player, self.level.platforms)
            if self.boss.health < self.boss_health:
                self.total_coins += (self.boss_health - self.boss.health) * self.coin_scaling
            self.boss_health = self.boss.health
        else:
            self.save_coins()
            g_state_manager.Change("WORLD_MAP", {
                "completed_level": self.level.area
            })

        self.level.update(dt, events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    g_state_manager.Change("PAUSE", {
                        "level": self.level,
                        "boss": self.boss,
                        "player": self.player,
                        "total_coins": self.total_coins
                    })

    def Exit(self):
        pass

    def render(self,screen):
        self.level.render(screen)
        self.boss.render(screen)
        self.player.render(screen)
        if self.player.alive:
            render_text(f"Player Health: {self.player.health}", 20, 20, self.font, screen)
        if self.boss.alive:
            render_text(f"Boss Health: {self.boss.health}", 20, 60, self.font, screen)
            
        render_text(f"Total Coins: {self.total_coins}", 20, 100, self.font, screen)
        
        
    def CheckVictory(self):
        pass
    
    def save_coins(self):
        """Save coins to the player's total coins in saveFile.json."""
        try:
            with open("saveFile.json", "r+") as file:
                data = json.load(file)
                data["total_coins"] = self.total_coins
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
        except FileNotFoundError:
            print("saveFile.json not found.")
        except KeyError:
            print("total_coins key not found in saveFile.json.")
