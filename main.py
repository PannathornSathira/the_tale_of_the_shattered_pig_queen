import pygame, sys
from src.Util import *
from src.constants import *
from src.Player import Player
from src.Level import Level
from src.bosses.BaseBoss import BaseBoss
from src.bosses.BlueDragonBoss import BlueDragonBoss
from src.bosses.WhiteSharkBoss import WhiteSharkBoss
from src.bosses.BlackWidowBoss import BlackWidowBoss

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()


class GameMain:
    def __init__(self):
        self.max_frame_rate = MAX_FRAME_RATE
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.player = Player()
        self.level = Level(area=3)
        self.level.CreateMap()
        self.boss = BlueDragonBoss(x=1100, y=100)
        # self.boss = WhiteSharkBoss(x=1100, y=100)
        # self.boss = BlackWidowBoss(x=1100, y=100)

        self.font = pygame.font.Font(None, 36)
        # self.sprite_collection = SpriteManager().spriteCollection

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        #self.player.update(dt, events)
        if self.player.alive:
            self.player.update(dt, events, self.level.platforms, self.boss)  
        self.level.update(dt, events)
        if self.boss.alive:
            self.boss.update(dt, self.player) 
        # No camera scroll update
        # self.camera_x_scroll = self.character_x - (WIDTH/2) + CHARACTER_WIDTH/2

    def render(self):
        self.screen.fill((255, 255, 255))
        
        self.level.render(self.screen)
        self.player.render(self.screen)
        self.boss.render(self.screen)
        if self.player.alive:
            self.render_text(f"Player Health: {self.player.health}", 20, 20)
        if self.boss.alive:
            self.render_text(f"Boss Health: {self.boss.health}", 20, 60)
    def render_text(self, text, x, y):
        """Render text at a given position."""
        text_surface = self.font.render(text, True, (0, 0, 0))  # Render text in black color
        self.screen.blit(text_surface, (x, y))
        
        
    def PlayGame(self):
        clock = pygame.time.Clock()

        while True:
            pygame.display.set_caption("running with {:d} FPS".format(int(clock.get_fps())))
            dt = clock.tick(self.max_frame_rate) / 1000.0

            # Input
            events = pygame.event.get()

            # Update
            self.update(dt, events)

            # Render
            self.render()

            # Screen update
            pygame.display.update()


if __name__ == '__main__':
    main = GameMain()
    main.PlayGame()
