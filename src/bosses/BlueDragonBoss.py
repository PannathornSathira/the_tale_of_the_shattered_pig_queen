import pygame
import math
import random
from src.constants import *
from src.bosses.BaseBoss import BaseBoss
from src.bosses.BossBullet import BossBullet
from src.bosses.BeamAttack import BeamAttack


class BlueDragonBoss(BaseBoss):
    def __init__(self, x, y, health=300, damage=10):
        super().__init__(x, y, health=health, damage=damage)

        # Customizing the appearance for the Blue Dragon
        self.image.fill((0, 0, 255))  # Set color to blue

        # Stomp attack properties
        self.stomp_attack_duration = 5.5
        self.stomp_duration_gap = 1
        self.stomp_duration_time = 0
        self.stomp_damage = self.damage
        self.stomp_stun_distance = 300
        self.stomp_effect_duration = 0.2
        self.stomp_effect_time = 0
        self.stomp_effect_isVisible = False
        self.stomp_effect_rect1 = pygame.Rect(
            0, GROUND_LEVEL_Y, WIDTH, 20
        )  # Define the size and position of the effect
        self.stomp_effect_rect2 = pygame.Rect(
            self.x + self.width / 2 - self.stomp_stun_distance,
            GROUND_LEVEL_Y,
            self.stomp_stun_distance * 2,
            20,
        )  # Define the size and position of the effect

        # Frozen pillars attack prop
        self.beam_count = 5
        self.beam_width = 150
        self.beam_gap = 60
        self.beam_height = 1000
        self.beam_delay = 0.25
        self.beams = []

        # Frostbite ring attack prop
        self.frostbite_barrage_duration = 2
        self.bullet_gap_cooldown = 0.2
        self.bullet_gap_time = 0
        self.bullet_layer_num = 4
        self.bullet_angle = 100
        self.barrage_starting_angle = 0
        self.barrage_starting_angle_random_shift_max = 90

        # Glacial shard attack prop
        self.ice_shards = []  # List to track summoned spiderlings
        self.ice_summon_gap_cooldown = 1
        self.ice_summon_gap_time = 0
        self.num_ice_shards = 3

    def update(self, dt, player, platforms):
        # Update position and check if the boss should attack
        super().update(dt, player, platforms)

        # Update ice shards
        for ice_shard in self.ice_shards:
            ice_shard.update(dt, player, self)
            if ice_shard.hit_player:
                player.take_damage(ice_shard.damage)
                self.ice_shards.remove(ice_shard)

            if not ice_shard.active:
                self.ice_shards.remove(ice_shard)

    def select_attack(self, player):
        attack_choice = random.choice(
            ["stomp", "frozen_pillars", "frostbite_ring", "glacial_shards"]
        )
        # attack_choice = random.choice(["glacial_shards"])

        if attack_choice == "stomp":
            self.current_attack = self.stomp
        elif attack_choice == "frozen_pillars":
            self.current_attack = self.frozen_pillars
        elif attack_choice == "frostbite_ring":
            self.current_attack = self.frostbite_ring
        elif attack_choice == "glacial_shards":
            self.current_attack = self.glacial_shards

    def stomp(self, dt, player):
        """
        Stomp: Stomps the ground, inflicting damage. If the player is too close, they get stunned for 3 seconds.
        """
        self.stomp_duration_time += dt
        if self.stomp_duration_time >= self.stomp_duration_gap:
            self.stomp_duration_time = 0

            # Calculate distance from player
            distance = abs(
                (self.x + self.width / 2) - (player.character_x + player.width / 2)
            )
            if player.character_y + player.height >= GROUND_LEVEL_Y - TILE_SIZE:
                player.take_damage(self.stomp_damage)

                # Check for stun
                if distance <= self.stomp_stun_distance:
                    player.stun(3)

            # Show stomp effect
            self.stomp_effect_isVisible = True
            self.stomp_effect_time = 0  # Reset effect timer

        # Update effect duration
        if self.stomp_effect_isVisible:
            self.stomp_effect_time += dt
            if self.stomp_effect_time >= self.stomp_effect_duration:
                self.stomp_effect_isVisible = False  # Hide effect after duration

        # End the attack after the designated duration
        if self.attack_elapsed_time >= self.stomp_attack_duration:
            self.end_attack()

    def frozen_pillars(self, dt, player):
        """
        Frozen Pillars: pillars attack from below screen to above.
        """
        beam_direction = "up"

        if self.attack_elapsed_time == 0:
            beam_x_positions = random.sample(
                range(WIDTH // (self.beam_width + self.beam_gap)), self.beam_count
            )
            for i in range(self.beam_count):
                self.beams.append(
                    BeamAttack(
                        beam_x_positions[i] * (self.beam_width + self.beam_gap),
                        HEIGHT,
                        beam_direction,
                        self.beam_width,
                        self.beam_height,
                        damage=self.damage,
                    )
                )

        # Add beams to the bullets list at intervals of 0.25 seconds
        beam_index = int(self.attack_elapsed_time // self.beam_delay) + 1
        if len(self.bullets) < beam_index and beam_index <= 5:
            self.bullets.append(self.beams[beam_index - 1])

        if len(self.bullets) == 0:
            self.end_attack()
            self.beams = []

    def frostbite_ring(self, dt, player):
        """
        Frostbite Ring: Cone-shaped bullet attack.
        """
        if self.attack_elapsed_time == 0:
            self.barrage_starting_angle = random.randint(
                -self.barrage_starting_angle_random_shift_max,
                self.barrage_starting_angle_random_shift_max,
            )
        bullet_direction = "left"
        bullet_x = self.x + (self.width // 2)  # Center the bullet on the boss
        bullet_y = self.y + (
            self.height // 2
        )  # Start bullet at the center height of the boss
        self.bullet_gap_time += dt
        if self.bullet_gap_time >= self.bullet_gap_cooldown:
            self.bullet_gap_time = 0
            for i in range(self.bullet_layer_num):
                bullet = BossBullet(
                    x=bullet_x,
                    y=bullet_y,
                    direction=bullet_direction,
                    dx=self.barrage_starting_angle - (self.bullet_angle * self.bullet_layer_num / 2) + (self.bullet_angle * i),
                    damage=self.damage
                )  # Create a bullet
                self.bullets.append(bullet)  # Add bullet to the list

        # End the bullet attack if the duration is over
        if self.attack_elapsed_time >= self.frostbite_barrage_duration:
            self.end_attack()

    def glacial_shards(self, dt, player):
        """
        Glacial Shards: Blue Dragon raises its hands and hurls large, slow-moving ice shards toward the player. These shards break apart after a certain distance, exploding into smaller, faster ice bullets that scatter in every direction.
        """
        self.ice_summon_gap_time += dt
        if self.ice_summon_gap_time >= self.ice_summon_gap_cooldown:
            self.ice_summon_gap_time = 0
            self.num_ice_shards -= 1
            spawn_x = self.x + self.width / 2 + random.randint(-100, 100)
            spawn_y = self.y + self.height / 2 + random.randint(-100, 100)
            ice_shard = IceShard(spawn_x, spawn_y, damage=self.damage)
            self.ice_shards.append(ice_shard)
            if self.num_ice_shards <= 0:
                self.end_attack()

    def render(self, screen):
        """Render the boss and possibly some visual effects for its attacks."""
        super().render(screen)

        # Render stomp effect if visible
        if self.stomp_effect_isVisible:
            pygame.draw.rect(screen, (255, 0, 0), self.stomp_effect_rect1)
            pygame.draw.rect(screen, (255, 165, 0), self.stomp_effect_rect2)

        for ice_shard in self.ice_shards:
            ice_shard.render(screen)


class IceShard:
    def __init__(self, x, y, speed=75, damage=5, turn_rate=50):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.size = 30
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((144, 213, 255))
        self.hit_player = False
        self.life_time = 10
        self.active = True

        # Starting direction (facing down initially)
        self.direction = math.radians(180)  # Facing downwards
        self.turn_rate = turn_rate  # Max turn rate per update in degrees

    def update(self, dt, player, boss):
        if self.active:
            self.life_time -= dt
            # Calculate direction towards the player
            target_x = player.character_x + player.width / 2 - self.size / 2
            target_y = player.character_y + player.height / 2 - self.size / 2
            dx = target_x - self.x
            dy = target_y - self.y
            target_angle = math.atan2(dy, dx)

            # Calculate angle difference and apply turn rate limitation
            angle_diff = target_angle - self.direction
            angle_diff = (angle_diff + math.pi) % (
                2 * math.pi
            ) - math.pi  # Normalize to [-pi, pi]

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
            if pygame.Rect(self.x, self.y, self.size, self.size).colliderect(
                player.rect
            ):
                self.hit_player = True

            if self.life_time <= 3:
                self.image.fill((255, 0, 0))

            if self.life_time <= 0:
                self.active = False
                self.explode(boss)

    def explode(self, boss):
        num_bullets = 12  # Number of bullets in the bloom
        bullet_speed = 400  # Speed of each bullet
        for i in range(num_bullets):
            angle = i * (2 * math.pi / num_bullets)  # Evenly space bullets in a circle
            bullet_dx = math.cos(angle) * bullet_speed
            bullet_dy = math.sin(angle) * bullet_speed
            bullet = BossBullet(
                self.x, self.y, "general", general_speed=(bullet_dx, bullet_dy), damage=self.damage
            )
            bullet.width = BULLET_WIDTH
            bullet.height = BULLET_WIDTH
            bullet.rect.width = BULLET_WIDTH
            bullet.rect.height = BULLET_WIDTH
            boss.bullets.append(bullet)  # Assign bullet to the boss

    def render(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))
