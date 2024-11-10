import pygame
import math
import random
from src.constants import *
from src.resources import *
from src.bosses.BaseBoss import BaseBoss
from src.bosses.BossBullet import BossBullet
from src.bosses.BeamAttack import BeamAttack

class MedusaBoss(BaseBoss):
    def __init__(self, x, y, health=300, damage=10, damage_speed_scaling=1):
        super().__init__(x, y, width=200, height=400, health=health, damage=damage, damage_speed_scaling=damage_speed_scaling)
        self.animation = sprite_collection["medusa_boss_idle"].animation
        self.damage_speed_scaling = damage_speed_scaling
        # Customizing the appearance for the Blue Dragon
        self.image.fill((0, 200, 200))  # Set color to blue
        
        # Petrifying charge Attack prop
        self.petrify_attack_duration = 5
        self.petrify_beam_gap_cooldown = 0.5
        self.petrify_beam_gap_time = 0
        self.petrify_beam_width = 200
        self.petrify_beam_height = 50
        self.petrify_beams = []
        self.petrify_stun_duration = 3
        
        # Snake strike attack prop
        self.snake_attack_duration = 3
        self.original_width = self.width
        self.original_height = self.height
        self.original_x = self.x
        self.original_y = self.y
        self.original_image = self.image.copy()
        
        # Arrow barrage prop
        self.arrow_barrage_duration = 2
        self.bullet_gap_cooldown = 0.2
        self.bullet_gap_time = 0
        self.bullet_layer_num = 5
        self.bullet_angle = 150
        self.barrage_starting_angle = 0
        self.barrage_starting_angle_random_shift_max = 90
        

    def update(self, dt, player, platforms):
        # Update position and check if the boss should attack
        super().update(dt, player, platforms)
        
        if self.current_attack:
            self.animation = sprite_collection["medusa_boss_fire"].animation
        else:
            self.animation = sprite_collection["medusa_boss_idle"].animation
            
        # Check for collisions between beams and the player to apply the stun effect
        for beam in self.petrify_beams:
            beam.update(dt)
            if beam.rect.colliderect(player.rect):
                player.stun(self.petrify_stun_duration)
            if not beam.active:
                self.petrify_beams.remove(beam)
            
        self.animation.update(dt)

    def select_attack(self, player):
        
        attack_choice = random.choice(["petrifying_charge","snake_strike","arrow_barrage","arrow_attack"])

        if attack_choice == "petrifying_charge":
            self.current_attack = self.petrifying_charge
        elif attack_choice == "snake_strike":
            self.current_attack = self.snake_strike
        elif attack_choice == "arrow_barrage":
            self.current_attack = self.arrow_barrage  
        elif attack_choice == "arrow_attack":
            self.current_attack = self.arrow_attack  
        

    def petrifying_charge(self, dt, player):
        """
        Petrifying Gaze: Medusa fires beams of energy from her eyes in straight lines, sweeping
        across the screen. Any player caught is stunned for 3 seconds.
        """
        beam_direction = "left"
        self.petrify_beam_gap_time += dt

        # Create a new beam if the cooldown time has passed
        if self.petrify_beam_gap_time >= self.petrify_beam_gap_cooldown:
            self.petrify_beam_gap_time = 0

            # Generate a beam at random vertical positions but spaced apart
            beam_y = random.randint(0, HEIGHT - self.petrify_beam_height)
            beam = BeamAttack(WIDTH, beam_y, beam_direction, self.petrify_beam_width, self.petrify_beam_height, self.damage, scaling=self.damage_speed_scaling)
            beam.damage = 0
            self.petrify_beams.append(beam)  # Store the beam in a list

        # End the attack after the designated duration
        if self.attack_elapsed_time >= self.petrify_attack_duration:
            self.end_attack()
            self.petrify_beam_gap_time = 0  # Reset the beam timing for next time
            
    def snake_strike(self, dt, player):
        """
        Snake Strike: Medusa elongates across the screen horizontally, reaching the player's vertical position
        and then retracts back to the original position and size.
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
        t = self.attack_elapsed_time / self.snake_attack_duration

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
            
    def arrow_barrage(self, dt, player):
        """
        Arrow Barrage: Cone-Shaped bullet attack
        """
        if self.attack_elapsed_time == 0:
            self.barrage_starting_angle = random.randint(-self.barrage_starting_angle_random_shift_max, self.barrage_starting_angle_random_shift_max)
        bullet_direction = "left"
        bullet_x = self.x + (self.width // 2)  # Center the bullet on the boss
        bullet_y = self.y + (self.height // 2)  # Start bullet at the center height of the boss
        self.bullet_gap_time += dt
        if self.bullet_gap_time >= self.bullet_gap_cooldown:
            self.bullet_gap_time = 0
            for i in range(self.bullet_layer_num):
                bullet = BossBullet(bullet_x, bullet_y, bullet_direction, self.barrage_starting_angle - (self.bullet_angle * self.bullet_layer_num / 2) + (self.bullet_angle*i), damage=self.damage, scaling=self.damage_speed_scaling)  # Create a bullet
                self.bullets.append(bullet)  # Add bullet to the list
        
        # End the bullet attack if the duration is over
        if self.attack_elapsed_time >= self.arrow_barrage_duration:
            self.end_attack()
            
    def arrow_attack(self, dt, player):
        """
        Arrow attack: Straight bullet attack
        """
        arrow_direction = "left"
        arrow_x = self.x + (self.width // 2)  # Center the bullet on the boss
        arrow_y = self.y + (self.height // 2)  # Start bullet at the center height of the boss
        arrow_speed = BULLET_SPEED * 2
        arrow_width = 100
        
        distance_y = (player.character_y + player.height // 2) - (self.y + (self.height // 2))
        distance_x = abs((player.character_x + player.width // 2) - (self.x + (self.width // 2)))
        
        speed_y =  distance_y * arrow_speed / (distance_x + 1)
        
        bullet = BossBullet(arrow_x, arrow_y, arrow_direction, speed_y, damage=self.damage, scaling=self.damage_speed_scaling)
        bullet.speed = arrow_speed
        bullet.width = arrow_width
        bullet.rect.width = arrow_width
        self.bullets.append(bullet)
        self.end_attack()


    def render(self, screen):
        """Render the boss and possibly some visual effects for its attacks."""
        if self.alive:
            img = self.animation.image
            img = pygame.transform.scale(img, (self.rect.width, self.rect.height))
            screen.blit(img, (self.x, self.y))
            for bullet in self.bullets:
                bullet.render(screen)
            
        for beam in self.petrify_beams:
            beam.render(screen)
            