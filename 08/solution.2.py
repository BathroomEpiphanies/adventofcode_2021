import sys


#   aaaa            aaaa    aaaa          
#  b    c       c       c       c  b    c 
#  b    c       c       c       c  b    c 
#                   dddd    dddd    dddd  
#  e    f       f  e            f       f 
#  e    f       f  e            f       f 
#   gggg            gggg    gggg          
#                                         
#   aaaa    aaaa    aaaa    aaaa    aaaa  
#  b       b            c  b    c  b    c 
#  b       b            c  b    c  b    c 
#   dddd    dddd            dddd    dddd  
#       f  e    f       f  e    f       f 
#       f  e    f       f  e    f       f 
#   gggg    gggg            gggg    gggg  


lines = [l.strip() for l in sys.stdin.readlines()]

print('*1:',sum(1 for l in lines for x in l.split(' | ')[1].split(' ') if len(x) in {2,3,4,7}))

def decode_number(signal_part,output_part):
    signals = [frozenset(y) for y in signal_part.split(' ')]
    outputs = [frozenset(y) for y in output_part.split(' ')]
    lookup = {}
    lookup[1] = next(signals.pop(i) for i,s in enumerate(signals) if len(s)==2)
    lookup[4] = next(signals.pop(i) for i,s in enumerate(signals) if len(s)==4)
    lookup[7] = next(signals.pop(i) for i,s in enumerate(signals) if len(s)==3)
    lookup[8] = next(signals.pop(i) for i,s in enumerate(signals) if len(s)==7)
    lookup[9] = next(signals.pop(i) for i,s in enumerate(signals) if len(s)==6 and s>lookup[4])
    lookup[0] = next(signals.pop(i) for i,s in enumerate(signals) if len(s)==6 and s>lookup[7])
    lookup[6] = next(signals.pop(i) for i,s in enumerate(signals) if len(s)==6)
    lookup[3] = next(signals.pop(i) for i,s in enumerate(signals) if len(s)==5 and s>lookup[1])
    lookup[5] = next(signals.pop(i) for i,s in enumerate(signals) if len(s)==5 and s<lookup[9])
    lookup[2] = next(signals.pop(i) for i,s in enumerate(signals) if len(s)==5)
    lookup = {v:k for k,v in lookup.items()}
    return sum(lookup[x]*10**i for i,x in enumerate(reversed(outputs)))

displays = [decode_number(*line.split(' | ')) for line in lines]
print(displays)
print('*2:',sum(displays))
