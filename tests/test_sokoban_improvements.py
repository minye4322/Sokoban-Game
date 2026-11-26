from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch

from sokoban import (
    LEVELS,
    choose_start_level,
    choose_move_limit,
    format_level_summary,
    is_cleared,
    is_deadlocked,
    is_move_limit_reached,
    find_hint,
    load_level,
    move_player,
    undo,
)
from sokoban_exercise import apply_move, completed, new_board


class SokobanImprovementTests(unittest.TestCase):
    def test_four_levels_are_loaded(self):
        self.assertEqual(len(LEVELS), 4)
        for level in LEVELS:
            load_level(level)

    def test_fourth_level_can_be_completed(self):
        game = load_level(LEVELS[3])
        for key in "awawwdddssdww":
            self.assertTrue(move_player(game, key), key)
        self.assertTrue(is_cleared(game))

    def test_start_level_selection_accepts_level_number(self):
        with patch("builtins.input", side_effect=["5", "3"]), redirect_stdout(StringIO()):
            self.assertEqual(choose_start_level(), 2)

    def test_start_level_selection_can_quit(self):
        with patch("builtins.input", return_value="q"), redirect_stdout(StringIO()):
            self.assertIsNone(choose_start_level())

    def test_completion_summary_includes_level_moves_and_pushes(self):
        game = load_level(LEVELS[0])
        game["moves"] = 12
        game["pushes"] = 3
        self.assertEqual(
            format_level_summary(2, game),
            "ステージ2の結果: 移動回数 12回 / 押した回数 3回",
        )

    def test_move_limit_is_optional_and_stops_at_limit(self):
        game = load_level(LEVELS[0])
        self.assertFalse(is_move_limit_reached(game, None))
        self.assertFalse(is_move_limit_reached(game, 2))
        game["moves"] = 2
        self.assertTrue(is_move_limit_reached(game, 2))

    def test_move_limit_selection_validates_choice_and_limit(self):
        with patch("builtins.input", side_effect=["maybe", "y", "0", "7"]), redirect_stdout(StringIO()):
            self.assertEqual(choose_move_limit(), 7)
        with patch("builtins.input", return_value="n"), redirect_stdout(StringIO()):
            self.assertIsNone(choose_move_limit())

    def test_hint_finds_shortest_first_move_without_changing_game(self):
        game = load_level(LEVELS[0])
        original_player = game["player"]
        original_boxes = game["boxes"].copy()
        self.assertEqual(find_hint(game), "w")
        self.assertEqual(game["player"], original_player)
        self.assertEqual(game["boxes"], original_boxes)
        self.assertEqual(game["moves"], 0)

    def test_hint_reports_no_route_for_stuck_box(self):
        game = load_level([
            "#####",
            "#$  #",
            "##@.#",
            "#####",
        ])
        self.assertIsNone(find_hint(game))

    def test_push_count_and_undo_restore_boxes(self):
        game = load_level([
            "#####",
            "# . #",
            "# $ #",
            "#  @#",
            "#####",
        ])
        self.assertTrue(move_player(game, "w"))
        self.assertEqual(game["moves"], 1)
        self.assertEqual(game["pushes"], 0)

        game = load_level([
            "#####",
            "#   #",
            "# $ #",
            "# @ #",
            "# . #",
            "#####",
        ])
        self.assertTrue(move_player(game, "w"))
        self.assertEqual(game["pushes"], 1)
        undo(game)
        self.assertEqual(game["pushes"], 0)

    def test_corner_deadlock_detection(self):
        game = load_level([
            "#####",
            "#   #",
            "# $ #",
            "# @ #",
            "# . #",
            "#####",
        ])
        box = (1, 1)
        game["boxes"] = {box}
        self.assertTrue(is_deadlocked(game, box))
        game["boxes"] = {(2, 2)}
        self.assertFalse(is_deadlocked(game, (2, 2)))

    def test_exercise_push_and_wall_rules(self):
        board = new_board("#####\n# . #\n# $ #\n# @ #\n#####")
        self.assertTrue(apply_move(board, "w"))
        self.assertTrue(completed(board))


if __name__ == "__main__":
    unittest.main()
