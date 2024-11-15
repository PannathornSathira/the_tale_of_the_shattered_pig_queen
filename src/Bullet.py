from src.constants import *
import random, pygame, math
class Bullet:
    def __init__(self, x, y, direction, general_speed=(0, 0), damage=1, angle_offset=0, bullet_type="normal"):
        self.x = x
        self.y = y
        self.direction = direction  # "left" or "right"
        self.speed = BULLET_SPEED  # Bullet speed
        self.scaling = 1
        self.dx = general_speed[0]
        self.dy = general_speed[1]
        self.bullet_type = bullet_type
        self.angle_offset = angle_offset
        # Calculate direction based on angle offset for shotgun
        if angle_offset != 0:
            angle_radians = math.radians(angle_offset)
            if direction == "right":
                self.dx = self.speed * math.cos(angle_radians)
                self.dy = -self.speed * math.sin(angle_radians)
            elif direction == "left":
                self.dx = -self.speed * math.cos(angle_radians)
                self.dy = -self.speed * math.sin(angle_radians)

        # Set bullet dimensions and color based on bullet type
        self.travelled_distance = 0
        if self.bullet_type == "shotgun":
            self.max_distance = 350
            self.width = BULLET_LENGTH
            self.height = BULLET_WIDTH
            self.color = (160, 0, 0)  # Orange color for shotgun bullets
        else:
            self.max_distance = None
            self.color = (128, 0, 128)
            if direction == "up" or direction == "down":
                self.width = BULLET_WIDTH
                self.height = BULLET_LENGTH
            else:
                self.width = BULLET_LENGTH
                self.height = BULLET_WIDTH
        self.active = True  # If the bullet is still on the screen
        self.damage = damage
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, dt):
        actual_speed = self.speed * self.scaling 
        if self.bullet_type == "shotgun" and self.travelled_distance >= self.max_distance:
            self.active = False
            return
        # Move the bullet in the correct direction
        if self.direction == "right" and self.angle_offset == 0:
            self.x += actual_speed * dt
            self.travelled_distance += abs(actual_speed * dt)       
        elif self.direction == "left" and self.angle_offset == 0:
            self.x -= actual_speed * dt
            self.travelled_distance += abs(actual_speed * dt)        
        elif self.direction == "up":
            self.y -= actual_speed * dt
            self.travelled_distance += abs(actual_speed * dt)        
        elif self.direction == "down":
            self.y += actual_speed * dt
            self.travelled_distance += abs(actual_speed * dt)        
        else:
            self.x += self.dx * dt
            self.travelled_distance += math.sqrt(self.dx**2 + self.dy**2) * dt            
            self.y += self.dy * dt
        
            # If the bullet moves off-screen, deactivate it
        if self.x + self.width < 0 or self.x > WIDTH or self.y + self.height < 0 or self.y > HEIGHT:
                self.active = False
                
        self.rect.x = self.x
        self.rect.y = self.y

    def render(self, screen):
        # Draw the bullet (just a simple rectangle for now)
        pygame.draw.rect(screen, self.color, self.rect)
