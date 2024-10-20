from src.constants import *
from src.resources import *
import pygame

def RenderScore(screen, score):
    small_font = pygame.font.Font('./fonts/font.ttf', 24)
    t_score = small_font.render("Score:", False, (255, 255, 255))
    t_score_val = small_font.render(str(score), False, (255, 255, 255))
    screen.blit(t_score, (WIDTH - 180, 5))
    rect = t_score_val.get_rect()
    rect.topright = (WIDTH - 60, 5)
    screen.blit(t_score_val, rect)

def RenderHealth(screen, health):
    x_pos = WIDTH - 300
    for i in range(health):
        screen.blit(sprite_collection["heart"].image, (x_pos, 4))
        x_pos += 33

    for i in range(3-health):
        screen.blit(sprite_collection["empty_heart"].image, (x_pos, 4))
        x_pos += 33
