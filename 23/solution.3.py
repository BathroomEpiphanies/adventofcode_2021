import sys
import re

import itertools
import collections
import networkx as nx
from queue import PriorityQueue


lines = [l.strip() for l in sys.stdin.readlines()]

_hallways = [0,1,2,3,4,5,6,7,8,9,10]
hallways = [0,1,3,5,7,9,10]
siderooms_a = [11,12,13,14]
siderooms_b = [15,16,17,18]
siderooms_c = [19,20,21,22]
siderooms_d = [23,24,25,26]
siderooms_1 = [14,18,22,26]
siderooms_2 = [13,17,21,25]
siderooms_3 = [12,16,20,24]
siderooms_4 = [11,15,19,23]
# 0    00 01 02 03 04 05 06 07 08 09 10
# 1          14    18    22    26
# 2          13    17    21    25
# 3          12    16    20    24
# 4          11    15    19    23

rooms = nx.DiGraph()
# edges between corridor rooms
for i,j in zip( _hallways , _hallways[1:] ):
    rooms.add_edge(i,j,w=1)
    rooms.add_edge(j,i,w=1)
# edges going out from side rooms
for i,j in zip( siderooms_a , [12,13,14,2] ):
    rooms.add_edge(i,j,w=1)
for i,j in zip( siderooms_b , [16,17,18,4] ):
    rooms.add_edge(i,j,w=1)
for i,j in zip( siderooms_c , [20,21,22,6] ):
    rooms.add_edge(i,j,w=1)
for i,j in zip( siderooms_d , [24,25,26,8] ):
    rooms.add_edge(i,j,w=1)
# edges going into side rooms
for i,j in zip( [2,4,6,8] , siderooms_1 ):
    rooms.add_edge(i,j,w=1)
for i,j in zip( [2,4,6,8] , siderooms_2 ):
    rooms.add_edge(i,j,w=2)
for i,j in zip( [2,4,6,8] , siderooms_3 ):
    rooms.add_edge(i,j,w=3)
for i,j in zip( [2,4,6,8] , siderooms_4 ):
    rooms.add_edge(i,j,w=4)

#all_paths = collections.defaultdict(dict)
#for i,j in itertools.product(rooms.nodes(),repeat=2):
#    all_paths[i,j] = (nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'))
#    print(i,j,all_paths[i,j])


class Move:
    def __init__(self, source, destination, length, path, check):
        self.source = source
        self.destination = destination
        self.path = path[1:]
        self.check = check
        self.steps = length

    def __str__(self):
        return f'{self.source:2d} - {self.destination:2d}: {self.steps:2d} {self.path}'


home_moves = []
out_moves = []
all_moves = collections.defaultdict(dict)


# moves from hallway to side room D
for i,j in itertools.product( hallways , siderooms_d ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]==1000 and not any(0!=state.rooms[k]!=1000 for k in siderooms_d) and all(0==state.rooms[k] for k in move.path) )
    home_moves.append(all_moves[i][j])
# moves from side room A to side room D
for i,j in itertools.product( siderooms_a , siderooms_d ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]==1000 and not any(0!=state.rooms[k]!=1000 for k in siderooms_d) and all(0==state.rooms[k] for k in move.path) )
    home_moves.append(all_moves[i][j])
# moves from side room B to side room D
for i,j in itertools.product( siderooms_b , siderooms_d ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]==1000 and not any(0!=state.rooms[k]!=1000 for k in siderooms_d) and all(0==state.rooms[k] for k in move.path) )
    home_moves.append(all_moves[i][j])
# moves from side room C to side room D
for i,j in itertools.product( siderooms_c , siderooms_d ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]==1000 and not any(0!=state.rooms[k]!=1000 for k in siderooms_d) and all(0==state.rooms[k] for k in move.path) )
    home_moves.append(all_moves[i][j])

# moves from hallway to side room C
for i,j in itertools.product( hallways , siderooms_c ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]==100  and not any(0!=state.rooms[k]!=100  for k in siderooms_c) and all(0==state.rooms[k] for k in move.path) )
    home_moves.append(all_moves[i][j])
# moves from side room A to side room C
for i,j in itertools.product( siderooms_a , siderooms_c ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]==100  and not any(0!=state.rooms[k]!=100  for k in siderooms_c) and all(0==state.rooms[k] for k in move.path) )
    home_moves.append(all_moves[i][j])
# moves from side room B to side room C
for i,j in itertools.product( siderooms_b , siderooms_c ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]==100  and not any(0!=state.rooms[k]!=100  for k in siderooms_c) and all(0==state.rooms[k] for k in move.path) )
    home_moves.append(all_moves[i][j])
# moves from side room D to side room C
for i,j in itertools.product( siderooms_d , siderooms_c ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]==100  and not any(0!=state.rooms[k]!=100  for k in siderooms_c) and all(0==state.rooms[k] for k in move.path) )
    home_moves.append(all_moves[i][j])

# moves from hallway to side room B
for i,j in itertools.product( hallways , siderooms_b ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]==10   and not any(0!=state.rooms[k]!=10   for k in siderooms_b) and all(0==state.rooms[k] for k in move.path) )
    home_moves.append(all_moves[i][j])
