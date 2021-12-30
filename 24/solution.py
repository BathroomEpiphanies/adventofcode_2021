import sys
import itertools

lines = [l.strip() for l in sys.stdin.readlines()]

#a = [  0, 13, 11, 12, 10, 14, -1, 14,-16, -8, 12,-16,-13, -6, -6]
#b = [  0,  6, 11,  5,  6,  8, 14,  9,  4,  7, 13, 11, 11,  6,  1]
#d = [  1,  1,  1,  1,  1,  1, 26,  1, 26, 26,  1, 26, 26, 26, 26]

a = [0]+[int(l.split(' ')[-1]) for l in lines[ 5::18]]
b = [0]+[int(l.split(' ')[-1]) for l in lines[15::18]]
d = [1]+[int(l.split(' ')[-1]) for l in lines[ 4::18]]

def _loop(z,w,i):
    global RANGE
    if z>10_000_000:
        return ''
    if z%26 == w-a[i]:
        z = z//d[i]
    else:
        z = z//d[i]*26 + w+b[i]
    if i>13:
        return '#' if z==0 else ''
    for w in RANGE:
        test = loop(z,w,i+1)
        if test:
            return str(w)+test
    return ''

cache = {}
def loop(*args):
    if args not in cache:
        cache[args] = _loop(*args)
    return cache[args]



RANGE = [9,8,7,6,5,4,3,2,1]
print('*1:',loop(0,0,0)[:-1])

del(cache[0,0,0])
RANGE = [1,2,3,4,5,6,7,8,9]
print('*2:',loop(0,0,0)[:-1])
