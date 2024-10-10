from strategies.strategy import Strategy
from strategies.possible_board import PossibleBoard
from board import Board
from typing import Any, Tuple, Callable, Tuple, List
from strategies.game_state import GameState

Coordinate = Tuple[int, int]
SudokuEntry = Tuple[Coordinate, int]

class EliminateSingletonsStrategy:
    def is_compatible(self, state: GameState) -> bool:
        if state is None:
            return True
        elif isinstance(state.get("possible_board"), PossibleBoard):
            return True
        return False
    
    def apply(self, board: Board, state: GameState, verbose: bool | Callable[[Board], None] = False) -> Tuple[Board, GameState]:


        if state is None:
            state = dict(possible_board=PossibleBoard.from_board(board))

        def _eliminate_singletons(board: Board) -> Board:
            nonlocal state

            possible_board = state["possible_board"]
            new_board = board.copy()
            to_add: List[SudokuEntry] = list()

            for y in range(9):
                for x in range(9):
                    if len(possible_board[y, x]) == 1:
                        val = next(iter(possible_board[y, x]))
                        to_add.append(((y, x), val))

            for (y, x), val in to_add:
                new_board[y, x] = val
                possible_board[y, x] = val
            return new_board

 
        if verbose:
            verbose(board)

        old_board = board.copy()        

        new_board = _eliminate_singletons(old_board)

        while old_board != new_board:
            old_board = new_board
            new_board = _eliminate_singletons(old_board)
            if verbose:
                verbose(new_board)
        
        return new_board, state


class SoleCandidatesStrategy:
    def is_compatible(self, state: GameState) -> bool:
        if state is None:
            return True
        elif isinstance(state.get("possible_board"), PossibleBoard):
            return True
        return False
    

    def apply(self, board: Board, state: GameState, verbose: bool | Callable[[Board], None] = False) -> Tuple[Board, GameState]:

        if state is None:
            state = dict(possible_board=PossibleBoard.from_board(board))

        def _find_sole_candidates(board: Board) -> Board:
            nonlocal state

            possible_board = state["possible_board"]
            new_board = board.copy()
            to_add: List[SudokuEntry] = list()
            
            for y in range(9):
                seen_once = dict()
                seen_more_than_once = set()
                for x in range(9):     
                    vals = possible_board[y, x]
                    seen_more_than_once.update(set(seen_once.keys()).intersection(vals))
                    for val in vals - seen_once.keys():
                        seen_once[val] = x
                
                seen_only_once = seen_once.keys() - seen_more_than_once 
                for val in seen_only_once:
                    to_add.append(((y, seen_once[val]), val)) 

            for x in range(9):
                seen_once = dict()
                seen_more_than_once = set()
                for y in range(9):     
                    vals = possible_board[y, x]
                    seen_more_than_once.update(set(seen_once.keys()).intersection(vals))
                    for val in vals - seen_once.keys():
                        seen_once[val] = y
                
                seen_only_once = seen_once.keys() - seen_more_than_once 
                for val in seen_only_once:
                    to_add.append(((seen_once[val], x), val)) 
            
            for box_y in range(3):
                for box_x in range(3):
                    seen_once = dict()
                    seen_more_than_once = set()
                    
                    for i in range(3):
                        for j in range(3):
                            y = box_y*3+i
                            x = box_x*3+j
                            vals = possible_board[y, x]
                            seen_more_than_once.update(set(seen_once.keys()).intersection(vals))
                            for val in vals - seen_once.keys():
                                seen_once[val] = (i, j)
                    
                    seen_only_once = seen_once.keys() - seen_more_than_once
                    for val in seen_only_once:
                        i, j = seen_once[val]
                        to_add.append(((box_y*3+i, box_x*3+j), val))
                    
            to_add=list(set(to_add))

            for (y, x), val in to_add:
                new_board[y, x] = val
                possible_board[y, x] = val
            
            return new_board
 
            
 
        if verbose:
            verbose(board)

        old_board = board.copy()        

        new_board = _find_sole_candidates(old_board)

        while old_board != new_board:
            old_board = new_board
            new_board = _find_sole_candidates(old_board)
            if verbose:
                verbose(new_board)
        
        return new_board, state

        
        
        