import sys
import numpy as np


positions = np.array([x for l in sys.stdin.readlines() for x in l.split(',')],dtype='int64')
print(np.median(positions))

minpos = None
minfuel = np.inf
for p in range(min(positions),max(positions)):
    fuel = np.sum(abs(positions-p))
    if not minfuel or fuel < minfuel:
        minpos = p
        minfuel = fuel

print(minpos,minfuel)


minpos = None
minfuel = np.inf
for p in range(min(positions),max(positions)):
    d = abs(positions-p)
    fuel = np.sum((d+1)*d//2)
    if fuel < minfuel:
        minpos = p
        minfuel = fuel

print(minpos,minfuel)
