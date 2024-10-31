import pygame
import math
import random
from src.constants import *
from src.bosses.BaseBoss import BaseBoss
from src.bosses.BossBullet import BossBullet
from src.bosses.BeamAttack import BeamAttack

class SandWormBoss(BaseBoss):
    def __init__(self, x, y, health=300):
        super().__init__(x, y, health=health)

        # Customizing the appearance
        self.image.fill((255, 255, 0))
        
        # Sand bullet prop
        self.sand_bullet_speed = BULLET_SPEED * 2
        
        # Shockwave prop
        self.shockwave_damage = 10
        self.shockwave_distance = 600
        self.shockwave_effect_duration = 0.3
        self.shockwave_effect_time = 0
        self.shockwave_effect_isVisible = False
        self.shockwave_effect_rect = pygame.Rect(self.x + self.width / 2 - self.shockwave_distance, GROUND_LEVEL_Y, self.shockwave_distance * 2, 20)
        self.bullet_layer_num = 5
        self.bullet_angle = 150
        self.cone_starting_angle = 0
        self.cone_starting_angle_random_shift_max = 90
        
        # Dash attack prop
        self.dash_attack_duration = 3
        self.original_width = self.width
        self.original_height = self.height
        self.original_x = self.x
        self.original_y = self.y
        self.original_image = self.image.copy()
        
        self.first_trigger = True
        

    def update(self, dt, player, platforms):
        # Update position and check if the boss should attack
        super().update(dt, player, platforms)
        
        if self.first_trigger:
            player.default_move_speed = CHARACTER_MOVE_SPEED / 2
            player.movement_speed = player.default_move_speed
            self.first_trigger = False
        
        # Update effect duration
        if self.shockwave_effect_isVisible:
            self.shockwave_effect_time += dt
            if self.shockwave_effect_time >= self.shockwave_effect_duration:
                self.shockwave_effect_isVisible = False  # Hide effect after duration

    def select_attack(self, player):
        attack_choice = random.choice(["sand_bullet", "shockwave", "dash"])
        # attack_choice = random.choice(["dash"])

        if attack_choice == "sand_bullet":
            self.current_attack = self.sand_bullet
        elif attack_choice == "shockwave":
            self.current_attack = self.shockwave
        elif attack_choice == "dash":
            self.current_attack = self.dash  
            
    def sand_bullet(self, dt, player):
        """
        Sand bullet: Direct bullet attack.
        """
        bullet_direction = "left"
        bullet_x = self.x + (self.width // 2)  # Center the bullet on the boss
        bullet_y = self.y + (self.height // 2)  # Start bullet at the center height of the boss
        bullet_width = 100
        
        distance_y = (player.character_y + player.height // 2) - (self.y + (self.height // 2))
        distance_x = abs((player.character_x + player.width // 2) - (self.x + (self.width // 2)))
        
        speed_y =  distance_y * self.sand_bullet_speed / (distance_x + 1)
        
        bullet = BossBullet(bullet_x, bullet_y, bullet_direction, speed_y)
        bullet.speed = self.sand_bullet_speed
        bullet.width = bullet_width
        bullet.rect.width = bullet_width
        self.bullets.append(bullet)
        self.end_attack()
        
    def shockwave(self, dt, player):
        """
        Shockwave: Release a shockwave around Sand Worm, cone-shaped bullet appear.
        """
        # Calculate distance from player
        distance = abs((self.x + self.width / 2) - (player.character_x + player.width / 2))
        if player.character_y + player.height >= GROUND_LEVEL_Y - TILE_SIZE and distance <= self.shockwave_distance:
            player.take_damage(self.shockwave_damage)

        # Show stomp effect
        self.shockwave_effect_isVisible = True
        self.shockwave_effect_time = 0  # Reset effect timer
        
        # Cone shaped bullet
        self.cone_starting_angle = random.randint(-self.cone_starting_angle_random_shift_max, self.cone_starting_angle_random_shift_max)
        bullet_direction = "left"
        bullet_x = self.x + (self.width // 2)  # Center the bullet on the boss
        bullet_y = self.y + (self.height // 2)  # Start bullet at the center height of the boss
        for i in range(self.bullet_layer_num):
            bullet = BossBullet(bullet_x, bullet_y, bullet_direction, self.cone_starting_angle - (self.bullet_angle * self.bullet_layer_num / 2) + (self.bullet_angle*i))  # Create a bullet
            self.bullets.append(bullet)  # Add bullet to the list
                
        self.end_attack()
        
    def dash(self, dt, player):
        """
        Dash: Dash toward and attack the player
        """
        if self.attack_elapsed_time == 0:
            # Set initial y position to align with the player
            self.y = player.character_y + player.height / 2 - self.width / 2

            # Rotate the image for a horizontal strike position
            rotated_image = pygame.transform.rotate(self.image, 90)
            self.image = rotated_image
            self.rect = self.image.get_rect(center=(self.x + self.original_width // 2, self.y + self.height // 2))
            self.height = self.original_width

        # Calculate the normalized time variable for elongation and contraction
        t = self.attack_elapsed_time / self.dash_attack_duration

        # First half of the attack: elongate across the screen
        if t <= 0.5:
            # Increase width gradually to the screen width
            self.width = int(self.original_width + (WIDTH - self.original_width) * (t * 2))
            self.x = WIDTH - self.width  # Adjust x position to elongate from the right side
        else:
            # Second half: retract back to original width and position
            self.width = int(WIDTH - (WIDTH - self.original_width) * (t - 0.5) * 2)
            self.x = WIDTH - self.width  # Adjust position for retracting
            if self.width < self.original_width:
                self.width = self.original_width  # Restore to original width when finished

        # Adjust the image scale dynamically
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))

        # End the attack and reset to original size and position
        if t >= 1.0:
            self.end_attack()
            self.width = self.original_width
            self.height = self.original_height
            self.x = self.original_x
            self.y = self.original_y
            self.image = self.original_image
            self.rect = self.image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))


    def render(self, screen):
        """Render the boss and possibly some visual effects for its attacks."""
        super().render(screen)
        
        # Render shockwave effect if visible
        if self.shockwave_effect_isVisible:
            pygame.draw.rect(screen, (255, 0, 0), self.shockwave_effect_rect)
