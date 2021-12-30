import sys
import re

import itertools
import collections
import networkx as nx
from queue import PriorityQueue


Path = collections.namedtuple('path',['length','path'])
#Layout = collections.namedtuple('layout',['rooms','paths','side_rooms','hallway'])

class Layout:
    def __init__(self):
        self.rooms = nx.Graph()
        for r1,r2 in [
                ('H0','H1'), ('H1','H2'), ('H2','H3'), ('H3','H4'), ('H4','H5'), ('H5','H6'), ('H6','H7'), ('H7','H8'), ('H8','H9'), ('H9','Ha'),
                                          ('A0','H2'),              ('B0','H4'),              ('C0','H6'),              ('D0','H8'),
                                          ('A1','A0'),              ('B1','B0'),              ('C1','C0'),              ('D1','D0'),
                                          ('A2','A1'),              ('B2','B1'),              ('C2','C1'),              ('D2','D1'),
                                          ('A3','A2'),              ('B3','B2'),              ('C3','C2'),              ('D3','D2'),
                ]:
            self.rooms.add_edge(r1,r2)
        
        self.side_rooms = ['A0','A1','A2','A3','B0','B1','B2','B3','C0','C1','C2','C3','D0','D1','D2','D3']
        self.hallway = ['H0','H1','H3','H5','H7','H9','Ha']
        self.forbidden_rooms = ['H2','H4','H6','H8']
        self.allowed_rooms = list(set(self.side_rooms)|set(self.hallway))
        
        self.paths = collections.defaultdict(dict)
        for r1,r2 in itertools.product(self.side_rooms,self.hallway):
            path = nx.shortest_path(self.rooms, r1, r2)
            self.paths[r1][r2] = Path(len(path)-1, [r for r in path[1:] if r not in self.forbidden_rooms])
        for r1,r2 in itertools.product(self.hallway,self.side_rooms):
            path = nx.shortest_path(self.rooms, r1, r2)
            self.paths[r1][r2] = Path(len(path)-1, [r for r in path[1:] if r not in self.forbidden_rooms])
        for r1,r2 in itertools.product(self.side_rooms, self.side_rooms):
            if r1==r2:
                continue
            path = nx.shortest_path(self.rooms, r1, r2)
            self.paths[r1][r2] = Path(len(path)-1, [r for r in path[1:] if r not in self.forbidden_rooms])
    
    def print_paths(self):
        for s,e in self.paths.items():
            for t,f in e.items():
                print(s,t,f)
        
    def print_edges(self):
        for e in self.rooms.edges():
            print(e)
        

burrow = Layout()
#burrow.print_edges()
#burrow.print_paths()
#exit()
    
