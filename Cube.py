from smollEngine.Tex import *
import numpy as np

class Cube:
    def __init__(self, world, size=125, data=None):
        self.world = world
        self.size = size
        self.data = [[], [], [], [], [], []]

        self.dict = {   "bl": [255, 0,   0], # str to color values
                        "re": [0,   0,   255],
                        "gr": [0,   255, 0],
                        "or": [0,   128, 255],
                        "wh": [255, 255, 255],
                        "ye": [0,   255, 255]}

        self.starts =   np.array( # two opposite corners of the cube
                            [
                                [-size*1.5, -size*1.5,  size*1.5],
                                [ size*1.5,  size*1.5, -size*1.5]
                            ]
                                )

        self.directions = np.array([    [ 1,  1, 0], [ 1, 0, -1], [0,  1, -1],
                                        [-1, -1, 0], [-1, 0,  1], [0, -1, 1]])

        self.cornerSides = [ [0, 1, 2], [0, 1, 5], [1, 2, 3], [1, 3, 5],
                             [0, 2, 4], [0, 4, 5], [2, 3, 4], [3, 4, 5] ]

        self.cornerIncrements = [ [0, 0, 0], [1, 0, 0], [0, 0, -1], [1, 0, -1],
                                  [0, 1, 0], [1, 1, 0], [0, 1, -1], [1, 1, -1] ]

        self.lastCornerPositions = self.getCorners()

        self.angle = np.array([0, 0], dtype=np.float64)
        self.willBeRendered = self.getNearestSides()

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
        lines = file.readlines()
        for i in range(6):
            line = lines[i][:-1].replace(" ", "")
            res = list(map(lambda x: self.dict[x], line.split(",")))
            val = np.array([0, 0, 0])
            for j in range(3):
                val[self.nonZeros[i][0]] = 0
                for k in range(3):
                    pos = self.starts[i//3] + val*self.size
                    tex = self.createTexFromPos(pos, i, res[j*3+k])
                    self.data[i].append(tex)
                    val[self.nonZeros[i][0]] += self.directions[i][self.nonZeros[i][0]]
                val[self.nonZeros[i][1]] += self.directions[i][self.nonZeros[i][1]]

    def getRotationarrays(self, angley, anglex):
        arrY = np.array(
            [
                [ cos(angley), 0, sin(angley)],
                [ 0,           1, 0],
                [-sin(angley), 0, cos(angley)]
            ]
        )
        arrX = np.array(
            [
                [ 1, 0,            0],
                [ 0, cos(anglex), -sin(anglex)],
                [ 0, sin(anglex),  cos(anglex)]
            ]
        )
        return (arrY, arrX)

    def fullRotate(self, angley, anglex):
        self.angle += np.array((angley, anglex))
        arrY, arrX = self.getRotationarrays(angley, anglex)
        for dp in self.data:
            for tx in dp:
                for i in range(4):
                    tx.points[i] = np.dot(tx.points[i], arrY)
                    tx.points[i] = np.dot(tx.points[i], arrX)

        for i in range(len(self.lastCornerPositions)):
            self.lastCornerPositions[i] = np.dot(self.lastCornerPositions[i], arrY)
            self.lastCornerPositions[i] = np.dot(self.lastCornerPositions[i], arrX)

    def pointRotate(self, angley, anglex, point):
        arrY, arrX = self.getRotationarrays(angley, anglex)
        p = np.dot(point, arrY)
        p = np.dot(p, arrX)
        return p

    def update(self, arr):
        self.willBeRendered = self.getNearestSides()
        for i in self.willBeRendered:
            for j in range(9):
                self.data[i][j].update(arr, self.world.cam)

    def getCorners(self):
        corners = []
        for i in range(8):
            c = self.starts[0] + np.array(self.cornerIncrements[i])*self.size*3
            corners.append(c)
        return corners

    def getDistanceFromCam(self, corner):
        swcp = self.world.cam.pos
        dist = (swcp[0]-corner[0])**2 + (swcp[1]-corner[1])**2 + (swcp[2]-corner[2])**2
        return dist

    def getNearestCorner(self):
        corners = self.getCorners()
        corners = self.lastCornerPositions
        nearest = 0
        dist = float("inf")
        for i in range(len(corners)):
            currDist = self.getDistanceFromCam(corners[i])
            if currDist < dist:
                nearest = i
                dist = currDist
        return nearest

    def getNearestSides(self):
        nc = self.getNearestCorner()
        return self.cornerSides[nc]
