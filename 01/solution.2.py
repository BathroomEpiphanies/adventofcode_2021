import sys
import numpy as np

depths = np.array([int(n.strip()) for n in sys.stdin.readlines()])

print(np.size(np.where(np.convolve(depths,(1,-1),mode='valid')>0)))
print(np.size(np.where(np.convolve(depths,(1,0,0,-1),mode='valid')>0)))
print()

print(np.size(np.where(depths[1:]-depths[0:-1]>0)))
print(np.size(np.where(depths[3:]-depths[0:-3]>0)))
print()

print(sum(depths[1:]-depths[0:-1]>0))
print(sum(depths[3:]-depths[0:-3]>0))
print()


from functools import reduce,partial

a = reduce(np.correlate,[depths,(-1,1)])
b = reduce(np.correlate,[depths,(1,1,1),(-1,1)])

print(a)
print(b)

print(np.size(np.where(a>0)))
print(np.size(np.where(b>0)))

print()

#print(np.size(np.where(np.correlate(depths,(-1,1))>0)))
print(np.size(np.where(reduce(np.correlate,[depths,(-1,1)])>0)))
print(np.size(np.where(np.correlate(depths,(-1,1))>0)))
print(np.size(np.where(reduce(partial(np.convolve,mode='valid'),[depths,(1,1,1),(1,-1)])>0)))
print(sum(np.diff(np.convolve(depths,(1,1,1),'valid'))>0))
print()

#print(sum(np.diff(np.convolve(depths,(1,1,1),'valid')>0)))
print(sum(np.diff(depths)>0))
print(sum(np.diff(np.correlate(depths,(1,1,1)))>0))
print()

print(np.size(np.where(reduce(np.correlate,[depths,(1,1,1),(-1,1)])>0)))
