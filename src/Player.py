from src.constants import *
from src.Util import SpriteManager
import pygame
import time
from src.Bullet import Bullet
from src.platforms.SpecialPlatform import SpecialPlatform
from src.resources import *
class Player:
    def __init__(self, health=50):
        self.character_x = WIDTH / 2 - (CHARACTER_WIDTH) / 2
        self.character_y = GROUND_LEVEL_Y - CHARACTER_HEIGHT
        self.width = CHARACTER_WIDTH
        self.height = CHARACTER_HEIGHT
        self.direction = "front"  # left right front
        self.shooting_direction = "right"
        # self.sprite_collection = SpriteManager().spriteCollection
        self.animation = sprite_collection["king_fire_gun"].animation
        self.health = health
        self.max_health = health
        self.defense = 0
        self.velocity_y = 0  # Vertical speed (used for jumping/falling)
        self.is_jumping = False  # Track if the player is in the air
        self.on_ground = True
        self.jump_force = JUMP_FORCE  # Force applied when jumping
        self.gravity = GRAVITY  # Gravity that pulls the player down
        self.ground_y = self.character_y  # Starting ground level
        #timer for turning transparency (flash)
        self.flash_timer = 0
        #invincible
        self.invulnerable = False
        self.invulnerable_duration = 0
        self.invulnerable_timer = 0

        self.rect = pygame.Rect(self.character_x + CHARACTER_WIDTH, self.character_y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
        
        self.default_move_speed = CHARACTER_MOVE_SPEED
        self.movement_speed = CHARACTER_MOVE_SPEED
        self.alive = True
        self.bullets = []
        self.bullet_damage = 1
        self.firerate_cooldown = 0.2
        self.firerate_time = self.firerate_cooldown
        
        self.stun_duration = 0  # Track how long the player is stunned
        self.is_stunned = False  # Flag to check if the player is stunned
        
        self.poison_platform_accumulated_time = 0
        self.poison_platform_duration = 1
        
        
        self.active_weapon = "pistol"  # Default weapon
        self.shotgun_spread = 3  # Number of bullets for shotgun spread
        self.shotgun_angle = 15
        self.shotgun_ability = False
        self.shotgun_damage_scale = 0.6
        self.defense_scale = 1
        self.jump_ability= False
        self.jump_count = 0  # Track the number of jumps performed
        self.jump_scaling = 1
        
    def update(self, dt, events, platforms, boss):
        # Update stun timer if player is stunned
        if self.is_stunned:
            self.stun_duration -= dt
            if self.stun_duration <= 0:
                self.is_stunned = False  # Remove stun once duration ends
                self.velocity_y = 0
        
        self.rect.x = self.character_x
        self.rect.y = self.character_y
        
        pressedKeys = pygame.key.get_pressed()
        if not self.is_stunned:
            if pressedKeys[pygame.K_LEFT]:
                self.direction = "left"
                self.shooting_direction = "left"
                if self.character_x <= 0:
                    self.character_x = 0
                else:
                    self.character_x -= self.movement_speed * dt
            elif pressedKeys[pygame.K_RIGHT]:
                self.direction = "right"
                self.shooting_direction = "right"
                if self.character_x + self.width >= WIDTH:
                    self.character_x = WIDTH - self.width
                else:
                    self.character_x += self.movement_speed * dt
            """
            elif pressedKeys[pygame.K_z] and self.on_ground:
                self.is_jumping = True
                self.velocity_y = self.jump_force
                self.on_ground = False
            else:
                self.direction = "front"
            """
            if pressedKeys[pygame.K_z]:
                if self.on_ground:
                    # First jump
                    self.is_jumping = True
                    self.velocity_y = self.jump_force * self.jump_scaling
                    self.on_ground = False
                    self.jump_count = 1
                    gSounds["mc_jump"].play()
                elif self.jump_count == 1 and self.velocity_y > 0 and self.jump_ability:
                    # Double jump
                    self.is_jumping = True
                    self.velocity_y = self.jump_force * self.jump_scaling
                    self.jump_count += 1
                    gSounds["mc_jump"].play()
                    # print(self.jump_ability)
                    # print("Double Jump:", self.count_test)
                    # print("----------")
            """
            if pressedKeys[pygame.K_z] and pressedKeys[pygame.K_RIGHT] and self.on_ground:
                self.is_jumping = True
                self.velocity_y = self.jump_force  # Apply the jump force
                self.on_ground = False
                self.direction = "right"
                if self.character_x + self.width >= WIDTH:
                    self.character_x = WIDTH - self.width
                else:
                    self.character_x += self.movement_speed * dt  # Move right while jumping
            
            if pressedKeys[pygame.K_z] and pressedKeys[pygame.K_LEFT] and self.on_ground:
                self.is_jumping = True
                self.velocity_y = self.jump_force  # Apply the jump force
                self.on_ground = False
                self.direction = "left"
                if self.character_x <= 0:
                    self.character_x = 0
                else:
                    self.character_x -= self.movement_speed * dt  # Move right while jumping
            """   
            # Shooting control
            if pressedKeys[pygame.K_x]:
                self.animation.update(dt)
                self.firerate_time += dt
                if self.firerate_time >= self.firerate_cooldown:
                    self.firerate_time = 0
                    self.shoot()  # Trigger shooting and shooting animation
            else:
                self.firerate_time = self.firerate_cooldown
                self.animation.Idle()
                
            if pressedKeys[pygame.K_DOWN] and self.on_ground:
                self.on_ground = False
                self.character_y += self.rect.height
                self.velocity_y = self.gravity * dt
            
            if pressedKeys[pygame.K_1]:
                self.active_weapon = "pistol"
                self.animation = sprite_collection["king_fire_gun"].animation
                gSounds["mc_change_gun"].stop()
                gSounds["mc_change_gun"].play()
            elif pressedKeys[pygame.K_2] and self.shotgun_ability:
                self.active_weapon = "shotgun"
                self.animation = sprite_collection["king_fire_shotgun"].animation
                gSounds["mc_change_gun"].stop()
                gSounds["mc_change_gun"].play()
            
        for bullet in self.bullets:
            bullet.update(dt)
            if bullet.active and boss.rect.colliderect(pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)):
                bullet.active = False  # Deactivate bullet
                boss.take_damage(bullet.damage)  # Inflict damage to the boss 
        
        # Remove inactive bullets
        self.bullets = [bullet for bullet in self.bullets if bullet.active]   
        
        # Apply gravity
        if not self.on_ground:
            self.velocity_y += self.gravity * dt  # Apply gravity to vertical speed
            self.character_y += self.velocity_y * dt  # Update vertical position 
            
        
        if self.character_y >= self.ground_y:
            self.character_y = self.ground_y
            self.velocity_y = 0
            self.on_ground = True
            self.is_jumping = False
            self.jump_count = 0
            self.poison_platform_accumulated_time = 0  # Reset if not on poison platform
            self.revert_to_default()

        #self.check_platform_collision(platforms)
        colli,platform = self.check_platform_collision(platforms)
        if not colli:
            # No platform collision, apply gravity as player is in the air
            if self.character_y + CHARACTER_HEIGHT >= self.ground_y:
                pass
            elif self.character_y + CHARACTER_HEIGHT < self.ground_y:
                self.on_ground = False
        else:
            # Collided with a platform
            platform.trigger_effect(self)
            if platform.area == 2 and isinstance(platform, SpecialPlatform):
                # Poison platform logic
                self.poison_platform_accumulated_time += dt
                if self.poison_platform_accumulated_time >= self.poison_platform_duration:
                    self.take_damage(5)  # Apply damage every second on poison platform
            else:
                self.poison_platform_accumulated_time = 0  # Reset if not on poison platform
            self.character_y = platform.rect.top - CHARACTER_HEIGHT
            self.on_ground = True
            self.is_jumping = False
            self.velocity_y = 0
            self.jump_count = 0

        if self.invulnerable:
            self.flash_timer = self.flash_timer+dt
            self.invulnerable_timer = self.invulnerable_timer+dt

            if self.invulnerable_timer > self.invulnerable_duration:
                self.invulnerable = False
                self.invulnerable_timer = 0
                self.invulnerable_duration=0
                self.flash_timer=0
        
    def stun(self, duration):
        """Stuns the player for a given duration."""
        self.is_stunned = True
        self.stun_duration = duration
        
        
    def check_platform_collision(self, platforms):
        temp_rect = self.rect.copy()
        temp_rect.y = self.rect.y + (2 * self.rect.height / 3)
        temp_rect.height = self.rect.height / 3
        for platform_row in platforms:
            for platform in platform_row:
                if platform is not None:
                    if temp_rect.colliderect(platform.rect) and self.velocity_y > 0:
                        return True, platform
            
        return False, None
    
        
    def revert_to_default(self):
        self.movement_speed = self.default_move_speed
        
    def reset_position(self):
        self.character_x = WIDTH / 2 - (CHARACTER_WIDTH) / 2
        self.character_y = GROUND_LEVEL_Y - CHARACTER_HEIGHT
    
    def take_damage(self, damage):
        if not self.invulnerable:  # Only take damage if not invulnerable
            self.health -= damage * self.defense_scale
            gSounds["hit_player"].play()
            if self.health <= 0:
                self.alive = False
            self.SetInvulnerable(1) 
    
    def SetInvulnerable(self, duration):
        self.invulnerable = True
        self.invulnerable_duration = duration
    
    def shoot(self):
        # Create a bullet at the player's position, moving in the current direction
        bullet_x = self.character_x + CHARACTER_WIDTH // 2  # Adjust bullet starting position
        bullet_y = self.character_y + CHARACTER_HEIGHT // 2
        bullet_direction = self.shooting_direction
        if bullet_direction == 'front':
            bullet_direction= 'right'
        if self.active_weapon == "pistol":
            # Pistol fires a single bullet
            bullet = Bullet(bullet_x, bullet_y, bullet_direction, damage=self.bullet_damage)
            gSounds["mc_gun"].play()
            self.bullets.append(bullet)
        elif self.active_weapon == "shotgun":
            # Shotgun fires multiple bullets in a spread
            for i in range(self.shotgun_spread):
                angle_offset = (i - self.shotgun_spread // 2) * self.shotgun_angle
                bullet = Bullet(bullet_x, bullet_y, bullet_direction, angle_offset=angle_offset, bullet_type = "shotgun", damage=self.bullet_damage * self.shotgun_damage_scale)
                self.bullets.append(bullet)
            gSounds["mc_shotgun"].play()
                
        
    def render(self, screen):
        char_img = self.animation.image
        char_img = pygame.transform.scale(char_img, (self.rect.width, self.rect.height))
        if self.shooting_direction == "left":
            char_img = pygame.transform.flip(char_img, True, False)
        if self.alive:
             if int(self.flash_timer * 10) % 2 == 0:
                    screen.blit(char_img, (self.character_x, self.character_y))
        
        for bullet in self.bullets:
            bullet.render(screen)
