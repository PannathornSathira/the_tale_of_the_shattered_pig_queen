import pygame
from src.Dependency import *
from src.resources import *
from src.Util import *

class TutorialState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        # self.boss = BaseBoss()
        self.player = Player()
        self.level_tutor = Level(area=3)
        self.level_tutor.CreateMap()
        self.bg_image = background_dict["sky"]  # Set a default background for the tutorial
        self.total_coins = 0
        self.coin_scaling = 2  # Set a default coin scaling for the tutorial
        self.damage_potion_active = False
        self.damage_potion_timer = 0
        self.swiftness_potion_active = False
        self.swiftness_potion_timer = 0
        self.power_scale_swiftness = 1
        self.power_scale_damage = 1
        self.health_potion_image = potion_dict["health"]
        self.damage_potion_image = potion_dict["damage"]
        self.swiftness_potion_image = potion_dict["swiftness"]
        self.platform_lv = [[None for _ in range(8)] for _ in range(3)]
        # Set initial potion levels and counts
        self.damage_potions = 3
        self.health_potions = 3
        self.swiftness_potions = 3
        self.max_health = self.player.max_health
        self.player.shotgun_ability = True
        self.player.jump_ability = True
        # Manually set potion upgrade levels for the tutorial
        self.potion_levels = {
            "Health Potion": {
                "power": [0, 1.1, 1.2, 1.3, 1.4, 1.5]
            },
            "Damage Potion": {
                "power": [0, 1.1, 1.15, 1.2, 1.25, 1.3]
            },
            "Swiftness Potion": {
                "power": [0, 1.1, 1.15, 1.2, 1.25, 1.3]
            }
        }
        self.saved_values = {
            "damage_potion_upgrade_level": 2,
            "health_potion_upgrade_level": 2,
            "swiftness_potion_upgrade_level": 2
        }

    def Enter(self, params):
        
        gMusic["main"].fadeout(1000)  # Stop any other music
        #gMusic["tutorial"].play(-1)  # Play tutorial music

    def update(self, dt, events):
        if self.player.alive:
            self.player.update(dt, events, self.level_tutor.platforms, self.boss)  # Update player without boss or platforms

            # Potion timer handling
            if self.damage_potion_active:
                self.damage_potion_timer -= dt * 1000
                if self.damage_potion_timer <= 0:
                    self.player.bullet_damage /= self.power_scale_damage
                    self.damage_potion_active = False

            if self.swiftness_potion_active:
                self.swiftness_potion_timer -= dt * 1000
                if self.swiftness_potion_timer <= 0:
                    self.player.movement_speed /= self.power_scale_swiftness
                    self.player.default_move_speed /= self.power_scale_swiftness
                    self.swiftness_potion_active = False

            # Handle events
            for event in events:
                if event.type == pygame.KEYDOWN:

                    # Use damage potion by pressing 'A'
                    if event.key == pygame.K_a and self.damage_potions > 0 and not self.damage_potion_active:
                        level = self.saved_values["damage_potion_upgrade_level"]
                        self.power_scale_damage = self.potion_levels["Damage Potion"]["power"][level]
                        self.damage_potions -= 1
                        self.player.bullet_damage *= self.power_scale_damage
                        self.damage_potion_active = True
                        self.damage_potion_timer = 10000

                    # Use health potion by pressing 'S'
                    if event.key == pygame.K_s and self.health_potions > 0:
                        level = self.saved_values["health_potion_upgrade_level"]
                        power_scale_health = self.potion_levels["Health Potion"]["power"][level]
                        self.health_potions -= 1
                        self.player.health += power_scale_health * self.max_health
                        if self.player.health > self.max_health:
                            self.player.health = self.max_health

                    # Use swiftness potion by pressing 'D'
                    if event.key == pygame.K_d and self.swiftness_potions > 0 and not self.swiftness_potion_active:
                        level = self.saved_values["swiftness_potion_upgrade_level"]
                        self.power_scale_swiftness = self.potion_levels["Swiftness Potion"]["power"][level]
                        self.swiftness_potions -= 1
                        self.player.movement_speed *= self.power_scale_swiftness
                        self.player.default_move_speed *= self.power_scale_swiftness
                        self.swiftness_potion_active = True
                        self.swiftness_potion_timer = 10000
                    
                    if event.key == pygame.K_RETURN:
                        g_state_manager.Change("SHOP", {})

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))
        self.player.render(screen)
        self.level_tutor.render(screen)
        # Render player health
        render_text("Player HP:", 20, 0, self.font, screen)
        player_health_percentage = self.player.health / self.max_health
        player_health_bar_width = int(200 * player_health_percentage)
        pygame.draw.rect(screen, (255, 0, 0), (150, 2, player_health_bar_width, 20))
        pygame.draw.rect(screen, (255, 255, 255), (150, 2, 200, 20), 2)

        # Render potions and coins
        render_text(f"Coins: {self.total_coins}", 20, 80, self.font, screen)
        render_text(f": {self.damage_potions}", 55, 130, self.font, screen)
        screen.blit(self.damage_potion_image, (20, 120))
        
        render_text(f": {self.health_potions}", 120, 130, self.font, screen)
        screen.blit(self.health_potion_image, (90, 120))

        render_text(f": {self.swiftness_potions}", 190, 130, self.font, screen)
        screen.blit(self.swiftness_potion_image, (160, 120))

        # Show potion timers
        if self.damage_potion_active:
            remaining_time = int(self.damage_potion_timer / 1000)
            render_text(f"Damage Potion Time: {remaining_time}s", 20, 180, self.font, screen)
        if self.swiftness_potion_active:
            remaining_time = int(self.swiftness_potion_timer / 1000)
            render_text(f"Swiftness Potion Time: {remaining_time}s", 320, 180, self.font, screen)

    def Exit(self):
        pass
