import sys
import re
import itertools
from collections import defaultdict
import numpy as np


rotations = [
    np.array(a) for a in {
        tuple(tuple(r) for r in m) for m in (
            np.array([a,b,c]) for a,b,c in
            itertools.permutations([(0,0,1),(0,0,-1),(0,1,0),(0,-1,0),(1,0,0),(-1,0,0)],r=3)
        )
        if np.linalg.det(m)==1
    }
]

class Scanner:
    def __init__(self,beacons,positioned=False):
        self.beacons = beacons
        self.positioned = positioned
        self.rotations = [[np.matmul(rotation,b) for b in self.beacons] for rotation in rotations]
    
    def __str__(self):
        return f'{self.positioned}\n' + '\n'.join([f'{b}' for b in self.beacons]) + '\n'
    
    def reposition(self,rotation,translation,positioned=False):
        self.beacons = [np.matmul(rotation,b)+translation for b in self.beacons]
        self.positioned = positioned
    
    def overlap(s1,s2):
        for rotation,s2_rotated in zip(rotations,s2.rotations):
            for b1,b2 in itertools.product(s1.beacons,s2_rotated):
                translation = b1-b2
                s2_translated = [b+translation for b in s2_rotated]
                if len({tuple(b) for b in s1.beacons} & {tuple(b) for b in s2_translated}) >= 12:
                    return rotation,translation
        return None,None


lines = (l.strip() for l in sys.stdin.readlines())
scanners = []
for line in lines:
    beacons = []
    for line in lines:
        if not line:
            break
        beacons.append(np.array(line.split(','),int))
    scanners.append(Scanner(beacons))

#for s in scanners:
#    print(s)
#    print(s.rotations)


translations = [np.array((0,0,0))]
scanners[0].positioned = True
futile = set()
while not all(s.positioned for s in scanners):
    print('starting round')
    for (i1,s1),(i2,s2) in (((i1,s1),(i2,s2)) for (i1,s1),(i2,s2) in
                            itertools.permutations(enumerate(scanners),2) if
                            (s1.positioned and not s2.positioned) and ((i1,i2) not in futile)):
        print(i1,i2,end='')
        rotation,translation = Scanner.overlap(s1,s2)
        if rotation is not None:
            print(' aligns', end='')
            s2.reposition(rotation,translation,True)
            translations.append(translation)
        else:
            futile.add((i1,i2))
            futile.add((i2,i1))
        print()
    print(futile)
    for s in scanners:
        print(s)
    
        

#for s in scanners:
#    print(s)


beacons = {tuple(b) for s in scanners for b in s.beacons}
print(beacons)
print('*1:',len(beacons))


maxdist = max(round(np.linalg.norm(b1-b2,ord=1)) for b1,b2 in itertools.combinations(translations,2))
print('*2:',maxdist)
