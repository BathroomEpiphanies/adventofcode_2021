import sys
import itertools


lines = [l.strip() for l in sys.stdin.readlines()]

#           0        1    2       3       4      5       6        7     8         9
#segments = ['abcefg','cf','acdeg','acdfg','bcdf','abdfg','abdefg','acf','abcdefg','abcdfg']
segments = [
    'abcefg',  # 0
    'cf',      # 1
    'acdeg',   # 2
    'acdfg',   # 3
    'bcdf',    # 4
    'abdfg',   # 5
    'abdefg',  # 6
    'acf',     # 7
    'abcdefg', # 8
    'abcdfg'   # 9
]
[print(f'{i}:{s}') for i,s in enumerate(segments)]
print()


print('*1:',sum(1 for l in lines for x in l.split(' | ')[1].split(' ') if len(x) in {2,3,4,7}))


displays = []
for line in lines:
    for mix in (''.join(x) for x in itertools.permutations('abcdefg')):
        translation = line.translate(str.maketrans('abcdefg',mix))
        patterns = (''.join(sorted(s)) for s in translation.split(' | ')[0].split(' '))
        if all(p in segments for p in patterns):
            #print('abcdefg',mix)
            #print(line)
            print(translation)
            digits = [''.join(sorted(s)) for s in translation.split(' | ')[1].split(' ')]
            number = int(''.join([str(segments.index(p)) for p in digits]))
            #print(number)
            #print()
            displays.append(number)
            break

print(displays)
print(sum(displays))
