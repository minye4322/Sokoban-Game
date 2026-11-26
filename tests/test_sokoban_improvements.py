from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch

from sokoban import (
    LEVELS,
    MOVE_LIMITS,
    choose_challenge_mode,
    format_level_summary,
    is_cleared,
    is_deadlocked,
    is_move_limit_reached,
    find_hint,
    load_level,
    main,
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

    def test_game_starts_at_level_one_without_level_selection(self):
        output = StringIO()
        with patch("builtins.input", side_effect=["n", "w", "", "q"]), redirect_stdout(output):
            main()
        self.assertIn("ステージ1の結果", output.getvalue())

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

    def test_challenge_mode_uses_fixed_limits_without_asking_for_count(self):
        self.assertEqual(len(MOVE_LIMITS), len(LEVELS))
        with patch("builtins.input", side_effect=["maybe", "y"]), redirect_stdout(StringIO()):
            self.assertTrue(choose_challenge_mode())
        with patch("builtins.input", return_value="n"), redirect_stdout(StringIO()):
            self.assertFalse(choose_challenge_mode())

    def test_every_level_can_be_solved_within_its_fixed_limit(self):
        for rows, move_limit in zip(LEVELS, MOVE_LIMITS):
            game = load_level(rows)
            while not is_cleared(game):
                hint = find_hint(game)
                self.assertIsNotNone(hint)
                self.assertTrue(move_player(game, hint))
                self.assertLessEqual(game["moves"], move_limit)

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
