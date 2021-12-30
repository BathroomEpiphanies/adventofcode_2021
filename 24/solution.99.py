import itertools

const_as = [ 13, 11, 12, 10, 14, -1, 14,-16, -8, 12,-16,-13, -6, -6]
const_bs = [  6, 11,  5,  6,  8, 14,  9,  4,  7, 13, 11, 11,  6,  1]
const_ds = [  1,  1,  1,  1,  1, 26,  1, 26, 26,  1, 26, 26, 26, 26]

def loop(z,w,c1,c2,d):
    if w == z%26 + c1:
        z = z//d
    else:
        z = z//d*26 + w + c2
    return z


#           1    2    3    4    5    6    7    8    9   10   11   12   13   14
LIMIT = [10e6,10e6,10e6,10e6,10e6,10e6,10e6,10e6,10e5,10e5,10e5,10e4,10e3,10e1]
zs = {'':0}
for i,(a,b,d,L) in enumerate(zip(const_as,const_bs,const_ds,LIMIT),1):
    zs = {m+str(w):loop(z,w,a,b,d) for m,z in zs.items() for w in [1,2,3,4,5,6,7,8,9] if z<L}
    print(i,len(zs))
print('*1:', max(k for k,v in zs.items() if v==0))



LIMIT = 10_000_000
zs = {0: ''}
for a,b,d in zip(const_as,const_bs,const_ds):
    zs = {loop(z,w,a,b,d):m+str(w) for z,m in zs.items() for w in [1,2,3,4,5,6,7,8,9] if z<LIMIT}
print('*1:', zs[0])


zs = {0: ''}
for a,b,d in zip(const_as,const_bs,const_ds):
    zs = {loop(z,w,a,b,d):m+str(w) for z,m in zs.items() for w in [9,8,7,6,5,4,3,2,1] if z<LIMIT}
print('*2:', ''.join(str(w) for w in zs[0]))
