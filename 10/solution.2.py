import sys


lines = [list(l.strip()) for l in sys.stdin.readlines()]


parenthesis = { '(':')', '[':']', '{':'}', '<':'>' }
corruption_scoring = { ')':3, ']':57, '}':1197, '>':25137 }
closing_scoring = { '(':1, '[':2, '{':3, '<':4 }


corruption_score = 0
closing_score = []

for remaining in lines:
    seen = []
    while remaining:
        if remaining[0] in parenthesis:
            seen.append(remaining.pop(0))
        elif remaining[0] == parenthesis[seen[-1]]:
            seen.pop(-1)
            remaining.pop(0)
        else:
            break
    if remaining:
        corruption_score += corruption_scoring[remaining[0]]
    else:
        tmp = 0
        for p in reversed(seen):
            tmp = 5*tmp + closing_scoring[p]
        closing_score.append(tmp)
    print(''.join(seen),''.join(remaining))

print('*1:',corruption_score)
print('*2:',sorted(closing_score)[len(closing_score)//2])
