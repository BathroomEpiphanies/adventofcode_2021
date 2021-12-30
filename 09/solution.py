import sys
import itertools

import numpy as np
import cv2


np.set_printoptions(edgeitems=150, linewidth=420)

heightmap = np.pad( np.array([list(l.strip()) for l in sys.stdin.readlines()],dtype=int), 1, constant_values=10 )

print(heightmap)

low_points = (
    (heightmap[1:-1,1:-1]<heightmap[  :-2 , 1:-1 ]) &
    (heightmap[1:-1,1:-1]<heightmap[ 2:   , 1:-1 ]) &
    (heightmap[1:-1,1:-1]<heightmap[ 1:-1 ,  :-2 ]) &
    (heightmap[1:-1,1:-1]<heightmap[ 1:-1 , 2:   ])
).astype(dtype='int8')
print()

#print('Low points')
#print(low_points)
#print()

print('Risk level')
risklevel = low_points * (1+heightmap[1:-1,1:-1])
print(risklevel)
print(risklevel.sum())
print()

print('Basins')
basinmap = (heightmap<9).astype(dtype='int8')
print(basinmap)
print()

_,components,stats,_ = cv2.connectedComponentsWithStats(basinmap,connectivity=4)

print('Basins')
print(components)
print()

print('Basin stats')
print(stats)
print()

largest_basins = sorted(stats[1:,-1])[-3:]
print(largest_basins)
print(np.prod(largest_basins))

cv2.imwrite('debug.png',255*basinmap)
