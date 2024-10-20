from src.states.BaseState import BaseState
from src.constants import *
from src.Dependency import *
import pygame, sys

class GameOverState(BaseState):
    def __init__(self):
        super(GameOverState, self).__init__()

    def Exit(self):
        pass

    def Enter(self, params):
        pass

    def update(self,  dt, events):
        pass

    def render(self, screen):
        pass