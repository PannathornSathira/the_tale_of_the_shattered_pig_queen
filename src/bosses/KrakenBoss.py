import pygame
import math
import random
from src.constants import *
from src.bosses.BaseBoss import BaseBoss
from src.bosses.BossBullet import BossBullet
from src.bosses.BeamAttack import BeamAttack

class KrakenBoss(BaseBoss):
    def __init__(self, x, y, health=300, damage=10):
        super().__init__(x, y, health=health, damage=damage)

        # Customizing the appearance for the Blue Dragon
        self.color = (200, 200, 255)
        self.image.fill(self.color)  # Set color to blue

        self.position = "right"
        
        # Charge attack prop
        self.charge_duration = 2
        self.initial_y = self.y

        # Tempest attack prop
        self.tempest_duration = 2
        self.bullet_gap_cooldown = 0.2
        self.bullet_gap_time = 0
        self.bullet_layer_num = 4
        self.bullet_angle = 125
        self.barrage_starting_angle = 0
        self.barrage_starting_angle_random_shift_max = 90
        
        #Thunder strike attack prop
        self.beam_count = 5
        self.beam_width = 150
        self.beam_gap = 60
        self.beam_height = 1000
        self.beam_delay = 0.25
        self.beams = []

    def update(self, dt, player, platforms):
        # Update position and check if the boss should attack
        super().update(dt, player, platforms)

    def select_attack(self, player):
        
        attack_choice = random.choice(["charge", "tempest_barrage", "lightning_wave_beam", "thunder_strike_cluster"])
        # attack_choice = random.choice(["thunder_strike_cluster"])


        if attack_choice == "charge":
            self.current_attack = self.charge
        elif attack_choice == "tempest_barrage":
            self.current_attack = self.tempest_barrage
        elif attack_choice == "lightning_wave_beam":
            self.current_attack = self.lightning_wave_beam  
        elif attack_choice == "thunder_strike_cluster":
            self.current_attack = self.thunder_strike_cluster  
        

    def charge(self, dt, player):
        """Charge from the right side towards the player."""
        # Rotate the dragon while charging
        if self.position == "right":
            angle = -90  # Rotate 90 degrees left
        else:
            angle = 90  # Rotate 90 degrees right
        if self.attack_elapsed_time == 0:
            self.y = (4 * TILE_SIZE - CHARACTER_HEIGHT) * 3
            rotated_image = pygame.transform.rotate(self.image, angle)
            self.image = rotated_image
            self.rect = self.image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        
        t = self.attack_elapsed_time / self.charge_duration  # Normalized time [0, 1]
        tweened_t = self.ease_in_out_quad(t)

        # Interpolate the position based on the tweened time
        if self.position == "right":
            start_pos = WIDTH - self.width
            end_pos = 0
        else:
            start_pos = 0
            end_pos = WIDTH - self.width
            
        self.x = start_pos + tweened_t * (end_pos - start_pos)

        # End the charge if the duration is over
        if self.attack_elapsed_time >= self.charge_duration:
            self.y = self.initial_y
            
            # Reset the image to its original orientation
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(self.color)  # Set color back to blue

            # Reset the rectangle
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

            # Flip position
            if self.position == "right":
                self.position = "left"
            else:
                self.position = "right"

            self.x = end_pos
            self.end_attack()

    def tempest_barrage(self, dt, player):
        """Shoot bullets towards the player."""
        if self.attack_elapsed_time == 0:
            self.barrage_starting_angle = random.randint(-self.barrage_starting_angle_random_shift_max, self.barrage_starting_angle_random_shift_max)
        bullet_direction = "left" if self.position == "right" else "right"
        bullet_x = self.x + (self.width // 2)  # Center the bullet on the boss
        bullet_y = self.y + (self.height // 2)  # Start bullet at the center height of the boss
        self.bullet_gap_time += dt
        if self.bullet_gap_time >= self.bullet_gap_cooldown:
            self.bullet_gap_time = 0
            for i in range(self.bullet_layer_num):
                bullet = BossBullet(bullet_x, bullet_y, bullet_direction, self.barrage_starting_angle - (self.bullet_angle * self.bullet_layer_num / 2) + (self.bullet_angle*i), damage=self.damage)  # Create a bullet
                self.bullets.append(bullet)  # Add bullet to the list
        
        # End the bullet attack if the duration is over
        if self.attack_elapsed_time >= self.tempest_duration:
            self.end_attack()
            
    def lightning_wave_beam(self, dt, player):
        beam_direction = "left" if self.position == "right" else "right"
        if self.attack_elapsed_time == 0:
            if beam_direction == "left":
                start_x = 0 - BEAM_WIDTH
            else:
                start_x = WIDTH
            beam = BeamAttack(start_x, player.character_y + (player.height / 2) - (BEAM_HEIGHT / 2), beam_direction, damage=self.damage)
            self.bullets.append(beam)
            
        # End the attack if the duration is over
        if len(self.bullets) == 0:
            self.end_attack()
            
    def thunder_strike_cluster(self, dt, player):
        beam_direction = "down"

        if self.attack_elapsed_time == 0:
            beam_x_positions = random.sample(range(WIDTH // (self.beam_width+self.beam_gap)), self.beam_count)
            for i in range(self.beam_count):
                self.beams.append(BeamAttack(beam_x_positions[i] * (self.beam_width+self.beam_gap), 0 - self.beam_height, beam_direction, self.beam_width, self.beam_height, damage=self.damage))

        # Add beams to the bullets list at intervals of 0.25 seconds
        beam_index = int(self.attack_elapsed_time // self.beam_delay) + 1
        if len(self.bullets) < beam_index and beam_index <= 5:
            self.bullets.append(self.beams[beam_index - 1])
                
        if len(self.bullets) == 0:
            self.end_attack()
            self.beams = []

    def ease_in_out_quad(self, t):
        """Custom ease-in-out quadratic tweening function."""
        if t < 0.5:
            return 2 * t * t
        else:
            return -1 + (4 - 2 * t) * t

    def render(self, screen):
        """Render the boss and possibly some visual effects for its attacks."""
        super().render(screen)
