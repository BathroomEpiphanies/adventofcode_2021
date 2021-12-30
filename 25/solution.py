import sys
import re

import numpy as np

import itertools
import collections
import functools

lines = [l.strip() for l in sys.stdin.readlines()]
east = set(x+y*1j for y,r in enumerate(lines) for x,c in enumerate(r) if c=='>')
sout = set(x+y*1j for y,r in enumerate(lines) for x,c in enumerate(r) if c=='v')
xmax = len(lines[0])
ymax = len(lines)

def plot():
    for y in range(ymax):
        for x in range(xmax):
            if (x+y*1j) in east:
                print('>',end='')
            elif (x+y*1j) in sout:
                print('v',end='')
            else:
                print('.',end='')
        print()
                
def move(east,sout):
    def help(east,sout,cumbs,d):
        move = set()
        stay = set()
        allc = east|sout
        for c in cumbs:
            n = (c.real+d.real)%xmax + (c.imag+d.imag)%ymax*1j
            if n not in allc:
                move.add(n)
            else:
                stay.add(c)
        return len(move)>0,move|stay
    moved_east,east = help(east,sout,east,1)
    moved_sout,sout = help(east,sout,sout,1j)
    return (moved_east or moved_sout),east,sout


moved = True
for i in itertools.count():
    plot()
    print(i)
    print()
    moved,east,sout = move(east,sout)
    if not moved:
        break

print('*1:',i+1)
