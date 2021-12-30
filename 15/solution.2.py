import sys
import numpy as np
from queue import PriorityQueue
from collections import namedtuple

coord = namedtuple('coord',['x','y'])
dirs = (
    coord( 1, 0),
    coord( 0, 1),
    coord(-1, 0),
    coord( 0,-1)
)


lines = np.array([list(l.strip()) for l in sys.stdin.readlines()],'uint8')
xs1,ys1 = len(lines[0]),len(lines)
lines = np.hstack([lines+i for i in range(5)])
lines = np.vstack([lines+i for i in range(5)])
lines[lines>9] = (lines[lines>9]-1)%9+1
xs2,ys2 = len(lines[0]),len(lines)
cave = {coord(x,y):w for y,r in enumerate(lines) for x,w in enumerate(r)}


def find_minimal_danger(cave,s,e):
    queue = PriorityQueue()
    visited = set()
    queue.put((0,s))
    while not queue.empty():
        w,p = queue.get()
        if p in visited:
            continue
        elif p == e:
            return w
        else:
            visited.add(p)
        for d in dirs:
            q = coord(p.x+d.x,p.y+d.y)
            if q in cave and q not in visited:
                queue.put((w+cave[q],q))

print('*1:',find_minimal_danger(cave, coord(0,0), coord(xs1-1,ys1-1)))
print('*2:',find_minimal_danger(cave, coord(0,0), coord(xs2-1,ys2-1)))
