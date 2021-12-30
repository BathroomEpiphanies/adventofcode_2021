import sys
import re

import itertools
import collections
import networkx as nx
from queue import PriorityQueue


lines = [l.strip() for l in sys.stdin.readlines()]


_hallways = [16,17,23,18,24,19,25,20,26,21,22]
hallways = [16,17,18,19,20,21,22]
siderooms_a = [ 0, 1, 2, 3]
siderooms_b = [ 4, 5, 6, 7]
siderooms_c = [ 8, 9,10,11]
siderooms_d = [12,13,14,15]
siderooms_1 = [ 3, 7,11,15]
siderooms_2 = [ 2, 6,10,14]
siderooms_3 = [ 1, 5, 9,13]
siderooms_4 = [ 0, 4, 8,12]
# 0    16 17 23 18 24 19 25 20 26 21 22
# 1          03    07    11    15
# 2          02    06    10    14
# 3          01    05    09    13
# 4          00    04    08    12

rooms = nx.DiGraph()
# edges between corridor rooms
for i,j in zip( _hallways , _hallways[1:] ):
    rooms.add_edge(i,j,w=1)
    rooms.add_edge(j,i,w=1)
# edges going out from side rooms
for i,j in zip( siderooms_a , siderooms_a[1:]+[23] ):  rooms.add_edge(i,j,w=1)
for i,j in zip( siderooms_b , siderooms_b[1:]+[24] ):  rooms.add_edge(i,j,w=1)
for i,j in zip( siderooms_c , siderooms_c[1:]+[25] ):  rooms.add_edge(i,j,w=1)
for i,j in zip( siderooms_d , siderooms_d[1:]+[26] ):  rooms.add_edge(i,j,w=1)
# edges going into side rooms
for i,j in zip( [23,24,25,26] , siderooms_1 ): rooms.add_edge(i,j,w=1)
for i,j in zip( [23,24,25,26] , siderooms_2 ): rooms.add_edge(i,j,w=2)
for i,j in zip( [23,24,25,26] , siderooms_3 ): rooms.add_edge(i,j,w=3)
for i,j in zip( [23,24,25,26] , siderooms_4 ): rooms.add_edge(i,j,w=4)

#all_paths = collections.defaultdict(dict)
#for i,j in itertools.product(rooms.nodes(),repeat=2):
#    all_paths[i,j] = (nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'))
#    print(i,j,all_paths[i,j])


class Move:
    def __init__(self, source, destination, species, inrooms, length, path):
        self.source = source
        self.destination = destination
        self.species = species
        self.inrooms = inrooms
        self.path = path[1:]
        self.steps = length

    def __str__(self):
        return f'{self.source:2d} - {self.destination:2d}: {self.species:4d}  {self.steps:2d} {self.path}'
    
    def check(self,state):
        if self.destination in hallways:
            return state.rooms[self.source]!=0 and \
                   any(0!=state.rooms[k]!=self.species for k in self.inrooms) and \
                   all(0==state.rooms[k] for k in self.path)
        else:
            return state.rooms[self.source]==self.species and not \
                   any(0!=state.rooms[k]!=self.species for k in self.inrooms) and \
                   all(0==state.rooms[k] for k in self.path)

home_moves = []
out_moves = []

