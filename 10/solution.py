import sys


lines = [list(l.strip()) for l in sys.stdin.readlines()]


matching = { '(':')', '[':']', '{':'}', '<':'>' }
corruption_score = { ')':3, ']':57, '}':1197, '>':25137 }
closing_score = { ')':1, ']':2, '}':3, '>':4 }

def get_opening(seen,remaining):
    if not remaining:
        return seen
    if remaining[0] in matching:
        seen.append(remaining.pop(0))
        return get_opening(seen,remaining)
    elif remaining[0] == matching[seen[-1]]:
        seen.pop(-1)
        remaining.pop(0)
        return get_opening(seen,remaining)
    else:
        raise ValueError

def complete_opening(seen):
    return [matching[p] for p in reversed(seen)]

total_corruption_score = 0
total_closing_score = []
for line in lines:
    print(f'trying: {"".join(line)}')
    try:
        opening = get_opening([],line)
    except ValueError:
        total_corruption_score += corruption_score[line[0]]
        print(f'corrupted {"".join(line)} {corruption_score[line[0]]}')
    else:
        missing = complete_opening(opening)
        tmp = 0
        for p in missing:
            tmp = 5*tmp + closing_score[p]
        print(f'missing {"".join(missing)} {tmp}')
        total_closing_score.append(tmp)

total_closing_score.sort()
print('*1:',total_corruption_score)
print('*2:',total_closing_score[len(total_closing_score)//2])
