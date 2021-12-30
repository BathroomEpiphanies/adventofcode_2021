import re
import sys
import cv2

import numpy as np
from collections import defaultdict


ventlines = [((a,b),(c,d)) for l in sys.stdin.readlines() for a,b,c,d in [map(int,re.match(r'([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)',l).groups())]]


shape = (1000,1000)
ventfield = np.zeros(shape)
for line in ventlines:
    p1,p2 = line
    if p1[0]==p2[0] or p1[1]==p2[1]:
        subfield = np.zeros(shape)
        cv2.line(subfield,p1,p2,1)
        ventfield += subfield

print(np.sum(ventfield>1))
cv2.imwrite('debug_1.png',ventfield*255/np.max(ventfield))


ventfield = np.zeros(shape)
for line in ventlines:
    p1,p2 = line
    subfield = np.zeros(shape)
    cv2.line(subfield,p1,p2,1)
    ventfield += subfield

print(np.sum(ventfield>1))
cv2.imwrite('debug_2.png',ventfield*255/np.max(ventfield))
