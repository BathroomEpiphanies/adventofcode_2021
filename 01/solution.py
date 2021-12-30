import sys
from more_itertools import windowed,ilen

depths = [int(n.strip()) for n in sys.stdin.readlines()]
print(ilen(None for a,b in windowed(depths, 2) if a<b))

filtered = (sum(l) for l in windowed(depths, 3))
print([a<b for a,b in windowed(filtered,2)].count(True))
