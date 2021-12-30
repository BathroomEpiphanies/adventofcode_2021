import sys
import re
import itertools
import functools


starting_positions = tuple(int(re.match(r'Player \d starting position: (\d+)',l).groups()[0]) for l in sys.stdin.readlines())


dice = 0
scores = (0,0)
positions = starting_positions
active_player = 0
while all(s<1000 for s in scores):
    rollsum = 3*dice+1+2+3
    dice += 3
    positions = tuple((p+rollsum-1)%10+1 if i==active_player else p for i,p in enumerate(positions))
    scores = tuple(s+p if i==active_player else s for i,(p,s) in enumerate(zip(positions,scores)))
    active_player = (active_player+1) % len(scores)

print('*1:',dice*min(scores))


#@functools.cache
#def count_wins(active_player,positions,scores):
#    wins = tuple(1 if s>20 else 0 for s in scores)
#    if any(wins):
#        return wins
#    
#    wins = tuple(0 for _ in positions)
#    for rollsum in (sum(roll) for roll in itertools.product([1,2,3],repeat=3)):
#        next_player = (active_player+1) % len(scores)
#        next_positions = tuple((p+rollsum-1)%10+1 if i==active_player else p for i,p in enumerate(positions))
#        next_scores = tuple(s+p if i==active_player else s for i,(p,s) in enumerate(zip(next_positions,scores)))
#        wins = tuple(a+b for a,b in zip(wins,count_wins(next_player,next_positions,next_scores)))
#    return wins
#
#print('*2:',max(count_wins(0,starting_positions,tuple(0 for _ in starting_positions))))


@functools.cache
def count_wins(active,pos0,pos1,scr0,scr1):
    if scr0>=21:
        return (1,0)
    elif scr1>=21:
        return (0,1)
    else:
        win0,win1 = 0,0
        for roll in itertools.product([1,2,3],repeat=3):
            rollsum = sum(roll)
            if active==0:
                newp = (pos0+rollsum-1)%10+1
                add0,add1 = count_wins(1-active, newp, pos1, scr0+newp, scr1)
            else:
                newp = (pos1+rollsum-1)%10+1
                add0,add1 = count_wins(1-active, pos0, newp, scr0, scr1+newp)
            win0,win1 = win0+add0,win1+add1
        return win0,win1

print('*2:',max(count_wins(0,*starting_positions,*(0,0))))


print(dir(count_wins))
print(count_wins.cache_info())
print(len(count_wins.cache))
