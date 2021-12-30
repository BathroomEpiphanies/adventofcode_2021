import sys
import itertools

import numpy as np
import cv2


octupi = np.array([list(l.strip()) for l in sys.stdin.readlines()],dtype='uint8')

def evolve_octupi(octupi):
    octupi += 1
    handled = np.zeros_like(octupi,bool)
    while True:
        triggered = (octupi>9) & ~handled
        if not triggered.any():
            break
        flash = cv2.filter2D(
            triggered.astype('uint8'),
            ddepth=-1,
            kernel=np.ones((3,3)),
            borderType=cv2.BORDER_ISOLATED
        )
        octupi += flash
        handled |= triggered
    octupi[octupi>9] = 0
    return handled.sum()

flashes = 0
for i in range(1,101):
    flashes += evolve_octupi(octupi)
print(octupi)
print('*1:',flashes)

for i in itertools.count(i+1):
    if evolve_octupi(octupi) == octupi.size:
        break
print(octupi)
print('*2:',i)
