import sys
import numpy as np
np.set_printoptions(edgeitems=300, linewidth=100000)

lines = [l.strip() for l in sys.stdin.readlines()]

correction = [int(x=='#') for x in lines[0]]
#print(correction)

image = np.array([[v=='#' for v in row] for row in lines[2:]],'uint8')

turn = 0


def evolve_image(image):
    global turn
    image = np.pad(image, 2, constant_values=turn%2*correction[0])
    turn += 1
    next_image = np.zeros_like(image)
    def calc_pixel(x,y):
        value = \
            256*image[y-1,x-1] + 128*image[y-1,x  ] +  64*image[y-1,x+1] + \
             32*image[y  ,x-1] +  16*image[y  ,x  ] +   8*image[y  ,x+1] + \
              4*image[y+1,x-1] +   2*image[y+1,x  ] +   1*image[y+1,x+1]
        v = correction[value]
        #print(x,y,' ',v,value)
        return v
    #print(image)
    for y in range(1,len(image)-1):
        for x in range(1,len(image[0])-1):
            next_image[y,x] = calc_pixel(x,y)
    next_image = next_image[1:-1,1:-1]
    return next_image


for i in range(2):
    #print(image)
    print(i)
    image = evolve_image(image)
#print(image)
print('*1:',image.sum())

for i in range(50-2):
    #print(image)
    print(i)
    image = evolve_image(image)
#print(image)
print('*2:',image.sum())
