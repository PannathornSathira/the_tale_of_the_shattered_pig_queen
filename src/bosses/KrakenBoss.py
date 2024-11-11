import pygame
import math
import random
from src.constants import *
from src.resources import *
from src.bosses.BaseBoss import BaseBoss
from src.bosses.BossBullet import BossBullet
from src.bosses.BeamAttack import BeamAttack

class KrakenBoss(BaseBoss):
    def __init__(self, x, y, health=300, damage=10, damage_speed_scaling = 1):
        super().__init__(x=1050, y=200, width=350, height=350, health=health, damage=damage, damage_speed_scaling=damage_speed_scaling)
        self.animation = sprite_collection["kraken_boss_idle"].animation

        # Customizing the appearance for the Blue Dragon
        self.color = (200, 200, 255)
        self.image.fill(self.color)  # Set color to blue
        self.damage_speed_scaling = damage_speed_scaling
        self.position = "right"
        
        # Charge attack prop
        self.charge_duration = 2
        self.initial_y = self.y
        self.end_x_left = -100
        self.end_x_right = 1050

        # Tempest attack prop
        self.tempest_duration = 2
        self.bullet_gap_cooldown = 0.2
        self.bullet_gap_time = 0
        self.bullet_layer_num = 4
        self.bullet_angle = 125
        self.barrage_starting_angle = 0
        self.barrage_starting_angle_random_shift_max = 90
        self.lightnings = []
        self.lightning_speed = 800
        self.lightning_gap = 50
        self.lightning_current_pos = 0
        self.lightning_last_pos = 0
        
        #Thunder strike attack prop
        self.beam_count = 5
        self.beam_width = 100
        self.beam_gap = 150
        self.beam_height = 600
        self.beam_delay = 0.25
        self.beams = []

    def update(self, dt, player, platforms):
        # Update position and check if the boss should attack
        super().update(dt, player, platforms)
        self.animation.update(dt)
        for lightning in self.lightnings:
            lightning.update(dt, player)
            if not lightning.active:
                self.lightnings.remove(lightning)

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
            self.y = self.y - player.height - 10
            self.animation = sprite_collection["kraken_boss_charge"].animation
            gSounds["kraken_charge"].play()
        
        t = self.attack_elapsed_time / self.charge_duration  # Normalized time [0, 1]
        tweened_t = self.ease_in_out_quad(t)

        # Interpolate the position based on the tweened time
        if self.position == "right":
            start_pos = self.end_x_right
            end_pos = self.end_x_left
        else:
            start_pos = self.end_x_left
            end_pos = self.end_x_right
            
        self.x = start_pos + tweened_t * (end_pos - start_pos)

        # End the charge if the duration is over
        if self.attack_elapsed_time >= self.charge_duration:
            self.y = self.initial_y

            # Flip position
            if self.position == "right":
                self.position = "left"
            else:
                self.position = "right"

            self.x = end_pos
            self.animation = sprite_collection["kraken_boss_idle"].animation
            gSounds["kraken_charge"].fadeout(1000)
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
                bullet = BossBullet(bullet_x, bullet_y, bullet_direction, self.barrage_starting_angle - (self.bullet_angle * self.bullet_layer_num / 2) + (self.bullet_angle*i), damage=self.damage, scaling=self.damage_speed_scaling)  # Create a bullet
                bullet.set_image(sprite_collection["kraken_boss_bullet"].image)
                self.bullets.append(bullet)  # Add bullet to the list
            gSounds["kraken_bullet"].play()
        
        # End the bullet attack if the duration is over
        if self.attack_elapsed_time >= self.tempest_duration:
            self.end_attack()
            
    def lightning_wave_beam(self, dt, player):
        direction = "left" if self.position == "right" else "right"
        if self.attack_elapsed_time == 0:
            self.animation = sprite_collection["kraken_boss_lightning_wave_beam"].animation
            gSounds["kraken_thunder"].play()
            if direction == "left": 
                self.lightning_last_pos = WIDTH
                self.lightning_current_pos = WIDTH
            elif direction == "right":
                self.lightning_last_pos = 0
                self.lightning_current_pos = 0
                
        if direction == "left":
            self.lightning_current_pos -= self.lightning_speed * dt
            if self.lightning_current_pos <= self.lightning_last_pos - self.lightning_gap and self.lightning_current_pos >= 0:
                lightning_height = random.randint(200,400)
                lightning_width = lightning_height / 4
                self.lightnings.append(Lightning(self.lightning_current_pos, HEIGHT-lightning_height, lightning_width, lightning_height, self.damage))
                self.lightning_last_pos = self.lightning_current_pos
                
        elif direction == "right":
            self.lightning_current_pos += self.lightning_speed * dt
            if self.lightning_current_pos >= self.lightning_last_pos + self.lightning_gap and self.lightning_current_pos <= WIDTH:
                lightning_height = random.randint(200,400)
                lightning_width = lightning_height / 4
                self.lightnings.append(Lightning(self.lightning_current_pos, HEIGHT-lightning_height, lightning_width, lightning_height, self.damage))
                self.lightning_last_pos = self.lightning_current_pos
                
            
        
            # if beam_direction == "left":
            #     start_x = WIDTH - 1
            # else:
            #     start_x = 0 - BEAM_WIDTH + 1
            # beam = BeamAttack(start_x, player.character_y + (player.height / 2) - (BEAM_HEIGHT / 2), beam_direction, damage=self.damage, scaling=self.damage_speed_scaling)
            # beam.set_image(sprite_collection["kraken_boss_lightning"].image)
            # self.bullets.append(beam)
            
        # End the attack if the duration is over
        if len(self.lightnings) == 0 and self.attack_elapsed_time >= 1:
            self.animation = sprite_collection["kraken_boss_idle"].animation
            gSounds["kraken_thunder"].fadeout(1000)
            self.end_attack()
            
    def thunder_strike_cluster(self, dt, player):
        beam_direction = "down"

        if self.attack_elapsed_time == 0:
            self.animation = sprite_collection["kraken_boss_lightning_thunder_strike_cluster"].animation
            gSounds["kraken_thunder"].play()
            beam_x_positions = random.sample(range(WIDTH // (self.beam_width+self.beam_gap)), self.beam_count)
            for i in range(self.beam_count):
                beam = BeamAttack(beam_x_positions[i] * (self.beam_width+self.beam_gap), 0 - self.beam_height, beam_direction, self.beam_width, self.beam_height, damage=self.damage, scaling=self.damage_speed_scaling)
                beam.set_image(sprite_collection["kraken_boss_thunder"].image)
                self.beams.append(beam)

        # Add beams to the bullets list at intervals of 0.25 seconds
        beam_index = int(self.attack_elapsed_time // self.beam_delay) + 1
        if len(self.bullets) < beam_index and beam_index <= 5:
            self.bullets.append(self.beams[beam_index - 1])
                
        if len(self.bullets) == 0:
            self.animation = sprite_collection["kraken_boss_idle"].animation
            gSounds["kraken_thunder"].fadeout(1000)
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
        if self.alive:
            img = self.animation.image
            img = pygame.transform.scale(img, (self.rect.width, self.rect.height))
            if self.position == "left":
                img = pygame.transform.flip(img, True, False)
            screen.blit(img, (self.x, self.y))
            
        for bullet in self.bullets:
            bullet.render(screen)
            
        for lightning in self.lightnings:
            lightning.render(screen)


class Lightning:
    def __init__(self, x, y, width, height, damage=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = sprite_collection["kraken_boss_lightning"].image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.duration = 1
        self.timer = 0
        self.damage = damage
        self.active = True
        
    def update(self, dt, player):
        if self.rect.colliderect(player.rect):
            player.take_damage(self.damage)
            
        self.timer += dt
        if self.timer >= self.duration:
            self.active = False
            
    def render(self, screen):
        if self.active:
            img = self.image
            img = pygame.transform.scale(img, (self.rect.width, self.rect.height))
            screen.blit(img, (self.x, self.y))