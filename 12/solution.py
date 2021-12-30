import sys
from collections import defaultdict


caves = defaultdict(list)
for line in (l.strip() for l in sys.stdin.readlines()):
    a,b = line.split('-')
    if a!='end' and b!='start':
        caves[a].append(b)
    if a!='start' and b!='end':
        caves[b].append(a)


def find_paths(caves,path,extravisits,found):
    for candidate in caves[path[-1]]:
        extended = path+(candidate,)
        if candidate == 'end':
            found.add(extended)
        elif candidate.isupper() or candidate not in path:
            find_paths(caves,extended,extravisits,found)
        elif extravisits:
            find_paths(caves,extended,extravisits-1,found)


found = set()
find_paths(caves,('start',),0,found)
print('*1:',len(found))

found = set()
find_paths(caves,('start',),1,found)
print('*2:',len(found))
