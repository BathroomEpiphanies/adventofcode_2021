import itertools


const1 = [ 13, 11, 12, 10, 14, -1, 14,-16, -8, 12,-16,-13, -6, -6]
const2 = [  6, 11,  5,  6,  8, 14,  9,  4,  7, 13, 11, 11,  6,  1]
divs   = [  1,  1,  1,  1,  1, 26,  1, 26, 26,  1, 26, 26, 26, 26]
#           a   b   c   d   e   f   g   h   i   j   k   l   m   n

def program(model,depth):
    w,x,y,z = 0,0,0,0
    for i in range(depth):
        if model[i] == z%26+const1[i]:
            z = z//divs[i]
        else:
            z = z//divs[i]*26 + w+const2[i]
    return w,x,y,z
