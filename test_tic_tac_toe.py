"""Tests for tic_tac_toe.py. Run with: python3 -m unittest"""

import io
import itertools
import unittest
from contextlib import redirect_stdout
from unittest import mock

import tic_tac_toe as ttt

EMPTY = ttt.EMPTY


def board_with(x_cells=(), o_cells=()):
    board = [EMPTY] * 9
    for i in x_cells:
        board[i] = "X"
    for i in o_cells:
        board[i] = "O"
    return board


class WinnerTests(unittest.TestCase):
    def test_every_line_wins_for_both_marks(self):
        for line in ttt.WIN_LINES:
            for mark in ("X", "O"):
                board = [EMPTY] * 9
                for i in line:
                    board[i] = mark
                self.assertEqual(ttt.winner(board), mark, (line, mark))

    def test_full_board_without_a_line_is_a_draw(self):
        board = ["X", "O", "X",
                 "X", "O", "O",
                 "O", "X", "X"]
        self.assertEqual(ttt.winner(board), "draw")

    def test_win_on_the_last_move_beats_the_draw(self):
        # Full board, and the final move completed the top row: the win
        # is checked before the full-board draw on purpose.
        board = ["X", "X", "X",
                 "O", "O", "X",
                 "X", "O", "O"]
        self.assertEqual(ttt.winner(board), "X")

    def test_unfinished_board_has_no_result(self):
        self.assertIsNone(ttt.winner(board_with(x_cells=(0,), o_cells=(4,))))
        self.assertIsNone(ttt.winner([EMPTY] * 9))


class RenderTests(unittest.TestCase):
    def test_empty_cells_render_as_their_numbers(self):
        out = ttt.render([EMPTY] * 9)
        for n in "123456789":
            self.assertIn(n, out)

    def test_marks_replace_their_numbers(self):
        out = ttt.render(board_with(x_cells=(4,)))
        self.assertIn(" X ", out)
        self.assertNotIn(" 5 ", out)


class CasualCpuTests(unittest.TestCase):
    def test_takes_the_win_before_blocking(self):
        # O can win on the top row; X is also one from winning below.
        board = board_with(x_cells=(3, 4), o_cells=(0, 1))
        self.assertEqual(ttt.cpu_move(board), 2)

    def test_blocks_the_human_win(self):
        board = board_with(x_cells=(0, 1), o_cells=(4,))
        self.assertEqual(ttt.cpu_move(board), 2)

    def test_prefers_the_center_when_nothing_is_at_stake(self):
        self.assertEqual(ttt.cpu_move(board_with(x_cells=(0,))), 4)

    def test_only_ever_picks_a_free_cell(self):
        board = board_with(x_cells=(0, 2, 5, 7), o_cells=(1, 3, 6))
        move = ttt.cpu_move(board)
        self.assertIn(move, (4, 8))
        self.assertEqual(ttt.cpu_move(board_with(
            x_cells=(0, 1, 2, 3, 4, 5, 6, 7), o_cells=())), 8)

    def test_full_board_returns_none(self):
        board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
        self.assertIsNone(ttt.cpu_move(board))

    def test_board_is_not_modified(self):
        board = board_with(x_cells=(0, 1), o_cells=(4,))
        snapshot = list(board)
        ttt.cpu_move(board)
        ttt.cpu_move(board, hard=True)
        self.assertEqual(board, snapshot)


class HardCpuTests(unittest.TestCase):
    def test_takes_the_win(self):
        board = board_with(x_cells=(3, 4), o_cells=(0, 1))
        self.assertEqual(ttt.cpu_move(board, hard=True), 2)

    def test_blocks_the_only_saving_move(self):
        board = board_with(x_cells=(0, 1), o_cells=(4,))
        self.assertEqual(ttt.cpu_move(board, hard=True), 2)

    def _human_never_wins(self, cpu_mark):
        # Walk the whole game tree: the human tries every free cell at
        # every turn, the computer answers with its hard-mode move. A
        # single human win anywhere fails the test.
        human = "X" if cpu_mark == "O" else "O"

        def walk(board, turn):
            result = ttt.winner(board)
            if result is not None:
                self.assertNotEqual(result, human, board)
                return
            if turn == human:
                for i in range(9):
                    if board[i] == EMPTY:
                        board[i] = human
                        walk(board, cpu_mark)
                        board[i] = EMPTY
            else:
                move = ttt.cpu_move(board, cpu=cpu_mark, human=human, hard=True)
                board[move] = cpu_mark
                walk(board, human)
                board[move] = EMPTY

        walk([EMPTY] * 9, "X")

    def test_human_never_wins_against_hard_cpu_as_o(self):
        self._human_never_wins("O")

    def test_human_never_wins_against_hard_cpu_as_x(self):
        self._human_never_wins("X")


