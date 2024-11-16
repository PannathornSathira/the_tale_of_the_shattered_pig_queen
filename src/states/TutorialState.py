import pygame
from src.Dependency import *
from src.resources import *
from src.Util import *

class TutorialState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.boss = BaseBoss(x=-100, y=-100, width=0, height=0)
        self.player = Player()
        self.level_tutor = Level(area=1)
        self.level_tutor.CreateMap()
        self.bg_image = background_dict["sky_tutorial"]  # Set a default background for the tutorial
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        self.total_coins = 0
        
        self.max_health = self.player.max_health
        self.player.shotgun_ability = True
        self.player.jump_ability = True
        
        # Potion effects and levels
        self.potion_levels = POTION_LEVELS
        self.saved_values = {
            "damage_potion_upgrade_level": 2,
            "health_potion_upgrade_level": 2,
            "swiftness_potion_upgrade_level": 2,
        }
        
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
        gMusic["main"].fadeout(1000)  # Stop any other music
        # gMusic["tutorial"].play(-1)  # Play tutorial music

    def use_potion(self, potion):
        effect = self.potion_effects[potion]
        if effect["cooldown_timer"] > 0 or effect["active"]:
            return  # Prevent usage if cooldown is active or effect is ongoing
        
        level = self.saved_values[f"{potion}_potion_upgrade_level"]
        power = self.potion_levels[f"{potion.capitalize()} Potion"]["power"][level]
        
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
            self.player.update(dt, events, self.level_tutor.platforms, self.boss)
            self.update_potion_effects(dt)

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.use_potion("health")
                    elif event.key == pygame.K_s:
                        self.use_potion("damage")
                    elif event.key == pygame.K_d:
                        self.use_potion("swiftness")
                    elif event.key == pygame.K_RETURN:
                        g_state_manager.Change("SHOP", {})

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))
        self.player.render(screen)
        self.level_tutor.render(screen)
        
        # Render player health bar
        render_text("Player HP:", 20, 20, self.font, screen)
        player_health_percentage = self.player.health / self.max_health
        health_color = (255, 0, 0)
        player_health_bar_width = int(200 * player_health_percentage)
        pygame.draw.rect(screen, health_color, (150, 22, player_health_bar_width, 20))
        pygame.draw.rect(screen, (255, 255, 255), (150, 22, 200, 20), 2)

        # Render potions and timers
        render_text(f"Coins: {int(self.total_coins)}", 20, 60, self.font, screen)
        self.render_potion_status(screen, "health", 20, 100)
        self.render_potion_status(screen, "damage", 145, 100)
        self.render_potion_status(screen, "swiftness", 270, 100)

    def render_potion_status(self, screen, potion, x, y):
        potion_image = getattr(self, f"{potion}_potion_image")
        effect = self.potion_effects[potion]
        cooldown_time = int(effect["cooldown_timer"] / 1000) if effect["cooldown_timer"] > 0 else "Ready"
        render_text(f": {cooldown_time}", x + 35, y + 10, self.font, screen)
        screen.blit(potion_image, (x, y))

    def Exit(self):
        pass
