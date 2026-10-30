#!/usr/bin/env python3
"""Tic-Tac-Toe: a terminal game for two players, or one player vs the computer.

Usage:
    python3 tic_tac_toe.py            # interactive menu
    python3 tic_tac_toe.py --pvp      # two human players
    python3 tic_tac_toe.py --cpu      # play X against the computer (O)
    python3 tic_tac_toe.py --cpu --hard   # computer plays perfectly (minimax)
"""

import argparse
import random
import sys

EMPTY = " "
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]


def winner(board):
    """Return 'X' or 'O' if that player has won, 'draw' if full, else None."""
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    if EMPTY not in board:
        return "draw"
    return None


def render(board):
    cells = [c if c != EMPTY else str(i + 1) for i, c in enumerate(board)]
    rows = [" {} | {} | {} ".format(*cells[i:i + 3]) for i in (0, 3, 6)]
    return "\n---+---+---\n".join(rows)


def _minimax(board, is_max, cpu, human):
    result = winner(board)
    if result == cpu:
        return 1
    if result == human:
        return -1
    if result == "draw":
        return 0
    best = -2 if is_max else 2
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = cpu if is_max else human
            score = _minimax(board, not is_max, cpu, human)
            board[i] = EMPTY
            best = max(best, score) if is_max else min(best, score)
    return best


def cpu_move(board, cpu="O", human="X", hard=False):
    """Pick a move for the computer. Hard mode is unbeatable (minimax)."""
    free = [i for i, c in enumerate(board) if c == EMPTY]
    if not free:
        return None
    if not hard:
        # Casual play: win if possible, block if needed, otherwise random.
        for mark in (cpu, human):
            for i in free:
                board[i] = mark
                if winner(board) == mark:
                    board[i] = EMPTY
                    return i
                board[i] = EMPTY
        if board[4] == EMPTY:
            return 4
        return random.choice(free)
    best_score, best_moves = -2, []
    for i in free:
        board[i] = cpu
        score = _minimax(board, False, cpu, human)
        board[i] = EMPTY
        if score > best_score:
            best_score, best_moves = score, [i]
        elif score == best_score:
            best_moves.append(i)
    return random.choice(best_moves)


def read_move(board, player):
    while True:
        try:
            raw = input("Player {} - enter a cell number (1-9): ".format(player)).strip()
        except EOFError:
            print()
            return None
        if not raw.isdigit() or not 1 <= int(raw) <= 9:
            print("Please enter a number from 1 to 9.")
            continue
        idx = int(raw) - 1
        if board[idx] != EMPTY:
            print("That cell is already taken.")
            continue
        return idx


def play_game(vs_cpu=False, hard=False, scores=None):
    board = [EMPTY] * 9
    turn = "X"
    print(render(board))
    while True:
        result = winner(board)
        if result:
            if result == "draw":
                print("It's a draw.")
                if scores is not None:
                    scores["draws"] += 1
            else:
                print("Player {} wins!".format(result))
                if scores is not None:
                    scores[result] += 1
            return
        if vs_cpu and turn == "O":
            idx = cpu_move(board, hard=hard)
            print("Computer plays cell {}.".format(idx + 1))
        else:
            idx = read_move(board, turn)
            if idx is None:
                print("Game abandoned.")
                return
        board[idx] = turn
        print(render(board))
        turn = "O" if turn == "X" else "X"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Terminal Tic-Tac-Toe.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--pvp", action="store_true", help="two human players")
    mode.add_argument("--cpu", action="store_true", help="play against the computer")
    parser.add_argument("--hard", action="store_true",
                        help="with --cpu: computer plays perfectly (unbeatable)")
    args = parser.parse_args(argv)

    scores = {"X": 0, "O": 0, "draws": 0}
    print("Tic-Tac-Toe. Cells are numbered 1-9 as shown on the board.")
    while True:
        vs_cpu = args.cpu
        if not args.pvp and not args.cpu:
            try:
                choice = input("Mode: [1] two players  [2] vs computer  [q] quit: ").strip().lower()
            except EOFError:
                print()
                break
            if choice == "q":
                break
            vs_cpu = choice == "2"
        play_game(vs_cpu=vs_cpu, hard=args.hard, scores=scores)
        print("Score - X: {}  O: {}  Draws: {}".format(scores["X"], scores["O"], scores["draws"]))
        try:
            again = input("Play again? [y/N]: ").strip().lower()
        except EOFError:
            print()
            break
        if again != "y":
            break
    print("Final score - X: {}  O: {}  Draws: {}".format(scores["X"], scores["O"], scores["draws"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
