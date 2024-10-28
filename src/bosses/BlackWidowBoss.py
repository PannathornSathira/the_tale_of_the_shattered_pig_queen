import pygame
import math
import random
from src.constants import *
from src.bosses.BaseBoss import BaseBoss
from src.bosses.BossBullet import BossBullet
from src.bosses.BeamAttack import BeamAttack


class BlackWidowBoss(BaseBoss):
    def __init__(self, x, y, health=300):
        super().__init__(x, y, width=200, height=200, health=health)

        # Customizing the appearance
        self.image.fill((0, 0, 0))

        # Jumping attack properties
        self.jump_duration = 1.5
        self.jump_end_x = self.x
        self.jump_end_y = self.y
        self.jump_height = 500

        # Cobweb attack properties
        self.web = None
        self.web_width = 50
        self.web_height = 50
        self.web_image = pygame.Surface((self.web_width, self.web_height))
        self.web_image.fill((155, 155, 155))
        self.web_projectile_duration = 1
        self.web_slow_duration = 3
        self.web_slow_timer = 0
        self.web_is_slow = False

        # Poison attack properties
        self.poison_duration = 3  # Duration in seconds
        self.poison_tick_rate = 0.5  # Damage every 0.5 seconds
        self.poison_damage = 2  # Damage per tick
        self.is_poisoned = False
        self.poison_timer = 0
        self.poison_tick_timer = 0

        # Summoning properties
        self.spiderlings = []  # List to track summoned spiderlings

    def contact_hit(self, player):
        if self.rect.colliderect(player.rect):  # Check for collision with player
            # player.take_damage(10)  # Assume the player has a `take_damage` method
            self.apply_poison(player)

    def apply_poison(self, player):
        """Apply poison effect to the player."""
        if not self.is_poisoned:
            print("Got poisoned!")
            self.is_poisoned = True
            self.poison_timer = 0
            self.poison_tick_timer = 0

    def update_poison_effect(self, dt, player):
        """Manage poison damage over time if the player is poisoned."""
        if self.is_poisoned:
            self.poison_timer += dt
            self.poison_tick_timer += dt

            # Inflict poison damage at each tick interval
            if self.poison_tick_timer >= self.poison_tick_rate:
                # player.health -= self.poison_damage
                print("Take damage")
                self.poison_tick_timer = 0  # Reset tick timer

            # End poison effect after poison duration
            if self.poison_timer >= self.poison_duration:
                self.is_poisoned = False

    def update(self, dt, player):
        # Update position and check if the boss should attack
        super().update(dt, player)

        # Update poison effect
        self.update_poison_effect(dt, player)

        # Slow by web logic
        if self.web_is_slow:
            player.movement_speed = CHARACTER_MOVE_SPEED / 2
            self.web_slow_timer += dt
            if self.web_slow_timer >= self.web_slow_duration:
                player.movement_speed = CHARACTER_MOVE_SPEED
                self.web_is_slow = False

        # Update spiderlings
        for spiderling in self.spiderlings:
            spiderling.update(dt, player)
            if spiderling.hit_player:
                # player.take_damage(spiderling.damage)
                self.spiderlings.remove(spiderling)

    def select_attack(self, player):
        attack_choice = random.choice(["jump", "cobweb", "summon"])
        if attack_choice == "jump":
            self.current_attack = self.jump
        elif attack_choice == "cobweb":
            self.current_attack = self.cobweb
        elif attack_choice == "summon":
            self.current_attack = self.summon

    def jump(self, dt, player):
        if self.attack_elapsed_time == 0:
            # Record initial and target positions
            self.jump_start_x = self.x
            self.jump_start_y = self.y
            self.jump_end_x = player.character_x + player.width / 2 - self.width / 2
            self.jump_end_y = player.character_y + (3 * player.height) - self.height
            self.jump_peak_y = (
                self.jump_start_y - self.jump_height
            )  # Peak height for parabolic motion

        t = self.attack_elapsed_time / self.jump_duration
        if t <= 1.0:
            self.x = self.jump_start_x + t * (self.jump_end_x - self.jump_start_x)
            self.y = (
                (1 - t) * (1 - t) * self.jump_start_y
                + 2 * (1 - t) * t * self.jump_peak_y
                + t * t * self.jump_end_y
            )
        else:
            self.end_attack()
            self.x, self.y = self.jump_end_x, self.jump_end_y

    def cobweb(self, dt, player):
        if self.attack_elapsed_time == 0:
            self.web = pygame.Rect(
                self.x - self.width / 2,
                self.y + self.height / 2,
                self.web_width,
                self.web_height,
            )
            self.web_start_x = self.x
            self.web_start_y = self.y
            self.web_end_x = player.character_x + player.width / 2 - self.web_width / 2
            self.web_end_y = player.character_y + (3 * player.height) - self.web_height

        t = self.attack_elapsed_time / self.web_projectile_duration
        self.web.x = self.web_start_x + t * (self.web_end_x - self.web_start_x)
        self.web.y = self.web_start_y + t * (self.web_end_y - self.web_start_y)

        if self.web.colliderect(player.rect):
            self.web_is_slow = True
            self.web = None
            self.apply_poison(player)
            self.end_attack()

        elif (
            self.web.x + self.web_width < 0
            or self.web.x > WIDTH
            or self.web.y + self.web_height < 0
            or self.web.y > HEIGHT
        ):
            self.web = None
            self.end_attack()

    def summon(self, dt, player):
        """
        Summon spiderlings: Spiderlings appear randomly around the boss and try to attack the player.
        """
        if self.attack_elapsed_time == 0:
            spawn_x = self.x + self.width / 2 + random.randint(-100, 100)
            spawn_y = self.y + self.height / 2 + random.randint(-100, 100)
            spiderling = Spiderling(spawn_x, spawn_y)
            self.spiderlings.append(spiderling)
            self.end_attack()

    def render(self, screen):
        super().render(screen)
        for bullet in self.bullets:
            bullet.render(screen)

        if self.web is not None:
            screen.blit(self.web_image, (self.web.x, self.web.y))

        # Render spiderlings
        for spiderling in self.spiderlings:
            spiderling.render(screen)


class Spiderling:
    def __init__(self, x, y, speed=75, damage=5):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.size = 30
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((50, 50, 50))  # Spiderling color
        self.hit_player = False

    def update(self, dt, player):
        # Calculate direction towards the player
        target_x = player.character_x + player.width / 2 - self.size / 2
        target_y = player.character_y + player.height / 2 - self.size / 2
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # Normalize direction and move towards the player
        if distance > 0:
            self.x += (dx / distance) * self.speed * dt
            self.y += (dy / distance) * self.speed * dt

        # Check if spiderling hits the player
        if pygame.Rect(self.x, self.y, self.size, self.size).colliderect(player.rect):
            self.hit_player = True

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
