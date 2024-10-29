import pygame
from src.constants import *
from src.bosses.BeamAttack import BeamAttack
class BaseBoss:
    def __init__(self, x, y, width=200, height=400, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.width = width  # Width of the boss
        self.height = height  # Height of the boss
        self.image = pygame.Surface(
            (self.width, self.height)
        )  # Placeholder for boss image
        self.image.fill((255, 0, 0))  # Color for visualization (red)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.float_direction = 1  # 1 for down, -1 for up
        self.float_speed = 50  # Speed of vertical floating movement

        # Attack properties
        self.attack_cooldown = 5  # Time between attacks
        self.attack_delay_timer = 0
        self.attack_elapsed_time = 0
        self.current_attack = None  # Track the current attack pattern
        self.bullets = []  # List to hold active bullets
        
        self.alive = True

    def take_damage(self, amount):
        """Reduce health when taking damage."""
        self.health -= amount
        if self.health <= 0:
            self.die()
        
    def update(self, dt, player):

        self.rect.x = self.x
        self.rect.y = self.y

        # Update bullets
        for bullet in self.bullets:
            bullet.update(dt)
            
            if bullet.active and player.rect.colliderect(pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)):
                if not isinstance(bullet, BeamAttack):
                    bullet.active = False
                player.take_damage(10) 

            # Remove inactive bullets
            if not bullet.active:
                self.bullets.remove(bullet)

        if self.current_attack is None:
            # Attack if cooldown has elapsed
            self.attack_delay_timer += dt
            if self.attack_delay_timer >= self.attack_cooldown:
                self.select_attack(player)
                self.attack_elapsed_time = 0

        else:
            self.current_attack(dt, player)
            self.attack_elapsed_time += dt

        self.contact_hit(player)
                # for boss_bullet in boss.bullets:
        #     if boss_bullet.active and self.rect.colliderect(pygame.Rect(boss_bullet.x, boss_bullet.y, boss_bullet.width, boss_bullet.height)):
        #         boss_bullet.active = False
        #         self.take_damage(10) 

    def select_attack(self, player):
        pass

    # End the attack if the duration is over
    def end_attack(self):
        self.current_attack = None
        self.attack_delay_timer = 0
        self.attack_elapsed_time = 0

    def contact_hit(self, player):
        """Implement an attack pattern against the player."""
        # Placeholder attack logic: Check if the player is within a certain range
        if self.rect.colliderect(player.rect):  # Check for collision with player
            # player.take_damage(10)  # Assume the player has a `take_damage` method
            player.take_damage(10)

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
        
        

