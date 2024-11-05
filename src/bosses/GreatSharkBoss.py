import pygame
import math
import random
from src.constants import *
from src.bosses.BaseBoss import BaseBoss
from src.bosses.BossBullet import BossBullet
from src.bosses.BeamAttack import BeamAttack


class GreatSharkBoss(BaseBoss):
    def __init__(self, x, y, health=300, damage=10):
        super().__init__(x, y, health=health, damage=damage)

        # Customizing the appearance
        self.image.fill((200, 200, 200))  # Set color
        self.visible = True

        # Deepwater Assault Attack prop
        self.assault_count = 0  # Track the number of assaults performed
        self.next_assault_time = 0.5  # Delay before each new assault
        self.reappearance_duration = 0.3  # Time taken for the boss to reappear
        self.charge_duration = 2
        self.start_charge = True
        self.original_x = self.x
        self.original_y = self.y

        # Torpedo Attack prop
        self.torpedos = []
        self.torpedo_expo_speed = 20
        self.torpedo_explode_chance = 1.5
        self.torpedo_explode_radius = 250
        self.explosion = None
        self.explosion_timer = 0
        self.explosion_duration = 0.2
        self.torpedo_damage = self.damage

        # Churning Tides Attack prop
        self.churning_tides_pull_force = 30000
        self.vortex = None
        self.vortex_duration = 5
        self.vortex_timer = 0
        self.vortex_radius = 50

        # Rain Attack prop
        self.rain_duration = 5
        self.rain_bullet_gap_cooldown = 0.08
        self.rain_bullet_gap_time = 0
        self.rain_num_at_once = 2

    def update(self, dt, player, platforms):
        # Update position and check if the boss should attack
        super().update(dt, player, platforms)
        if self.explosion is not None:
            self.explosion_timer += dt
            if self.explosion_timer >= self.explosion_duration:
                self.explosion_timer = 0
                self.explosion = None
                
        for torpedo in self.torpedos:
            self.update_torpedo(torpedo, dt, player)
            
        if self.vortex is not None:
            self.update_vortex(dt, player)

    def select_attack(self, player):

        attack_choice = random.choice(["deepwater_assault", "torpedo", "churning_tides", "rain"])

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
        # Disappear and set up initial conditions at the start of the attack
        if self.attack_elapsed_time == 0:
            self.visible = False  # Hide the boss
            self.assault_directions = [random.choice(["left", "right", "below"]) for _ in range(3)]  # Randomize directions

        # Proceed if there are remaining assaults
        if self.assault_count < 3:
            # Reappear and charge after the initial delay
            if self.attack_elapsed_time >= self.next_assault_time:
                self.visible = True
                self.image.set_alpha(255)  # Make fully visible for the assault
                direction = self.assault_directions[self.assault_count]

                # Set the starting position and angle based on direction
                if self.start_charge:
                    self.visible = False
                    self.start_charge = False  # Start charge only once per assault
                    if direction == "left":
                        self.x = -self.width
                        self.y = player.character_y + player.height / 2 - self.height / 2
                        angle = -90
                    elif direction == "right":
                        self.x = WIDTH
                        self.y = player.character_y + player.height / 2 - self.height / 2
                        angle = 90
                    elif direction == "below":
                        self.x = player.character_x + player.width / 2 - self.width / 2
                        self.y = HEIGHT
                        angle = 0

                    # Rotate and update the boss rect to match charge direction
                    self.image = pygame.transform.rotate(self.image, angle)
                    self.rect = self.image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))

                # Calculate charge progress based on time interpolation
                t = (self.attack_elapsed_time - self.next_assault_time) / self.charge_duration

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
                if (self.attack_elapsed_time - self.next_assault_time) >= self.charge_duration:
                    self.assault_count += 1
                    self.next_assault_time += self.charge_duration + 0.5  # Set delay before the next assault
                    self.visible = False  # Hide the boss again
                    self.start_charge = True

                    # Reset angle for next assault
                    angle = 90 if direction == "left" else -90 if direction == "right" else 0
                    self.image = pygame.transform.rotate(self.image, angle)
                    self.rect = self.image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))

        # Finalize the attack sequence after three assaults
        if self.assault_count >= 3:
            self.reset_position()
            self.visible = True
            self.assault_count = 0
            self.next_assault_time = 0.5  # Reset delay for future attacks
            self.image.set_alpha(255)
            self.end_attack()

    def reset_position(self):
        """Reset the boss to the original visible position after the assault sequence."""
        self.x = self.original_x
        self.y = self.original_y


    def torpedo(self, dt, player):
        """
        The shark launches large, torpedo-like bullets that move slowly at first,
        then suddenly accelerate. After traveling a short distance, the torpedoes explode
        """

        torpedo = BeamAttack(
            self.x - self.width / 2, self.y + self.height / 2, "left", 100, 50, damage=self.damage
        )
        torpedo.speed = 0
        self.torpedos.append((torpedo, 0))

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
            if (
                distance_x > 0 and player.direction == "left"
            ):  # Player is left of vortex
                player.movement_speed = CHARACTER_MOVE_SPEED - pull_strength
            elif (
                distance_x > 0 and player.direction == "right"
            ):  # Player moving towards vortex
                player.movement_speed = CHARACTER_MOVE_SPEED + pull_strength
            elif (
                distance_x > 0 and player.direction == "front"
            ):  # Player is pulled inwards
                player.character_x += pull_strength * dt
            elif (
                distance_x < 0 and player.direction == "left"
            ):  # Player moving towards vortex
                player.movement_speed = CHARACTER_MOVE_SPEED + pull_strength
            elif (
                distance_x < 0 and player.direction == "right"
            ):  # Player is right of vortex
                player.movement_speed = CHARACTER_MOVE_SPEED - pull_strength
            elif (
                distance_x < 0 and player.direction == "front"
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

    def rain(self, dt, player):
        bullet_direction = "down"

        self.rain_bullet_gap_time += dt
        if self.rain_bullet_gap_time >= self.rain_bullet_gap_cooldown:
            self.rain_bullet_gap_time = 0
            for _ in range(self.rain_num_at_once):
                bullet = BossBullet(
                    random.randint(0, WIDTH), 0, bullet_direction, damage=self.damage
                )  # Create a bullet
                self.bullets.append(bullet)  # Add bullet to the list

        # End the bullet attack if the duration is over
        if self.attack_elapsed_time >= self.rain_duration:
            self.end_attack()

    def exponential_speed(self, t):
        return self.torpedo_expo_speed**t

    def render(self, screen):
        """Render the boss and possibly some visual effects for its attacks."""
        if self.visible:
            super().render(screen)
            
        for torpedo in self.torpedos:
            torpedo_bullet, _ = torpedo
            torpedo_bullet.render(screen)

        # Render explosions
        if self.explosion is not None:
            explosion_center, explosion_radius = self.explosion
            pygame.draw.circle(
                screen, (255, 100, 0), explosion_center, explosion_radius, 2
            )  # Orange circle

        # Render the vortex
        if self.vortex is not None:
            vortex_x, vortex_y = self.vortex
            pygame.draw.circle(
                screen,
                (0, 0, 255),
                (int(vortex_x), int(vortex_y)),
                self.vortex_radius,
                3,
            )  # Draw a blue circle for the vortex
            

