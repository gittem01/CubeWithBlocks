from math import sin
from math import cos
from math import pi
import numpy as np

class Camera:
    def __init__(self, pos=np.array([0, 0, 500], np.float64),
                angle=np.array([0, 0, 0], np.float64), e=np.array([0, 0, 500], np.float64)):
        self.pos = pos
        self.angle = angle
        self.e = e
        self.update()

    def update(self):
        self.array1 = np.array([[1, 0, 0],
                           [0, cos(self.angle[0]), sin(self.angle[0])],
                           [0, -sin(self.angle[0]), cos(self.angle[0])]])

        self.array2  = np.array([[cos(self.angle[1]), 0, -sin(self.angle[1])],
                           [0, 1, 0],
                           [sin(self.angle[1]), 0, cos(self.angle[1])]])

        self.array3 = np.array([[cos(self.angle[2]), sin(self.angle[2]), 0],
                           [-sin(self.angle[2]), cos(self.angle[2]), 0],
                           [0, 0, 1]])

    def put(self, point):
        array4 = point-self.pos
        result = np.dot(self.array1, self.array2)
        result = np.dot(result, self.array3)
        result = np.dot(result, array4)
        return np.array([result[0], result[1]])
        if result[2] < 0:
            return None
        b = np.array([0, 0], dtype=np.float64)
        b[0] = (self.e[2]/result[2])*result[0] + self.e[0]
        b[1] = (self.e[2]/result[2])*result[1] + self.e[1]

        return b
