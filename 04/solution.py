import re
import sys

import numpy as np
import itertools


input_lines = [l.strip() for l in sys.stdin.readlines()]

class BingoBoard:
    def __init__(self, board):
        self.board = board
        self.lines = [set(r) for r in self.board] + [set(c) for c in self.board.T]
        self.finished = False
    
    def __str__(self):
        return '\n'+str(self.board)+'\n'+str(self.lines)+'\n'+str(self.finished)+'\n'
    
    __repr__ = __str__
    
    def __iter__(self):
        return iter({n for l in self.lines for n in l})
    
    def __copy__(self):
        return BingoBoard(self.board)
    
    def mark_number(self,n):
        for l in self.lines:
            l -= {n}
        self.finished = not all(self.lines)
        return self.finished


numbers = np.array(input_lines[0].split(','),dtype=int)
tmp_game = [
    BingoBoard(np.array([re.split(r' +',r) for r in board], dtype=int))
    for board in [input_lines[i:i+5] for i in range(2,len(input_lines),6)]
]


game = tmp_game.copy()
for number,board in itertools.product(numbers,game):
    if board.mark_number(number):
        break

remaining = sum(board)
print(f'remaining: {remaining}, last number: {number}')
print(f'score: {number*remaining}')


game = tmp_game.copy()
for number,board in itertools.product(numbers,game):
    if board.mark_number(number) and all(b.finished for b in game):
        break

remaining = sum(board)
print(f'remaining: {remaining}, last number: {number}')
print(f'score: {number*remaining}')
