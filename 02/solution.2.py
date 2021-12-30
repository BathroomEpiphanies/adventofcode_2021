import sys
from collections import namedtuple


Command = namedtuple('Command',['action','steps'])
commands = [Command(a,int(b)) for l in sys.stdin.readlines() for a,b in [l.split(' ')]]
print(commands)


actions = {
    'down':    0+1j,
    'up':      0-1j,
    'forward': 1+0j,
}
position = 0+0j
for command in commands:
    position += command.steps*actions[command.action]

print(f'position: {position}, {int(position.real*position.imag)}')


actions = {
    'down':    0+1j,
    'up':      0-1j,
}
position = 0+0j
aim = 1+0j
for command in commands:
    if command.action in actions:
        aim += command.steps*actions[command.action]
    else:
        position += command.steps*aim

print(f'position: {position}, {int(position.real*position.imag)}')
