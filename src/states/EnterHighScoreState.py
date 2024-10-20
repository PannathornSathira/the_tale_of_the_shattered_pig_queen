from src.states.BaseState import BaseState
from src.constants import *
from src.resources import *
from src.Dependency import *
import pygame, sys

class EnterHighScoreState(BaseState):
    def __init__(self):
        super(EnterHighScoreState, self).__init__()

        self.highlighted_char = 1

    def Exit(self):
        pass

    def Enter(self, params):
        pass

    def update(self, dt, events):
        pass

    def render(self, screen):
        pass

