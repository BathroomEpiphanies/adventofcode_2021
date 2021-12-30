import sys
from collections import defaultdict


lines = [l.strip() for l in sys.stdin.readlines()]

correction = [int(x=='#') for x in lines[0]]

image = defaultdict(lambda:0)
for y,row in enumerate(lines[2:]):
    for x,v in enumerate(row):
        image[x+y*1j] = int(v=='#')


def print_image(image):
    minx = round(min(p.real for p in image))
    maxx = round(max(p.real for p in image))
    miny = round(min(p.imag for p in image))
    maxy = round(max(p.imag for p in image))
    
    for y in range(miny,maxy+1):
        for x in range(minx,maxx+1):
            print('#' if image[x+y*1j] else '.',end='')
        print()


def evolve_image(image,turn):
    image.default_factory = (lambda:1-turn%2)
    next_image = defaultdict(lambda:None)
    next_image.default_factory = image.default_factory
    dirs = [
        (-1 -1*1j), ( 0 -1*1j), ( 1 -1*1j),
        (-1 +0*1j), ( 0 +0*1j), ( 1 +0*1j),
        (-1 +1*1j), ( 0 +1*1j), ( 1 +1*1j),
    ]
    vals = [2**i for i in range(8,-1,-1)]
    for p1 in list(image.keys()):
        for p in (p1+d for d in dirs if p1+d not in next_image):
            l = [image[p+d]*v for d,v in zip(dirs,vals)]
            x = sum(image[p+d]*v for d,v in zip(dirs,vals))
            #print(p,x)
            #print(l)
            next_image[p] = correction[sum(image[p+d]*v for d,v in zip(dirs,vals))]
    return next_image



for i in range(2):
    #print(image)
    print(i)
    image = evolve_image(image,i)
#print(image)
print('*1:',sum(image.values()))
