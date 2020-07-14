import cv2
from .Tex import *
from .Camera import *

class World:
    def __init__(self, size, winName="CubeSim"):
        self.winName = winName
        self.size = size
        self.arr = np.zeros((size[1], size[0], 3), dtype=np.uint8)
        self.cam = Camera()
        self.textures = []

    def loop(self, key):
        copArr = self.arr.copy()
        for tex in self.textures:
            tex.update(copArr, self.cam)
        cv2.imshow(self.winName, copArr)
