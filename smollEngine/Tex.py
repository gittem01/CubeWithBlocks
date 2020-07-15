from .Camera import *
import cv2

class Tex:
    def __init__(self, points, color):
        self.points = points # [[x0, y0, z0], .., [x4, y4, z4]]
        self.color = color # [B, G, R]

    def update(self, arr, cam):
        self.draw(arr, cam)

    def draw(self, arr, cam):
        drawPoints = []
        for point in self.points:
            sp = cam.put(point)
            if type(sp) != type(None):
                drawPoints.append(sp + np.array([800, 450]))
        drawPoints = np.array(drawPoints, dtype=np.int32)
        if len(drawPoints) != 4:
            return
        cv2.fillPoly(arr, [drawPoints], self.color)
        for i in range(len(drawPoints)):
            cv2.line(arr, tuple(drawPoints[i]), tuple(drawPoints[(i+1)%len(drawPoints)]),
             (0, 0, 0), 2, cv2.LINE_AA)
