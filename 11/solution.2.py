import sys
import numpy as np
import cv2

from itertools import count
from more_itertools import tail


octupi = np.array([list(l.strip()) for l in sys.stdin.readlines()],dtype='uint8')


def octupi_evolver(octupi):
    FLASH_KERNEL = np.ones((3,3))
    while True:
        octupi += 1
        handled = np.zeros_like(octupi,'bool')
        while True:
            triggered = (octupi>9) & ~handled
            if not triggered.any():
                break
            flash = cv2.filter2D(
                triggered.astype('uint8'),
                ddepth=-1,
                kernel=FLASH_KERNEL,
                borderType=cv2.BORDER_ISOLATED
            )
            handled |= triggered
            octupi += flash
        octupi[octupi>9] = 0
        flashes = handled.sum()
        yield flashes
        if flashes == octupi.size:
            return

flashes = octupi_evolver(octupi)

print(octupi)
print('*1:',sum(f for _,f in zip(range(100),flashes)))

_,i = next(tail(1,zip(flashes,count(101))))
print(octupi)
print('*2:',i)
