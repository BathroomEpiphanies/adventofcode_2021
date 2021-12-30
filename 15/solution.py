import sys
import networkx as nx

import numpy as np
import itertools
np.set_printoptions(edgeitems=30, linewidth=100000)

lines = np.array([list(l.strip()) for l in sys.stdin.readlines()],'uint8')
xm1 = len(lines[0])-1
ym1 = len(lines)-1

lines = np.hstack([lines+i for i in range(5)])
lines = np.vstack([lines+i for i in range(5)])
lines = (lines-1)%9+1

xm2 = len(lines[0])-1
ym2 = len(lines)-1
caves = nx.DiGraph()
for x,y in itertools.product(range(xm2+1),range(ym2+1)):
    if x<xm2:
        caves.add_edge( (x+0)+(y+0)*1j, (x+1)+(y+0)*1j, danger=lines[y+0,x+1] )
        caves.add_edge( (x+1)+(y+0)*1j, (x+0)+(y+0)*1j, danger=lines[y+0,x+0] )
    if y<ym2:
        caves.add_edge( (x+0)+(y+0)*1j, (x+0)+(y+1)*1j, danger=lines[y+1,x+0] )
        caves.add_edge( (x+0)+(y+1)*1j, (x+0)+(y+0)*1j, danger=lines[y+0,x+0] )


path = nx.shortest_path(caves, 0+0*1j, xm1+ym1*1j, weight='danger')
print('*1',sum(caves.edges[(n1,n2)]['danger'] for n1,n2 in zip(path,path[1:])))

path = nx.shortest_path(caves, 0+0*1j, xm2+ym2*1j, weight='danger')
print('*2',sum(caves.edges[(n1,n2)]['danger'] for n1,n2 in zip(path,path[1:])))
