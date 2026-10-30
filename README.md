# Tic-Tac-Toe

A basic Python Tic-Tac-Toe game for the terminal. Play against a friend on the
same keyboard, or against the computer.

## Features

- Two-player mode on one terminal
- Computer opponent with two difficulties:
  - Casual: takes wins, blocks losses, otherwise plays loosely
  - Hard: minimax play, provably unbeatable (verified by an exhaustive
    game-tree check)
- Running score across rounds (X wins, O wins, draws)
- No dependencies: standard library only

## Run

```sh
python3 tic_tac_toe.py            # asks which mode you want
python3 tic_tac_toe.py --pvp      # two human players
python3 tic_tac_toe.py --cpu      # you are X, computer is O
python3 tic_tac_toe.py --cpu --hard
```

Cells are numbered 1-9 as shown on the board:

```
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
```

Type the number of the cell you want, or `q` at the mode prompt to quit.

## License

MIT (see LICENSE).
