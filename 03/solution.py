import sys
import json

import numpy as np


numbers = np.array([list(n.strip()) for n in sys.stdin.readlines()],dtype=int)
#list(map(print,numbers))
#print(len(numbers))


def to_int(number):
    return number.dot(2**np.arange(len(number)-1,-1,-1, dtype=int))
    
def most_common_bits(numbers):
    return (2*np.sum(numbers,axis=0)>=len(numbers)).astype(int)

gamma = most_common_bits(numbers)
epsilon = 1-gamma

print(f'gamma {gamma}')
print(f'epsilon {epsilon}')
print(to_int(gamma)*to_int(epsilon))


def reduce_numbers(numbers, reverse):
    tmp = [n for n in numbers]
    for i,_ in enumerate(numbers[0]):
        if len(tmp)<=1:
            break
        counts = most_common_bits(tmp)
        #list(map(print,tmp))
        #print(counts,'c')
        #print((not principle) ^ bool(counts[i]))
        #print()
        tmp = [t for t in tmp if t[i]==reverse^counts[i]]
    return tmp

generator = reduce_numbers(numbers, False)[0]
scrubber = reduce_numbers(numbers, True)[0]

print(f'generator {generator}')
print(f'scrubber {scrubber}')
print(to_int(generator)*to_int(scrubber))
