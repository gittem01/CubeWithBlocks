from .Tex import *
from .Camera import *

class World:
    def __init__(self, size, winName="CubeSim"):
        self.winName = winName
        self.size = size
        self.arr = np.zeros((size[1], size[0], 3), dtype=np.uint8)
        cv2.namedWindow(winName)
        cv2.setMouseCallback(winName, self.mouseCallback)
        self.lastMouse = None
        self.cam = Camera()
        self.cube = None

    def mouseCallback(self, event, x, y, what1, what2):
        if self.lastMouse != None:
            diff = [x-self.lastMouse[0], y-self.lastMouse[1]]
            self.cube.fullRotate(-diff[0]/200, diff[1]/200)

        if  event == cv2.EVENT_LBUTTONDOWN or\
            event == cv2.EVENT_RBUTTONDOWN or\
            event == cv2.EVENT_MBUTTONDOWN or\
            self.lastMouse != None:

            self.lastMouse = [x, y]

        if  event == cv2.EVENT_LBUTTONUP or\
            event == cv2.EVENT_RBUTTONUP or\
            event == cv2.EVENT_MBUTTONUP:

            self.lastMouse = None


    def loop(self, key):
        copArr = self.arr.copy()
        if self.cube:
            self.cube.update(copArr)
        cv2.imshow(self.winName, copArr)
