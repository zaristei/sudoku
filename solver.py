from strategies.strategy import Strategy, BruteForce, SmarterBruteForce, CompositeStrategy
from strategies.elimination import EliminateSingletonsStrategy, SoleCandidatesStrategy
from board import Board
from sudoku_bank.intake import parse_file
import curses
import tqdm
from io import StringIO
import time
from typing import Iterable, Callable, Any
import numpy as np

def solve(board: Board, strategies: Iterable[Strategy], verbose: bool | Callable[[Board], None] = False):
    if verbose:
        verbose(board)
    
    state: Any = None
    original_board = board.copy()
    old_board = board.copy()
    while not board.is_complete():
        old_board = board.copy()
        for strategy in strategies:
            board, state = strategy.apply(board, state, verbose)
        
        if old_board == board:
            break 
    solved = len(np.nonzero(board.cells)[0])/81
    return board, solved

def _solve_verbose(stdscr, boards, strategies):

    solved = []
    was_solved = []
    stream = StringIO()
    def _update_board(board):
        stdscr.addstr(1, 0, str(board))
        stdscr.refresh()

    for i in tqdm.tqdm(range(10000), file=stream, ascii=False):
        stdscr.addstr(0, 0, stream.getvalue())
        stdscr.refresh()
        board = Board(boards[i])
        finished_board, is_solved = solve(board, strategies, verbose=_update_board)
        solved.append(finished_board)
        was_solved.append(is_solved)
    return solved, was_solved

if __name__ == "__main__":
    boards = parse_file("sudoku_bank/sudoku-exchange-puzzle-bank/medium.txt")
    strategies = [SmarterBruteForce()]
    smarter_strategies = [CompositeStrategy([EliminateSingletonsStrategy(), SoleCandidatesStrategy()])]
    bf_start = time.time()
    #solved, was_solved = curses.wrapper(_solve_verbose, boards, strategies)
    smarter_start = time.time()
    solved, was_solved = curses.wrapper(_solve_verbose, boards, smarter_strategies)
    end = time.time()
    for i, board in enumerate(solved):
        print(f"Board {i}: {(was_solved[i]!=1)*'Not ' + 'Solved'}")
        print(board)
    print (f"Brute Force: {smarter_start-bf_start} s")
    print (f"Smarter Brute Force: {end-smarter_start} s")
    print (f"Solve rate: {sum(was_solved)/len(was_solved)*100}%")
    