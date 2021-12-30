import re
import sys
import cv2

import numpy as np
from collections import defaultdict


ventlines = [((a+b*1j),(c+d*1j)) for l in sys.stdin.readlines() for a,b,c,d in [map(int,re.match(r'([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)',l).groups())]]

def print_field(field):
    for r in range(10):
        for c in range(10):
            print(field[c+r*1j],end='')
        print()

def draw_ventline(field,p1,p2):
    length = max(map(lambda z:round(abs(z)),[(p1-p2).real,(p1-p2).imag]))
    step = (p2-p1)/length if length>0 else 0
    while p1 != p2:
        field[p1] += 1
        p1 += step
    field[p2] += 1

def calc_danger(field):
    return sum([1 for p,v in field.items() if v>1])


ventfield = defaultdict(lambda:0)
for a,b in ventlines:
    if ((b-a)**2).imag == 0:
        draw_ventline(ventfield,a,b)
print_field(ventfield)
print('*1:',calc_danger(ventfield))

for a,b in ventlines:
    if ((b-a)**2).imag != 0:
        draw_ventline(ventfield,a,b)
print_field(ventfield)
print('*2:',calc_danger(ventfield))


exit(0)

image = np.zeros((1000,1000))
for r in range(1000):
    for c in range(1000):
        z = c+r*1j
        image[r,c] = ventfield[z]
cv2.imwrite('debug.png',image*255/np.max(image))
