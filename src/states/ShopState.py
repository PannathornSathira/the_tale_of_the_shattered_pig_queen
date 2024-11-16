import pygame
from src.Dependency import *
from src.constants import *
from src.resources import *
from src.Util import *
import pygame
import json
from src.Dependency import *
from src.constants import *
from src.resources import *
from src.Util import *

class ShopState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.item_font = pygame.font.Font(None, 20)
        self.items_left = ["Health Upgrade", "Damage Upgrade", "Movement Speed", "Defense Upgrade","Jump Upgrade", "Shotgun Upgrade", "Start Journey"
                           #"Slow Motion Upgrade"
                           ]
        self.items_right = [
                            #"Health Potion", "Damage Potion", "Swiftness Potion"
                             "Health Potion Upgrade", "Damage Potion Upgrade", "Swiftness Potion Upgrade"
                            ]
        self.side = 'left' 
        self.selected_item_index = 0
        self.total_coins = 0
        self.damage_potions = 0
        self.health_potions = 0
        self.swiftness_potions = 0
        self.bg_image = pygame.image.load("./graphics/Backgrounds/Shop.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH + 5, HEIGHT + 5))
        self.text_color = (255, 255, 255)
        self.item_images = {}
        # Define upgrade costs and levels
        self.hp_levels = [50, 60, 70, 80, 90, 100]
        self.hp_costs = [0, 50, 150, 400, 800, 1500]
        self.dmg_levels = [10, 12, 14, 16, 18, 20]
        self.dmg_costs = [0, 100, 250, 600, 1200, 2000]
        self.speed_levels = [1.0, 1.05, 1.10, 1.15, 1.20, 1.25]
        self.speed_costs = [0, 80, 200, 500, 1000, 1800]
        self.defense_levels = [1.0, 1.05, 1.10, 1.15, 1.20, 1.25]
        self.defense_costs = [0, 120, 300, 700, 1400, 2500]
        self.shop_dict1 = shop_dict
        self.jump_levels = [0.0, 1, 1.05, 1.10, 1.15, 1.20]
        self.jump_costs = [0, 150, 300, 600, 1200, 2000]
        
        self.shotgun_levels = [0.0, 0.40, 0.46, 0.53, 0.6, 0.66]
        self.shotgun_costs = [0, 100, 300, 600, 1200, 2000]
        
        self.slowmo_levels = [1, 0.9, 0.85, 0.8, 0.75, 0.7]
        self.slowmo_costs = [0, 100, 300, 700, 1300, 2000]
        # Potion levels and costs
        self.potion_levels = {
            "Health Potion": {
                "levels": [0, 30, 35, 40, 45, 50],
                "costs": [0, 50, 120, 250, 400, 600]
            },
            "Damage Potion": {
                "levels": [0, 5, 10, 15, 20, 25],
                "costs": [0, 50, 120, 250, 400, 600]
            },
            "Swiftness Potion": {
                "levels": [0, 5, 10, 15, 20, 25],
                "costs": [0, 50, 120, 250, 400, 600]
            }
        }

        self.item_images = {
            "Health Upgrade": shop_dict["hp_upgrade"],
            "Damage Upgrade": shop_dict["damage_upgrade"],
            "Movement Speed": shop_dict["speed_upgrade"],
            "Defense Upgrade": shop_dict["def_upgrade"],
            "Jump Upgrade": shop_dict["2jump_upgrade"],
            "Slow Motion Upgrade": shop_dict["slow_upgrade"],
            "Shotgun Upgrade": shop_dict["shotgun_upgrade"],
            "Health Potion": shop_dict["health_potion"],
            "Damage Potion": shop_dict["damage_potion"],
            "Swiftness Potion": shop_dict["swiftness_potion"],
            "Health Potion Upgrade": shop_dict["health_potion"],
            "Damage Potion Upgrade": shop_dict["damage_potion"],
            "Swiftness Potion Upgrade": shop_dict["swiftness_potion"],
            "Start Journey": shop_dict["shop_continue"],
        }
        
    def Exit(self):
        gMusic["shop"].fadeout(1000)

    def Enter(self, params):
        gMusic["shop"].play(-1)
        saved_values = read_saveFile()
        if saved_values:
            self.saved_values = saved_values

    def purchase_item(self, item):
        if item == "Health Upgrade":
            current_hp_level = self.hp_levels.index(self.saved_values["health"]) if self.saved_values["health"] in self.hp_levels else 0
            if current_hp_level < len(self.hp_levels) - 1:
                next_hp_cost = self.hp_costs[current_hp_level + 1]
                if self.saved_values["total_coins"] >= next_hp_cost:
                    self.saved_values["total_coins"] -= next_hp_cost
                    self.saved_values["health"] = self.hp_levels[current_hp_level + 1]
                    save_values(self.saved_values)
                
        elif item == "Damage Upgrade":
            current_dmg_level = self.dmg_levels.index(self.saved_values["bullet_damage"]) if self.saved_values["bullet_damage"] in self.dmg_levels else 0
            if current_dmg_level < len(self.dmg_levels) - 1:
                next_dmg_cost = self.dmg_costs[current_dmg_level + 1]
                if self.saved_values["total_coins"] >= next_dmg_cost:
                    self.saved_values["total_coins"] -= next_dmg_cost
                    self.saved_values["bullet_damage"] = self.dmg_levels[current_dmg_level + 1]
                    save_values(self.saved_values)
                
        elif item == "Movement Speed":
            current_speed_level = self.speed_levels.index(self.saved_values["movement_speed"]) if self.saved_values["movement_speed"] in self.speed_levels else 0
            if current_speed_level < len(self.speed_levels) - 1:
                next_speed_cost = self.speed_costs[current_speed_level + 1]
                if self.saved_values["total_coins"] >= next_speed_cost:
                    self.saved_values["total_coins"] -= next_speed_cost
                    self.saved_values["movement_speed"] = self.speed_levels[current_speed_level + 1]
                    save_values(self.saved_values)
                
        elif item == "Defense Upgrade":
            current_defense_level = self.defense_levels.index(self.saved_values["defense"]) if self.saved_values["defense"] in self.defense_levels else 0
            if current_defense_level < len(self.defense_levels) - 1:
                next_defense_cost = self.defense_costs[current_defense_level + 1]
                if self.saved_values["total_coins"] >= next_defense_cost:
                    self.saved_values["total_coins"] -= next_defense_cost
                    self.saved_values["defense"] = self.defense_levels[current_defense_level + 1]
                    save_values(self.saved_values)
                
        elif item == "Jump Upgrade":
            current_jump_level = self.jump_levels.index(self.saved_values["jump"]) if self.saved_values["jump"] in self.jump_levels else 0
            if current_jump_level < len(self.jump_levels) - 1:
                next_jump_cost = self.jump_costs[current_jump_level + 1]
                if self.saved_values["total_coins"] >= next_jump_cost:
                    self.saved_values["total_coins"] -= next_jump_cost
                    self.saved_values["jump"] = self.jump_levels[current_jump_level + 1]
                    save_values(self.saved_values)
        
        elif item == "Shotgun Upgrade":
            current_shotgun_level = self.shotgun_levels.index(self.saved_values["shotgun"]) if self.saved_values["shotgun"] in self.shotgun_levels else 0
            if current_shotgun_level < len(self.shotgun_levels) - 1:
                next_shotgun_cost = self.shotgun_costs[current_shotgun_level + 1]
                if self.saved_values["total_coins"] >= next_shotgun_cost:
                    self.saved_values["total_coins"] -= next_shotgun_cost
                    self.saved_values["shotgun"] = self.shotgun_levels[current_shotgun_level + 1]
                    save_values(self.saved_values)
        
        elif item == "Slow Motion Upgrade":
            current_slowmo_level = self.slowmo_levels.index(self.saved_values["boss_damage_speed"]) if self.saved_values["boss_damage_speed"] in self.slowmo_levels else 0
            if current_slowmo_level < len(self.slowmo_levels) - 1:
                next_slowmo_cost = self.slowmo_costs[current_slowmo_level + 1]
                if self.saved_values["total_coins"] >= next_slowmo_cost:
                    self.saved_values["total_coins"] -= next_slowmo_cost
                    self.saved_values["boss_damage_speed"] = self.slowmo_levels[current_slowmo_level + 1]
                    save_values(self.saved_values)
        
        elif item == "Damage Potion":
            current_potion_level = self.saved_values["damage_potion_upgrade_level"]
            potion_cost = self.potion_levels["Damage Potion"]["costs"][current_potion_level]
            if self.saved_values["total_coins"] >= potion_cost:
                self.saved_values["total_coins"] -= potion_cost
                self.saved_values["damage_potions"] += 1
                save_values(self.saved_values)
        
        elif item == "Health Potion":
            current_potion_level = self.saved_values["health_potion_upgrade_level"]
            potion_cost = self.potion_levels["Health Potion"]["costs"][current_potion_level]
            if self.saved_values["total_coins"] >= potion_cost:
                self.saved_values["total_coins"] -= potion_cost
                self.saved_values["health_potions"] += 1
                save_values(self.saved_values)
        
        
        
        elif item == "Swiftness Potion":
            current_potion_level = self.saved_values["swiftness_potion_upgrade_level"]
            potion_cost = self.potion_levels["Swiftness Potion"]["costs"][current_potion_level]  # Set the cost of the Swiftness Potion
            if self.saved_values["total_coins"] >= potion_cost:
                self.saved_values["total_coins"] -= potion_cost
                self.saved_values["swiftness_potions"] += 1
                save_values(self.saved_values)
        
        elif item in ["Health Potion Upgrade", "Damage Potion Upgrade", "Swiftness Potion Upgrade"]:
            potion_name = item.replace(" Upgrade", "")
            potion_info = self.potion_levels[potion_name]
            current_potion_level = self.saved_values.get(f"{item.lower().replace(' ', '_')}_level", 0)
            if current_potion_level < len(potion_info["levels"]) - 1:
                next_potion_cost = potion_info["costs"][current_potion_level + 1]
                if self.saved_values["total_coins"] >= next_potion_cost:
                    self.saved_values["total_coins"] -= next_potion_cost
                    self.saved_values[f"{item.lower().replace(' ', '_')}_level"] = current_potion_level + 1
                    save_values(self.saved_values)
                             
        elif item == "Start Journey":
            g_state_manager.Change("WORLD_MAP", {
                "completed_level": None,
            })

    def update(self, dt, events):
        # Handle player input for selecting items and purchasing
        items_left_count = len(self.items_left)
        items_right_count = len(self.items_right)
        total_items = items_left_count + items_right_count
        items_per_row = 3

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    # Move down by items_per_row positions
                    self.selected_item_index = (self.selected_item_index + items_per_row) % total_items

                elif event.key == pygame.K_UP:
                    # Move up by items_per_row positions
                    self.selected_item_index = (self.selected_item_index - items_per_row) % total_items

                elif event.key == pygame.K_LEFT:
                    # Move left within the grid or wrap to the rightmost item in the previous row
                    if self.selected_item_index % items_per_row > 0:
                        self.selected_item_index -= 1
                    else:
                        self.selected_item_index = (self.selected_item_index - 1) % total_items

                elif event.key == pygame.K_RIGHT:
                    # Move right within the grid or wrap to the leftmost item in the next row
                    if (self.selected_item_index + 1) % items_per_row != 0:
                        self.selected_item_index = (self.selected_item_index + 1) % total_items
                    else:
                        self.selected_item_index = (self.selected_item_index + 1) % total_items

                elif event.key == pygame.K_RETURN:
                    # Purchase the selected item
                    if self.selected_item_index < items_left_count:
                        self.purchase_item(self.items_left[self.selected_item_index])
                    else:
                        self.purchase_item(self.items_right[self.selected_item_index - items_left_count])

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))
        title_left = "Player Status"
        title_right = "Consumable Items"
        
        
        menu_bg_width = screen.get_width() - 80  # Width to cover both left and right item sections
        menu_bg_height = 550  # Height to cover both item sections
        menu_bg_surface = pygame.Surface((menu_bg_width, menu_bg_height), pygame.SRCALPHA)
        menu_bg_surface.fill((96, 96, 96, 200))  # RGBA, 128 is the alpha value for 50% transparency

        # Blit the transparent background at the desired position
        screen.blit(menu_bg_surface, (40, 90))
        title_left_surface = self.font.render(title_left, True, self.text_color)
        title_right_surface = self.font.render(title_right, True, self.text_color)
        screen.blit(title_left_surface, (50, 100))
        screen.blit(title_right_surface, (screen.get_width() // 2 + 50, 100))
        items_left_count = len(self.items_left)
        
        # Draw grid layout for left items
        for index, item in enumerate(self.items_left):
            if item == "Start Journey":
                icon = self.get_item_icon(item)
                x = (screen.get_width() // 2) - (icon.get_width() // 2)
                y = 150 + (index // 3) * 150
                screen.blit(icon, (x, y))
                text_surface = self.item_font.render(item, True, self.text_color)
                screen.blit(text_surface, (x - 15, y - 15))
            else:
                x = 100 + (index % 3) * 150 + 50  # Adjust x position for columns
                y = 150 + (index // 3) * 150
                icon = self.get_item_icon(item)
                screen.blit(icon, (x, y))
                text_surface = self.item_font.render(item, True, self.text_color)
                screen.blit(text_surface, (x - 25, y - 10))
            # Check if the current item is selected and apply green hover effect
            if self.selected_item_index == index:
                # Draw a green border around the icon
                pygame.draw.rect(screen, (0, 255, 0), (x - 5, y - 5, icon.get_width() + 10, icon.get_height() + 10), 3)
            
            
            
            # Draw level bar below the item icon
            level = self.get_current_level(item)  # Implement this function to get the level of each item
            max_level = 5  # Implement this function to get the max level of each item
            square_size = 8  # Size of each level square
            spacing = 4
            if item != "Start Journey":
                for lvl in range(max_level):
                    square_x = x + lvl * (square_size + spacing)  # Horizontal position
                    square_y = y + icon.get_height() + 15  # Position below icon

                    # Draw filled or unfilled square based on the current level
                    color = (255, 0, 0) if lvl < level else (128, 128, 128)
                    pygame.draw.rect(screen, color, (square_x, square_y, square_size, square_size))
                     #Show each item's price
                price = self.get_item_price(item)
                price_text_surface = self.item_font.render(f"${price}", True, (255, 255, 255))
                screen.blit(price_text_surface, (x, y + icon.get_height() + 30))
           
            
        # Draw grid layout for right items
        for index, item in enumerate(self.items_right):
            x = screen.get_width() // 2 + 50 + (index % 3) * 180 + 50
            y = 150 + (index // 3) * 150
            icon = self.get_item_icon(item)

            # Calculate the global index of the item in the right grid
            global_index = items_left_count + index
            if self.selected_item_index == global_index:
                pygame.draw.rect(screen, (0, 255, 0), (x - 5, y - 5, icon.get_width() + 30, icon.get_height() + 30), 3)
            
            screen.blit(icon, (x, y))
            text_surface = self.item_font.render(item, True, self.text_color)
            screen.blit(text_surface, (x - 25, y - 15))
            
             # Draw level bar below the item icon
            level = self.get_current_level(item)  # Implement this function to get the level of each item
            max_level = 5  # Implement this function to get the max level of each item
            square_size = 8  # Size of each level square
            spacing = 4
            for lvl in range(max_level):
                    square_x = x + lvl * (square_size + spacing)  # Horizontal position
                    square_y = y + icon.get_height() + 15  # Position below icon

                    # Draw filled or unfilled square based on the current level
                    color = (255, 0, 0) if lvl < level else (128, 128, 128)
                    pygame.draw.rect(screen, color, (square_x, square_y, square_size, square_size))
            #Show each item's price
            price = self.get_item_price(item)
            price_text_surface = self.item_font.render(f"${price}", True, (255, 255, 255))
            screen.blit(price_text_surface, (x, y + icon.get_height() + 30))
        
        
        coins_text = f"Coins: {int(self.saved_values['total_coins'])}"
        
        # # Render the potion counts
        coins_surface = self.font.render(coins_text, True, self.text_color)

        screen.blit(coins_surface, (50, 600))

    def read_saveFile(self):
        """Read the save file and return the data as a dictionary."""
        try:
            with open(SAVE_FILE_NAME, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return {}
    
    
    def get_item_icon(self, item):
        return self.item_images.get(item, pygame.Surface((50, 50)))

    def get_current_level(self, item):
    # Retrieve the current level for the item based on saved values
        try:
            if item == "Health Upgrade":
                return self.hp_levels.index(self.saved_values["health"])
            elif item == "Damage Upgrade":
                return self.dmg_levels.index(self.saved_values["bullet_damage"])
            elif item == "Movement Speed":
                return self.speed_levels.index(self.saved_values["movement_speed"])
            elif item == "Defense Upgrade":
                return self.defense_levels.index(self.saved_values["defense"])
            elif item == "Jump Upgrade":
                return self.jump_levels.index(self.saved_values["jump"])
            elif item == "Slow Motion Upgrade":
                return self.slowmo_levels.index(self.saved_values["boss_damage_speed"])
            elif item == "Shotgun Upgrade":
                return self.shotgun_levels.index(self.saved_values["shotgun"])
            elif item == "Health Potion":
                return self.saved_values.get("health_potion_upgrade_level", 0)
            elif item == "Damage Potion":
                return self.saved_values.get("damage_potion_upgrade_level", 0)
            elif item == "Swiftness Potion":
                return self.saved_values.get("swiftness_potion_upgrade_level", 0)
            elif item == "Health Potion Upgrade":
                return self.saved_values.get("health_potion_upgrade_level", 0)
            elif item == "Damage Potion Upgrade":
                return self.saved_values.get("damage_potion_upgrade_level", 0)
            elif item == "Swiftness Potion Upgrade":
                return self.saved_values.get("swiftness_potion_upgrade_level", 0)
        except:
            return 0  # Default if item has no level

    def get_max_level(self, item):
        # Define the max level for each item
        if item == "Health Upgrade":
            return len(self.hp_levels) - 1
        elif item == "Damage Upgrade":
            return len(self.dmg_levels) - 1
        elif item == "Movement Speed":
            return len(self.speed_levels) - 1
        elif item == "Defense Upgrade":
            return len(self.defense_levels) - 1
        elif item == "Jump Upgrade":
            return len(self.jump_levels) - 1
        elif item == "Slow Motion Upgrade":
            return len(self.slowmo_levels) - 1
        elif item == "Shotgun Upgrade":
            return len(self.shotgun_levels) - 1
        elif item == "Health Potion":
            return len(self.potion_levels["Health Potion"]["levels"]) - 1
        elif item == "Damage Potion":
            return len(self.potion_levels["Damage Potion"]["levels"]) - 1
        elif item == "Swiftness Potion":
            return len(self.potion_levels["Swiftness Potion"]["levels"]) - 1
        elif item == "Health Potion Upgrade":
            return len(self.potion_levels["Health Potion"]["levels"]) - 1
        elif item == "Damage Potion Upgrade":
            return len(self.potion_levels["Damage Potion"]["levels"]) - 1
        elif item == "Swiftness Potion Upgrade":
            return len(self.potion_levels["Swiftness Potion"]["levels"]) - 1
        return 1
    def get_item_price(self, item):
        if item == "Health Upgrade":
            level = self.get_current_level(item)
            return self.hp_costs[level + 1] if level < len(self.hp_costs) - 1 else "MAX"
        elif item == "Damage Upgrade":
            level = self.get_current_level(item)
            return self.dmg_costs[level + 1] if level < len(self.dmg_costs) - 1 else "MAX"
        elif item == "Movement Speed":
            level = self.get_current_level(item)
            return self.speed_costs[level + 1] if level < len(self.speed_costs) - 1 else "MAX"
        elif item == "Defense Upgrade":
            level = self.get_current_level(item)
            return self.defense_costs[level + 1] if level < len(self.defense_costs) - 1 else "MAX"
        elif item == "Jump Upgrade":
            level = self.get_current_level(item)
            return self.jump_costs[level + 1] if level < len(self.jump_costs) - 1 else "MAX"
        elif item == "Shotgun Upgrade":
            level = self.get_current_level(item)
            return self.shotgun_costs[level + 1] if level < len(self.shotgun_costs) - 1 else "MAX"
        elif item == "Health Potion Upgrade":
            level = self.saved_values.get("health_potion_upgrade_level", 0)
            return self.potion_levels["Health Potion"]["costs"][level + 1] if level < len(self.potion_levels["Health Potion"]["costs"]) - 1 else "MAX"
        elif item == "Damage Potion Upgrade":
            level = self.saved_values.get("damage_potion_upgrade_level", 0)
            return self.potion_levels["Damage Potion"]["costs"][level + 1] if level < len(self.potion_levels["Damage Potion"]["costs"]) - 1 else "MAX"
        elif item == "Swiftness Potion Upgrade":
            level = self.saved_values.get("swiftness_potion_upgrade_level", 0)
            return self.potion_levels["Swiftness Potion"]["costs"][level + 1] if level < len(self.potion_levels["Swiftness Potion"]["costs"]) - 1 else "MAX"
        return "N/A"


    # Ensure to initialize pygame and create an instance of ShopState
    # Then manage the state transitions as per your game's flow.
