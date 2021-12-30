import sys
import numpy as np


fish = np.array([[n.count(str(i))] for l in sys.stdin.readlines() for n in [l.replace(',','')] for i in range(9)], dtype='int64')
print(fish)

M = np.array(
    (
        (0,1,0,0,0,0,0,0,0),
        (0,0,1,0,0,0,0,0,0),
        (0,0,0,1,0,0,0,0,0),
        (0,0,0,0,1,0,0,0,0),
        (0,0,0,0,0,1,0,0,0),
        (0,0,0,0,0,0,1,0,0),
        (1,0,0,0,0,0,0,1,0),
        (0,0,0,0,0,0,0,0,1),
        (1,0,0,0,0,0,0,0,0),
    )
)

print(M)
print(np.linalg.matrix_power(M,80))
print(np.linalg.matrix_power(M,80)@fish)

print(np.sum(np.linalg.matrix_power(M,80)@fish))
print(np.sum(np.linalg.matrix_power(M,256)@fish))
