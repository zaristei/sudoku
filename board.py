import numpy as np
from dataclasses import dataclass


@dataclass
class Board: 
    cells: np.ndarray
    

    def __getitem__(self, idx):
        y, x = idx
        return self.cells[y, x]
    
    def __setitem__(self, idx, val):
        y, x = idx
        self.cells[y, x] = val
    
    def __hash__(self):
        return hash(self.__repr__())
    
    def __eq__(self, other):
        return str(self) == str(other)

    def is_filled(self, y, x) -> bool:
        return self[y, x] > 0
    
    def rows(self) -> np.ndarray:
        return self.cells

    def cols(self) -> np.ndarray:
        return self.cells.T
    
    def squares(self) -> np.ndarray:
        squares = np.zeros((9, 9), dtype=int)
        for i in range(3):
            for j in range(3):
                squares[i*3+j] = self.cells[i*3:i*3+3, j*3:j*3+3].reshape(-1)
        return squares
    
    def is_valid(self) -> bool:
        def _check_validity(arr):
            for bunch in arr:
                seen = set()
                for num in bunch:
                    if num > 0 and num in seen:
                        return False
                    else:
                        seen.add(num)
            return True
        
        return all(_check_validity(arr) for arr in [self.rows(), self.cols(), self.squares()])
    
    def is_complete(self) -> bool:
        return np.all(self.cells > 0) and self.is_valid()
    
    def copy(self):
        return Board(self.cells.copy())
    
    def __str__(self):
        return \
            f"""-------------
|{self.cells[0][0]}{self.cells[0][1]}{self.cells[0][2]}|{self.cells[0][3]}{self.cells[0][4]}{self.cells[0][5]}|{self.cells[0][6]}{self.cells[0][7]}{self.cells[0][8]}|
|{self.cells[1][0]}{self.cells[1][1]}{self.cells[1][2]}|{self.cells[1][3]}{self.cells[1][4]}{self.cells[1][5]}|{self.cells[1][6]}{self.cells[1][7]}{self.cells[1][8]}|
|{self.cells[2][0]}{self.cells[2][1]}{self.cells[2][2]}|{self.cells[2][3]}{self.cells[2][4]}{self.cells[2][5]}|{self.cells[2][6]}{self.cells[2][7]}{self.cells[2][8]}|
-------------
|{self.cells[3][0]}{self.cells[3][1]}{self.cells[3][2]}|{self.cells[3][3]}{self.cells[3][4]}{self.cells[3][5]}|{self.cells[3][6]}{self.cells[3][7]}{self.cells[3][8]}|
|{self.cells[4][0]}{self.cells[4][1]}{self.cells[4][2]}|{self.cells[4][3]}{self.cells[4][4]}{self.cells[4][5]}|{self.cells[4][6]}{self.cells[4][7]}{self.cells[4][8]}|
|{self.cells[5][0]}{self.cells[5][1]}{self.cells[5][2]}|{self.cells[5][3]}{self.cells[5][4]}{self.cells[5][5]}|{self.cells[5][6]}{self.cells[5][7]}{self.cells[5][8]}|
-------------
|{self.cells[6][0]}{self.cells[6][1]}{self.cells[6][2]}|{self.cells[6][3]}{self.cells[6][4]}{self.cells[6][5]}|{self.cells[6][6]}{self.cells[6][7]}{self.cells[6][8]}|
|{self.cells[7][0]}{self.cells[7][1]}{self.cells[7][2]}|{self.cells[7][3]}{self.cells[7][4]}{self.cells[7][5]}|{self.cells[7][6]}{self.cells[7][7]}{self.cells[7][8]}|
|{self.cells[8][0]}{self.cells[8][1]}{self.cells[8][2]}|{self.cells[8][3]}{self.cells[8][4]}{self.cells[8][5]}|{self.cells[8][6]}{self.cells[8][7]}{self.cells[8][8]}|
-------------""".replace("0", ".")