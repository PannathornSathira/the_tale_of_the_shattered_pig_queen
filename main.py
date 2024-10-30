import pygame, sys
from src.Util import *
from src.constants import *
from src.states.MapSelectState import MapSelectState
from src.states.BaseState import BaseState
from src.states.PlayState import PlayState
from src.states.ShopState import ShopState
from src.states.PauseState import PauseState


pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()

class GameMain:
    def __init__(self):
        self.max_frame_rate = MAX_FRAME_RATE
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font(None, 36)
        
        # State management
        self.states = {
            "MAIN_MENU": BaseState(self.screen, self.font),
            "PLAY": PlayState(self.screen, self.font),
            "WORLD_MAP": MapSelectState(self.screen, self.font),
            "SHOP": ShopState(self.screen, self.font),
            "PAUSE": PauseState(self.screen, self.font),
        }
        self.current_state = "MAIN_MENU"

    def update(self, dt, events):
        # Handle global events (e.g., quit)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Update current state
        if self.current_state == "MAIN_MENU":
            # Main Menu Logic
            self.states["MAIN_MENU"].update(dt, events)
            if self.states["MAIN_MENU"].start_game:
                self.current_state = "WORLD_MAP"
        elif self.current_state == "PLAY":
            # Play State Logic
            self.states["PLAY"].update(dt, events)
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.current_state = "PAUSE"
        elif self.current_state == "WORLD_MAP":
            # Play State Logic
            self.states["WORLD_MAP"].update(dt, events)
            if self.states["WORLD_MAP"].start_game:
                self.current_state = "PLAY"
            elif self.states["WORLD_MAP"].go_to_shop:
                self.current_state = "SHOP"
        elif self.current_state == "SHOP":
            self.states["SHOP"].update(dt, events)
        elif self.current_state == "PAUSE":
            result, params = self.states["PAUSE"].update(dt, events)
            if result == "RESUME":
                self.current_state = "PLAY"

    def render(self):
        self.screen.fill((255, 255, 255))
        
        # Render current state
        if self.current_state == "MAIN_MENU":
            self.states["MAIN_MENU"].render()
        elif self.current_state == "PLAY":
            self.states["PLAY"].render()
        elif self.current_state == "WORLD_MAP":
            self.states["WORLD_MAP"].render()
        elif self.current_state == "SHOP":
            self.states["SHOP"].render()
        elif self.current_state == "PAUSE":
            self.states["PAUSE"].render()
        
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
