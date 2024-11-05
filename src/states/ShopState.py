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
        self.items_left = ["Health Upgrade", "Damage Upgrade", "Movement Speed", "Defense Upgrade", "Start Journey"]
        self.items_right = ["Health Potion", "Damage Potion", "Swiftness Potion"]
        self.side = 'left' 
        self.selected_item_index = 0
        self.total_coins = 0
        self.damage_potions = 0
        self.health_potions = 0
        self.swiftness_potions = 0
        self.bg_image = pygame.image.load("./graphics/Backgrounds/Shop.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH + 5, HEIGHT + 5))
        self.text_color = (255, 255, 255)
        
        # Define upgrade costs and levels
        self.hp_levels = [50, 100, 200, 350, 500, 750]
        self.hp_costs = [0, 50, 150, 400, 800, 1500]
        self.dmg_levels = [10, 15, 25, 45, 80, 130]
        self.dmg_costs = [0, 100, 250, 600, 1200, 2000]
        self.speed_levels = [1.0, 1.05, 1.10, 1.15, 1.20, 1.30]
        self.speed_costs = [0, 80, 200, 500, 1000, 1800]

    def Exit(self):
        pass

    def Enter(self, params):
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
                    print(f"Purchased Health Upgrade. New health: {self.saved_values['health']}. Coins left: {self.total_coins}.")
                else:
                    print("Not enough coins to purchase Health Upgrade.")
            else:
                print("Health is already at max level.")
                
        elif item == "Damage Upgrade":
            current_dmg_level = self.dmg_levels.index(self.saved_values["bullet_damage"]) if self.saved_values["bullet_damage"] in self.dmg_levels else 0
            if current_dmg_level < len(self.dmg_levels) - 1:
                next_dmg_cost = self.dmg_costs[current_dmg_level + 1]
                if self.saved_values["total_coins"] >= next_dmg_cost:
                    self.saved_values["total_coins"] -= next_dmg_cost
                    self.saved_values["bullet_damage"] = self.dmg_levels[current_dmg_level + 1]
                    save_values(self.saved_values)
                    print(f"Purchased Damage Upgrade. New damage: {self.saved_values['bullet_damage']}. Coins left: {self.saved_values["total_coins"]}.")
                else:
                    print("Not enough coins to purchase Damage Upgrade.")
            else:
                print("Damage is already at max level.")
                
        elif item == "Movement Speed":
            current_speed_level = self.speed_levels.index(self.saved_values["movement_speed"]) if self.saved_values["movement_speed"] in self.speed_levels else 0
            if current_speed_level < len(self.speed_levels) - 1:
                next_speed_cost = self.speed_costs[current_speed_level + 1]
                if self.saved_values["total_coins"] >= next_speed_cost:
                    self.saved_values["total_coins"] -= next_speed_cost
                    self.saved_values["movement_speed"] = self.speed_levels[current_speed_level + 1]
                    save_values(self.saved_values)
                    print(f"Purchased Movement Speed Upgrade. New speed: {self.saved_values['movement_speed']}. Coins left: {self.saved_values["total_coins"]}.")
                else:
                    print("Not enough coins to purchase Movement Speed Upgrade.")
            else:
                print("Movement speed is already at max level.")

        elif item == "Damage Potion":
            potion_cost = 300  # Set the cost of the Damage Potion
            if self.saved_values["total_coins"] >= potion_cost:
                self.saved_values["total_coins"] -= potion_cost
                self.saved_values["damage_potions"] += 1
                save_values(self.saved_values)
                print(f"Purchased Damage Potion. Potions available: {self.saved_values["damage_potions"]}. Coins left: {self.saved_values["total_coins"]}.")
            else:
                print("Not enough coins to purchase Damage Potion.")
        
        elif item == "Health Potion":
            potion_cost = 250  # Set the cost of the Health Potion
            if self.saved_values["total_coins"] >= potion_cost:
                self.saved_values["total_coins"] -= potion_cost
                self.saved_values["health_potions"] += 1
                save_values(self.saved_values)
                print(f"Purchased Health Potion. Potions available: {self.saved_values["health_potions"]}. Coins left: {self.saved_values["total_coins"]}.")
            else:
                print("Not enough coins to purchase Health Potion.")
        
        elif item == "Swiftness Potion":
            potion_cost = 250  # Set the cost of the Swiftness Potion
            if self.saved_values["total_coins"] >= potion_cost:
                self.saved_values["total_coins"] -= potion_cost
                self.saved_values["swiftness_potions"] += 1
                save_values(self.saved_values)
                print(f"Purchased Swiftness Potion. Potions available: {self.saved_values["swiftness_potions"]}. Coins left: {self.saved_values["total_coins"]}.")
            else:
                print("Not enough coins to purchase Swiftness Potion.")   
                     
        elif item == "Start Journey":
            g_state_manager.Change("WORLD_MAP", {
                "completed_level": None,
            })

    def update(self, dt, events):
        # Handle player input for selecting items and purchasing
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.side == 'left':
                        self.selected_item_index = (self.selected_item_index + 1) % len(self.items_left)
                    elif self.side == 'right':
                        self.selected_item_index = (self.selected_item_index + 1) % len(self.items_right)
                elif event.key == pygame.K_UP:
                    if self.side == 'left':
                        self.selected_item_index = (self.selected_item_index - 1) % len(self.items_left)
                    elif self.side == 'right':
                        self.selected_item_index = (self.selected_item_index - 1) % len(self.items_right)
                elif event.key == pygame.K_LEFT:
                    if self.side == 'right':
                        self.side = 'left'
                        self.selected_item_index = min(self.selected_item_index, len(self.items_left) - 1)
                elif event.key == pygame.K_RIGHT:
                    if self.side == 'left':
                        self.side = 'right'
                        self.selected_item_index = min(self.selected_item_index, len(self.items_right) - 1)
                elif event.key == pygame.K_RETURN:
                    if self.side == 'left':
                        self.purchase_item(self.items_left[self.selected_item_index])
                    elif self.side == 'right':
                        self.purchase_item(self.items_right[self.selected_item_index])

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))
        title_left = "Player Status"
        title_right = "Consumable Items"
        title_left_surface = self.font.render(title_left, True, self.text_color)
        title_right_surface = self.font.render(title_right, True, self.text_color)
        screen.blit(title_left_surface, (50, 100))
        screen.blit(title_right_surface, (screen.get_width() // 2 + 50, 100))

        # Render left-side shop items
        for index, item in enumerate(self.items_left):
            color = (0, 255, 0) if self.side == 'left' and index == self.selected_item_index else self.text_color
            text_surface = self.font.render(item, True, color)
            screen.blit(text_surface, (50, 150 + index * 50))

        # Render right-side shop items
        for index, item in enumerate(self.items_right):
            color = (0, 255, 0) if self.side == 'right' and index == self.selected_item_index else self.text_color
            text_surface = self.font.render(item, True, color)
            screen.blit(text_surface, (screen.get_width() // 2 + 50, 150 + index * 50))
        
        coins_text = f"Coins: {self.saved_values["total_coins"]}"
        potions_text = f"Damage Potions: {self.saved_values["damage_potions"]}"
        health_potions_text = f"Health Potions: {self.saved_values["health_potions"]}"
        swiftness_potions_text = f"Swiftness Potions: {self.saved_values["swiftness_potions"]}"

        # Render the potion counts
        coins_surface = self.font.render(coins_text, True, self.text_color)
        potions_surface = self.font.render(potions_text, True, self.text_color)
        health_potions_surface = self.font.render(health_potions_text, True, self.text_color)
        swiftness_potions_surface = self.font.render(swiftness_potions_text, True, self.text_color)

        screen.blit(coins_surface, (50, 450))
        screen.blit(potions_surface, (screen.get_width() // 2 + 50, 450))
        screen.blit(health_potions_surface, (screen.get_width() // 2 + 50, 500))
        screen.blit(swiftness_potions_surface, (screen.get_width() // 2 + 50, 550))

    def read_saveFile(self):
        """Read the save file and return the data as a dictionary."""
        try:
            with open(SAVE_FILE_NAME, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading save file: {e}")
            return {}

# Ensure to initialize pygame and create an instance of ShopState
# Then manage the state transitions as per your game's flow.
