import pygame
import math
import random
from src.constants import *
from src.bosses.BaseBoss import BaseBoss
from src.bosses.BossBullet import BossBullet
from src.bosses.BeamAttack import BeamAttack


class WraithBoss(BaseBoss):
    def __init__(self, x, y, health=300, damage=10, damage_speed_scaling=1):
        super().__init__(x, y, width=150, height=300, health=health, damage=damage, damage_speed_scaling=damage_speed_scaling)
        self.damage_speed_scaling = damage_speed_scaling
        self.player_character_x = 0
        self.player_character_y = 0

        # Customizing the appearance
        self.image.fill((0, 0, 0))  # Set color
        self.visible = True
        
        # Blindness attack properties
        self.blindness_active = False
        self.blindness_duration = 5  # Duration in seconds
        self.blindness_timer = 0  # Timer to track blindness effect duration
        self.spotlight_radius = 500  # Radius around player that remains visible

        #Homing Bullet attack prop
        self.homing_bullet_duration = 3
        self.bullet_gap_cooldown = 0.5
        self.bullet_gap_time = 0
        self.bullet_layer_num = 3
        self.bullet_angle = 90
        self.barrage_starting_angle = 100
        self.barrage_starting_angle_random_shift_max = 0
        self.homing_bullets = []  # List to track summoned homing bullets
        
        #Haunting Wail attack prop
        self.original_x = self.x
        self.original_y = self.y
        self.haunting_wail_duration = 5
        self.haunting_wail_bullet_speed = 400  # Speed of each bullet
        self.haunting_wail_bullet_gap_cooldown = 0.05
        self.haunting_wail_bullet_gap_time = 0
        self.haunting_wail_current_angle = 0
        self.haunting_wail_num_bullets_in_circle = 30
        
        #Illusions attack prop
        self.illusions_minibosses = []
        self.illusion_speed = 75
        self.illusion_damage = 15
        self.illusion_health = 500
        

    def update(self, dt, player, platforms):
        # Update position and check if the boss should attack
        super().update(dt, player, platforms)
        
        self.player_character_x = player.character_x
        self.player_character_y = player.character_y
        
        # Update blindness effect
        if self.blindness_active:
            self.blindness_timer += dt
            if self.blindness_timer >= self.blindness_duration:
                self.end_blindness()
                
        # Update homing bullets
        for bullet in self.homing_bullets:
            bullet.update(dt, player)
            if bullet.hit_player:
                player.take_damage(bullet.damage)
                self.homing_bullets.remove(bullet)
                
            if not bullet.active:
                self.homing_bullets.remove(bullet)
                
        for illusion in self.illusions_minibosses:
            if illusion.alive:
                illusion.update(dt, player, platforms)
            else:
                self.illusions_minibosses.remove(illusion)

    def select_attack(self, player):

        attack_choice = random.choice(["blindness", "homing_bullet", "illusions", "haunting_wail"])

        if attack_choice == "blindness":
            self.current_attack = self.blindness
        elif attack_choice == "homing_bullet":
            self.current_attack = self.homing_bullet
        elif attack_choice == "illusions":
            self.current_attack = self.illusions
        elif attack_choice == "haunting_wail":
            self.current_attack = self.haunting_wail
            
    def blindness(self, dt, player):
        """
        Blindness: Reduce player vision by 75% for 5 seconds
        """
        if not self.blindness_active:
            self.blindness_active = True
            self.blindness_timer = 0
        self.end_attack()
            
    def end_blindness(self):
        """Deactivate blindness and reset variables."""
        self.blindness_active = False
        self.blindness_timer = 0
        
    def homing_bullet(self, dt, player):
        """
        Homing bullet: Homing bullet attacking pattern, disappears after 5 seconds.
        """
        if self.attack_elapsed_time == 0:
            self.barrage_starting_angle = random.randint(-self.barrage_starting_angle_random_shift_max, self.barrage_starting_angle_random_shift_max)
        bullet_x = self.x + (self.width // 2)  # Center the bullet on the boss
        bullet_y = self.y + (self.height // 2)  # Start bullet at the center height of the boss
        self.bullet_gap_time += dt
        if self.bullet_gap_time >= self.bullet_gap_cooldown:
            self.bullet_gap_time = 0
            for i in range(self.bullet_layer_num):
                bullet = HomingBullet(bullet_x, bullet_y, damage=self.damage,scaling=self.damage_speed_scaling)  # Create a bullet
                bullet.direction = math.radians(self.barrage_starting_angle - (self.bullet_angle * self.bullet_layer_num / 2) + (self.bullet_angle*i))
                self.homing_bullets.append(bullet)  # Add bullet to the list
        
        # End the bullet attack if the duration is over
        if self.attack_elapsed_time >= self.homing_bullet_duration:
            self.end_attack()
            
    def illusions(self, dt, player):
        """
        Illusions: Splitting into 4 decoy spirits. The player must defeat all Illusions to cancel this ability. Attacking illusions does not affect Boss HP.
        """
        if self.attack_elapsed_time == 0:
            spawn_points = [(0,0), (WIDTH-self.width,0), (0, HEIGHT-self.height), (WIDTH-self.width, HEIGHT-self.height)]
            for i in range(4):
                miniboss = IllusionBoss(spawn_points[i][0], spawn_points[i][1], self.width, self.height, speed=self.illusion_speed, damage=self.illusion_damage, health=self.illusion_health)
                self.illusions_minibosses.append(miniboss)
            self.y = HEIGHT + 100
            
        if len(self.illusions_minibosses) <= 0:
            self.end_attack()
            self.y = self.original_y
        

    def haunting_wail(self, dt, player):
        """
        Haunting Wail: Teleport to the middle, shoot bullets in a circling pattern over time.
        """
        # Initialize the attack setup
        if self.attack_elapsed_time == 0:
            # Teleport to the center
            self.x = WIDTH / 2 - self.width / 2
            self.y = HEIGHT / 2 - self.height / 2 - (HEIGHT - GROUND_LEVEL_Y - TILE_SIZE)
            self.haunting_wail_current_angle = 0  # Start angle for the first bullet
        
        # Fire bullets one at a time in a circle
        self.haunting_wail_bullet_gap_time += dt
        if self.haunting_wail_bullet_gap_time >= self.haunting_wail_bullet_gap_cooldown:
            self.haunting_wail_bullet_gap_time = 0
            
            # Calculate bullet direction based on current angle
            bullet_dx = math.cos(self.haunting_wail_current_angle) * self.haunting_wail_bullet_speed
            bullet_dy = math.sin(self.haunting_wail_current_angle) * self.haunting_wail_bullet_speed
            
            # Create and position the bullet
            bullet = BossBullet(self.x + self.width / 2, self.y + self.height / 2, "general", self.damage, (bullet_dx, bullet_dy), damage=self.damage, scaling=self.damage_speed_scaling)
            bullet.width = BULLET_WIDTH
            bullet.height = BULLET_WIDTH
            bullet.rect.width = BULLET_WIDTH
            bullet.rect.height = BULLET_WIDTH
            self.bullets.append(bullet)
            
            # Increment angle to create a circular firing pattern
            angle_increment = (2 * math.pi) / self.haunting_wail_num_bullets_in_circle
            self.haunting_wail_current_angle = (self.haunting_wail_current_angle + angle_increment) % (2 * math.pi)
        
        # End the attack after the duration is over
        if self.attack_elapsed_time >= self.haunting_wail_duration:
            # Reset position and end the attack
            self.x = self.original_x
            self.y = self.original_y
            self.end_attack()


    def render(self, screen):
        if self.visible:
            super().render(screen)
            
        # Render blindness effect with spotlight
        if self.blindness_active:
            # Create a full-screen overlay with a dark fill
            darkness_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            darkness_overlay.fill((0, 0, 0, 255))  # Set overall transparency to darken screen

            # Create a spotlight effect (circle) around the player position
            spotlight_radius = self.spotlight_radius
            spotlight_surface = pygame.Surface((spotlight_radius * 2, spotlight_radius * 2), pygame.SRCALPHA)

            # Draw gradient spotlight effect
            for i in range(spotlight_radius, 0, -10):
                alpha = int(255 * (1 - (i / spotlight_radius)))  # Gradient transparency
                pygame.draw.circle(spotlight_surface, (0, 0, 0, alpha), (spotlight_radius, spotlight_radius), i)

            # Position spotlight at player's center on the screen
            spotlight_pos = (self.player_character_x - spotlight_radius + CHARACTER_WIDTH / 2 * 3, self.player_character_y - spotlight_radius + CHARACTER_HEIGHT / 2 * 3)
            darkness_overlay.blit(spotlight_surface, spotlight_pos, special_flags=pygame.BLEND_RGBA_SUB)

            # Draw the overlay onto the screen
            screen.blit(darkness_overlay, (0, 0))
    
        # Render homing bullets
        for bullet in self.homing_bullets:
            bullet.render(screen)
            
        for illusion in self.illusions_minibosses:
            illusion.render(screen)
    

class HomingBullet:
    def __init__(self, x, y, speed=125, damage=10, turn_rate=50, scaling=1):
        self.x = x
        self.y = y
        self.speed = speed
        self.scaling = scaling
        self.damage = damage
        self.size = 5
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((191, 0, 255))
        self.hit_player = False
        self.life_time = 10
        self.active = True

        # Starting direction
        self.direction = math.radians(180)  # Facing downwards
        self.turn_rate = turn_rate  # Max turn rate per update in degrees

    def update(self, dt, player):
        if self.active:
            self.speed=self.scaling
            self.life_time -= dt
            # Calculate direction towards the player
            target_x = player.character_x + player.width / 2 - self.size / 2
            target_y = player.character_y + player.height / 2 - self.size / 2
            dx = target_x - self.x
            dy = target_y - self.y
            target_angle = math.atan2(dy, dx)

            # Calculate angle difference and apply turn rate limitation
            angle_diff = target_angle - self.direction
            angle_diff = (angle_diff + math.pi) % (2 * math.pi) - math.pi  # Normalize to [-pi, pi]

            # Limit turning speed
            max_turn = math.radians(self.turn_rate) * dt
            if abs(angle_diff) < max_turn:
                self.direction = target_angle
            else:
                self.direction += max_turn if angle_diff > 0 else -max_turn

            # Move in the current direction
            self.x += math.cos(self.direction) * self.speed * dt
            self.y += math.sin(self.direction) * self.speed * dt

            # Check if IceShard hits the player
            if pygame.Rect(self.x, self.y, self.size, self.size).colliderect(player.rect):
                self.hit_player = True
                
            if self.life_time <= 0:
                self.active = False

    def render(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))
        
        
class IllusionBoss(BaseBoss):
    def __init__(self, x, y, width, height, speed=75, damage=15, health=500):
        super().__init__(x, y, width=150, height=300, health=health)
        self.speed = speed
        self.damage = damage
        self.image.fill((0,0,0))  # Spiderling color
        
        self.alive = True

    def update(self, dt, player, platforms):
        super().update(dt, player, platforms)
        # Calculate direction towards the player
        target_x = player.character_x + player.width / 2 - self.width / 2
        target_y = player.character_y + player.height / 2 - self.height / 2
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # Normalize direction and move towards the player
        if distance > 0:
            self.x += (dx / distance) * self.speed * dt
            self.y += (dy / distance) * self.speed * dt

        # Check if spiderling hits the player
        if self.alive:
            self.contact_hit(player)
            
        for bullet in player.bullets:
            if bullet.active and self.rect.colliderect(pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)):
                bullet.active = False
                self.take_damage(bullet.damage)
            

    def contact_hit(self, player):
        """Implement an attack pattern against the player."""
        # Placeholder attack logic: Check if the player is within a certain range
        if self.rect.colliderect(player.rect):  # Check for collision with player
            player.take_damage(self.damage)

    def render(self, screen):
        super().render(screen)

