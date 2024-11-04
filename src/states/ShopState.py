import pygame
from src.Dependency import *
from src.constants import *
class ShopState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.items_left = ["Health Upgrade", "Damage Upgrade", "Movement Speed", "Defense Upgrade", "Back To World Map"]
        self.items_right = ["Health Potion", "Damage Potion", "Swiftness Potion"]
        self.side = 'left' 
        self.selected_item_index = 0
        self.hp_levels = [50, 100, 200, 350, 500, 750]
        self.hp_costs = [0, 50, 150, 400, 800, 1500]
        self.dmg_levels = [10, 15, 25, 45, 80, 130]
        self.dmg_costs = [0, 100, 250, 600, 1200, 2000]
        self.speed_levels = [1.0, 1.05, 1.10, 1.15, 1.20, 1.30]
        self.speed_costs = [0, 80, 200, 500, 1000, 1800]
        self.damage_potions = 0
        self.health_potions = 0
        self.swiftness_potions = 0
        self.bg_image = pygame.image.load("./graphics/Shop.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH + 5, HEIGHT + 5))
        self.text_color = (0,0,0)
    def Exit(self):
        pass

    def Enter(self, params):
        self.player = params.get("player")
        self.total_coins = params.get("total_coins")
        self.complete_level = params.get("completed_level")
        self.damage_potions = params.get("damage_potions", 0)
        self.health_potions = params.get("health_potions", 0)
        self.swiftness_potions = params.get("swiftness_potions", 0)
    
    def purchase_item(self, item):
        if item == "Health Upgrade":
            current_hp_level = self.hp_levels.index(self.player.health) if self.player.health in self.hp_levels else 0
            if current_hp_level < len(self.hp_levels) - 1:
                next_hp_cost = self.hp_costs[current_hp_level + 1]
                if self.total_coins >= next_hp_cost:
                    self.total_coins -= next_hp_cost
                    self.player.health = self.hp_levels[current_hp_level + 1]
                    print(f"Purchased Health Upgrade. Player health is now {self.player.health}. Coins left: {self.total_coins}.")
                else:
                    print("Not enough coins to purchase Health Upgrade.")
            else:
                print("Health is already at max level.")
                
        elif item == "Damage Upgrade":
            current_dmg_level = self.dmg_levels.index(self.player.bullet_damage) if self.player.bullet_damage in self.dmg_levels else 0
            if current_dmg_level < len(self.dmg_levels) - 1:
                next_dmg_cost = self.dmg_costs[current_dmg_level + 1]
                if self.total_coins >= next_dmg_cost:
                    self.total_coins -= next_dmg_cost
                    self.player.bullet_damage = self.dmg_levels[current_dmg_level + 1]
                    print(f"Purchased Damage Upgrade. Player damage is now {self.player.bullet_damage}. Coins left: {self.total_coins}.")
                else:
                    print("Not enough coins to purchase Damage Upgrade.")
            else:
                print("Damage is already at max level.")
                
        elif item == "Movement Speed":
            current_speed_level = self.speed_levels.index(self.player.movement_speed) if self.player.movement_speed in self.speed_levels else 0
            if current_speed_level < len(self.speed_levels) - 1:
                next_speed_cost = self.speed_costs[current_speed_level + 1]
                if self.total_coins >= next_speed_cost:
                    self.total_coins -= next_speed_cost
                    self.player.movement_speed = self.speed_levels[current_speed_level + 1] * CHARACTER_MOVE_SPEED
                    self.player.default_move_speed = self.speed_levels[current_speed_level + 1] * CHARACTER_MOVE_SPEED
                else:
                    print("Not enough coins to purchase Movement Speed Upgrade.")
            else:
                print("Movement speed is already at max level.")
        elif item == "Defense Upgrade":
            pass
        elif item == "Damage Potion":
            potion_cost = 300  # Set the cost of the Damage Potion
            if self.total_coins >= potion_cost:
                self.total_coins -= potion_cost
                self.damage_potions += 1  # Increase the potion count
                print(f"Purchased Damage Potion. Potions available: {self.damage_potions}. Coins left: {self.total_coins}.")
            else:
                print("Not enough coins to purchase Damage Potion.")
        
        elif item == "Health Potion":
            potion_cost = 250  # Set the cost of the Damage Potion
            if self.total_coins >= potion_cost:
                self.total_coins -= potion_cost
                self.health_potions += 1
                print(f"Purchased Health Potion. Potions available: {self.health_potions}. Coins left: {self.total_coins}.")
            else:
                print("Not enough coins to purchase Health Potion.")
        
        elif item == "Swiftness Potion":
            potion_cost = 250  # Set the cost of the Damage Potion
            if self.total_coins >= potion_cost:
                self.total_coins -= potion_cost
                self.swiftness_potions += 1
                print(f"Purchased Health Potion. Potions available: {self.swiftness_potions}. Coins left: {self.total_coins}.")
            else:
                print("Not enough coins to purchase Health Potion.")   
                     
        elif item == "Back To World Map":
            g_state_manager.Change("WORLD_MAP", {
                "player": self.player,
                "total_coins": self.total_coins,
                "completed_level": self.complete_level,
                "damage_potions": self.damage_potions,
                "health_potions": self.health_potions,
                "swiftness_potions": self.swiftness_potions
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
        # Fill the screen with a background color
        # Light gray color
        #screen.fill((200, 200, 200))
        self.text_color = (51,255,255)  
        screen.blit(self.bg_image, (0, 0))
        title_left = "Player Status"
        title_right = "Consumable Items"
        title_left_surface = pygame.font.Font(None, 48).render(title_left, True, self.text_color)
        title_left_rect = title_left_surface.get_rect(topleft=(50, 100))
        screen.blit(title_left_surface, title_left_rect)
        
        title_right_surface = pygame.font.Font(None, 48).render(title_right, True, self.text_color)
        title_right_rect = title_right_surface.get_rect(topleft=(screen.get_width() // 2 + 50, 100))
        screen.blit(title_right_surface, title_right_rect)
        # Render left-side shop items
        for index, item in enumerate(self.items_left):
            color = (0, 255, 0) if self.side == 'left' and index == self.selected_item_index else self.text_color
            text_surface = self.font.render(item, True, color)
            text_rect = text_surface.get_rect(topleft=(50, 150 + index * 50))
            screen.blit(text_surface, text_rect)

        # Render right-side shop items
        for index, item in enumerate(self.items_right):
            color = (0, 255, 0) if self.side == 'right' and index == self.selected_item_index else self.text_color
            text_surface = self.font.render(item, True, color)
            text_rect = text_surface.get_rect(topleft=(screen.get_width() // 2 + 50, 150 + index * 50))
            screen.blit(text_surface, text_rect)
        
        coins_text = f"Coins: {self.total_coins}"
        coins_surface = self.font.render(coins_text, True, self.text_color)
        coins_rect = coins_surface.get_rect(topleft=(20, 20))
        screen.blit(coins_surface, coins_rect)

        potions_text = f"Damage Potions: {self.damage_potions}"
        potions_surface = self.font.render(potions_text, True, self.text_color)
        potions_rect = potions_surface.get_rect(topleft=(20, 50))
        screen.blit(potions_surface, potions_rect)
        
        potions_text = f"Health Potions: {self.health_potions}"
        potions_surface = self.font.render(potions_text, True, self.text_color)
        potions_rect = potions_surface.get_rect(topleft=(320, 50))
        screen.blit(potions_surface, potions_rect)
        
        potions_text = f"Swiftness Potions: {self.swiftness_potions}"
        potions_surface = self.font.render(potions_text, True, self.text_color)
        potions_rect = potions_surface.get_rect(topleft=(620, 50))
        screen.blit(potions_surface, potions_rect)
        # Update the display
        pygame.display.update()
