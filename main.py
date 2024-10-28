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
        # self.boss = BlueDragonBoss(x=1100, y=100)
        # self.boss = WhiteSharkBoss(x=1100, y=100)
        self.boss = BlackWidowBoss(x=1100, y=100)

        # self.sprite_collection = SpriteManager().spriteCollection

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        #self.player.update(dt, events)
        self.player.update(dt, events, self.level.platforms)  
        self.level.update(dt, events)  
        self.boss.update(dt, self.player)
        # No camera scroll update
        # self.camera_x_scroll = self.character_x - (WIDTH/2) + CHARACTER_WIDTH/2

    def render(self):
        self.screen.fill((255, 255, 255))
        
        self.level.render(self.screen)
        self.player.render(self.screen)
        self.boss.render(self.screen)
        

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
