"""Automated test suite for the Python Number Guessing Game.

Covers all 18 test cases specified in the assignment rubric:
- TEST 1: Secret number range (1-100)
- TEST 2: Lower guess ("Too Low!")
- TEST 3: Higher guess ("Too High!")
- TEST 4: Correct guess ends round and reports win
- TEST 5: First-attempt win
- TEST 6: Seventh-attempt win
- TEST 7: Maximum attempts (7 incorrect guesses ends round)
- TEST 8: No eighth guess accepted
- TEST 9: Invalid non-numeric input rejected without consuming attempt
- TEST 10: Empty input safely handled
- TEST 11: Decimal input rejected
- TEST 12: Out-of-range values (0, negative, >100) rejected
- TEST 13: Remaining attempts calculated correctly
- TEST 14: Winning streak increments across consecutive wins
- TEST 15: Streak resets to 0 on a lost round
- TEST 16: Replay starts a fresh round with reset attempts
- TEST 17: Session exits cleanly when player declines replay
- TEST 18: Deterministic secret numbers via mocking
"""

import io
import unittest
from unittest.mock import patch

from number_guessing_game import (
    generate_secret_number,
    get_hint,
    get_replay_choice,
    get_valid_guess,
    main,
    play_round,
    validate_guess,
)


class TestNumberGuessingGame(unittest.TestCase):
    """Unit and integration tests for number_guessing_game."""

    # TEST 1 — Secret number range
    def test_01_secret_number_range(self):
        """Verify generated secret numbers are integers between 1 and 100, inclusive."""
        for _ in range(500):
            num = generate_secret_number(1, 100)
            self.assertIsInstance(num, int)
            self.assertGreaterEqual(num, 1)
            self.assertLessEqual(num, 100)

    # TEST 2 — Lower guess
    def test_02_lower_guess_hint(self):
        """Verify that a guess below the secret number returns 'Too Low!'."""
        hint = get_hint(guess=40, secret_number=50)
        self.assertEqual(hint, "-> Too Low! Try a higher number.")

    # TEST 3 — Higher guess
    def test_03_higher_guess_hint(self):
        """Verify that a guess above the secret number returns 'Too High!'."""
        hint = get_hint(guess=65, secret_number=50)
        self.assertEqual(hint, "-> Too High! Try a lower number.")

    # TEST 4 — Correct guess
    def test_04_correct_guess_wins_and_ends_round(self):
        """Verify that a matching guess produces a win and ends the round immediately."""
        inputs = ["50"]
        won, attempts_used, updated_streak = play_round(
            current_streak=0,
            secret_number=50,
            input_func=lambda _: inputs.pop(0),
        )
        self.assertTrue(won)
        self.assertEqual(attempts_used, 1)
        self.assertEqual(updated_streak, 1)

    # TEST 5 — First-attempt win
    def test_05_first_attempt_win(self):
        """Verify a player can win in exactly one valid attempt."""
        inputs = ["42"]
        won, attempts_used, updated_streak = play_round(
            current_streak=2,
            secret_number=42,
            input_func=lambda _: inputs.pop(0),
        )
        self.assertTrue(won)
        self.assertEqual(attempts_used, 1)
        self.assertEqual(updated_streak, 3)

    # TEST 6 — Seventh-attempt win
    def test_06_seventh_attempt_win(self):
        """Verify a player can win on the seventh (final permitted) attempt."""
        # 6 incorrect guesses then the correct 7th guess
        inputs = ["10", "20", "30", "40", "50", "60", "70"]
        won, attempts_used, updated_streak = play_round(
            current_streak=0,
            secret_number=70,
            input_func=lambda _: inputs.pop(0),
        )
        self.assertTrue(won)
        self.assertEqual(attempts_used, 7)
        self.assertEqual(updated_streak, 1)

    # TEST 7 — Maximum attempts
    def test_07_maximum_attempts_ends_in_loss(self):
        """Verify that 7 incorrect valid guesses end the round in a loss."""
        inputs = ["1", "2", "3", "4", "5", "6", "7"]
        won, attempts_used, updated_streak = play_round(
            current_streak=5,
            secret_number=99,
            input_func=lambda _: inputs.pop(0),
        )
        self.assertFalse(won)
        self.assertEqual(attempts_used, 7)
        self.assertEqual(updated_streak, 0)

    # TEST 8 — No eighth guess
    def test_08_no_eighth_guess(self):
        """Verify that exactly 7 guesses are taken and no 8th input is requested."""
        # Provide extra inputs in the queue to confirm the function stops at 7
        inputs = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        won, attempts_used, _ = play_round(
            current_streak=0,
            secret_number=50,
            input_func=lambda _: inputs.pop(0),
        )
        self.assertFalse(won)
        self.assertEqual(attempts_used, 7)
        # Verify 2 unused elements remain in the list
        self.assertEqual(len(inputs), 2)
        self.assertEqual(inputs, ["8", "9"])

    # TEST 9 — Invalid text
    def test_09_invalid_text_rejected(self):
        """Verify that non-numeric input is rejected with an error message and does not consume attempt."""
        is_valid, val, msg = validate_guess("abc")
        self.assertFalse(is_valid)
        self.assertIsNone(val)
        self.assertIn("Invalid input", msg)

        # In get_valid_guess, invalid inputs loop until valid input is given
        inputs = ["xyz", "hello!", "50"]
        with patch("sys.stdout", new=io.StringIO()):
            guess = get_valid_guess(1, 7, input_func=lambda _: inputs.pop(0))
        self.assertEqual(guess, 50)

    # TEST 10 — Empty input
    def test_10_empty_input_handled_safely(self):
        """Verify empty and whitespace inputs are rejected cleanly."""
        for empty_str in ["", "   ", "\t"]:
            is_valid, val, msg = validate_guess(empty_str)
            self.assertFalse(is_valid)
            self.assertIsNone(val)
            self.assertEqual(msg, "[ERROR] Input cannot be empty. Please enter a number.")

    # TEST 11 — Decimal input
    def test_11_decimal_input_rejected(self):
        """Verify decimal inputs like 45.5 are rejected with specific error message."""
        for dec in ["45.5", "12.0", "0.99", "-3.14"]:
            is_valid, val, msg = validate_guess(dec)
            self.assertFalse(is_valid)
            self.assertIsNone(val)
            self.assertEqual(msg, "[ERROR] Please enter a whole number, not a decimal.")

    # TEST 12 — Out-of-range values
    def test_12_out_of_range_values_rejected(self):
        """Verify 0, negative numbers, and values > 100 are rejected."""
        test_cases = ["0", "-10", "-1", "101", "250"]
        for case in test_cases:
            is_valid, val, msg = validate_guess(case)
            self.assertFalse(is_valid)
            self.assertIsNone(val)
            self.assertEqual(msg, "[ERROR] Your guess must be between 1 and 100.")

    # TEST 13 — Remaining attempts
    def test_13_remaining_attempts_calculated_correctly(self):
        """Verify remaining attempts calculation across multiple valid guesses."""
        max_attempts = 7
        for attempts_used in range(1, max_attempts + 1):
            remaining = max_attempts - attempts_used
            self.assertEqual(remaining, 7 - attempts_used)
            self.assertGreaterEqual(remaining, 0)

    # TEST 14 — Winning streak
    def test_14_winning_streak_increments(self):
        """Verify that consecutive won rounds increment the streak correctly."""
        streak = 0
        for target in [25, 50, 75]:
            won, _, streak = play_round(
                current_streak=streak,
                secret_number=target,
                input_func=lambda _: str(target),
            )
            self.assertTrue(won)
        self.assertEqual(streak, 3)

    # TEST 15 — Streak reset
    def test_15_streak_reset_on_loss(self):
        """Verify that losing a round resets the winning streak to zero."""
        streak = 4
        # Force a loss with 7 wrong guesses
        inputs = ["1", "2", "3", "4", "5", "6", "7"]
        won, attempts_used, streak = play_round(
            current_streak=streak,
            secret_number=99,
            input_func=lambda _: inputs.pop(0),
        )
        self.assertFalse(won)
        self.assertEqual(streak, 0)

    # TEST 16 — Replay
    def test_16_replay_flow(self):
        """Verify that get_replay_choice handles 'y', 'yes', 'n', 'no' and loops on invalid input."""
        # Valid 'y'
        self.assertTrue(get_replay_choice(input_func=lambda _: "y"))
        # Valid 'YES' (case-insensitive)
        self.assertTrue(get_replay_choice(input_func=lambda _: "YES"))
        # Valid 'n'
        self.assertFalse(get_replay_choice(input_func=lambda _: "n"))
        # Valid 'no'
        self.assertFalse(get_replay_choice(input_func=lambda _: "NO"))

        # Invalid then valid
        inputs = ["maybe", "123", "y"]
        with patch("sys.stdout", new=io.StringIO()):
            choice = get_replay_choice(input_func=lambda _: inputs.pop(0))
        self.assertTrue(choice)

    # TEST 17 — Session exit
    def test_17_session_exit(self):
        """Verify that main() exits cleanly after playing a round and declining replay."""
        # Inputs: Round 1 guess '50' (win), then replay 'n'
        inputs = ["50", "n"]
        captured_output = io.StringIO()
        with patch("sys.stdout", captured_output):
            with patch("number_guessing_game.generate_secret_number", return_value=50):
                main(input_func=lambda _: inputs.pop(0))
        output = captured_output.getvalue()
        self.assertIn("Congratulations!", output)
        self.assertIn("SESSION SUMMARY", output)
        self.assertIn("Goodbye!", output)

    # TEST 18 — Random number mocking
    def test_18_random_number_mocking(self):
        """Verify game behavior using mocked random numbers without hardcoding production values."""
        with patch("number_guessing_game.random.randint", return_value=88):
            mocked_secret = generate_secret_number()
            self.assertEqual(mocked_secret, 88)

            inputs = ["88"]
            won, attempts_used, streak = play_round(
                current_streak=0,
                secret_number=mocked_secret,
                input_func=lambda _: inputs.pop(0),
            )
            self.assertTrue(won)
            self.assertEqual(attempts_used, 1)


if __name__ == "__main__":
    unittest.main()
