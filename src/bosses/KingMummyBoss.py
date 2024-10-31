import pygame
import math
import random
from src.constants import *
from src.bosses.BaseBoss import BaseBoss
from src.bosses.BossBullet import BossBullet
from src.bosses.BeamAttack import BeamAttack

class KingMummyBoss(BaseBoss):
    def __init__(self, x, y, health=300):
        super().__init__(x, y, width=50, height=80, health=health)
        self.image.fill((200, 200, 200))
        self.visible = True

        # Revive properties
        self.num_life = 2
        self.reviving = False
        self.invulnerable = False
        self.revive_timer = 0
        self.blink_timer = 0
        self.blink_interval = 0.25
        self.revive_duration = 3
        self.original_health = self.health
        
        # Attack properties
        self.platforms = None
        self.bandages = []
        self.bandage_duration = 15
        self.bandage_time = self.bandage_duration
        self.bandage_timer = 0
        self.num_bandages = 10
        self.bandage_width = 40
        self.bandage_height = 10
        
        # Jump attack properties
        self.move_speed = 75
        self.jump_force = JUMP_FORCE
        self.gravity = GRAVITY
        self.velocity_y = 0
        self.on_ground = False
        self.ground_y = GROUND_LEVEL_Y
        self.jump_duration = 10
        self.x = WIDTH / 2 - self.width / 2
        self.y = 0 - self.height
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Cursed Speed properties
        self.cursed_speed_duration = 5
        self.original_move_speed = self.move_speed

    def update(self, dt, player, platforms):
        super().update(dt, player, platforms)
        self.platforms = platforms

        if self.reviving:
            self.revive(dt)
            self.current_attack = None
            
        if len(self.bandages) > 0:
            self.update_bandages(dt, player)
        
        if not self.reviving:  
            if self.on_ground and player.on_ground:
                if player.character_y < self.y:
                    self.velocity_y = self.jump_force
                    self.on_ground = False
            
            if player.character_x < self.x:
                self.x -= self.move_speed * dt
            elif player.character_x > self.x:
                self.x += self.move_speed * dt

        if not self.on_ground:
            self.velocity_y += self.gravity * dt
            self.y += self.velocity_y * dt

        collided, platform = self.check_platform_collision(self.platforms)
        if collided:
            self.y = platform.rect.top - self.height + 1
            self.on_ground = True
            self.velocity_y = 0
        else:
            self.on_ground = False

        if self.y + self.height >= self.ground_y:
            self.y = self.ground_y - self.height
            self.velocity_y = 0
            self.on_ground = True

        self.rect.x = self.x
        self.rect.y = self.y

    def select_attack(self, player):
        attack_choice = random.choice(["cursed_wrappings", "cursed_speed"])
        if attack_choice == "cursed_wrappings":
            self.current_attack = self.cursed_wrappings
        elif attack_choice == "cursed_speed":
            self.current_attack = self.cursed_speed

    def die(self):
        """Handle boss death."""
        self.num_life -= 1
        if self.num_life < 0:
            print("Boss defeated!")
            self.alive = False
        else:
            self.reviving = True
            self.invulnerable = True
            self.revive_timer = 0

    def revive(self, dt):
        """Make the boss invulnerable and blink during revival."""
        self.revive_timer += dt
        self.blink_timer += dt

        if self.blink_timer >= self.blink_interval:
            self.visible = not self.visible
            self.blink_timer = 0

        if self.revive_timer >= self.revive_duration:
            self.reviving = False
            self.invulnerable = False
            self.visible = True
            self.health = self.original_health
            
    def cursed_wrappings(self, dt, player):
        """Spawns bandages with a blinking appearance phase."""
        self.bandages = []

        ground_y = GROUND_LEVEL_Y - 10
        platform_rects = [
            platform.rect for row in self.platforms for platform in row if platform is not None
        ]

        num_ground_bandages = self.num_bandages // 2
        num_platform_bandages = self.num_bandages - num_ground_bandages

        for _ in range(min(num_platform_bandages, len(platform_rects))):
            platform_rect = random.choice(platform_rects)
            x = random.randint(platform_rect.x, platform_rect.x + platform_rect.width - self.bandage_width)
            y = platform_rect.y
            bandage = Bandage(x, y, self.bandage_width, self.bandage_height)
            self.bandages.append(bandage)

        for _ in range(num_ground_bandages):
            x = random.randint(0, WIDTH - self.bandage_width)
            bandage = Bandage(x, ground_y, self.bandage_width, self.bandage_height)
            self.bandages.append(bandage)

        self.end_attack()
        
    def cursed_speed(self, dt, player):
        """
        Cursed Speed: The mummy walks faster for 5 seconds
        """
        self.move_speed = self.original_move_speed * 2
        if self.attack_elapsed_time >= self.cursed_speed_duration:
            self.move_speed = self.original_move_speed
            self.end_attack()


    def check_platform_collision(self, platforms):
        for platform_row in platforms:
            for platform in platform_row:
                if platform and self.rect.colliderect(platform.rect) and self.velocity_y >= 0:
                    return True, platform
        return False, None


    def update_bandages(self, dt, player):
        for bandage in self.bandages:
            bandage.update(dt)
            if bandage.active and bandage.rect.colliderect(player.rect):
                player.take_damage(bandage.damage)
                self.bandages.remove(bandage)

    def render(self, screen):
        if self.visible:
            super().render(screen)
        for bandage in self.bandages:
            bandage.render(screen)

class Bandage:
    def __init__(self, x, y, width, height, appearance_duration=1, blink_interval=0.1):
        self.rect = pygame.Rect(x, y, width, height)
        self.active = False
        self.appearance_timer = appearance_duration
        self.blink_timer = 0
        self.blink_interval = blink_interval
        self.visible = False
        self.damage = 10

    def update(self, dt):
        if not self.active:
            self.appearance_timer -= dt
            self.blink_timer += dt
            if self.blink_timer >= self.blink_interval:
                self.visible = not self.visible
                self.blink_timer = 0
            if self.appearance_timer <= 0:
                self.active = True
                self.visible = True

    def render(self, screen):
        if self.visible:
            pygame.draw.rect(screen, (150, 75, 0), self.rect)
