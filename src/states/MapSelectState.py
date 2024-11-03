from src.Dependency import *

class MapSelectState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.map_areas = [
            pygame.Rect(100, 100, 200, 150),  # Area 1
            pygame.Rect(400, 100, 200, 150),  # Area 2
            pygame.Rect(100, 300, 200, 150),  # Area 3
            pygame.Rect(400, 300, 200, 150),  # Area 4
            pygame.Rect(100, 500, 200, 150),  # Area 5 (Final Boss)
            pygame.Rect(700, 300, 200, 150,)# Shop
        ]
        self.start_game = False
        self.go_to_shop = False
        self.selected_area_index = None
        
        self.boss_spawn_x = 1100
        self.boss_spawn_y = 100
        
        self.completed_levels = []  # Track completed levels
        self.difficulty = len(self.completed_levels) + 1
        
        self.total_coins = 0

    def Exit(self):
        pass

    def Enter(self, params):
        if params["completed_level"]:
            self.completed_levels.append(params["completed_level"])
            self.difficulty = len(self.completed_levels) + 1
        else:
            self.completed_levels = []
            self.difficulty = len(self.completed_levels) + 1
            
        self.get_total_coins()

    def update(self, dt, events):

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check if player collides with any area
        for index, area in enumerate(self.map_areas):
            if area.collidepoint(mouse_pos):
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if index < 4 and index + 1 not in self.completed_levels:
                                level = Level(area=index+1)
                                level.CreateMap()
                                player = Player()
                                boss = self.spawn_boss(area=index+1)
                                g_state_manager.Change("PLAY", {
                                    "level": level,
                                    "boss": boss,
                                    "player": player,
                                    "difficulty": self.difficulty,
                                    "total_coins": self.total_coins
                                })
                            elif index == 4:
                                # Final Boss (Area 5), check if all previous levels are completed
                                if all(lvl in self.completed_levels for lvl in range(1, 5)):
                                    level = Level(area=5)
                                    level.CreateMap()
                                    player = Player()
                                    boss = self.spawn_boss(area=5)
                                    g_state_manager.Change("PLAY", {
                                        "level": level,
                                        "boss": boss,
                                        "player": player,
                                        "difficulty": self.difficulty,
                                        "total_coins": self.total_coins
                                    })
                            elif index == 5:
                                g_state_manager.Change("SHOP", {})
                self.selected_area_index = index
                break
        else:
            self.selected_area_index = None
            
    def spawn_boss(self, area):
        if self.difficulty == 1:
            health = 100
            damage = 10
        elif self.difficulty == 2:
            health = 250
            damage = 15
        elif self.difficulty == 3:
            health = 500
            damage = 25
        elif self.difficulty == 4:
            health = 1000
            damage = 35
        elif self.difficulty == 5:
            health = 2000
            damage = 50
            
        if area == 1:
            return random.choice([KrakenBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage), GreatSharkBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage)])
        elif area == 2:
            return random.choice([BlackWidowBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage), MedusaBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage)])
        elif area == 3:
            return random.choice([BlueDragonBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage), TornadoFiendBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage)])
        elif area == 4:
            return random.choice([KingMummyBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage), SandWormBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage)])
        elif area == 5:
            return WraithBoss(self.boss_spawn_x, self.boss_spawn_y, health, damage)

    def render(self, screen):
        # Fill the screen with a background color
        screen.fill((173, 216, 230))  # Light blue color

        # Draw each map area as a rectangle
        for index, area in enumerate(self.map_areas):
            # Set color based on whether level is completed or locked
            if index < 4:
                color = (0, 255, 0) if index == self.selected_area_index else (255, 0, 0)
                if index + 1 in self.completed_levels:
                    color = (128, 128, 128)  # Gray if completed
            elif index == 4:
                # Final Boss area - locked until levels 1-4 are completed
                if all(lvl in self.completed_levels for lvl in range(1, 5)):
                    color = (0, 255, 0) if index == self.selected_area_index else (255, 0, 0)
                else:
                    color = (128, 128, 128)  # Gray if locked
            else:
                color = (0, 255, 0) if index == self.selected_area_index else (255, 0, 0)

            pygame.draw.rect(screen, color, area)

            # Draw area name
            area_name = f"Area {index + 1}" if index < 5 else "Shop"
            if index == 4 and not all(lvl in self.completed_levels for lvl in range(1, 5)):
                area_name += " (Locked)"
            text_surface = self.font.render(area_name, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=area.center)
            screen.blit(text_surface, text_rect)
        
        render_text(f"Total Coins: {self.total_coins}", 20, 20, self.font, screen)
        
    def get_total_coins(self):
        try:
            with open("saveFile.json", "r+") as file:
                data = json.load(file)
                self.total_coins = data["total_coins"]
        except FileNotFoundError:
            print("saveFile.json not found.")
        except KeyError:
            print("total_coins key not found in saveFile.json.")