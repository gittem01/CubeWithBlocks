from smollEngine.World import *
from Cube import *
import time

w = World((900, 900))

c = Cube(w)
c.fullRotate(pi/4, pi/4)
w.cube = c

while 1:
    st = time.time()
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

    w.loop(key)

    try:
        print("FPS:", int(1/(time.time()-st))," "*10, end="\r")
    except:
        pass
