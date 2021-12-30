import sys
import operator
from functools import reduce

lines = [l.strip() for l in sys.stdin.readlines()]


def handle_input(remaining):
    global version_sum
    if not remaining or all(d=='0' for d in remaining):
        return None,None,''
    
    version,remaining = int(remaining[0:3],2),remaining[3:]
    typeid,remaining = int(remaining[0:3],2),remaining[3:]
    version_sum += version
    
    operators = {
        0: ('sum', operator.add),
        1: ('prod',operator.mul),
        2: ('min', min),
        3: ('max', max),
        4: ('id',  id),
        5: ('gt',  operator.gt),
        6: ('lt',  operator.lt),
        7: ('eq',  operator.eq),
    }
    
    if typeid == 4:
        literal = ''
        while True:
            chunk,remaining = remaining[0:5],remaining[5:]
            literal += chunk[1:]
            if chunk[0] == '0':
                break
        parsed = [str(int(literal,2))]
        values = [int(literal,2)]
    else:
        lengthtype,remaining = remaining[0],remaining[1:]
        if lengthtype == '0':
            length,remaining = int(remaining[:15],2),remaining[15:]
            subpacket,remaining = remaining[:length],remaining[length:]
            parsed = []
            values = []
            while subpacket:
                p,v,subpacket = handle_input(subpacket)
                if p:
                    parsed.append(p)
                    values.append(v)
        elif lengthtype == '1':
            length,remaining = int(remaining[:11],2),remaining[11:]
            parsed = []
            values = []
            for i in range(length):
                p,v,remaining = handle_input(remaining)
                if p:
                    parsed.append(p)
                    values.append(v)
    return f'{operators[typeid][0]}({",".join(parsed)})', reduce(operators[typeid][1],values), remaining


for line in lines:
    print(line)
    version_sum = 0
    remaining = ''.join(f'{int(d,16):04b}' for d in line)
    parsed,value,remaining = handle_input(remaining)
    print(f'{parsed} = {value}')
    print('*1:',version_sum)
    print('*2:',value)
    print()
