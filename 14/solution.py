import sys

from collections import Counter
import operator
from functools import reduce


lines = [l.strip() for l in sys.stdin.readlines()]
polymer = lines[0]
rules = {k:v for k,v in (line.split(' -> ') for line in lines[2:])}


cache = {}
def helper(pair,iterations):
    if (pair,iterations) not in cache:
        if iterations == 0:
            cache[(pair,iterations)] = Counter(pair)
        else:
            a,b = pair
            c = rules[pair]
            cache[(pair,iterations)] = \
                helper(a+c,iterations-1) + \
                helper(c+b,iterations-1) - \
                Counter(c)
    return cache[(pair,iterations)].copy()

def expand_and_count(polymer,iterations):
    return reduce(
        operator.add,
        (helper(a+b,iterations) for a,b in zip(polymer,polymer[1:]))
    ) - Counter(polymer[1:-1])


d = sorted(expand_and_count(polymer,10).values(),reverse=True)
print('*1:',d[0]-d[-1])

d = sorted(expand_and_count(polymer,40).values(),reverse=True)
print('*2:',d[0]-d[-1])