class ReadMoveTests(unittest.TestCase):
    def run_read_move(self, answers, board=None):
        board = board if board is not None else [EMPTY] * 9
        out = io.StringIO()
        with mock.patch("builtins.input", side_effect=answers):
            with redirect_stdout(out):
                result = ttt.read_move(board, "X")
        return result, out.getvalue()

    def test_accepts_a_cell_number_and_converts_to_an_index(self):
        result, _ = self.run_read_move(["5"])
        self.assertEqual(result, 4)

    def test_rejects_out_of_range_and_non_digits_then_retries(self):
        result, out = self.run_read_move(["0", "10", "abc", "3"])
        self.assertEqual(result, 2)
        self.assertEqual(out.count("Please enter a number from 1 to 9."), 3)

    def test_superscript_two_is_rejected_not_a_crash(self):
        # The character passes str.isdigit() but int() rejects it; the
        # ASCII check is what keeps this from killing the game.
        result, out = self.run_read_move(["\u00b2", "1"])
        self.assertEqual(result, 0)
        self.assertIn("Please enter a number from 1 to 9.", out)

    def test_taken_cell_is_rejected_then_retries(self):
        board = board_with(x_cells=(0,))
        result, out = self.run_read_move(["1", "2"], board=board)
        self.assertEqual(result, 1)
        self.assertIn("That cell is already taken.", out)

    def test_eof_abandons(self):
        result, _ = self.run_read_move([EOFError()])
        self.assertIsNone(result)

    def test_ctrl_c_abandons_like_eof(self):
        result, _ = self.run_read_move([KeyboardInterrupt()])
        self.assertIsNone(result)


class PlayGameTests(unittest.TestCase):
    def run_game(self, answers, **kwargs):
        scores = {"X": 0, "O": 0, "draws": 0}
        out = io.StringIO()
        with mock.patch("builtins.input", side_effect=answers):
            with redirect_stdout(out):
                ttt.play_game(scores=scores, **kwargs)
        return scores, out.getvalue()

    def test_scripted_pvp_win_scores_once(self):
        scores, out = self.run_game(["1", "4", "2", "5", "3"])
        self.assertIn("Player X wins!", out)
        self.assertEqual(scores, {"X": 1, "O": 0, "draws": 0})

    def test_abandoned_game_changes_no_score(self):
        scores, out = self.run_game(["1", EOFError()])
        self.assertIn("Game abandoned.", out)
        self.assertEqual(scores, {"X": 0, "O": 0, "draws": 0})

    def test_cpu_game_runs_to_a_result(self):
        # Feed moves until the game ends; extra answers are harmless
        # because input is only read on human turns.
        answers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"] * 2
        scores, out = self.run_game(answers, vs_cpu=True)
        total = scores["X"] + scores["O"] + scores["draws"]
        self.assertEqual(total, 1)


class MainTests(unittest.TestCase):
    def run_main(self, answers, argv=()):
        out = io.StringIO()
        with mock.patch("builtins.input", side_effect=answers):
            with redirect_stdout(out):
                code = ttt.main(list(argv))
        return code, out.getvalue()

    def test_mode_prompt_rejects_a_bad_choice_then_quits(self):
        code, out = self.run_main(["3", "q"])
        self.assertEqual(code, 0)
        self.assertIn("Please enter 1, 2, or q.", out)
        self.assertIn("Final score - X: 0  O: 0  Draws: 0", out)

    def test_eof_at_mode_prompt_ends_the_session(self):
        code, out = self.run_main([EOFError()])
        self.assertEqual(code, 0)
        self.assertIn("Final score", out)

    def test_ctrl_c_at_mode_prompt_ends_the_session(self):
        code, out = self.run_main([KeyboardInterrupt()])
        self.assertEqual(code, 0)
        self.assertIn("Final score", out)

    def test_full_session_from_the_menu(self):
        code, out = self.run_main(["1", "1", "4", "2", "5", "3", "n"])
        self.assertEqual(code, 0)
        self.assertIn("Player X wins!", out)
        self.assertIn("Final score - X: 1  O: 0  Draws: 0", out)

    def test_ctrl_c_at_play_again_ends_the_session(self):
        code, out = self.run_main(["1", "4", "2", "5", "3", KeyboardInterrupt()],
                                  argv=["--pvp"])
        self.assertEqual(code, 0)
        self.assertIn("Final score - X: 1", out)


class CliTests(unittest.TestCase):
    def test_hard_with_pvp_is_an_argparse_error(self):
        with mock.patch("sys.stderr", new=io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:
                ttt.main(["--hard", "--pvp"])
        self.assertEqual(ctx.exception.code, 2)

    def test_help_exits_zero(self):
        with mock.patch("sys.stdout", new=io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:
                ttt.main(["--help"])
        self.assertEqual(ctx.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
