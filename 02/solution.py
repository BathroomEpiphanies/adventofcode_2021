import re
import sys


commands = [re.match(r'(?P<action>[^ ]+) (?P<steps>[0-9]+)', l).groupdict() for l in sys.stdin.readlines()]

actions = {
    'down':    0+1j,
    'up':      0-1j,
    'forward': 1+0j,
}

position = 0+0j
for command in commands:
    position += int(command['steps'])*actions[command['action']]

print(f'position: {position}, {int(position.real*position.imag)}')


position = 0+0j
aim = 1+0j
for command in commands:
    if command['action'] in ['down','up']:
        aim += int(command['steps'])*actions[command['action']]
    else:
        position += int(command['steps'])*aim

print(f'position: {position}, {int(position.real*position.imag)}')
