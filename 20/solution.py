import sys
import cv2
import numpy as np


lines = [l.strip() for l in sys.stdin.readlines()]
image = np.array([[v=='#' for v in row] for row in lines[2:]],'int16')
correction = np.array([int(x=='#') for x in lines[0]],'int16')
enhance = np.vectorize(lambda x: correction[x])

def to_string(image):
    return '\n'.join(''.join('#' if v else '.' for v in row) for row in image)

KERNEL = np.array([2**i for i in range(9)][::-1]).reshape(3,3)


def evolve_image(image,turn):
    image = np.pad(image, 1, constant_values=enhance(0)*turn%2)
    image = cv2.filter2D(image,-1,KERNEL,borderType=cv2.BORDER_REPLICATE)
    image = enhance(image)
    return image
    

for turn in range(2):
    image = evolve_image(image,turn)
print('*1:',image.sum())


for turn in range(2,50):
    image = evolve_image(image,turn)
print('*2:',image.sum())
