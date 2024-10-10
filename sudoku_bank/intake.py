import numpy as np

def parse_file(path: str) -> list[np.ndarray]:
    with open(path) as f:
        boards = []
        for line in f:
            boards.append(np.array([int(val) for val in line.split(' ')[1]]).reshape(9, 9))
            
        return boards