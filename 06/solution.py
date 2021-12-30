import sys


fish = [int(n) for l in sys.stdin.readlines() for n in l.split(',')]
print(fish)

def breed(shoal,days):
    for _ in range(days):
        shoal = [shoal[(i+1)%8] for i in range(9)]
        shoal[6] += shoal[8]
    return shoal

shoal = [fish.count(i) for i in range(9)]
print(sum(breed(shoal,80)))
shoal = [fish.count(i) for i in range(9)]
print(sum(breed(shoal,256)))