class State:


    def __init__(self, cost, config, history):
        self.cost = cost
        self.config = config
        self.history = history
    
    def print(self):
        print( ''.join(self.config[r] if r in self.config and self.config[r] else '.' for r in ['H0','H1','H2','H3','H4','H5','H6','H7','H8','H9','Ha']) + '  ' + str(self.cost) + '\n' +
               '  ' + ' '.join(self.config[r] for r in ['A0','B0','C0','D0']) + '  ' + '\n' +
               '  ' + ' '.join(self.config[r] for r in ['A1','B1','C1','D1']) + '  ' + '\n' + 
               '  ' + ' '.join(self.config[r] for r in ['A2','B2','C2','D2']) + '  ' + '\n' + 
               '  ' + ' '.join(self.config[r] for r in ['A3','B3','C3','D3']) + '  '         ) 
    
    def __str__(self):
        return f'{self.cost}  {len(self.history)}' + '  ' + \
            '( ' + ', '.join(r+':'+self.config[r] for r in sorted(burrow.side_rooms)) + ' )' + \
            '( ' + ', '.join(r+':'+self.config[r] for r in sorted(burrow.hallway)) + ' )'
    __repr__ = __str__
    
    def __lt__(self, other):
        return self.cost<other.cost
    
    def matches(self, other):
        return hash(self)==hash(other)
    
    def __hash__(self):
        return hash(tuple(self.config[r] for r in burrow.allowed_rooms))
    
    def plot_graph(self):
        import matplotlib.pyplot as plt
        import graphviz as gv
        from networkx.drawing.nx_agraph import graphviz_layout
        graphpos = graphviz_layout(burrow.rooms)
        nx.draw(burrow.rooms,graphpos,node_size=400,node_color='#AADDDD')
        nx.draw_networkx_labels(burrow.rooms,graphpos,{n:f"{n}:{start_state.config[n] if n in start_state.config and start_state.config[n] else '_'}" for n in burrow.rooms.nodes()},font_size=10)
        nx.drawing.nx_pydot.write_dot(burrow.rooms,"debug.dot")
        plt.show()
    
    def make_next_state(self, r1, r2):
        move_costs = { 'A':1,'B':10, 'C':100, 'D':1000 }
        species = self.config[r1]
        next_config = self.config.copy()
        next_config[r1] = '.'
        next_config[r2] = self.config[r1]
        next_cost = self.cost + burrow.paths[r1][r2].length * move_costs[species]
        next_history = self.history.copy()
        next_history.append(self)
        return State(next_cost,next_config,next_history)
    
    def find_next_states(self):
        next_states = []
        allowed_to_move = []
        for r1 in (r for r,s in self.config.items() if s!='.'):
            #print(r1)
            species = self.config[r1]
            if r1 in ['A0','A1','A2','A3'] and any(self.config[r]!='A' for r in ['A0','A1','A2','A3'] if self.config[r]!='.') or \
               r1 in ['B0','B1','B2','B3'] and any(self.config[r]!='B' for r in ['B0','B1','B2','B3'] if self.config[r]!='.') or \
               r1 in ['C0','C1','C2','C3'] and any(self.config[r]!='C' for r in ['C0','C1','C2','C3'] if self.config[r]!='.') or \
               r1 in ['D0','D1','D2','D3'] and any(self.config[r]!='D' for r in ['D0','D1','D2','D3'] if self.config[r]!='.') or \
               r1 in burrow.hallway :
                allowed_to_move.append(r1)
        #print('allowed to move', sorted(allowed_to_move))
        for r1 in allowed_to_move:
            species = self.config[r1]
            
            allowed_destinations = []
            for r2,destination in burrow.paths[r1].items():
                #print(f'{r1}-{r2}',' '.join(f'{r}:{self.config[r]}' for r in destination.path))
                if r2 in ['A0','A1','A2','A3'] and species!='A' or \
                   r2 in ['B0','B1','B2','B3'] and species!='B' or \
                   r2 in ['C0','C1','C2','C3'] and species!='C' or \
                   r2 in ['D0','D1','D2','D3'] and species!='D' :
                    #print('fails: moving to wrong side room')
                    continue
                if r2 in ['A0','A1','A2','A3'] and any(self.config[r]!='A' for r in ['A0','A1','A2','A3'] if self.config[r]!='.') or \
                   r2 in ['B0','B1','B2','B3'] and any(self.config[r]!='B' for r in ['B0','B1','B2','B3'] if self.config[r]!='.') or \
                   r2 in ['C0','C1','C2','C3'] and any(self.config[r]!='C' for r in ['C0','C1','C2','C3'] if self.config[r]!='.') or \
                   r2 in ['D0','D1','D2','D3'] and any(self.config[r]!='D' for r in ['D0','D1','D2','D3'] if self.config[r]!='.'):
                    #print('fails: wrong species still in room')
                    continue
                if any(self.config[r]!='.' for r in destination.path):
                    #print('fails: path occupied')
                    continue
                allowed_destinations.append(r2)
            
            if    species=='D' and 'D3' in allowed_destinations: return [self.make_next_state(r1,'D3')]
            elif  species=='D' and 'D2' in allowed_destinations: return [self.make_next_state(r1,'D2')]
            elif  species=='D' and 'D1' in allowed_destinations: return [self.make_next_state(r1,'D1')]
            elif  species=='D' and 'D0' in allowed_destinations: return [self.make_next_state(r1,'D0')]
            elif  species=='C' and 'C3' in allowed_destinations: return [self.make_next_state(r1,'C3')]
            elif  species=='C' and 'C2' in allowed_destinations: return [self.make_next_state(r1,'C2')]
            elif  species=='C' and 'C1' in allowed_destinations: return [self.make_next_state(r1,'C1')]
            elif  species=='C' and 'C0' in allowed_destinations: return [self.make_next_state(r1,'C0')]
            elif  species=='B' and 'B3' in allowed_destinations: return [self.make_next_state(r1,'B3')]
            elif  species=='B' and 'B2' in allowed_destinations: return [self.make_next_state(r1,'B2')]
            elif  species=='B' and 'B1' in allowed_destinations: return [self.make_next_state(r1,'B1')]
            elif  species=='B' and 'B0' in allowed_destinations: return [self.make_next_state(r1,'B0')]
            elif  species=='A' and 'A3' in allowed_destinations: return [self.make_next_state(r1,'A3')]
            elif  species=='A' and 'A2' in allowed_destinations: return [self.make_next_state(r1,'A2')]
            elif  species=='A' and 'A1' in allowed_destinations: return [self.make_next_state(r1,'A1')]
            elif  species=='A' and 'A0' in allowed_destinations: return [self.make_next_state(r1,'A0')]
            else:
                for r2 in allowed_destinations:
                    next_states.append( self.make_next_state(r1,r2) )
        
        #print('finding next states for')
        #self.print()
        #print()
        #print('returning next states')
        #for s in next_states:
        #    s.print()
        #    print()
        #print('those were it')
        
        return next_states

    def solve(self,goal):
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
            if state.matches(goal):
                break
            if state.cost>=progress:
                print(f'\r{progress}',end='')
                progress += 100
            #state.print()
            for next_state in state.find_next_states():
                if next_state not in found:
                    found.add( next_state )
                    queue.put( next_state )
        print('\r',end='')
        if state.matches(goal):
            return state
        else:
            return  None
    



