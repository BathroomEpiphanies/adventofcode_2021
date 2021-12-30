import sys
import re
import itertools
from math import floor,ceil


class node:
    def __init__(self,a,b):
        self.a = a
        self.b = b
        
    def __str__(self):
        return f'[{str(self.a)},{str(self.b)}]'
    __repr__ = __str__
    
    def explode(self,pa=None,pb=None,depth=0):
        indent = depth*'  '
        #print(indent,'exploding',self,pa,pb,depth,file=sys.stderr)
        if isinstance(pa,int):
            if isinstance(self.a,int):
                self.a += pa
                tmp = True,False,0,0
                ##print(indent,'returning',tmp,file=sys.stderr)
                return tmp
            else:
                tmp = self.a.explode(pa,None,depth+1)
                ##print(indent,'returning',tmp,file=sys.stderr)
                return tmp
        if isinstance(pb,int):
            if isinstance(self.b,int):
                self.b += pb
                tmp = True,False,0,0
                ##print(indent,'returning',tmp,file=sys.stderr)
                return tmp
            else:
                tmp = self.b.explode(None,pb,depth+1)
                ##print(indent,'returning',tmp,file=sys.stderr)
                return tmp

        
        ax,bx = 0,0
        if isinstance(self.a,node):
            ex,de,ax,bx = self.a.explode(None,None,depth+1)
            #print(indent,'exploded a',self,ex,de,ax,bx,file=sys.stderr)
            if ex and isinstance(bx,int):
                if de:
                    self.a = 0
                if isinstance(self.b,int):
                    self.b += bx
                    #print(indent,self,file=sys.stderr)
                    tmp = True,False,ax,None
                    ##print(indent,'returning',tmp,file=sys.stderr)
                    return tmp
                else:
                    #print(indent,self,file=sys.stderr)
                    tmp = self.b.explode(bx,None,depth+1)
                    ex2,de2,ax2,bx2 = tmp
                    tmp = ex2,de2,ax,None
                    ##print(indent,'returning',tmp,file=sys.stderr)
                    return tmp
            if ex:
                tmp = True,False,ax,bx
                ##print(indent,'returning',tmp,file=sys.stderr)
                return tmp
        
        if isinstance(self.b,node):
            ex,de,ax,bx = self.b.explode(None,None,depth+1)
            #print(indent,'exploded b',self,ex,de,ax,bx,file=sys.stderr)
            if ex and isinstance(ax,int):
                if de:
                    self.b = 0
                if isinstance(self.a,int):
                    self.a += ax
                    #print(indent,self,file=sys.stderr)
                    tmp = True,False,None,bx
                    ##print(indent,'returning',tmp,file=sys.stderr)
                    return tmp
                else:
                    #print(indent,self,file=sys.stderr)
                    tmp = self.a.explode(None,ax,depth+1)
                    ex2,de2,ax2,bx2 = tmp
                    tmp = ex2,de2,None,bx
                    ##print(indent,'returning',tmp,file=sys.stderr)
                    return tmp
            if ex:
                tmp = True,False,ax,bx
                ##print(indent,'returning',tmp,file=sys.stderr)
                return tmp
        
        if depth>3:
            tmp = True,True,self.a,self.b
            ##print(indent,'returning',tmp,file=sys.stderr)
            return tmp
        else:
            tmp = False,False,None,None
            ##print(indent,'returning',tmp,file=sys.stderr)
            return tmp
    
    def split(self):
        if isinstance(self.a,int) and self.a>9:
            self.a = node(floor(self.a/2),ceil(self.a/2))
            return True
        elif isinstance(self.a,node) and self.a.split():
            return True
        elif isinstance(self.b,int) and self.b>9:
            self.b = node(floor(self.b/2),ceil(self.b/2))
            return True
        elif isinstance(self.b,node) and self.b.split():
            return True
        return False
    
    def reduce(self):
        while True:
            while True:
                tmp = self.explode()
                #print('',file=sys.stderr)
                #print(self,tmp)
                if not tmp[0]:
                    break
            #print('finished exploding')
            tmp = self.split()
            #print(self,tmp)
            if not tmp:
                break
        #print('',file=sys.stderr)
    
    def __abs__(self):
        return 3*abs(self.a) + 2*abs(self.b)
    

class SnailFish:
    
    n = None
    def __init__(self,line):
        nums = {}
        chars = (chr(c) for c in itertools.count(ord('a')))
        while True:
            #print(line)
            m = re.search(r'\[([\d\w]+),([\d\w]+)\]',line)
            if not m:
                break
            a,b = m.group(1,2)
            c = next(chars)
            #print(c,m,m.group(0),a,b)
            line = re.sub(rf'\[{m.group(0)[1:-1]}\]',c,line)
            #print(line)
            nums[c] = node(nums[a] if a in nums else int(a),nums[b] if b in nums else int(b))
        #print(nums)
        self.n = nums[c]
    
    def __str__(self):
        return str(self.n)
    __repr__ = __str__

    def __add__(self,other):
        self.n = node(self.n,other.n)
        
        self.n.reduce()
        return self
    
    def __abs__(self):
        return abs(self.n)



#a = SnailFish('[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]')
#b = SnailFish('[2,2]')
#print(a)
#print(b)
#print(a+b)
#exit()


#a = SnailFish('[[[[4,3],4],4],[7,[[8,4],9]]]')
#b = SnailFish('[1,1]')
#print(a)
#print(b)
#print(a+b)
#exit()


lines = [l.strip() for l in sys.stdin.readlines()]
#numbers = [SnailFish(l) for l in lines]
#
#print('adding numbers')
#m = numbers[0]
##for n in numbers[1:2]:
#for n in numbers[1:]:
#    print(m)
#    print(n)
#    print(m+n)
#    print()
#
#print('calculating abs')
#print(abs(m))


maxabs = 0
for i,j in ((i,j) for i,j in itertools.product(range(len(lines)),repeat=2) if i!=j):
    print(i,j)
    a = SnailFish(lines[i])
    b = SnailFish(lines[j])
    c = a+b
    val = abs(c)
    #print(i,j,a,b,c,)
    maxabs = max(val,maxabs)
print(maxabs)




#for a in [ '[[[[[9,8],1],2],3],4]',
#           '[7,[6,[5,[4,[3,2]]]]]',
#           '[[6,[5,[4,[3,2]]]],1]',
#           '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]', ]:
#    a = SnailFish(a)
#    print(a)
#    print(a.n.explode(None,None,0))
#    print()
#    print(a.n.explode(None,None,0))
#    print()
#exit()


#a = SnailFish('[[[[4,3],4],4],[7,[[8,4],9]]]')
#b = SnailFish('[1,1]')
#print(a)
#print(b)
#print(a+b)
#
#while True:
#    while True:
#        tmp = a.n.explode()
#        print(a,tmp)
#        print()
#        if not tmp[0]:
#            break
#    tmp = a.n.split()
#    print(a,tmp)
#    if not tmp:
#        break
#
#exit()

