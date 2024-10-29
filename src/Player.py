from src.constants import *
from src.Util import SpriteManager
import pygame
import time
from src.Bullet import Bullet
class Player:
    def __init__(self, health=100):
        self.character_x = WIDTH / 2 - (CHARACTER_WIDTH) / 2
        self.character_y = (6 * TILE_SIZE - CHARACTER_HEIGHT) * 3
        self.width = CHARACTER_WIDTH
        self.height = CHARACTER_HEIGHT
        self.direction = "front"  # left right front
        self.sprite_collection = SpriteManager().spriteCollection
        self.animation = self.sprite_collection["character_front"].animation
        self.health = health
        self.velocity_y = 0  # Vertical speed (used for jumping/falling)
        self.is_jumping = False  # Track if the player is in the air
        self.on_ground = True
        self.jump_force = JUMP_FORCE  # Force applied when jumping
        self.gravity = GRAVITY  # Gravity that pulls the player down
        self.ground_y = self.character_y  # Starting ground level
        
        self.rect = pygame.Rect(self.character_x + CHARACTER_WIDTH, self.character_y, CHARACTER_WIDTH, CHARACTER_HEIGHT * 2.5)
        
        self.movement_speed = CHARACTER_MOVE_SPEED
        self.alive = True
        self.bullets = []
        
        self.stun_duration = 0  # Track how long the player is stunned
        self.is_stunned = False  # Flag to check if the player is stunned

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
                self.animation = self.sprite_collection["character_walk_right"].animation
                self.character_x -= self.movement_speed * dt
            elif pressedKeys[pygame.K_RIGHT]:
                self.direction = "right"
                self.animation = self.sprite_collection["character_walk_right"].animation
                self.character_x += self.movement_speed * dt
            elif pressedKeys[pygame.K_SPACE] and self.on_ground:
                self.is_jumping = True
                self.velocity_y = self.jump_force
                self.on_ground = False
                self.animation = self.sprite_collection["character_walk_right"].animation
            else:
                self.direction = "front"
                self.animation = self.sprite_collection["character_front"].animation
                
            if pressedKeys[pygame.K_SPACE] and pressedKeys[pygame.K_RIGHT] and self.on_ground:
                self.is_jumping = True
                self.velocity_y = self.jump_force  # Apply the jump force
                self.on_ground = False
                self.direction = "right"
                self.animation = self.sprite_collection["character_walk_right"].animation
                self.character_x += self.movement_speed * dt  # Move right while jumping
            
            if pressedKeys[pygame.K_SPACE] and pressedKeys[pygame.K_LEFT] and self.on_ground:
                self.is_jumping = True
                self.velocity_y = self.jump_force  # Apply the jump force
                self.on_ground = False
                self.direction = "left"
                self.animation = self.sprite_collection["character_walk_right"].animation
                self.character_x -= self.movement_speed * dt  # Move right while jumping
            if pressedKeys[pygame.K_RETURN]:
                self.shoot()
            
        for bullet in self.bullets:
            bullet.update(dt)
            if bullet.active and boss.rect.colliderect(pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)):
                bullet.active = False  # Deactivate bullet
                boss.take_damage(1)  # Inflict damage to the boss 
        
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
            self.character_y = platform.rect.top - CHARACTER_HEIGHT * 2.5
            self.on_ground = True
            self.is_jumping = False
            self.velocity_y = 0
    
        self.animation.update(dt)
        
    def stun(self, duration):
        """Stuns the player for a given duration."""
        self.is_stunned = True
        self.stun_duration = duration
        
        
    def check_platform_collision(self, platforms):
            for platform_row in platforms:
                for platform in platform_row:
                    if platform is not None:
                        if self.rect.colliderect(platform.rect) and self.velocity_y > 0:
                            return True, platform
            
            return False, None
    
        
    def revert_to_default(self):
        self.movement_speed = CHARACTER_MOVE_SPEED
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
    
    
    def shoot(self):
        # Create a bullet at the player's position, moving in the current direction
        bullet_x = self.character_x + CHARACTER_WIDTH // 2  # Adjust bullet starting position
        bullet_y = self.character_y + CHARACTER_HEIGHT // 2
        bullet_direction = self.direction
        if bullet_direction == 'front':
            bullet_direction= 'right'
        # Add the new bullet to the list of active bullets
        bullet = Bullet(bullet_x, bullet_y, bullet_direction)
        self.bullets.append(bullet)
        
    def render(self, screen):
        char_img = self.animation.image
        if self.direction == "left":
            char_img = pygame.transform.flip(char_img, True, False)
        if self.alive:
            screen.blit(char_img, (self.character_x, self.character_y))
        
        for bullet in self.bullets:
            bullet.render(screen)
        
