import unittest

from sokoban import LEVELS, is_cleared, is_deadlocked, load_level, move_player, undo
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
