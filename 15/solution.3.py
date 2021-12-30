import sys
import networkx as nx

import numpy as np
np.set_printoptions(edgeitems=30, linewidth=100000)

lines = np.array([list(l.strip()) for l in sys.stdin.readlines()],'uint8')
xm1 = len(lines[0])-1
ym1 = len(lines)-1

lines = np.hstack([lines+i for i in range(5)])
lines = np.vstack([lines+i for i in range(5)])
lines[lines>9] = (lines[lines>9]-1)%9+1

xm2 = len(lines[0])-1
ym2 = len(lines)-1
caves = nx.DiGraph()
for y,line in enumerate(lines[:-1]):
    for x,r in enumerate(line[:-1]):
        caves.add_edge( ((x+0)+(y+0)*1j,'i'), ((x+0)+(y+0)*1j,'o'), weight=int(r) )
        
        caves.add_edge( ((x+0)+(y+0)*1j,'o'), ((x+1)+(y+0)*1j,'i'), weight=0 )
        caves.add_edge( ((x+1)+(y+0)*1j,'o'), ((x+0)+(y+0)*1j,'i'), weight=0 )
        
        caves.add_edge( ((x+0)+(y+0)*1j,'o'), ((x+0)+(y+1)*1j,'i'), weight=0 )
        caves.add_edge( ((x+0)+(y+1)*1j,'o'), ((x+0)+(y+0)*1j,'i'), weight=0 )
    
    caves.add_edge( ((xm2)+(y+0)*1j,'i'), ((xm2 )+(y+0)*1j,'o'), weight=int(line[xm2]) )
    
    caves.add_edge( ((xm2)+(y+0)*1j,'o'), ((xm2 )+(y+1)*1j,'i'), weight=0 )
    caves.add_edge( ((xm2)+(y+1)*1j,'o'), ((xm2 )+(y+0)*1j,'i'), weight=0 )

y = ym2
line = lines[y]
for x,r in enumerate(line[:-1]):
    caves.add_edge( ((x+0)+(y+0)*1j,'i'), ((x+0)+(y+0)*1j,'o'), weight=int(r))
    
    caves.add_edge( ((x+0)+(y+0)*1j,'o'), ((x+1)+(y+0)*1j,'i'), weight=0)
    caves.add_edge( ((x+1)+(y+0)*1j,'o'), ((x+0)+(y+0)*1j,'i'), weight=0)

x = xm2
caves.add_edge( ((x+0)+(y+0)*1j,'i'), ((x+0)+(y+0)*1j,'o'), weight=int(line[xm2]))


path = nx.shortest_path(caves, (0+0*1j,'o'), (xm1+ym1*1j,'o'), weight='weight')
print('*2',sum(caves.edges[(n1,n2)]['weight'] for n1,n2 in zip(path,path[1:])))

path = nx.shortest_path(caves, (0+0*1j,'o'), (xm2+ym2*1j,'o'), weight='weight')
print('*2',sum(caves.edges[(n1,n2)]['weight'] for n1,n2 in zip(path,path[1:])))


import cv2

image = 255*np.ones_like(lines)
for p in path:
    image[int(p[0].imag),int(p[0].real)] = 0
    print(p[0])
cv2.imwrite('debug.png',image)
