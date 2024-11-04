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
        
        self.damage_potion_active = False
        self.damage_potion_timer = 0
        
        #self.health_potion_active = False
        #self.health_potion_timer = 0
        
        self.swiftness_potion_active = False
        self.swiftness_potion_timer = 0

    def Enter(self, params):
        self.level = params["level"]
        self.boss = params["boss"]
        self.player = params["player"]
        self.total_coins = params["total_coins"]
        self.difficulty = params["difficulty"]
        if self.difficulty == 1:
            self.coin_scaling = 10
        elif self.difficulty == 2:
            self.coin_scaling = 20
        elif self.difficulty == 3:
            self.coin_scaling = 50
        elif self.difficulty == 4:
            self.coin_scaling = 100
        elif self.difficulty == 5:
            self.coin_scaling = 200
        self.boss_health = self.boss.health
        self.max_health = self.player.health
        
        self.damage_potions = params.get("damage_potions", 0)
        self.health_potions = params.get("health_potions", 0)
        self.swiftness_potions = params.get("swiftness_potions", 0)

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
            
        if self.damage_potion_active:
            self.damage_potion_timer -= dt * 1000  # Decrease timer
            if self.damage_potion_timer <= 0:
                # Reset player damage after potion effect ends
                self.player.bullet_damage /= 1.1
                self.damage_potion_active = False
                print("Damage Potion effect has ended.")
        
        if self.swiftness_potion_active:
            self.swiftness_potion_timer -= dt * 1000  # Decrease timer
            if self.swiftness_potion_timer <= 0:
                # Reset player movement after potion effect ends
                self.player.movement_speed /= 1.1
                self.player.default_move_speed /= 1.1
                self.swiftness_potion_active = False
                print("Swiftness Potion effect has ended.")
        self.level.update(dt, events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    g_state_manager.Change("PAUSE", {
                        "level": self.level,
                        "boss": self.boss,
                        "player": self.player,
                        "total_coins": self.total_coins,
                        "difficulty": self.difficulty,
                        "damage_potions": self.damage_potions,
                        "health_potions": self.health_potions,
                        "swiftness_potions": self.swiftness_potions
                    })
                # Activate the damage potion by Press T
                if event.key == pygame.K_t and self.damage_potions > 0 and not self.damage_potion_active:
                   
                    self.damage_potions -= 1
                    self.player.bullet_damage *= 1.1  # Increase damage by 10%
                    self.damage_potion_active = True
                    self.damage_potion_timer = 10000  # Set the timer for 10 seconds
                
                # Activate the health potion by Press Y
                if event.key == pygame.K_y and self.health_potions > 0:
                    self.health_potions -= 1
                    self.player.health += 1.10 * self.max_health  # Increase health by 10% of max hp
                
                # Activate the health potion by Press U
                if event.key == pygame.K_u and self.swiftness_potions > 0 and not self.swiftness_potion_active:
                    self.swiftness_potions -= 1
                    self.player.movement_speed *= 1.1
                    self.player.default_move_speed *= 1.1
                    self.swiftness_potion_active = True
                    self.swiftness_potion_timer = 10000  # Set the timer for 10 seconds

    def Exit(self):
        pass

    def render(self,screen):
        self.boss.render(screen)
        self.level.render(screen)
        self.player.render(screen)
        if self.player.alive:
            render_text(f"Player Health: {self.player.health}", 20, 20, self.font, screen)
        if self.boss.alive:
            render_text(f"Boss Health: {self.boss.health}", 20, 60, self.font, screen)
            
        render_text(f"Total Coins: {self.total_coins}", 20, 100, self.font, screen)
        render_text(f"Damage Potions: {self.damage_potions}", 20, 140, self.font, screen)
        render_text(f"Health Potions: {self.health_potions}", 320, 140, self.font, screen)
        render_text(f"Swiftness Potions: {self.swiftness_potions}", 620, 140, self.font, screen)

        
        
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
