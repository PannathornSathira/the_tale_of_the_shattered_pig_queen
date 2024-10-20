from src.states.BaseState import BaseState
from src.constants import *
from src.Dependency import *
import pygame, sys

from src.Paddle import Paddle
from src.LevelMaker import LevelMaker



class MapSelectState(BaseState):
    def __init__(self):
        super(PaddleSelectState, self).__init__()
        pass
    def Exit(self):
        pass

    def Enter(self, params):
        pass

    def update(self,  dt, events):
        pass
    def render(self, screen):
        pass