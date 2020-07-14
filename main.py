from smollEngine.World import *
from Cube import *
import time

p1 = np.array([     [-15, -15, 15],
                    [-15,  15, 15],
                    [ 15,  15, 15],
                    [ 15, -15, 15]])
c1 = [0, 0, 255]
tx1 = Tex(p1, c1)

w = World((1600, 900))
#w.textures.append(tx1)

c = Cube(w)

while 1:
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

    w.loop(key)
