from typing import Protocol, Callable, Any, Tuple
from board import Board
from strategies.game_state import GameState

class Strategy(Protocol):
    def is_compatible(self, state: GameState) -> bool:
        pass

    def apply(self, board: Board, state: GameState, verbose: bool | Callable[[Board], None] = False) -> Tuple[Board, GameState]:
        pass


class BruteForce:
    def is_compatible(self, state: GameState) -> bool:
        return True

    def apply(self, board: Board, state: GameState, verbose: bool | Callable[[Board], None] = False) -> Tuple[Board, GameState]:

        def _determine_if_valid_solution(board: Board) -> Board | bool:
            if verbose:
                verbose(board)

            if not board.is_valid():
                return False
            
            board_to_solve = board.copy()
            for y, row in enumerate(board_to_solve.rows()):
                for x, num in enumerate(row):
                    if num == 0:
                        for i in range(1,10):
                            board_to_solve[y, x] = i

                            result = _determine_if_valid_solution(board_to_solve)
                            if result:
                                return result
                        return False # No valid candidates

            assert board.is_complete(), "This should never happen"
            return board
                                
        return _determine_if_valid_solution(board), state


class SmarterBruteForce:
    def is_compatible(self, state: GameState) -> bool:
        return True

    def apply(self, board: Board, state: Any, verbose: bool | Callable[[Board], None] = False) -> Tuple[Board, GameState]:
        def _determine_if_valid_solution(board: Board, start_y: int=0, start_x: int=0) -> Board | bool:
            if verbose:
                verbose(board)

            if not board.is_valid():
                return False
            
            board_to_solve = board.copy()
            rows = board_to_solve.rows()
            left_for_rows = [set(range(1, 10)) - set(row) for row in board_to_solve.rows()]
            left_for_cols = [set(range(1, 10)) - set(col) for col in board_to_solve.cols()]
            left_for_squares = [set(range(1, 10)) - set(square) for square in board_to_solve.squares()]
            for y in range(start_y, 9):
                row = rows[y]
                for x in range(start_x, 9):
                    num = row[x]
                    if num == 0:
                        left_for_pos = left_for_rows[y] & left_for_cols[x] & left_for_squares[y//3*3+x//3]
                        for _, i in enumerate(left_for_pos):
                            board_to_solve[y, x] = i
                            
                            result = _determine_if_valid_solution(board_to_solve, y, x)
                            if result:
                                return result
                        return False # No valid candidates
                start_x = 0

            assert board.is_complete(), "This should never happen:\n" + str(board)
            return board
                                
        return _determine_if_valid_solution(board), state

class CompositeStrategy:
    def __init__(self, strategies: Tuple[Strategy]):
        self.strategies = strategies

    def is_compatible(self, state: GameState) -> bool:
        return all(strategy.is_compatible(state) for strategy in self.strategies)

    def apply(self, board: Board, state: GameState, verbose: bool | Callable[[Board], None] = False) -> Tuple[Board, GameState]:
        old_board = board.copy()
        new_board = board.copy() 
        for strategy in self.strategies:
            new_board, state = strategy.apply(new_board, state, verbose)
        
        while old_board != new_board:
            old_board = new_board.copy()
            for strategy in self.strategies:
                new_board, state = strategy.apply(new_board, state, verbose)
        
        return new_board, state