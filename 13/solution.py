import sys
import re

import numpy as np


lines = (l.strip() for l in sys.stdin.readlines())

message = set()
folds = []
maxx = 0
maxy = 0
for line in lines:
    m = re.match(r'(\d+),(\d+)',line)
    if m:
        x,y = (int(n) for n in line.split(','))
        message.add((x,y))
        maxx = max(maxx,x)
        maxy = max(maxy,y)
    m = re.match(r'fold along (\w)=(\d+)',line)
    if m:
        d,c = m.groups()[0],int(m.groups()[1])
        folds.append((d,c))


def print_message(message,maxx,maxy):
    for r in range(maxy):
        for c in range(maxx):
            print('#' if (c,r) in message else ' ', end='')
        print()


for i,(d,c) in enumerate(folds):
    if d=='y':
        message = {(x,y) if y<c else (x,c-(y-c)) for x,y in message}
        maxy = c
    if d=='x':
        message = {(x,y) if x<c else (c-(x-c),y) for x,y in message}
        maxx = c
    if i==0:
        print('1:',len(message))

print('*2:')
print_message(message,maxx,maxy)
