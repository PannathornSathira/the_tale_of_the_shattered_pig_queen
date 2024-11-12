import pygame
import math
import random
from src.constants import *
from src.resources import *
from src.bosses.BaseBoss import BaseBoss
from src.bosses.BossBullet import BossBullet

class SandWormBoss(BaseBoss):
    def __init__(self, x, y, health=300, damage=10, damage_speed_scaling=1):
        super().__init__(x - 100, HEIGHT-600, width=300, height=600, health=health, damage=damage, damage_speed_scaling=damage_speed_scaling)
        self.animation = sprite_collection["sandworm_boss_idle"].animation
        self.damage_speed_scaling = damage_speed_scaling
        # Customizing the appearance
        self.image.fill((255, 255, 0))
        
        # Sand bullet prop
        self.sand_bullet_speed = BULLET_SPEED * 2.5
        
        # Shockwave prop
        self.shockwave_damage = self.damage
        self.shockwave_distance = 600
        self.shockwave_effect_duration = 0.3
        self.shockwave_effect_time = 0
        self.shockwave_effect_isVisible = False
        self.shockwave_effect_rect = pygame.Rect(self.x + self.width / 2 - self.shockwave_distance, GROUND_LEVEL_Y, self.shockwave_distance * 2, 50)
        self.bullet_layer_num = 7
        self.bullet_angle = 120
        self.cone_starting_angle = 0
        self.cone_starting_angle_random_shift_max = 90
        self.shockwave_effect_animation = sprite_collection["sandworm_boss_shockwave_effect"].animation
        
        # Dash attack prop
        self.dash_attack_duration = 2
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
            self.shockwave_effect_animation.update(dt)
            if self.shockwave_effect_time >= self.shockwave_effect_duration:
                self.shockwave_effect_isVisible = False  # Hide effect after duration
                self.shockwave_effect_animation.Refresh()
                
        if self.current_attack == self.shockwave and self.warning_time_timer >= 0:
            self.animation = sprite_collection["sandworm_boss_shockwave"].animation
            
        if self.current_attack == self.sand_bullet and self.warning_time_timer >= 0:
            self.animation = sprite_collection["sandworm_boss_sand_bullet"].animation
                
        self.animation.update(dt)

    def select_attack(self, player):
        attack_choice = random.choice(["sand_bullet", "shockwave", "dash"])
        # attack_choice = random.choice(["sand_bullet"])

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
        bullet_height = 40
        
        distance_y = (player.character_y + player.height // 2) - (self.y + (self.height // 2))
        distance_x = abs((player.character_x + player.width // 2) - (self.x + (self.width // 2)))
        
        speed_y =  distance_y * self.sand_bullet_speed / (distance_x + 1)
        
        bullet = BossBullet(bullet_x, bullet_y, bullet_direction, speed_y, scaling=self.damage_speed_scaling)
        bullet.speed = self.sand_bullet_speed
        bullet.width = bullet_width
        bullet.height = bullet_height
        bullet.rect.width = bullet_width
        bullet.rect.height = bullet_height
        bullet.set_image(sprite_collection["sandworm_bullet1"].image)
        self.bullets.append(bullet)
        
        sprite_collection["sandworm_boss_sand_bullet"].animation.Refresh()
        self.animation = sprite_collection["sandworm_boss_idle"].animation
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
            bullet = BossBullet(bullet_x, bullet_y, bullet_direction, self.cone_starting_angle - (self.bullet_angle * self.bullet_layer_num / 2) + (self.bullet_angle*i), damage=self.damage, scaling=self.damage_speed_scaling)  # Create a bullet
            bullet.width = 50
            bullet.height = 20
            bullet.re_initialize()
            bullet.set_image(sprite_collection["sandworm_bullet2"].image)
            self.bullets.append(bullet)  # Add bullet to the list
            
        sprite_collection["sandworm_boss_shockwave"].animation.Refresh()
        self.animation = sprite_collection["sandworm_boss_idle"].animation
        self.end_attack()
        
    def dash(self, dt, player):
        """
        Dash: Dash toward and attack the player
        """
        if self.attack_elapsed_time == 0:
            # Set initial x position to align with the player
            self.x = player.character_x + player.width / 2 - self.width / 2
            self.y = 0

        # Calculate the normalized time variable for elongation and contraction
        t = self.attack_elapsed_time / self.dash_attack_duration

        max_height = self.original_height
        min_height = 100
        if t <= 0.2:
            self.height = min_height
            self.y = HEIGHT - min_height
            self.animation = sprite_collection["sandworm_boss_dash_start"].animation
        # First half of the attack: elongate upwards from the ground
        elif t <= 0.6:
            # Increase height gradually up to a limit (e.g., 1/3 of screen height)
            self.height = int(max_height * ((t - 0.2) * 2.5))
            # Adjust y so the bottom of the boss stays at ground level
            self.y = HEIGHT - self.height
            if t <= 0.4:
                self.animation = sprite_collection["sandworm_boss_dash_1"].animation
            else:
                self.animation = sprite_collection["sandworm_boss_dash_2"].animation

        # Second half: contract height back down to original
        else:
            self.height = int(max_height - (max_height * ((t - 0.6) * 2.5)))
            self.y = HEIGHT - self.height  # Keep the base at ground level
            if t <= 0.8:
                self.animation = sprite_collection["sandworm_boss_dash_2"].animation
            else:
                self.animation = sprite_collection["sandworm_boss_dash_1"].animation
            # Clamp to prevent overshooting original height
            if self.height < min_height:
                self.height = min_height
                self.animation = sprite_collection["sandworm_boss_dash_start"].animation

        # Adjust the image scale dynamically
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))

        # End the attack and reset to original size and position
        if t >= 1.0:
            self.animation = sprite_collection["sandworm_boss_idle"].animation
            self.width = self.original_width
            self.height = self.original_height
            self.x = self.original_x
            self.y = self.original_y
            self.image = self.original_image
            self.rect = self.image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            self.end_attack()


    def render(self, screen):
        """Render the boss and possibly some visual effects for its attacks."""
        if self.alive:
            img = self.animation.image
            img = pygame.transform.scale(img, (self.rect.width + 200, self.rect.height))
            screen.blit(img, (self.x -100, self.y))
        for bullet in self.bullets:
            bullet.render(screen)
        
        # Render shockwave effect if visible
        if self.shockwave_effect_isVisible:
            img = sprite_collection["sandworm_boss_shockwave_effect"].animation.image
            img = pygame.transform.scale(img, (self.shockwave_effect_rect.width, self.shockwave_effect_rect.height))
            screen.blit(img, (self.shockwave_effect_rect.x, self.shockwave_effect_rect.y))
