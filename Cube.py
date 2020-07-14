import numpy as np
from smollEngine.Tex import *
import random

class Cube:
    def __init__(self, world, size=10, data=None):
        self.world = world
        self.size = size

        if data == None:
            self.data = [[], [], [], [], [], []]
        else:
            self.data = data

        self.dict = {   "bl": [255, 0,   0],
                        "re": [0,   0,   255],
                        "gr": [0,   255, 0],
                        "or": [0,   128, 255],
                        "wh": [255, 255, 255],
                        "ye": [0,   255, 255]}

        self.starts =   np.array(
                            [
                                [-size*1.5, -size*1.5,  size*1.5],
                                [ size*1.5,  size*1.5, -size*1.5]
                            ]
                                )

        self.directions = np.array([    [ 1,  1, 0], [ 1, 0, -1], [0,  1, -1],
                                        [-1, -1, 0], [-1, 0,  1], [0, -1, 1]])
        nz = np.nonzero(self.directions)
        self.nonZeros = nz[1].reshape(-1, 2)
        self.createTextures()

    def createTexFromPos(self, pos, sideId, color):
        positions = np.zeros((4, 3))
        for i in range(4):
            positions[i] = pos
        positions[1][self.nonZeros[sideId][0]] += self.directions[sideId][self.nonZeros[sideId][0]]*self.size
        positions[3][self.nonZeros[sideId][1]] += self.directions[sideId][self.nonZeros[sideId][1]]*self.size
        positions[2] += self.directions[sideId]*self.size

        reTex = Tex(positions, color)
        return reTex

    def createTextures(self, file="cubeData01.csv"):
        file = open(file, "r")
        for i in range(6):
            line = file.readline()[:-1].replace(" ", "")
            res = list(map(lambda x: self.dict[x], line.split(",")))
            val = np.array([0, 0, 0])
            for j in range(3):
                val[self.nonZeros[i][0]] = 0
                for k in range(3):
                    pos = self.starts[i//3] + val*self.size
                    tex = self.createTexFromPos(pos, i, res[j*3+k])
                    self.world.textures.append(tex)
                    self.data[i].append(tex)
                    val[self.nonZeros[i][0]] += self.directions[i][self.nonZeros[i][0]]
                val[self.nonZeros[i][1]] += self.directions[i][self.nonZeros[i][1]]

    def getData(self, file):

        for i in range(6):
            line = file.readline()[:-1].replace(" ", "")
            res = list(map(lambda x: self.dict[x], line.split(",")))
            for color in res:
                tx = Tex(None, color)