# moves from side room A to side room B
for i,j in itertools.product( siderooms_a , siderooms_b ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]==10   and not any(0!=state.rooms[k]!=10   for k in siderooms_b) and all(0==state.rooms[k] for k in move.path) )
    home_moves.append(all_moves[i][j])
# moves from side room C to side room B
for i,j in itertools.product( siderooms_c , siderooms_b ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]==10   and not any(0!=state.rooms[k]!=10   for k in siderooms_b) and all(0==state.rooms[k] for k in move.path) )
    home_moves.append(all_moves[i][j])
# moves from side room D to side room C
for i,j in itertools.product( siderooms_d , siderooms_b ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]==10   and not any(0!=state.rooms[k]!=10   for k in siderooms_b) and all(0==state.rooms[k] for k in move.path) )
    home_moves.append(all_moves[i][j])

# moves from hallway to side room A
for i,j in itertools.product( hallways , siderooms_a ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]==1    and not any(0!=state.rooms[k]!=1    for k in siderooms_a) and all(0==state.rooms[k] for k in move.path) )
    home_moves.append(all_moves[i][j])
# moves from side room B to side room A
for i,j in itertools.product( siderooms_b , siderooms_a ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]==1    and not any(0!=state.rooms[k]!=1    for k in siderooms_a) and all(0==state.rooms[k] for k in move.path) )
    home_moves.append(all_moves[i][j])
# moves from side room C to side room A
for i,j in itertools.product( siderooms_c , siderooms_a ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]==1    and not any(0!=state.rooms[k]!=1    for k in siderooms_a) and all(0==state.rooms[k] for k in move.path) )
    home_moves.append(all_moves[i][j])
# moves from side room D to side room A
for i,j in itertools.product( siderooms_d , siderooms_a ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]==1    and not any(0!=state.rooms[k]!=1    for k in siderooms_a) and all(0==state.rooms[k] for k in move.path) )
    home_moves.append(all_moves[i][j])


# moves from side room A to hallway
for i,j in itertools.product( siderooms_a , hallways ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]!=0    and     any(0!=state.rooms[k]!=1    for k in siderooms_a) and all(0==state.rooms[k] for k in move.path) )
    out_moves.append(all_moves[i][j])
# moves from side room B to hallway
for i,j in itertools.product( siderooms_b , hallways ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]!=0    and     any(0!=state.rooms[k]!=10   for k in siderooms_b) and all(0==state.rooms[k] for k in move.path) )
    out_moves.append(all_moves[i][j])
# moves from side room C to hallway
for i,j in itertools.product( siderooms_c , hallways ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]!=0    and     any(0!=state.rooms[k]!=100  for k in siderooms_c) and all(0==state.rooms[k] for k in move.path) )
    out_moves.append(all_moves[i][j])
# moves from side room D to hallway
for i,j in itertools.product( siderooms_d , hallways ):
    all_moves[i][j] = Move(i, j, nx.shortest_path_length(rooms,i,j,weight='w'), nx.shortest_path(rooms,i,j,weight='w'), lambda state,move: state.rooms[move.source]!=0    and     any(0!=state.rooms[k]!=1000 for k in siderooms_d) and all(0==state.rooms[k] for k in move.path) )
    out_moves.append(all_moves[i][j])


#for r1,r2,m in ((r1,r2,m) for r1,moves in all_moves.items() for r2,m in moves.items()):
#    print(m)
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
            if move.check(self,move):
                #print(move,move.check(self,move))
                return [_make_state(move)]
        return [_make_state(move) for move in out_moves if move.check(self,move)]
        #for move in out_moves:
        #    print(move,move.check(self,move))
        #exit()
    
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

        
target_state = State(float('inf'), [0 for _ in _hallways]+[1 for _ in siderooms_a]+[10 for _ in siderooms_b]+[100 for _ in siderooms_c]+[1000 for _ in siderooms_d],None)
#print('target_state')
#target_state.print()
#print()


tr = {'.':0, 'A':1, 'B':10, 'C':100, 'D':1000}
start_config = 27*[0]
for i,c in zip( _hallways , re.findall(r'[ABCD.]',lines[1]) ):
    start_config[i] = tr[c]
for i,c in zip( siderooms_1 , re.findall(r'[ABCD.]',lines[2]) ):
    start_config[i] = tr[c]
for i,c in zip( siderooms_2 , re.findall(r'[ABCD.]',lines[3]) ):
    start_config[i] = tr[c]
for i,c in zip( siderooms_3 , 'ABCD' ):
    start_config[i] = tr[c]
for i,c in zip( siderooms_4 , 'ABCD' ):
    start_config[i] = tr[c]
start_state = State(0,start_config,[])
#print('start_state')
#start_state.print()
#print()

solution = start_state.solve(target_state)
for s in solution.history:
    s.print()
    print()
solution.print()
print()
print('*1:', solution.cost)
#solution.print()

exit()

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
#print('start_state')
#start_state.print()
#print()

solution = start_state.solve(target_state)
for s in solution.history:
    s.print()
    print()
solution.print()
print()
#solution.print()
    
