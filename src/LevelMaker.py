import random, pygame, math
from src.Brick import Brick

#patterns
NONE = 1
SINGLE_PYRAMID = 2
MULTI_PYRAMID = 3

SOLID = 1            # all colors the same in this row
ALTERNATE = 2        # alternative colors
SKIP = 3             # skip every other brick
NONE = 4             # no block this row


class LevelMaker:
    def __init__(self):
        pass

    @classmethod
    def CreateMap(cls, level):
        
        pass