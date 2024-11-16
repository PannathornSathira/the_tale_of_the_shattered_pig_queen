import pygame
import math
import random
from src.constants import *
from src.bosses.BaseBoss import BaseBoss
from src.resources import *

class KingMummyBoss(BaseBoss):
    def __init__(self, x, y, health=300, damage=10, damage_speed_scaling = 1):
        super().__init__(x, y, width=140, height=200, health=health, damage=damage, damage_speed_scaling = damage_speed_scaling)
        self.animation = sprite_collection["king_mummy_boss_idle"].animation
        self.visible = True
        self.direction = "left"
        self.damage_speed_scaling = damage_speed_scaling
        # Revive properties
        self.num_life = 2
        self.reviving = False
        self.invulnerable = False
        self.revive_timer = 0
        self.blink_timer = 0
        self.blink_interval = 0.25
        self.revive_duration = 3
        self.original_health = self.health * 0.7
        self.health = self.original_health
        self.revive_image = sprite_collection["king_mummy_dead"].image
        
        # Attack properties
        self.platforms = None
        self.bandages = []
        self.bandage_duration = 15
        self.bandage_time = self.bandage_duration
        self.bandage_timer = 0
        self.num_bandages = 10
        self.bandage_width = 40
        self.bandage_height = 20
        
        # Jump attack properties
        self.move_speed = 100
        self.jump_force = JUMP_FORCE
        self.gravity = GRAVITY
        self.velocity_y = 0
        self.on_ground = False
        self.ground_y = GROUND_LEVEL_Y
        self.jump_cooldown = 2.5
        self.jump_cooldown_timer = 0
        self.x = WIDTH / 2 - self.width / 2
        self.y = 0 - self.height
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Cursed Speed properties
        self.cursed_speed_duration = 5
        self.original_move_speed = self.move_speed
        
        gSounds["mummy_sound"].play(-1)

    def update(self, dt, player, platforms):
        super().update(dt, player, platforms)
        self.platforms = platforms
        
        self.jump_cooldown_timer += dt
        
        if self.current_attack == self.cursed_speed:
            self.jump_cooldown = 1.5
        else:
            self.jump_cooldown = 3
        
        if self.current_attack:
            self.animation = sprite_collection["king_mummy_boss_attack"].animation
        else:
            self.animation = sprite_collection["king_mummy_boss_idle"].animation

        if self.reviving:
            self.revive(dt)
            self.current_attack = None
            
        if len(self.bandages) > 0:
            self.update_bandages(dt, player)
        
        if not self.reviving:  
            if self.on_ground and player.on_ground:
                if self.jump_cooldown_timer >= self.jump_cooldown:
                    if player.character_y + player.height < (self.y + self.height) / 2:
                        self.velocity_y = 1.6 * self.jump_force
                        self.on_ground = False
                        self.jump_cooldown_timer = 0
                    elif player.character_y + player.height < self.y + self.height:
                        self.velocity_y = self.jump_force
                        self.on_ground = False
                        self.jump_cooldown_timer = 0
                    elif player.character_y + player.height > self.y + self.height:
                        self.on_ground = False
                        self.y += self.height / 2
                        self.rect.y = self.y
                        self.velocity_y = self.gravity * dt
                        self.jump_cooldown_timer = 0
            
            if player.character_x + player.width <= self.x + 10:
                self.x -= self.move_speed * dt
                self.direction = "left"
            elif player.character_x + 10 >= self.x + self.width:
                self.x += self.move_speed * dt
                self.direction = "right"

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
        
        self.animation.update(dt)

    def select_attack(self, player):
        attack_choice = random.choice(["cursed_wrappings", "cursed_speed"])
        if attack_choice == "cursed_wrappings":
            self.current_attack = self.cursed_wrappings
        elif attack_choice == "cursed_speed":
            self.current_attack = self.cursed_speed
            if not self.reviving:
                gSounds["mummy_speed"].play()

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
            gSounds["mummy_sound"].fadeout(1000)

    def revive(self, dt):
        """Make the boss invulnerable and blink during revival."""
        self.revive_timer += dt
        self.blink_timer += dt
        
        if self.revive_timer / self.revive_duration >= 0.8:
            self.revive_image = sprite_collection["king_mummy_revive"].image
            self.rect.width = 200
            self.width = 200
        else:
            self.revive_image = sprite_collection["king_mummy_dead"].image
            self.rect.width = 80
            self.width = 80

        if self.blink_timer >= self.blink_interval:
            self.visible = not self.visible
            self.blink_timer = 0

        if self.revive_timer >= self.revive_duration:
            self.reviving = False
            self.invulnerable = False
            self.visible = True
            self.health = self.original_health
            self.rect.width = 140
            self.width = 140
            gSounds["mummy_sound"].play(-1)
            
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
            y = platform_rect.y - 10
            bandage = Bandage(x, y, self.bandage_width, self.bandage_height, damage=self.damage)
            self.bandages.append(bandage)

        for _ in range(num_ground_bandages):
            x = random.randint(0, WIDTH - self.bandage_width)
            bandage = Bandage(x, ground_y, self.bandage_width, self.bandage_height, damage=self.damage)
            self.bandages.append(bandage)
            
        gSounds["mummy_bandage_grab"].play()
        self.end_attack()
        
    def cursed_speed(self, dt, player):
        """
        Cursed Speed: The mummy walks faster for 5 seconds
        """
        self.move_speed = self.original_move_speed * 2
        if self.attack_elapsed_time >= self.cursed_speed_duration:
            self.move_speed = self.original_move_speed
            gSounds["mummy_speed"].fadeout(1000)
            self.end_attack()


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


    def update_bandages(self, dt, player):
        for bandage in self.bandages:
            bandage.update(dt)
            if bandage.active and bandage.rect.colliderect(player.rect):
                player.take_damage(bandage.damage)
                self.bandages.remove(bandage)

    def render(self, screen):
        if self.alive:
            if self.visible:
                if self.reviving:
                    char_img = self.revive_image
                else:
                    char_img = self.animation.image
                    
                if self.current_attack:
                    offset = 60
                else:
                    offset = 20
                char_img = pygame.transform.scale(char_img, (self.rect.width + offset, self.rect.height))
                if self.direction == "right":
                    char_img = pygame.transform.flip(char_img, True, False)
                    screen.blit(char_img, (self.x, self.y))
                else:
                    screen.blit(char_img, (self.x - offset//2, self.y))
            for bandage in self.bandages:
                bandage.render(screen)

class Bandage:
    def __init__(self, x, y, width, height, appearance_duration=1, blink_interval=0.1, damage=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.active = False
        self.appearance_timer = appearance_duration
        self.blink_timer = 0
        self.blink_interval = blink_interval
        self.visible = False
        self.damage = damage
        self.animation = sprite_collection["king_mummy_cursed_wrapping"].animation

    def update(self, dt):
        self.animation.update(dt)
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
        img = self.animation.image
        img = pygame.transform.scale(img, (self.rect.width, self.rect.height))
        screen.blit(img, (self.rect.x, self.rect.y))
