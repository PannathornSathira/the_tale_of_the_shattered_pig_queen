from src.Dependency import *
from src.resources import *
from src.constants import *
from src.Util import *

class MapSelectState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.bg_image = pygame.image.load("./graphics/Backgrounds/main_map.PNG")
        self.map_areas = [
            pygame.Rect(400, 70, 200, 150),  # Area 1
            pygame.Rect(850, 130, 200, 150),  # Area 2
            pygame.Rect(630, 400, 200, 150),  # Area 3
            pygame.Rect(280, 480, 200, 150),  # Area 4
            pygame.Rect(970, 500, 200, 150),  # Area 5 (Final Boss)
            pygame.Rect(80, 80, 200, 150),  # Shop (End Journey)
        ]
        
        # Initialize the player character
        self.character = pygame.Rect(100, 100, 60, 85)  # Character's starting position and size
        self.character_animation = sprite_collection["king_select_map"].animation
        self.character_direction = "right"
        self.character_speed = 5  # Speed of the character movement
        self.selected_area_index = None

        # Other attributes
        self.start_game = False
        self.go_to_shop = False
        self.boss_spawn_x = 1100
        self.boss_spawn_y = 100
        self.completed_levels = []  # Track completed levels
        self.difficulty = len(self.completed_levels) + 1
        
        self.health_potion_image = potion_dict["health"]
        
        self.damage_potion_image = potion_dict["damage"]
        
        self.swifness_potion_image = potion_dict["swiftness"]
    
    def Exit(self):
        gMusic["map"].fadeout(1000)

    def Enter(self, params):
        self.saved_values = read_saveFile()
        self.player = params.get("player")
        if not self.player:
            self.player = Player()
            # Configure player based on save file
            self.player.health = self.saved_values["health"]
            self.player.max_health = self.saved_values["health"]
            self.player.defense = self.saved_values["defense"]
            if self.saved_values["jump"] == 0:
                self.player.jump_ability = False
            else:
                self.player.jump_ability = True
                self.player.jump_scaling = self.saved_values["jump"]
            
            if self.saved_values["shotgun"] == 0:
                self.player.shotgun_ability = False
            else:
                self.player.shotgun_ability = True
                self.player.shotgun_damage_scale = self.saved_values["shotgun"]
                
            self.player.default_move_speed = self.saved_values["movement_speed"] * CHARACTER_MOVE_SPEED
            self.player.bullet_damage = self.saved_values["bullet_damage"]
            
            self.character.x = 100
            self.character.y = 100
            
        self.slow_damage_boss = self.saved_values["boss_damage_speed"]
        self.player.revert_to_default()
        self.player.reset_position()

        # Update completed levels
        self.complete_level = params.get("completed_level")
        completed_levels = params.get("completed_levels")
        if self.complete_level:
            self.completed_levels.append(self.complete_level)
            self.difficulty = len(self.completed_levels) + 1
        elif not completed_levels:
            self.completed_levels = []
            self.difficulty = 1
        else:
            self.completed_levels = completed_levels
        
        gMusic["map"].play(-1)

    def update(self, dt, events):
        # Update character position based on keypresses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.character.y -= self.character_speed
            if self.character.y <= 0:
                self.character.y = 0
        if keys[pygame.K_DOWN]:
            self.character.y += self.character_speed
            if self.character.y + self.character.height >= HEIGHT:
                self.character.y = HEIGHT - self.character.height
        if keys[pygame.K_LEFT]:
            self.character.x -= self.character_speed
            self.character_direction = "left"
            if self.character.x <= 0:
                self.character.x = 0
        if keys[pygame.K_RIGHT]:
            self.character.x += self.character_speed
            self.character_direction = "right"
            if self.character.x + self.character.width >= WIDTH:
                self.character.x = WIDTH - self.character.width

        # Check if player character collides with any map area
        for index, area in enumerate(self.map_areas):
            if self.character.colliderect(area):
                self.selected_area_index = index
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        # Trigger area selection based on the current index
                        if index < 4 and index + 1 not in self.completed_levels:
                            self.start_level(index + 1, area)
                        elif index == 4 and all(lvl in self.completed_levels for lvl in range(1, 5)):
                            self.start_level(5, area)  # Start the final boss level
                        elif index == 5:
                            g_state_manager.Change("PAUSE", {
                                "prev_state": "map",
                                "player": self.player,
                                "total_coins": self.saved_values["total_coins"],
                                "completed_levels": self.completed_levels
                            })
                break
        else:
            self.selected_area_index = None

    def start_level(self, area_index, area_rect):
        level = Level(area=area_index)
        level.CreateMap()
        boss = self.spawn_boss(area=area_index)
        g_state_manager.Change("PLAY", {
            "level": level,
            "boss": boss,
            "player": self.player,
            "difficulty": self.difficulty,
            "total_coins": self.saved_values["total_coins"],
        })
        
    def spawn_boss(self, area):
        if self.difficulty == 1:
            health = 2000
            damage = 12
        elif self.difficulty == 2:
            health = 2500
            damage = 14
        elif self.difficulty == 3:
            health = 3000
            damage = 16
        elif self.difficulty == 4:
            health = 3500
            damage = 18
        elif self.difficulty == 5:
            health = 4000
            damage = 20
            
        if area == 3:
            return random.choice([KrakenBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage, damage_speed_scaling=self.slow_damage_boss), GreatSharkBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage, damage_speed_scaling=self.slow_damage_boss)])
        elif area == 2:
            return random.choice([BlackWidowBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage, damage_speed_scaling=self.slow_damage_boss), MedusaBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage, damage_speed_scaling=self.slow_damage_boss)])
        elif area == 1:
            return random.choice([BlueDragonBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage, damage_speed_scaling=self.slow_damage_boss), TornadoFiendBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage, damage_speed_scaling=self.slow_damage_boss)])
        elif area == 4:
            return random.choice([KingMummyBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage, damage_speed_scaling=self.slow_damage_boss), SandWormBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage, damage_speed_scaling=self.slow_damage_boss)])
        elif area == 5:
            return WraithBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage, damage_speed_scaling=self.slow_damage_boss)

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))

        # Draw the character
        char_img = self.character_animation.image
        char_img = pygame.transform.scale(char_img, (self.character.width, self.character.height))
        if self.character_direction == "left":
            char_img = pygame.transform.flip(char_img, True, False)
        screen.blit(char_img, (self.character.x, self.character.y))

        
        
        # Draw each map area with color based on its status
        for index, area in enumerate(self.map_areas):
            color = (0, 255, 0) if index == self.selected_area_index else (255, 0, 0)
            if index < 4 and index + 1 in self.completed_levels:
                color = (128, 128, 128)  # Gray if completed
            elif index == 4 and not all(lvl in self.completed_levels for lvl in range(1, 5)):
                color = (128, 128, 128)  # Gray if locked
            elif index == 5:
                color = (0, 255, 0) if index == self.selected_area_index else (0, 128, 128)
            else:
                color = (0, 255, 0) if index == self.selected_area_index else (255, 0, 0)

            s = pygame.Surface((area.width, area.height))
            s.set_alpha(170)
            s.fill(color)
            screen.blit(s, (area.x, area.y))

            # Display area names
            if index == 0:
                area_name = "Sky"
            elif index == 1:
                area_name = "Forest"
            elif index == 2:
                area_name = "Sea"
            elif index == 3:
                area_name = "Desert"
            elif index == 4:
                area_name = "Castle"
            else:
                area_name = "Shop"
            if index == 4 and not all(lvl in self.completed_levels for lvl in range(1, 5)):
                area_name += " (Locked)"
            text_surface = self.font.render(area_name, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=area.center)
            screen.blit(text_surface, text_rect)

        render_text(f"Total Coins: {int(self.saved_values['total_coins'])}", 20, 20, self.font, screen)
