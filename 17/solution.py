import sys
import re

from collections import namedtuple

coord = namedtuple('coord',['x','y'])


m = re.match(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)', sys.stdin.readlines()[0])
xmin,xmax,ymin,ymax = (int(n) for n in m.groups())


def get_trajectory(v):
    p = coord(0,0)
    hit = False
    trajectory = []
    while p.x<=xmax and p.y>=ymin:
        if p.x>=xmin and p.y<=ymax:
            hit = True
        trajectory.append(p)
        p = coord(p.x+v.x,p.y+v.y)
        v = coord(max(0,v.x-1),v.y-1)
    return hit,trajectory


def plot_trajectory(trajectory):
    for y in range( max(ymax, max(p[1] for p in trajectory)),
                    min(ymin-1, min(p[1] for p in trajectory))-1,
                    -1 ):
        for x in range(0,max(xmax, max(p[0] for p in trajectory))+2):
            if (x,y) in trajectory:
                print('#',end='')
            elif xmin<=x<=xmax and ymin<=y<=ymax:
                print('T',end='')
            else:
                print('.',end='')
        print()
    return


maxheight = 0
hits = 0
for vx in range(1,xmax+1):
    for vy in range(ymin,-ymin):
        hit,trajectory = get_trajectory(coord(vx,vy))
        if hit:
            hits += 1
            maxheight = max(maxheight, max(p.y for p in trajectory))
            #plot_trajectory(trajectory)


print('*1:',maxheight)
print('*2:',hits)
