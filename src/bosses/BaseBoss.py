import pygame
from src.constants import *
from src.BossBullet import BossBullet
class BaseBoss:
    def __init__(self, x, y, speed=2, health=100):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.width = 200  # Width of the boss
        self.height = 400  # Height of the boss
        self.image = pygame.Surface((self.width, self.height))  # Placeholder for boss image
        self.image.fill((255, 0, 0))  # Color for visualization (red)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.float_direction = 1  # 1 for down, -1 for up
        self.float_speed = 50  # Speed of vertical floating movement
        self.attack_timer = 0  # Timer for attacks
        self.attack_delay = 1000  # Delay between attacks in milliseconds
        self.alive = True
        self.bullets = []

    def take_damage(self, amount):
        """Reduce health when taking damage."""
        self.health -= amount
        if self.health <= 0:
            self.die()
        
    def update(self, dt, player):
        # Update position
        self.rect.x += self.speed * dt  # Move right at constant speed

        # Floating effect
        self.y += self.float_direction * self.float_speed * dt
        if self.y > HEIGHT - self.height - (5 * TILE_SIZE) or self.y < 0:  # Bounce between top and bottom
            self.float_direction *= -1

        self.rect.y = self.y
        
        # Check for attack
        self.attack_timer += dt * 1000  # Convert dt to milliseconds
        if self.attack_timer >= self.attack_delay:
            self.attack(player)
            self.attack_timer = 0  # Reset timer after attack

        for bullet in self.bullets:
            bullet.update(dt)

    # Remove inactive bullets
        self.bullets = [bullet for bullet in self.bullets if bullet.active]
        
    def attack(self, player):
        """Implement an attack pattern against the player."""
        # Placeholder attack logic: Check if the player is within a certain range
        if self.rect.colliderect(player.rect):  # Check for collision with player
            player.take_damage(50)  # Assume the player has a `take_damage` method
        bullet_x = self.rect.left  # Start bullet from the left edge of the boss
        bullet_y = self.rect.centery
        direction = "left"  # Always shoot towards the left
        bullet = BossBullet(bullet_x, bullet_y, direction)
        self.bullets.append(bullet)


    def take_damage(self, amount):
        """Reduce health when taking damage."""
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        """Handle boss death."""
        print("Boss defeated!")  # Placeholder for boss defeat logic
        self.alive = False

    def render(self, screen):
        """Draw the boss on the screen."""
        if self.alive:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        
        for bullet in self.bullets:
            bullet.render(screen)
        
        