for (_,outrooms),(species,inrooms) in itertools.product([(0,hallways),(1,siderooms_a),(10,siderooms_b),(100,siderooms_c),(1000,siderooms_d)], repeat=2):
    if inrooms==hallways or outrooms==inrooms:
        continue
    for i,j in itertools.product( outrooms , inrooms ):
        home_moves.append( Move(i, j, species, inrooms, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w')) )

for (species,outrooms),inrooms in itertools.product([(1,siderooms_a),(10,siderooms_b),(100,siderooms_c),(1000,siderooms_d)],[hallways]):
    for i,j in itertools.product( outrooms , inrooms ):
        out_moves.append( Move(i, j, species, outrooms, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w')) )


#for move in home_moves:
#    print(move)
#for move in out_moves:
#    print(move)
#exit()

# import matplotlib.pyplot as plt
# import graphviz as gv
# from networkx.drawing.nx_agraph import graphviz_layout
# graphpos = graphviz_layout(rooms)
# nx.draw(rooms,graphpos,node_size=400,node_color='#AADDDD')
# nx.draw_networkx_labels(rooms,graphpos,{n:f"{n}" for n in rooms.nodes()},font_size=10)
# #nx.draw_networkx_edge_labels(rooms,graphpos,{(u,v)['weight'] for (u,v,d) in rooms.edges(data=True)})
# nx.drawing.nx_pydot.write_dot(rooms,"debug.dot")
# plt.show()


class State:
    def __init__(self, cost, rooms, history):
        self.cost = cost
        self.rooms = rooms
        self.history = history

    def __str__(self):
        return str(self.rooms)+' '+str(self.cost)
    
    def print(self):
        tr = {0:'.', 1:'A', 10:'B', 100:'C', 1000:'D'}
        print( ''.join(tr[self.rooms[r]] for r in _hallways) + '  ' + str(self.cost) + '\n' +
               '  ' + ' '.join(tr[self.rooms[r]] for r in siderooms_1) + '  ' + '\n' + 
               '  ' + ' '.join(tr[self.rooms[r]] for r in siderooms_2) + '  ' + '\n' + 
               '  ' + ' '.join(tr[self.rooms[r]] for r in siderooms_3) + '  ' + '\n' + 
               '  ' + ' '.join(tr[self.rooms[r]] for r in siderooms_4) + '  ' )
    
    def __lt__(self,other):
        return self.cost<other.cost
    
    def __hash__(self):
        return hash(tuple(self.rooms))
    
    def next_states(self):
        def _make_state(move):
            next_cost = self.cost + move.steps*self.rooms[move.source]
            next_rooms = self.rooms.copy()
            next_rooms[move.destination] = next_rooms[move.source]
            next_rooms[move.source] = 0
            next_history = self.history.copy()
            next_history.append(self)
            return State(next_cost,next_rooms,next_history)
        for move in home_moves:
            if move.check(self):
                return [_make_state(move)]
        return [_make_state(move) for move in out_moves if move.check(self)]
    
    def solve(self,target):
        verbose = False
        #verbose = True
        maxlen = 0
        progress = 100
        queue = PriorityQueue()
        queue.put(self)
        found = set()
        visited = set()
        while not queue.empty():
            state = queue.get()
            if state in visited:
                continue
            visited.add(state)
            if len(self.history)>14:
                continue
            if verbose:
                print('examining state')
                print(state)
                state.print()
                print()
                print('adding states to queue')
            if state.rooms == target.rooms:
                break
            maxlen = max(maxlen,queue.qsize())
            if state.cost>=progress:
                print(f'\r{progress}, {maxlen}',end='')
                progress += 100
            for next_state in state.next_states():
                if verbose:
                    next_state.print()
                    print()
                #queue.put( next_state )
                if next_state not in found:
                    found.add( next_state )
                    queue.put( next_state )
        print()
        print('\r',end='')
        if state.rooms == target.rooms:
            return state
        else:
            return  None


target_state = State(float('inf'), [1 for _ in siderooms_a]+[10 for _ in siderooms_b]+[100 for _ in siderooms_c]+[1000 for _ in siderooms_d]+[0 for _ in _hallways],None)
print('target_state')
target_state.print()
print()


#tr = {'.':0, 'A':1, 'B':10, 'C':100, 'D':1000}
#start_config = 27*[0]
#for i,c in zip( _hallways , re.findall(r'[ABCD.]',lines[1]) ):
#    start_config[i] = tr[c]
#for i,c in zip( siderooms_1 , re.findall(r'[ABCD.]',lines[2]) ):
#    start_config[i] = tr[c]
#for i,c in zip( siderooms_2 , re.findall(r'[ABCD.]',lines[3]) ):
#    start_config[i] = tr[c]
#for i,c in zip( siderooms_3 , 'ABCD' ):
#    start_config[i] = tr[c]
#for i,c in zip( siderooms_4 , 'ABCD' ):
#    start_config[i] = tr[c]
#start_state = State(0,start_config,[])
#print('start_state')
#start_state.print()
#print()
#
#solution = start_state.solve(target_state)
#for s in solution.history:
#    s.print()
#    print()
#solution.print()
#print()
#print(f'solved in {len(solution.history)} moves')
#print()
#print('*1:', solution.cost)

#exit()

tr = {'.':0, 'A':1, 'B':10, 'C':100, 'D':1000}
start_config = 27*[0]
for i,c in zip( _hallways , re.findall(r'[ABCD.]',lines[1]) ):
    start_config[i] = tr[c]
for i,c in zip( siderooms_1 , re.findall(r'[ABCD.]',lines[2]) ):
    start_config[i] = tr[c]
for i,c in zip( siderooms_2 , 'DCBA' ):
    start_config[i] = tr[c]
for i,c in zip( siderooms_3 , 'DBAC' ):
    start_config[i] = tr[c]
for i,c in zip( siderooms_4 , re.findall(r'[ABCD.]',lines[3]) ):
    start_config[i] = tr[c]
start_state = State(0,start_config,[])
print('start_state')
start_state.print()
print()

solution = start_state.solve(target_state)
for s in solution.history:
    s.print()
    print()
solution.print()
print()
print(f'solved in {len(solution.history)} moves')
print()
print('*2:', solution.cost)
    
