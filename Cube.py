import numpy as np
from smollEngine.Tex import *
class Cube:
    def __init__(self, size=1, data=None):
        self.size = size
        if data == None:
            self.data = [[], [], [], [], [], []]
        else:
            self.data = data

        self.dict = {   "bl": [255, 0,   0],
                        "re": [0,   0,   255],
                        "gr": [0,   255, 255],
                        "or": [0,   128, 255],
                        "wh": [255, 255, 255],
                        "ye": [0,   255, 255]}

    def getData(self, file):
        file = open(file, "r")
        for i in range(6):
            line = file.readline()[:-1].replace(" ", "")
            res = list(map(lambda x: self.dict[x], line.split(",")))
            for color in res:
                tx = Tex(None, color)
