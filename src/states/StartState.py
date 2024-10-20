from src.states.BaseState import BaseState
import pygame, sys
from src.constants import *
from src.Dependency import *

class StartState(BaseState):
    def __init__(self):
        super(StartState, self).__init__()
        #start = 1,       ranking = 2
        pass

    def Exit(self):
        pass

    def Enter(self, params):
        self.high_scores = params['high_scores']

    def render(self, screen):
        pass

    def update(self, dt, events):
        pass
