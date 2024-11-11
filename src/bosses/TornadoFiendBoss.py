import pygame
import math
import random
from src.constants import *
from src.resources import *
from src.bosses.BaseBoss import BaseBoss
from src.bosses.BossBullet import BossBullet
from src.bosses.BeamAttack import BeamAttack

class TornadoFiendBoss(BaseBoss):
    def __init__(self, x, y, health=300, damage=10, damage_speed_scaling=1):
        super().__init__(x, y, height=300, health=health, damage=damage, damage_speed_scaling=damage_speed_scaling)
        self.max_health = health
        self.damage_speed_scaling = damage_speed_scaling
        # Customizing the appearance
        self.image.fill((230, 230, 255))  # Set color to blue
        self.animation = sprite_collection["tornado_boss_idle"].animation
        
        # Cyclone barage attack prop
        self.barrage_gap = 0.4  # Time between rows in seconds
        self.barrage_attack_duration = 5
        self.barrage_time = 0
        self.barrage_rows = 5  # Number of rows in the barrage
        self.barrage_row_y_positions = [1 * TILE_SIZE * 4, 2 * TILE_SIZE * 4, 3 * TILE_SIZE * 4, GROUND_LEVEL_Y - TILE_SIZE]
        self.barrage_previeous_row = 0
        self.barrage_isFromLeft = True
        
        # Tornado swarm attack prop
        self.fiendlings = []
        
        # Tornado judgement attack prop
        self.beam_count = 5
        self.beam_width = 100
        self.beam_gap = 100
        self.beam_height = 500
        self.beam_delay = 0.25
        self.beams = []
        
        # Tornado frenzy attack prop
        self.tornado_frenzy_duration = 10
        self.original_x = self.x
        self.original_y = self.y
        self.tornado_frenzy_speed = 200

    def update(self, dt, player, platforms):
        # Update position and check if the boss should attack
        super().update(dt, player, platforms)
        
        # Update fiendlings
        for fiendling in self.fiendlings:
            fiendling.update(dt, player, platforms)
            if not fiendling.alive:
                self.fiendlings.remove(fiendling)
                
        if self.warning_time_timer > 0:
            if self.current_attack == self.tornado_swarm:
                self.animation = sprite_collection["tornado_boss_summon"].animation
            elif self.current_attack == self.cyclone_barrage:
                self.animation = sprite_collection["tornado_boss_barrage"].animation
        else:
            self.animation = sprite_collection["tornado_boss_idle"].animation
                
        self.animation.update(dt)

    def select_attack(self, player):
        attack_choice = random.choice(["cyclone_barrage", "tornado_swarm", "tornado_judgement", "tornado_frenzy"])
        # attack_choice = random.choice(["tornado_frenzy"])

        if attack_choice == "cyclone_barrage":
            self.current_attack = self.cyclone_barrage
        elif attack_choice == "tornado_swarm":
            self.current_attack = self.tornado_swarm
        elif attack_choice == "tornado_judgement":
            self.current_attack = self.tornado_judgement  
        elif attack_choice == "tornado_frenzy":
            self.current_attack = self.tornado_frenzy  

    def cyclone_barrage(self, dt, player):
        """
        Cyclone Barrage: Tornado Fiend spins, and bullets appear in rows across the screen, alternating direction.
        """
        self.barrage_time += dt

        if self.barrage_time >= self.barrage_gap:
            self.barrage_time = 0

            # Calculate y-position of the new row
            row_y = random.choice([y for y in self.barrage_row_y_positions if y != self.barrage_previeous_row])
            
            if self.barrage_isFromLeft:  # Left to Right
                x_position = 0
                direction = "right"
            else:  # Right to Left
                x_position = WIDTH
                direction = "left"

            # Create bullet and add to boss's bullet list
            bullet = BossBullet(x_position, row_y, direction, damage=self.damage, scaling=self.damage_speed_scaling)
            if direction == "right":
                img = pygame.transform.flip(sprite_collection["tornado_bullet"].image, True, False)
            else:
                img = sprite_collection["tornado_bullet"].image
            bullet.set_image(img)
            self.bullets.append(bullet)
            
            self.barrage_isFromLeft = not self.barrage_isFromLeft
            self.barrage_previeous_row = row_y
                

        # End the attack after a specific duration or when all rows are fired
        if self.attack_elapsed_time >= self.barrage_attack_duration:
            self.end_attack()
            
    def tornado_swarm(self, dt, player):
        """
        Tornado Swarm: Tornado Fiend summons smaller clones that race across the screen, creating unpredictable obstacles.
        """
        spawn_x = self.x + self.width / 2 + random.randint(-100, 100)
        spawn_y = self.y + self.height / 2 + random.randint(-100, 100)
        fiendling = Fiendling(spawn_x, spawn_y, damage=self.damage//2, health=self.max_health // 10)
        self.fiendlings.append(fiendling)
        self.end_attack()
        
    def tornado_judgement(self, dt, player):
        """
        Tornado Judgment: Tornado Fiend flies to the top of the screen and summons massive pillars of light that shoot down toward the player’s position.
        """
        beam_direction = "down"
        
        if self.attack_elapsed_time == 0:
            self.y = 0 - self.height / 2
            self.x = WIDTH / 2 - self.width / 2
            beam_x_positions = random.sample(range(WIDTH // (self.beam_width+self.beam_gap)), self.beam_count)
            for i in range(self.beam_count):
                beam = BeamAttack(beam_x_positions[i] * (self.beam_width+self.beam_gap), 0 - self.beam_height, beam_direction, self.beam_width, self.beam_height, damage=self.damage, scaling=self.damage_speed_scaling)
                beam.set_image(sprite_collection["tornado_lightning"].image)
                self.beams.append(beam)

        # Add beams to the bullets list at intervals of 0.25 seconds
        beam_index = int(self.attack_elapsed_time // self.beam_delay) + 1
        if len(self.bullets) < beam_index and beam_index <= 5:
            self.bullets.append(self.beams[beam_index - 1])
                
        if len(self.bullets) == 0:
            self.x = self.original_x
            self.y = self.original_y
            self.end_attack()
            self.beams = []
            
        # if self.attack_elapsed_time >= self.barrage_attack_duration:
        #     self.x = self.original_x
        #     self.y = self.original_y
        #     self.end_attack()
            
    def tornado_frenzy(self, dt, player):
        """
        Tornado's Frenzy: Fly and chase the player for 10 seconds.
        """
        if self.attack_elapsed_time == 0:
            self.original_x = self.x
            self.original_y = self.y
            
        # Calculate direction towards the player
        target_x = player.character_x + player.width / 2 - self.width / 2
        target_y = player.character_y + player.height / 2 - self.height / 2
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # Normalize direction and move towards the player
        if distance > 0:
            self.x += (dx / distance) * self.tornado_frenzy_speed * dt
            self.y += (dy / distance) * self.tornado_frenzy_speed * dt
        
        if self.attack_elapsed_time >= self.tornado_frenzy_duration:
            self.end_attack()
            self.x = self.original_x
            self.y = self.original_y


    def render(self, screen):
        """Render the boss and possibly some visual effects for its attacks."""
        if self.alive:
            img = self.animation.image
            img = pygame.transform.scale(img, (self.rect.width, self.rect.height))
            screen.blit(img, (self.x, self.y))
            
        for bullet in self.bullets:
            bullet.render(screen)
        
        for fiendling in self.fiendlings:
            fiendling.render(screen)
            

class Fiendling:
    def __init__(self, x, y, speed=75, damage=5, health=50):
        self.x = x
        self.y = y
        self.width = CHARACTER_WIDTH
        self.height = CHARACTER_HEIGHT
        self.direction = random.choice(["left", "right"])  # Start in a random direction

        # Placeholder fiendling image
        self.animation = sprite_collection["tornado_boss_fiendling"].animation

        self.speed = speed
        self.damage = damage
        self.alive = True
        self.health = health

        # Movement and jump variables
        self.velocity_y = 0
        self.is_jumping = False
        self.on_ground = False
        self.jump_force = JUMP_FORCE
        self.gravity = GRAVITY
        self.ground_y = GROUND_LEVEL_Y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # AI movement timer
        self.change_direction_interval = random.randint(1, 3)  # Seconds to change direction
        self.last_direction_change = 0

    def update(self, dt, player, platforms):
        # Increment timer and change direction if the interval has passed
        self.last_direction_change += dt
        # if self.direction == "jump":
        #     self.direction = random.choice(["left", "right"])  # Ensure it doesn’t jump again immediately
        if self.last_direction_change >= self.change_direction_interval:
            self.last_direction_change = 0
            self.direction = random.choice(["left","right","jump","down"])
            self.change_direction_interval = random.randint(1, 3)
            
        if self.x + self.width >= WIDTH:
            self.direction = "left"
        elif self.x <= 0:
            self.direction = "right"
        
        # Apply movement based on direction
        if self.direction == "left":
            self.x -= self.speed * dt
        elif self.direction == "right":
            self.x += self.speed * dt
        elif self.direction == "jump" and self.on_ground:
            self.is_jumping = True
            self.velocity_y = self.jump_force
            self.on_ground = False
            self.direction = random.choice(["left", "right"])
        elif self.direction == "down" and self.on_ground and self.y + self.height < self.ground_y:
            self.on_ground = False
            self.y += self.height + 20
            self.rect.y = self.y
            self.velocity_y = self.gravity * dt
            self.direction = random.choice(["left", "right"])
        
        # Apply gravity
        if not self.on_ground:
            self.velocity_y += self.gravity * dt
            self.y += self.velocity_y * dt
            
        # Platform collision check
        collided, platform = self.check_platform_collision(platforms)
        if not collided:
            # No platform collision, apply gravity as player is in the air
            if self.y + CHARACTER_HEIGHT >= self.ground_y:
                pass
            elif self.y + CHARACTER_HEIGHT < self.ground_y:
                self.on_ground = False
        else:
            self.y = platform.rect.top - CHARACTER_HEIGHT
            self.on_ground = True
            self.is_jumping = False
            self.velocity_y = 0

        # Reset position when fiendling touches ground
        if self.y + self.height >= self.ground_y:
            self.y = self.ground_y - self.height
            self.velocity_y = 0
            self.on_ground = True
            self.is_jumping = False

        # Update the fiendling's rect position
        self.rect.x = self.x
        self.rect.y = self.y

        # Check collision with player
        if self.rect.colliderect(player.rect) and self.alive:
            player.take_damage(self.damage)
            
        # Check player hit fiendling
        for bullet in player.bullets:
            if bullet.rect.colliderect(self) and self.alive:
                self.take_damage(bullet.damage)
                player.bullets.remove(bullet)
                
        self.animation.update(dt)

    def check_platform_collision(self, platforms):
        for platform_row in platforms:
            for platform in platform_row:
                if platform and self.rect.colliderect(platform.rect) and self.velocity_y > 0:
                    return True, platform
        return False, None

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False

    def render(self, screen):
        if self.alive:
            img = self.animation.image
            img = pygame.transform.scale(img, (self.rect.width, self.rect.height))
            if self.direction == "left":
                img = pygame.transform.flip(img, True, False)
            screen.blit(img, (self.x, self.y))

        

