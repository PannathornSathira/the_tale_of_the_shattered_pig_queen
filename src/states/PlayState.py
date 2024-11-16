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
        
        # Potion effects and levels
        self.potion_levels = POTION_LEVELS
        
        # Potion effect management
        self.potion_effects = {
            "health": {
                "active": False, "effect_timer": 0, "cooldown_timer": 0,
                "duration": 0, "cooldown": 15000
            },
            "damage": {
                "active": False, "effect_timer": 0, "cooldown_timer": 0,
                "duration": 5000, "cooldown": 30000
            },
            "swiftness": {
                "active": False, "effect_timer": 0, "cooldown_timer": 0,
                "duration": 5000, "cooldown": 30000
            },
        }
        self.health_potion_image = potion_dict["health"]
        self.damage_potion_image = potion_dict["damage"]
        self.swiftness_potion_image = potion_dict["swiftness"]
        
    def Enter(self, params):
        gMusic["main"].stop()
        self.level = params["level"]
        self.saved_values = read_saveFile()
        
        if self.level.area == 3:
            self.bg_image = background_dict["sea"]
        elif self.level.area == 2:
            self.bg_image = background_dict["forest"]
        elif self.level.area == 1:
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
            self.coin_scaling = 0.1
        elif self.difficulty == 2:
            self.coin_scaling = 0.2
        elif self.difficulty == 3:
            self.coin_scaling = 0.3
        elif self.difficulty == 4:
            self.coin_scaling = 0.4
        elif self.difficulty == 5:
            self.coin_scaling = 0.5
        self.boss_health = self.boss.health
        self.max_health = self.player.max_health
        self.max_boss_health = self.boss.health # For boss health bar

    def use_potion(self, potion):
        effect = self.potion_effects[potion]
        if effect["cooldown_timer"] > 0 or effect["active"]:
            return  # Prevent usage if cooldown is active or effect is ongoing
        
        level = self.saved_values[f"{potion}_potion_upgrade_level"]
        power = self.potion_levels[f"{potion.capitalize()} Potion"]["power"][level]
        
        if level == 0:
            return
        
        if potion == "health":
            self.player.health += power * self.max_health
            self.player.health = min(self.player.health, self.max_health)
        elif potion == "damage":
            self.player.bullet_damage *= power
        elif potion == "swiftness":
            self.player.movement_speed *= power
            self.player.default_move_speed *= power

        effect["active"] = True if potion != "health" else False
        effect["effect_timer"] = effect["duration"]
        effect["cooldown_timer"] = effect["cooldown"]
        gSounds["mc_potion"].play()

    def reset_potion_effect(self, potion):
        if potion == "damage":
            self.player.bullet_damage /= self.potion_levels["Damage Potion"]["power"][self.saved_values["damage_potion_upgrade_level"]]
        elif potion == "swiftness":
            self.player.movement_speed /= self.potion_levels["Swiftness Potion"]["power"][self.saved_values["swiftness_potion_upgrade_level"]]
            self.player.default_move_speed /= self.potion_levels["Swiftness Potion"]["power"][self.saved_values["swiftness_potion_upgrade_level"]]

    def update_potion_effects(self, dt):
        for potion, effect in self.potion_effects.items():
            if effect["effect_timer"] > 0:
                effect["effect_timer"] -= dt * 1000
                if effect["effect_timer"] <= 0:
                    effect["active"] = False
                    self.reset_potion_effect(potion)
            
            if effect["cooldown_timer"] > 0:
                effect["cooldown_timer"] -= dt * 1000
                if effect["cooldown_timer"] <= 0:
                    effect["cooldown_timer"] = 0

    def update(self, dt, events):
        if self.player.alive:
            self.player.update(dt, events, self.level.platforms, self.boss)
            self.update_potion_effects(dt)
        else:
            pygame.mixer.stop()
            save_values({
                "total_coins": self.total_coins,
            })
            for potion, effect in self.potion_effects.items():
                effect["cooldown_timer"] = 0
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
            })
            self.player.bullets = []
            if isinstance(self.boss, SandWormBoss):
                self.player.default_move_speed *= 2
            if self.level.area == 5:
                g_state_manager.Change("END", {
                    "play_check": True,
                  })
            else:
                g_state_manager.Change("WORLD_MAP", {
                    "player": self.player,
                    "completed_level": self.level.area
                })
            gMusic["victory"].play(maxtime=1800)
            
        # if self.damage_potion_active:
        #     self.damage_potion_timer -= dt * 1000  # Decrease timer
        #     if self.damage_potion_timer <= 0:
        #         # Reset player damage after potion effect ends
        #         self.player.bullet_damage /= self.power_scale_damage
        #         self.damage_potion_active = False
        #         print("Damage Potion effect has ended.")

        # if self.health_potion_active:
        #     self.health_potion_timer -= dt * 1000  # Decrease timer
        #     if self.health_potion_timer <= 0:
        #         # Reset player damage after potion effect ends
        #         self.health_potion_active = False
        #         print("Health Potion effect has ended.")
        
        
        # if self.swiftness_potion_active:
        #     self.swiftness_potion_timer -= dt * 1000  # Decrease timer
        #     if self.swiftness_potion_timer <= 0:
        #         # Reset player movement after potion effect ends
        #         self.player.movement_speed /= self.power_scale_swiftness
        #         self.player.default_move_speed /= self.power_scale_swiftness
        #         self.swiftness_potion_active = False
        #         print("Swiftness Potion effect has ended.")
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
                    })

                if event.key == pygame.K_a:
                    self.use_potion("health")
                elif event.key == pygame.K_s:
                    self.use_potion("damage")
                elif event.key == pygame.K_d:
                    self.use_potion("swiftness")

    def Exit(self):
        pass

    def render(self,screen):
        screen.blit(self.bg_image, (0, 0))
        
        self.level.render(screen)
        self.boss.render(screen)
        self.player.render(screen)
        if self.player.alive:
            render_text("Player HP:", 20, 10, self.font, screen)
            player_health_percentage = self.player.health / self.max_health
            health_color = (255, 0, 0)
            player_health_bar_width = int(200 * player_health_percentage)
            pygame.draw.rect(screen, health_color, (150, 10, player_health_bar_width, 20))
            pygame.draw.rect(screen, (255, 255, 255), (150, 10, 200, 20), 2)
        if self.boss.alive:
            render_text("Boss HP:", 20, 40, self.font, screen)
            boss_health_percentage = self.boss_health / self.max_boss_health
            boss_health_bar_width = int(200 * boss_health_percentage) 
            pygame.draw.rect(screen, (0, 0, 255), (150, 40, boss_health_bar_width, 20)) 
            pygame.draw.rect(screen, (255, 255, 255), (150, 40, 200, 20), 2)

        # Render potions and timers
        render_text(f"Coins: {int(self.total_coins)}", 20, 70, self.font, screen)
        self.render_potion_status(screen, "health", 20, 100)
        self.render_potion_status(screen, "damage", 145, 100)
        self.render_potion_status(screen, "swiftness", 270, 100)

    def render_potion_status(self, screen, potion, x, y):
        level = self.saved_values[f"{potion}_potion_upgrade_level"]
        potion_image = getattr(self, f"{potion}_potion_image")
        effect = self.potion_effects[potion]
        if level == 0:
            cooldown_time = "-"
        else:
            cooldown_time = int(effect["cooldown_timer"] / 1000) if effect["cooldown_timer"] > 0 else "Ready"
        render_text(f": {cooldown_time}", x + 35, y + 10, self.font, screen)
        screen.blit(potion_image, (x, y))
        
        
    def CheckVictory(self):
        pass
