import sys
import re

import numpy as np


sequences = [(c,[int(n) for n in l]) for c,*l in (re.match(r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)', l).groups() for l in sys.stdin.readlines())]
core = np.zeros((101,101,101))


class Cube:
    def __init__(self,xmin,xmax,ymin,ymax,zmin,zmax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax
    
    def __str__(self):
        return f'x={self.xmin}..{self.xmax}, y={self.ymin}..{self.ymax}, z={self.zmin}..{self.zmax}'
    
    def __abs__(self):
        if (self.xmax>=self.xmin) and (self.ymax>=self.ymin) and (self.zmax>=self.zmin):
            return (1+self.xmax-self.xmin) * (1+self.ymax-self.ymin) * (1+self.zmax-self.zmin)
        else:
            return 0
    
    def remove(self,othr):
        if self.xmax<othr.xmin or othr.xmax<self.xmin or \
           self.ymax<othr.ymin or othr.ymax<self.ymin or \
           self.zmax<othr.zmin or othr.zmax<self.zmin:
            return [self]
        
        cubes = []
        
        xlow = Cube( self.xmin,min(self.xmax,othr.xmin-1)              , self.ymin,self.ymax , self.zmin,self.zmax )
        xhgh = Cube( max(othr.xmax+1,self.xmin),self.xmax              , self.ymin,self.ymax , self.zmin,self.zmax )
        xmid = Cube( max(othr.xmin,self.xmin),min(othr.xmax,self.xmax) , self.ymin,self.ymax , self.zmin,self.zmax )
        
        ylow = Cube( xmid.xmin,xmid.xmax , xmid.ymin,min(xmid.ymax,othr.ymin-1)              , xmid.zmin,xmid.zmax )
        yhgh = Cube( xmid.xmin,xmid.xmax , max(othr.ymax+1,xmid.ymin),xmid.ymax              , xmid.zmin,xmid.zmax )
        ymid = Cube( xmid.xmin,xmid.xmax , max(othr.ymin,xmid.ymin),min(othr.ymax,xmid.ymax) , xmid.zmin,xmid.zmax )
        
        zlow = Cube( ymid.xmin,ymid.xmax , ymid.ymin,ymid.ymax , ymid.zmin,min(ymid.zmax,othr.zmin-1)              )
        zhgh = Cube( ymid.xmin,ymid.xmax , ymid.ymin,ymid.ymax , max(othr.zmax+1,ymid.zmin),ymid.zmax              )
        zmid = Cube( ymid.xmin,ymid.xmax , ymid.ymin,ymid.ymax , max(othr.zmin,ymid.zmin),min(othr.zmin,ymid.zmin) )
        
        return [c for c in [xlow,xhgh,ylow,yhgh,zlow,zhgh] if abs(c)>0]


class Core:
    def __init__(self):
        self.cubes = []
    
    def __abs__(self):
        return sum(abs(c) for c in self.cubes)
    
    def add_cube(self,cube):
        self.cubes = [d for c in self.cubes for d in c.remove(cube)]+[cube]
    
    def remove_cube(self,cube):
        self.cubes = [d for c in self.cubes for d in c.remove(cube)]
    
    def print(self):
        print(f'core {abs(self)}')
        for c in self.cubes:
            print(c)



core = Core()
for i,(flip,coords) in enumerate(sequences):
    c = Cube(*coords)
    print(i,flip,c,abs(c),len(core.cubes))
    if flip == 'on':
        core.add_cube(c)
    else:
        core.remove_cube(c)


fullcount = abs(core)
inf = float('inf')
core.remove_cube(Cube(-inf,-51,-inf,inf,-inf,inf))
core.remove_cube(Cube(  51,inf,-inf,inf,-inf,inf))
core.remove_cube(Cube(-inf,inf,-inf,-51,-inf,inf))
core.remove_cube(Cube(-inf,inf,  51,inf,-inf,inf))
core.remove_cube(Cube(-inf,inf,-inf,inf,-inf,-51))
core.remove_cube(Cube(-inf,inf,-inf,inf,  51,inf))


print('*1:',abs(core))
print('*2:',fullcount)
