from board import Board
from dataclasses import dataclass, field
import numpy as np
from typing import List, Set

BITMAP_TRANSFORM = np.array([1,2,3,5,7,11,13,17,19,23])
OPTIONS = set(range(10))

@dataclass
class PossibleBitMap:
    possible_values: Set[int] = field(default_factory=lambda: set(range(1,10)), init=False)
    filled: bool = False
    
    @property
    def possibilities(self):
        return self.possible_values
    
    def is_filled(self):
        return self.filled

    def is_possible(self, int_val: int) -> bool:
        return int_val in self.possible_values

    def drop(self, int_val: int):
        self.possible_values.discard(int_val)
    
    def add(self, int_val: int):
        self.possible_values.add(int_val)

    @classmethod
    def from_ints(cls, ints: np.ndarray):

        unique_ints = set(ints)
        assert unique_ints.issubset(OPTIONS), f"Values must be in {OPTIONS}, got {unique_ints}"
        
        bitmap = cls()

        for i in ints:
            bitmap.drop(i)
    
    def fill(self, int_val):
        assert self.is_possible(int_val), f"Value {int_val} is not one of the possible values {self.possible_values}"
        self.possible_values = {int_val}
        self.filled = True


@dataclass
class PossibleBoard:
    possible_values: List[List[PossibleBitMap]] = field(default_factory = lambda: [[PossibleBitMap() for _ in range(9)] for _ in range(9)], init=False)

    def __getitem__(self, idx) -> Set[int]:
        y, x = idx
        return self.possible_values[y][x].possibilities

    def __setitem__(self, idx, val):
        y, x = idx

        for i in range(9):
            if i != x:
                self.possible_values[y][i].drop(val)
        for j in range(9):
            if j != y:
                self.possible_values[j][x].drop(val)

        box = (y//3, x//3)
        for i in range(3):
            for j in range(3):
                y_, x_ = box[0]*3+i, box[1]*3+j
                if y_ != y or x_ != x:
                    self.possible_values[y_][x_].drop(val)

        self.possible_values[y][x].fill(val)

    @classmethod
    def from_board(cls, board: Board):
        possible_board = cls()
        for y in range(9):
            for x in range(9):
                if board.is_filled(y, x):
                    possible_board[y, x] = board[y, x]
        return possible_board 