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
        self.bg_image = pygame.transform.scale( self.bg_image, (WIDTH, HEIGHT))
        self.total_coins = 0
        self.coin_scaling = 2  # Set a default coin scaling for the tutorial
        
        self.damage_potion_active = False
        self.damage_potion_timer = 0
        self.damage_potion_active_time = 10
        
        self.swiftness_potion_active = False
        self.swiftness_potion_timer = 0
        self.swiftness_potion_active_time = 10
        
        self.health_potion_active = False
        self.health_potion_timer = 0
        
        self.power_scale_swiftness = 1
        self.power_scale_damage = 1
        self.health_potion_image = potion_dict["health"]
        self.damage_potion_image = potion_dict["damage"]
        self.swiftness_potion_image = potion_dict["swiftness"]
        self.platform_lv = [[None for _ in range(8)] for _ in range(3)]
        # Set initial potion levels and counts
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

            if self.health_potion_active:
                self.health_potion_timer -= dt * 1000  # Decrease timer
                if self.health_potion_timer <= 0:
                    # Reset player damage after potion effect ends
                    self.health_potion_active = False
                    print("Health Potion effect has ended.")
            
            # Handle events
            for event in events:
                if event.type == pygame.KEYDOWN:

                    # Use health potion by pressing 'A'
                    if event.key == pygame.K_a and not self.health_potion_active:
                        level = self.saved_values["health_potion_upgrade_level"]
                        power_scale_health = self.potion_levels["Health Potion"]["power"][level]
                        #self.health_potions -= 1
                        self.player.health += power_scale_health * self.max_health
                        if self.player.health > self.max_health:
                            self.player.health = self.max_health
                        self.health_potion_active = True
                        self.health_potion_timer = 10000
                        gSounds["mc_potion"].play()

                    # Use health potion by pressing 'S'
                    if event.key == pygame.K_s and not self.damage_potion_active:
                        level = self.saved_values["damage_potion_upgrade_level"]
                        self.power_scale_damage = self.potion_levels["Damage Potion"]["power"][level]
                        #self.damage_potions -= 1
                        self.player.bullet_damage *= self.power_scale_damage
                        self.damage_potion_active = True
                        self.damage_potion_timer = 60000
                        gSounds["mc_potion"].play()


                    # Use swiftness potion by pressing 'D'
                    if event.key == pygame.K_d and not self.swiftness_potion_active:
                        level = self.saved_values["swiftness_potion_upgrade_level"]
                        self.power_scale_swiftness = self.potion_levels["Swiftness Potion"]["power"][level]
                        # self.swiftness_potions -= 1
                        self.player.movement_speed *= self.power_scale_swiftness
                        self.player.default_move_speed *= self.power_scale_swiftness
                        self.swiftness_potion_active = True
                        self.swiftness_potion_timer = 30000
                        gSounds["mc_potion"].play()
                    
                    if event.key == pygame.K_RETURN:
                        g_state_manager.Change("SHOP", {})

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))
        self.player.render(screen)
        self.level_tutor.render(screen)
        # Render player health
        render_text("Player HP:", 20, 20, self.font, screen)
        player_health_percentage = self.player.health / self.max_health
        player_health_bar_width = int(200 * player_health_percentage)
        pygame.draw.rect(screen, (255, 0, 0), (150, 22, player_health_bar_width, 20))
        pygame.draw.rect(screen, (255, 255, 255), (150, 22, 200, 20), 2)

        # Render potions and coins
        render_text(f"Coins: {self.total_coins}", 20, 60, self.font, screen)
        
        remaining_time_health = int(self.health_potion_timer / 1000)
        if remaining_time_health == 0:
            remaining_time_health = "Ready"
        render_text(f": {remaining_time_health}", 55, 110, self.font, screen)
        screen.blit(self.health_potion_image, (20, 100))
        
        remaining_time_damage = int(self.damage_potion_timer / 1000)  # Convert to seconds
        if remaining_time_damage == 0:
            remaining_time_damage = "Ready"
        render_text(f": {remaining_time_damage}", 180, 110, self.font, screen)
        screen.blit(self.damage_potion_image, (145, 100))
        
        remaining_time_swiftness = int(self.swiftness_potion_timer / 1000)
        if remaining_time_swiftness == 0:
            remaining_time_swiftness = "Ready"
        render_text(f": {remaining_time_swiftness}", 305, 110, self.font, screen)
        screen.blit(self.swiftness_potion_image, (270, 100))

    def Exit(self):
        pass
