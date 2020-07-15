from smollEngine.World import *
from Cube import *
import time

w = World((1600, 900))

c = Cube(w)
w.cube = c

val = 0
while 1:
    st = time.time()
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    if key == ord("m"):
        val += 1

    c.willBeRendered = c.cornerSides[val%8]
    w.loop(key)
    try:
        print("FPS:", 1/(time.time()-st), end="\r")
    except:
        pass
