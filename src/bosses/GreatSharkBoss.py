import pygame
import math
import random
from src.constants import *
from src.resources import *
from src.bosses.BaseBoss import BaseBoss
from src.bosses.BossBullet import BossBullet
from src.bosses.BeamAttack import BeamAttack


class GreatSharkBoss(BaseBoss):
    def __init__(self, x, y, health=300, damage=10, damage_speed_scaling=1):
        super().__init__(1000, y, width=270, height=300, health=health, damage=damage, damage_speed_scaling=damage_speed_scaling)
        self.y = GROUND_LEVEL_Y - self.height
        self.rect.y = self.y
        self.damage_speed_scaling = damage_speed_scaling
        # Customizing the appearance
        self.image.fill((200, 200, 200))  # Set color
        self.visible = True
        self.animation = sprite_collection["greatshark_boss_idle"].animation
        self.direction = "left"
        
        self.attack_effect_rect = pygame.Rect(self.x - 200, self.y + self.height/2 - 100, 200, 200)
        self.attack_effect_visible = False
        self.attack_effect_animation = sprite_collection["greatshark_boss_attack_effect"].animation

        # Deepwater Assault Attack prop
        self.assault_count = 0  # Track the number of assaults performed
        self.next_assault_time = 0.5  # Delay before each new assault
        self.reappearance_duration = 0.3  # Time taken for the boss to reappear
        self.charge_duration = 2
        self.start_charge = True
        self.original_x = self.x
        self.original_y = self.y
        self.original_width = self.width
        self.original_height = self.height
        self.prepare_time = 1.3

        # Torpedo Attack prop
        self.torpedos = []
        self.torpedo_expo_speed = 20
        self.torpedo_explode_chance = 1.5
        self.torpedo_explode_radius = 250
        self.explosion = None
        self.explosion_timer = 0
        self.explosion_duration = 0.2
        self.torpedo_damage = self.damage
        self.torpedo_explode_animation = sprite_collection["greatshark_boss_torpedo_explode"].animation
        self.torpedo_explode_effect_rect = None

        # Churning Tides Attack prop
        self.churning_tides_pull_force = 30000
        self.vortex = None
        self.vortex_duration = 5
        self.vortex_timer = 0
        self.vortex_radius = 50
        self.vortex_animation = sprite_collection["greatshark_boss_vortex"].animation

        # Rain Attack prop
        self.rain_duration = 5
        self.rain_bullet_gap_cooldown = 0.1
        self.rain_bullet_gap_time = 0
        self.rain_num_at_once = 2

    def update(self, dt, player, platforms):
        # Update position and check if the boss should attack
        super().update(dt, player, platforms)
        if self.explosion is not None:
            self.explosion_timer += dt
            self.torpedo_explode_animation.update(dt)
            if self.explosion_timer >= self.explosion_duration:
                self.explosion_timer = 0
                self.explosion = None
                self.torpedo_explode_effect_rect = None
        else:
            self.torpedo_explode_animation.Refresh()
                
        for torpedo in self.torpedos:
            self.update_torpedo(torpedo, dt, player)
            
        if self.vortex is not None:
            self.vortex_animation.update(dt)
            self.update_vortex(dt, player)
            
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.width
        self.rect.height = self.height
            
        self.animation.update(dt)
        
        if self.warning_time_timer > 0 and self.current_attack != self.deepwater_assault:
            self.attack_effect_visible = True
        else:
            self.attack_effect_visible = False
        
        if self.attack_effect_visible:
            self.attack_effect_animation.update(dt)
        else:
            self.attack_effect_animation.Refresh()

    def select_attack(self, player):

        attack_choice = random.choice(["deepwater_assault", "torpedo", "churning_tides", "rain"])
        # attack_choice = random.choice(["rain"])


        if attack_choice == "deepwater_assault":
            self.current_attack = self.deepwater_assault
        elif attack_choice == "torpedo":
            self.current_attack = self.torpedo
        elif attack_choice == "churning_tides":
            self.current_attack = self.churning_tides
        elif attack_choice == "rain":
            self.current_attack = self.rain

    def deepwater_assault(self, dt, player):
        """
        Deepwater Assault: The White Shark disappears and performs three consecutive attacks,
        randomly choosing to come from the left, right, or below the player.
        """       
        if self.attack_elapsed_time == 0:
            self.assault_directions = [random.choice(["left", "right", "below"]) for _ in range(3)]  # Randomize directions    
            
        if self.attack_elapsed_time <= self.prepare_time:
            self.animation = sprite_collection["greatshark_boss_prepare_assault"].animation
        else:
            self.visible = False  # Hide the boss
            # Proceed if there are remaining assaults
            if self.assault_count < 3:
                # Reappear and charge after the initial delay
                if self.attack_elapsed_time - self.prepare_time >= self.next_assault_time:
                    self.visible = True
                    self.image.set_alpha(255)  # Make fully visible for the assault
                    direction = self.assault_directions[self.assault_count]

                    # Set the starting position and angle based on direction
                    if self.start_charge:
                        self.visible = False
                        self.start_charge = False  # Start charge only once per assault
                        if direction == "left":
                            self.width = 300
                            self.height = 150
                            self.x = -self.width
                            self.y = player.character_y + player.height / 2 - self.height / 2
                            self.direction = "left"
                            self.animation = sprite_collection["greatshark_boss_assault"].animation
                        elif direction == "right":
                            self.width = 300
                            self.height = 150
                            self.x = WIDTH
                            self.y = player.character_y + player.height / 2 - self.height / 2
                            self.direction = "right"
                            self.animation = sprite_collection["greatshark_boss_assault"].animation
                        elif direction == "below":
                            self.width = 150
                            self.height = 300
                            self.x = player.character_x + player.width / 2 - self.width / 2
                            self.y = HEIGHT
                            self.direction = "up"
                            self.animation = sprite_collection["greatshark_boss_assault_up"].animation

                        # Rotate and update the boss rect to match charge direction
                        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

                    # Calculate charge progress based on time interpolation
                    t = (self.attack_elapsed_time - self.prepare_time - self.next_assault_time) / self.charge_duration

                    # Interpolate position towards target direction
                    if direction in ["left", "right"]:
                        start_pos = -self.width if direction == "right" else WIDTH
                        end_pos = WIDTH + self.width if direction == "right" else -self.width
                        self.x = start_pos + t * (end_pos - start_pos)
                    elif direction == "below":
                        start_pos = HEIGHT
                        end_pos = -self.height
                        self.y = start_pos + t * (end_pos - start_pos)

                    # Conclude the current assault when the charge duration is complete
                    if (self.attack_elapsed_time - self.prepare_time - self.next_assault_time) >= self.charge_duration:
                        self.assault_count += 1
                        self.next_assault_time += self.charge_duration + 0.5  # Set delay before the next assault
                        self.visible = False  # Hide the boss again
                        self.start_charge = True

        # Finalize the attack sequence after three assaults
        if self.assault_count >= 3:
            self.reset_position()
            self.visible = True
            self.assault_count = 0
            self.next_assault_time = 0.5  # Reset delay for future attacks
            self.image.set_alpha(255)
            sprite_collection["greatshark_boss_prepare_assault"].animation.Refresh()
            self.animation = sprite_collection["greatshark_boss_idle"].animation
            self.direction = "left"
            self.end_attack()

    def reset_position(self):
        """Reset the boss to the original visible position after the assault sequence."""
        self.x = self.original_x
        self.y = self.original_y
        self.width = self.original_width
        self.height = self.original_height


    def torpedo(self, dt, player):
        """
        The shark launches large, torpedo-like bullets that move slowly at first,
        then suddenly accelerate. After traveling a short distance, the torpedoes explode
        """

        torpedo = BeamAttack(
            self.x - self.width / 2, self.y + self.height / 2, "left", 100, 50, damage=self.damage
        )
        torpedo.set_image(sprite_collection["greatshark_boss_torpedo"].image)
        torpedo.speed = 0
        self.torpedos.append((torpedo, 0))
        
        gSounds['shark_missile'].play()

        self.end_attack()
            
    def update_torpedo(self, torpedo_pair, dt, player):
        # Update torpedo's speed using an exponential function
        torpedo, time_exist = torpedo_pair
        torpedo.update(dt)
        time_exist += dt
        t = time_exist
        
        torpedo.speed = self.exponential_speed(t)

        # Calculate how far the torpedo has traveled as a fraction of the screen width
        distance_traveled = abs(WIDTH - torpedo.x)
        travel_fraction = distance_traveled / WIDTH

        # Check if the torpedo has traveled more than half the screen width
        if travel_fraction > 0.5:
            # Increase the chance to explode as it travels further
            explode_chance = (
                self.torpedo_explode_chance ** (travel_fraction * 10) / 100
            )

            # Attempt to explode with the given chance
            if random.random() < explode_chance:
                self.explode_torpedo(torpedo, player)
                return  # Exit the function after explosion
            
        # Torpedo explode if contact player
        if player.rect.colliderect(torpedo.rect):
            self.explode_torpedo(torpedo, player)
            player.take_damage(self.torpedo_damage)
        
        # Remove the torpedo if it moves off-screen
        if torpedo.x < 0:
            self.torpedos = [t for t in self.torpedos if t[0] != torpedo]
        else:
            # Reassign the updated torpedo tuple to the list to keep the updated time_exist
            for i, (torp, _) in enumerate(self.torpedos):
                if torp == torpedo:
                    self.torpedos[i] = (torpedo, time_exist)

    def explode_torpedo(self, torpedo, player):
        """
        Handle the explosion of a torpedo by creating a circular blast.
        """
        # Create explosion effect with a defined radius
        explosion_radius = self.torpedo_explode_radius
        explosion_center = (
            int(torpedo.x + torpedo.width // 2),
            int(torpedo.y + torpedo.height // 2),
        )

        # Add explosion visual effect
        self.explosion = (explosion_center, explosion_radius)

        # Optionally, apply damage to the player if within the explosion radius
        # Check player's distance from the explosion and apply damage if close enough
        player_distance = math.sqrt((explosion_center[0] - player.character_x)**2 + (explosion_center[1] - player.character_y)**2)
        if player_distance <= explosion_radius:
            player.take_damage(self.torpedo_damage)  # Example damage value

        # Remove the torpedo from the bullets list
        self.torpedos = [t for t in self.torpedos if t[0] != torpedo]
        
        self.torpedo_explode_effect_rect = pygame.Rect(explosion_center[0] - explosion_radius, explosion_center[1] - explosion_radius, explosion_radius*2, explosion_radius*2)
        
        gSounds['shark_missile'].stop()
        gSounds['shark_missile_explode'].play(maxtime=1000, fade_ms=500)

    def churning_tides(self, dt, player):
        """
        Churning Tides: The White Shark creates vortexes of water that pull the player toward
        certain areas of the screen. The player's speed is adjusted based on the distance from the vortex.
        """
        # Define the vortex center randomly on the screen
        vortex_x = random.randint(WIDTH // 4, 3 * WIDTH // 4)
        vortex_y = random.randint(HEIGHT // 4, 3 * HEIGHT // 4)
        
        if self.vortex is None:
            self.vortex = (vortex_x, vortex_y)

        gSounds["shark_vortex"].play()
        self.end_attack()
            
    def update_vortex(self, dt, player):
        self.vortex_timer += dt
        vortex_x, vortex_y = self.vortex
        # Calculate distance between the player and the vortex center
        distance_x = vortex_x - (player.character_x + player.width / 2)
        distance_y = vortex_y - (player.character_y + player.height / 2)
        distance = math.sqrt(distance_x**2 + distance_y**2)

        # Pull force decreases with distance, simulating a vortex effect
        pull_strength = abs(
            self.churning_tides_pull_force / (distance + 1)
        )  # Avoid division by zero

        # Determine player's direction relative to the vortex
        if distance > self.vortex_radius:
            # Player is outside the vortex radius, apply pulling effect based on direction
            # if (
            #     distance_x > 0 and player.direction == "left"
            # ):  # Player is left of vortex
            #     player.movement_speed = CHARACTER_MOVE_SPEED - pull_strength
            # elif (
            #     distance_x > 0 and player.direction == "right"
            # ):  # Player moving towards vortex
            #     player.movement_speed = CHARACTER_MOVE_SPEED + pull_strength
            # elif (
            #     distance_x < 0 and player.direction == "left"
            # ):  # Player moving towards vortex
            #     player.movement_speed = CHARACTER_MOVE_SPEED + pull_strength
            # elif (
            #     distance_x < 0 and player.direction == "right"
            # ):  # Player is right of vortex
            #     player.movement_speed = CHARACTER_MOVE_SPEED - pull_strength
            if (
                distance_x > 0
            ):  # Player is pulled inwards
                player.character_x += pull_strength * dt
            elif (
                distance_x < 0
            ):  # Player is pulled inwards
                player.character_x -= pull_strength * dt
        else:
            # Player is within the vortex radius, slow down or keep them in place
            player.movement_speed = CHARACTER_MOVE_SPEED / 2
            player.take_damage(self.damage)

        # Ensure movement speed stays within a reasonable range
        player.movement_speed = max(
            0, min(player.movement_speed, CHARACTER_MOVE_SPEED * 2)
        )
        
        if self.vortex_timer >= self.vortex_duration:
            player.revert_to_default()
            self.vortex_timer = 0
            self.vortex = None
            gSounds["shark_vortex"].fadeout(1000)

    def rain(self, dt, player):
        bullet_direction = "down"
        gSounds["shark_rain"].play()

        self.rain_bullet_gap_time += dt
        if self.rain_bullet_gap_time >= self.rain_bullet_gap_cooldown:
            self.rain_bullet_gap_time = 0
            for _ in range(self.rain_num_at_once):
                bullet = BossBullet(
                    random.randint(0, WIDTH), 0, bullet_direction, damage=self.damage, scaling=self.damage_speed_scaling
                )  # Create a bullet
                bullet.width = 8
                bullet.height = 30
                bullet.re_initialize()
                bullet.set_image(sprite_collection["greatshark_boss_bullet"].image)
                self.bullets.append(bullet)  # Add bullet to the list

        # End the bullet attack if the duration is over
        if self.attack_elapsed_time >= self.rain_duration:
            gSounds["shark_rain"].fadeout(1000)
            self.end_attack()

    def exponential_speed(self, t):
        return self.torpedo_expo_speed**t

    def render(self, screen):
        """Render the boss and possibly some visual effects for its attacks."""
        if self.alive and self.visible:
            img = self.animation.image
            img = pygame.transform.scale(img, (self.rect.width, self.rect.height))
            if self.direction == "right":
                img = pygame.transform.flip(img, True, False)
            screen.blit(img, (self.x, self.y))
            
        for torpedo in self.torpedos:
            torpedo_bullet, _ = torpedo
            torpedo_bullet.render(screen)

        # Render explosions
        if self.torpedo_explode_effect_rect is not None:
            img = self.torpedo_explode_animation.image
            img = pygame.transform.scale(img, (self.torpedo_explode_effect_rect.width, self.torpedo_explode_effect_rect.height))
            screen.blit(img, (self.torpedo_explode_effect_rect.x, self.torpedo_explode_effect_rect.y))
            

        # Render the vortex
        if self.vortex is not None:
            vortex_x, vortex_y = self.vortex
            img = self.vortex_animation.image
            img = pygame.transform.scale(img, (self.vortex_radius + 200, self.vortex_radius))
            screen.blit(img, (vortex_x - 100, vortex_y))
            
            # pygame.draw.circle(
            #     screen,
            #     (0, 0, 255),
            #     (int(vortex_x), int(vortex_y)),
            #     self.vortex_radius,
            #     3,
            # )  # Draw a blue circle for the vortex
            
        if self.attack_effect_visible:
            img = self.attack_effect_animation.image
            img = pygame.transform.scale(img, (self.attack_effect_rect.width, self.attack_effect_rect.height))
            screen.blit(img, (self.attack_effect_rect.x, self.attack_effect_rect.y))
        
        for bullet in self.bullets:
            bullet.render(screen)