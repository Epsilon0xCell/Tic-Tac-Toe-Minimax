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
# The board is a flat list of 9. Index 0 is the cell the player calls 1,
# and index 8 is cell 9, so every line below is written in list indexes
# and read_move() is the one place that converts a typed number.
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]


def winner(board):
    """Return 'X' or 'O' if that player has won, 'draw' if full, else None."""
    # I check the lines before I check for a full board. On the last move
    # of a game both can be true at once, and that game is a win, not a
    # draw. Swapping these two checks would quietly mis-score it.
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    if EMPTY not in board:
        return "draw"
    return None


def render(board):
    # An empty cell prints its own number. The board is the help text: a
    # player reads the number off the drawing and types that number, so
    # I do not need a separate diagram anywhere.
    cells = [c if c != EMPTY else str(i + 1) for i, c in enumerate(board)]
    rows = [" {} | {} | {} ".format(*cells[i:i + 3]) for i in (0, 3, 6)]
    return "\n---+---+---\n".join(rows)


def _minimax(board, is_max, cpu, human):
    # Scores are only win, draw, or loss for the computer: 1, 0, -1.
    # I put no depth in the score, so a win in one move and a win in
    # five moves score the same here. That is a limit I know about. It
    # cannot turn a win into a loss, it only means hard mode does not
    # always take the fastest win on the board.
    # This also changes the board it is handed and changes it back. The
    # caller gets its board in the exact state it passed in, and that
    # restore is what lets cpu_move() try a cell, read the score, and
    # still offer the same cell list to the real game.
    result = winner(board)
    if result == cpu:
        return 1
    if result == human:
        return -1
    if result == "draw":
        return 0
    # -2 and 2 sit outside the real score range on purpose. The first
    # free cell always beats the starting value, so best is never left
    # holding a sentinel that looks like a score.
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
        # The mark order is the whole tactic. I test the computer mark
        # first, so a move that wins now is taken even when the human is
        # also one move from winning. Testing human first would block a
        # win that was already there. Each test places a mark, asks
        # winner(), and clears the cell again, including on the return
        # path, so the real board never keeps a trial move.
        for mark in (cpu, human):
            for i in free:
                board[i] = mark
                if winner(board) == mark:
                    board[i] = EMPTY
                    return i
                board[i] = EMPTY
        # Center comes after the two tactical checks, not before. Taking
        # the center first would feel stronger and would still lose the
        # games where a win or a block was sitting in a corner.
        if board[4] == EMPTY:
            return 4
        return random.choice(free)
    # Hard mode keeps every move tied for best and picks one at random,
    # so two hard games do not play out the same way. Wave 3 checked the
    # full game tree behind this mode and found 0 human wins in it, so
    # picking at random among the tied best moves costs nothing there.
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
        # I require ASCII digits, not isdigit() alone. The superscript
        # two character passes isdigit() and then crashes int(), which
        # is the crash I fixed after it killed a game mid move. The or
        # chain also protects int(): it only runs when both character
        # tests have already passed, so int() never sees the bad input.
        if not raw.isascii() or not raw.isdigit() or not 1 <= int(raw) <= 9:
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
        # I test for a result at the top of the loop, after the board has
        # been printed and the turn has swapped. A win is announced on
        # the pass after the winning move lands, and the score changes
        # in this same block, so there is no second place that scores a
        # game. An abandoned game returns from read_move below and never
        # reaches this block again, which is why it changes no score.
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
        # In computer mode the human is always X and the computer is
        # always O. I gate on the turn, not on a separate flag, so the
        # computer can never move twice or take the opening move.
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
    # I reject hard with two player mode before any game starts. Hard
    # has no computer to apply to there, and letting the flag ride along
    # in silence would tell the user a harder game was coming.
    if args.hard and args.pvp:
        parser.error("--hard only applies with --cpu")

    # One scores dict lives here for the whole session and play_game()
    # only adds to it. A fresh board per game with a shared score is the
    # split I want: rounds reset, the running count does not.
    scores = {"X": 0, "O": 0, "draws": 0}
    print("Tic-Tac-Toe. Cells are numbered 1-9 as shown on the board.")
    while True:
        # vs_cpu is reset from the flags at the top of every round. When
        # the mode prompt runs it overwrites this for one game only, so a
        # choice made for round one cannot stick to round two.
        vs_cpu = args.cpu
        if not args.pvp and not args.cpu:
            # I use a flag here instead of breaking straight out because
            # the inner prompt has two ways to end without a game, typing
            # q and closing input, and both have to skip play_game() and
            # still land on the final score print below.
            quit_requested = False
            while True:
                try:
                    choice = input("Mode: [1] two players  [2] vs computer  [q] quit: ").strip().lower()
                except EOFError:
                    print()
                    quit_requested = True
                    break
                if choice == "q":
                    quit_requested = True
                    break
                if choice in ("1", "2"):
                    vs_cpu = choice == "2"
                    break
                # Anything else asks again. This prompt used to treat
                # every answer that was not 2 or q as two player mode,
                # so typing 3 started a game the user never picked.
                print("Please enter 1, 2, or q.")
            if quit_requested:
                break
        play_game(vs_cpu=vs_cpu, hard=args.hard, scores=scores)
        print("Score - X: {}  O: {}  Draws: {}".format(scores["X"], scores["O"], scores["draws"]))
        # Only a plain y plays again. Enter, n, yes, and closing input
        # all end the session. I would rather end on a stray answer than
        # start a game nobody asked for.
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
