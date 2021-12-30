import sys
import re
import itertools
import json

from math import floor,ceil

class SnailFish:

    def explode(snail):
        i = 0
        count = 0
        for i,c in enumerate(snail):
            count += {']':-1,'[':1}.get(c,0)
            if count>4:
                break
        for j,c in enumerate(snail[i:],i):
            if c==']':
                break
        if i>=j:
            return False,snail
        a,b = (int(n) for n in re.findall(r'\d+',snail[i:j+1]))
        out = re.sub(r'\d+', lambda x: f'{int(x.group()[::-1])+a}'[::-1], snail[  :i][::-1], count=1)[::-1] + '0' + \
              re.sub(r'\d+', lambda x: f'{int(x.group()[:: 1])+b}'[:: 1], snail[j+1:][:: 1], count=1)[:: 1]
        return out!=snail,out
    
    def split(snail):
        out = re.sub(r'\d{2}',lambda x: f'[{floor(int(x.group())/2)},{ceil(int(x.group())/2)}]', snail, count=1)
        return out!=snail,out
    
    def reduce(snail):
        while True:
            while True:
                changed,snail = SnailFish.explode(snail)
                if not changed:
                    break
            changed,snail = SnailFish.split(snail)
            if not changed:
                break
        return snail
    
    def __init__(self,snail):
        self.snail = SnailFish.reduce(snail)
    
    def __str__(self):
        return self.snail
    __repr__ = __str__
    
    def __add__(self,other):
        return SnailFish(f'[{self.snail},{other.snail}]')

    def __abs__(self):
        def h(n):
            return 3*(n[0] if isinstance(n[0],int) else h(n[0]))+2*(n[1] if isinstance(n[1],int) else h(n[1]))
        return h(json.loads(self.snail))


snails = [SnailFish(l.strip()) for l in sys.stdin.readlines()]
total = snails[0]
for snail in snails[1:]:
    print(total)
    print(snail)
    total += snail
    print(total)
    print()

print('*1:',abs(total))

maxabs = max(abs(a+b) for a,b in itertools.permutations(snails,2))
print('*2:',maxabs)

