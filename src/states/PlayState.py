import random, pygame, sys
from src.states.BaseState import BaseState
from src.constants import *
from src.Dependency import *
#import src.CommonRender as CommonRender

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()
        self.paused = False

    def Enter(self, params):
        pass
    

    def update(self,  dt, events):
        pass

    def Exit(self):
        pass

    def render(self, screen):
        pass

    def CheckVictory(self):
        pass
