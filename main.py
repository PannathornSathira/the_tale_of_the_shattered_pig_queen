import pygame, sys
from src.Util import *
from src.constants import *
from src.states.MapSelectState import MapSelectState
from src.states.MainMenuState import MainMenuState
from src.states.PlayState import PlayState
from src.states.ShopState import ShopState
from src.states.PauseState import PauseState
from src.Player import Player
from src.Level import Level
from src.bosses.WraithBoss import WraithBoss
from src.resources import *

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()

class GameMain:
    def __init__(self):
        self.max_frame_rate = MAX_FRAME_RATE
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.player = Player()
        self.level = Level(area=3)
        self.level.CreateMap()
        self.boss = WraithBoss(x=1100, y=100)
        
        self.font = pygame.font.Font(None, 36)

        g_state_manager.SetScreen(self.screen)
        
        # Define all states and set in StateMachine
        states = {
            "MAIN_MENU": MainMenuState(self.screen, self.font),
            "PLAY": PlayState(self.screen, self.font),
            "WORLD_MAP": MapSelectState(self.screen, self.font),
            "SHOP": ShopState(self.screen, self.font),
            "PAUSE": PauseState(self.screen, self.font),
        }
        g_state_manager.SetStates(states)
        
        # Start in Main Menu
        g_state_manager.Change("MAIN_MENU", {})

    def update(self, dt, events):
        # Handle global events (e.g., quit)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Update current state
        g_state_manager.update(dt, events)
        
        if self.player.alive:
            self.player.update(dt, events, self.level.platforms, self.boss)  
        self.level.update(dt, events)
        
        if self.boss.alive:
            self.boss.update(dt, self.player, self.level.platforms) 

    def render(self):
        self.screen.fill((255, 255, 255))
        
        # Render current state
        g_state_manager.render()
        
        # Update display
        pygame.display.update()

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

if __name__ == '__main__':
    main = GameMain()
    main.PlayGame()