lines = [l.strip() for l in sys.stdin.readlines()]
solved_state = State( float('inf'), { r:r[0] for r in burrow.side_rooms} | { r:'.'  for r in burrow.hallway }, [] )
#print('solved_state')
#solved_state.print()
#print()


start_state = State(0, { r:'.' for r in burrow.allowed_rooms }, [])
start_state.config.update( {r:s for r,s in zip(['H0','H1','H2','H3','H4','H5','H6','H7','H8','H9','Ha','Hb'], re.findall(r'[ABCD.]',lines[1]))} )
start_state.config.update( {r:s for r,s in zip(['A0','B0','C0','D0'], re.findall(r'[ABCD.]',lines[2]))} )
start_state.config.update( {r:s for r,s in zip(['A1','B1','C1','D1'], re.findall(r'[ABCD.]',lines[3]))} )
start_state.config.update( {r:s for r,s in zip(['A2','B2','C2','D2'], 'ABCD.')} )
start_state.config.update( {r:s for r,s in zip(['A3','B3','C3','D3'], 'ABCD.')} )
#print('start_state')
#start_state.print()
#print()

solution = start_state.solve(solved_state)
#for s in solution.history:
#    s.print()
#    print(s.cost)
#    print()
#solution.print()
print('*1:', solution.cost)


start_state = State(0, { r:'.' for r in burrow.allowed_rooms }, [])
start_state.config.update( {r:s for r,s in zip(['H0','H1','H2','H3','H4','H5','H6','H7','H8','H9','Ha','Hb'], re.findall(r'[ABCD.]',lines[1]))} )
start_state.config.update( {r:s for r,s in zip(['A0','B0','C0','D0'], re.findall(r'[ABCD.]',lines[2]))} )
start_state.config.update( {r:s for r,s in zip(['A1','B1','C1','D1'], 'DCBA.')} )
start_state.config.update( {r:s for r,s in zip(['A2','B2','C2','D2'], 'DBAC.')} )
start_state.config.update( {r:s for r,s in zip(['A3','B3','C3','D3'], re.findall(r'[ABCD.]',lines[3]))} )
#print('start_state')
#start_state.print()
#print()

solution = start_state.solve(solved_state)
#for s in solution.history:
#    s.print()
#    print(s.cost)
#    print()
#solution.print()
print('*2:', solution.cost)
