# import random, pygame, sys
# from src.constants import *
from src.Dependency import *
from src.resources import *
from src.Util import *

class PlayState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.player = Player()
        self.level = None
        self.boss = None
        self.bg_image = None
        self.total_coins = 0
        self.boss_health = 0
        self.coin_scaling = 0
        
        self.damage_potion_active = False
        self.damage_potion_timer = 0
        
        self.health_potion_active = False
        self.health_potion_timer = 0
        
        self.swiftness_potion_active = False
        self.swiftness_potion_timer = 0
        
        self.power_scale_swiftness=1
        self.power_scale_damage=1
        
        self.health_potion_image = potion_dict["health"]
        
        self.damage_potion_image = potion_dict["damage"]
        
        self.swifness_potion_image = potion_dict["swiftness"]
        # Potion levels and costs
        self.potion_levels = {
            "Health Potion": {
                "power": [0, 1.1, 1.2, 1.3, 1.4, 1.5]
            },
            "Damage Potion": {
                "power": [0, 1.1, 1.15, 1.2, 1.25, 1.3, 30],
            },
            "Swiftness Potion": {
                "power": [0, 1.1, 1.15, 1.2, 1.25, 1.3, 30],
            }
        }
        
    def Enter(self, params):
        gMusic["main"].stop()
        self.level = params["level"]
        self.saved_values = read_saveFile()
        
        if self.level.area == 1:
            self.bg_image = background_dict["sea"]
        elif self.level.area == 2:
            self.bg_image = background_dict["forest"]
        elif self.level.area == 3:
            self.bg_image = background_dict["sky"]
        elif self.level.area == 4:
            self.bg_image = background_dict["desert"]
        elif self.level.area == 5:
            self.bg_image = background_dict["castle"]
        self.boss = params["boss"]
        
        if pygame.mixer.music.get_busy():
            # Check if music is actually paused before calling unpause
            if pygame.mixer.get_pos() == -1:
                pygame.mixer.music.unpause()
        else:
            if isinstance(self.boss, KrakenBoss):
                gMusic["kraken"].play(-1)
            elif isinstance(self.boss, GreatSharkBoss):
                gMusic["greatshark"].play(-1)
            elif isinstance(self.boss, MedusaBoss):
                gMusic["medusa"].play(-1)
            elif isinstance(self.boss, BlackWidowBoss):
                gMusic["blackwidow"].play(-1)
            elif isinstance(self.boss, BlueDragonBoss):
                gMusic["bluedragon"].play(-1)
            elif isinstance(self.boss, TornadoFiendBoss):
                gMusic["tornadofiend"].play(-1)
            elif isinstance(self.boss, KingMummyBoss):
                gMusic["mummy"].play(-1)
            elif isinstance(self.boss, SandWormBoss):
                gMusic["sandworm"].play(-1)
            elif isinstance(self.boss, WraithBoss):
                gMusic["wraith"].play(-1)
            
        self.player = params["player"]
        self.total_coins = params["total_coins"]
        self.difficulty = params["difficulty"]
        if self.difficulty == 1:
            self.coin_scaling = 2
        elif self.difficulty == 2:
            self.coin_scaling = 4
        elif self.difficulty == 3:
            self.coin_scaling = 6
        elif self.difficulty == 4:
            self.coin_scaling = 8
        elif self.difficulty == 5:
            self.coin_scaling = 10
        self.boss_health = self.boss.health
        self.max_health = self.player.max_health
        self.max_boss_health = self.boss.health # For boss health bar
        self.damage_potions = params.get("damage_potions", 0)
        self.health_potions = params.get("health_potions", 0)
        self.swiftness_potions = params.get("swiftness_potions", 0)


    def update(self, dt, events):
        if self.player.alive:
            self.player.update(dt, events, self.level.platforms, self.boss)
        else:
            pygame.mixer.stop()
            save_values({
                "total_coins": self.total_coins,
                "damage_potions": self.damage_potions,
                "health_potions": self.health_potions,
                "swiftness_potions": self.swiftness_potions
            })
            g_state_manager.Change("SHOP", {})

        if self.boss.alive:
            self.boss.update(dt, self.player, self.level.platforms)
            if self.boss.health < self.boss_health:
                self.total_coins += (self.boss_health - self.boss.health) * self.coin_scaling
            self.boss_health = self.boss.health
        else:
            pygame.mixer.stop()
            save_values({
                "total_coins": self.total_coins,
                "damage_potions": self.damage_potions,
                "health_potions": self.health_potions,
                "swiftness_potions": self.swiftness_potions
            })
            self.player.bullets = []
            if self.level.area == 5:
                g_state_manager.Change("END", {
                    "play_check": True,
                  })
                gMusic["victory"].play(-1)
            else:
                g_state_manager.Change("WORLD_MAP", {
                    "player": self.player,
                    "completed_level": self.level.area
                })
                gMusic["victory"].play(maxtime=1800)
            
        if self.damage_potion_active:
            self.damage_potion_timer -= dt * 1000  # Decrease timer
            if self.damage_potion_timer <= 0:
                # Reset player damage after potion effect ends
                self.player.bullet_damage /= self.power_scale_damage
                self.damage_potion_active = False
                print("Damage Potion effect has ended.")

        if self.health_potion_active:
            self.health_potion_timer -= dt * 1000  # Decrease timer
            if self.health_potion_timer <= 0:
                # Reset player damage after potion effect ends
                self.health_potion_active = False
                print("Health Potion effect has ended.")
        
        
        if self.swiftness_potion_active:
            self.swiftness_potion_timer -= dt * 1000  # Decrease timer
            if self.swiftness_potion_timer <= 0:
                # Reset player movement after potion effect ends
                self.player.movement_speed /= self.power_scale_swiftness
                self.player.default_move_speed /= self.power_scale_swiftness
                self.swiftness_potion_active = False
                print("Swiftness Potion effect has ended.")
        self.level.update(dt, events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.pause()
                    g_state_manager.Change("PAUSE", {
                        "prev_state": "play",
                        "level": self.level,
                        "boss": self.boss,
                        "player": self.player,
                        "total_coins": self.total_coins,
                        "difficulty": self.difficulty,
                        "damage_potions": self.damage_potions,
                        "health_potions": self.health_potions,
                        "swiftness_potions": self.swiftness_potions
                    })
                # Activate the damage potion by Press A
                if event.key == pygame.K_a and self.damage_potions > 0 and not self.damage_potion_active:
                    current_potion_level = self.saved_values["damage_potion_upgrade_level"]
                    self.power_scale_damage = self.potion_levels["Damage Potion"]["power"][current_potion_level]
                    #self.damage_potions -= 1
                    self.player.bullet_damage *= self.power_scale_damage  # Increase damage by 10%
                    self.damage_potion_active = True
                    self.damage_potion_timer = 60000  # Set the timer for 10 seconds
                    gSounds["mc_potion"].play()
                
                # Activate the health potion by Press S
                if event.key == pygame.K_s and self.health_potions > 0 and not self.health_potion_active:
                    current_potion_level = self.saved_values["health_potion_upgrade_level"]
                    power_scale_health = self.potion_levels["Health Potion"]["power"][current_potion_level]
                    #self.health_potions -= 1
                    self.player.health += power_scale_health * self.max_health  # Increase health by 10% of max hp
                    self.health_potion_active = True
                    self.health_potion_timer = 60000
                    if self.player.health > self.max_health:
                        self.player.health = self.max_health
                    gSounds["mc_potion"].play()
                
                # Activate the health potion by Press D
                if event.key == pygame.K_d and self.swiftness_potions > 0 and not self.swiftness_potion_active:
                    current_potion_level = self.saved_values["swiftness_potion_upgrade_level"]
                    self.power_scale_swiftness = self.potion_levels["Swiftness Potion"]["power"][current_potion_level]
                    #self.swiftness_potions -= 1
                    self.player.movement_speed *= self.power_scale_swiftness
                    self.player.default_move_speed *= self.power_scale_swiftness
                    self.swiftness_potion_active = True
                    self.swiftness_potion_timer = 60000  # Set the timer for 10 seconds
                    gSounds["mc_potion"].play()

    def Exit(self):
        pass

    def render(self,screen):
        screen.blit(self.bg_image, (0, 0))
        
        self.level.render(screen)
        self.boss.render(screen)
        self.player.render(screen)
        if self.player.alive:
            render_text("Player HP:", 20, 0, self.font, screen)
            player_health_percentage = self.player.health / self.max_health
            player_health_bar_width = int(200 * player_health_percentage)  # Adjust the width as needed
            pygame.draw.rect(screen, (255, 0, 0), (150, 2, player_health_bar_width, 20))  # Red health bar
            pygame.draw.rect(screen, (255, 255, 255), (150, 2, 200, 20), 2)
        if self.boss.alive:
            render_text("Boss HP:", 20, 40, self.font, screen)
            boss_health_percentage = self.boss_health / self.max_boss_health
            boss_health_bar_width = int(200 * boss_health_percentage) 
            pygame.draw.rect(screen, (0, 0, 255), (150, 40, boss_health_bar_width, 20)) 
            pygame.draw.rect(screen, (255, 255, 255), (150, 40, 200, 20), 2)
            
        render_text(f"Coins: {self.total_coins}", 20, 80, self.font, screen)
        
        remaining_time_damage = int(self.damage_potion_timer / 1000)  # Convert to seconds
        render_text(f": {remaining_time_damage}", 55, 130, self.font, screen)
        screen.blit(self.damage_potion_image, (20, 120))
        #render_text(f"Health Potions: {self.health_potions}", 320, 120, self.font, screen)
        
        remaining_time_health = int(self.health_potion_timer / 1000) 
        render_text(f": {remaining_time_health}", 130, 130, self.font, screen)
        screen.blit(self.health_potion_image, (100, 120))
        
        remaining_time_swiftness = int(self.swiftness_potion_timer / 1000)
        render_text(f": {remaining_time_swiftness}", 210, 130, self.font, screen)
        screen.blit(self.swifness_potion_image, (180, 120))
        
        
    def CheckVictory(self):
        pass
