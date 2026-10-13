"""Python Number Guessing Game.

An interactive console game demonstrating core Python fundamentals:
variables, random number generation, input validation, loops,
conditional branching, streak tracking, and automated testing.
"""

import random
import sys
from typing import Callable, Optional, Tuple

# Ensure UTF-8 support for console output on Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def safe_print(*args, **kwargs) -> None:
    """Print to console with safe fallback for legacy terminal codecs."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        out_file = kwargs.get("file", sys.stdout)
        text = sep.join(str(a) for a in args) + end
        encoding = getattr(out_file, "encoding", "ascii") or "ascii"
        clean_text = text.encode(encoding, errors="replace").decode(encoding)
        if out_file:
            out_file.write(clean_text)
            out_file.flush()


def generate_secret_number(min_val: int = 1, max_val: int = 100) -> int:
    """Generate a random secret integer between min_val and max_val, inclusive."""
    return random.randint(min_val, max_val)


def validate_guess(
    raw_input: str, min_val: int = 1, max_val: int = 100
) -> Tuple[bool, Optional[int], Optional[str]]:
    """Validate player's raw string input for the guessing game.

    Handles:
    - Case A: Non-numeric input
    - Case B: Empty input
    - Case C: Decimal input
    - Case D, E, F: Below range, above range, negative input

    Returns:
        Tuple of (is_valid, parsed_integer_or_None, error_message_or_None)
    """
    text = raw_input.strip()

    # Case B: Empty input
    if not text:
        return False, None, "[ERROR] Input cannot be empty. Please enter a number."

    # Case C: Decimal input check
    if "." in text:
        try:
            float(text)
            return False, None, "[ERROR] Please enter a whole number, not a decimal."
        except ValueError:
            pass

    # Case A: Non-numeric input check
    try:
        val = int(text)
    except ValueError:
        return (
            False,
            None,
            f"[ERROR] Invalid input! Please enter a whole number between {min_val} and {max_val}.",
        )

    # Cases D, E, F: Range boundaries (below min, above max, negative)
    if val < min_val or val > max_val:
        return False, None, f"[ERROR] Your guess must be between {min_val} and {max_val}."

    return True, val, None


def get_hint(guess: int, secret_number: int) -> str:
    """Return the directional hint based on comparison between guess and secret."""
    if guess < secret_number:
        return "-> Too Low! Try a higher number."
    elif guess > secret_number:
        return "-> Too High! Try a lower number."
    return ""


def get_valid_guess(
    attempt_num: int,
    max_attempts: int,
    input_func: Optional[Callable[[str], str]] = None,
) -> int:
    """Prompt the user repeatedly until a valid guess is provided.

    Invalid inputs do not consume an attempt.
    """
    read_input = input_func if input_func is not None else input

    while True:
        raw_text = read_input(f"[Attempt {attempt_num}/{max_attempts}] Enter your guess: ")
        is_valid, guess, error_msg = validate_guess(raw_text)
        if is_valid and guess is not None:
            return guess
        safe_print(f"\n{error_msg}\n")


def play_round(
    current_streak: int,
    max_attempts: int = 7,
    secret_number: Optional[int] = None,
    input_func: Optional[Callable[[str], str]] = None,
) -> Tuple[bool, int, int]:
    """Execute a single round of the Number Guessing Game.

    Args:
        current_streak: Current consecutive win streak entering this round.
        max_attempts: Maximum permitted valid guesses (default: 7).
        secret_number: Pre-determined secret number (used for testing).
                       If None, a random number between 1 and 100 is generated.
        input_func: Callable for reading user input (defaults to built-in input).

    Returns:
        Tuple of (won: bool, attempts_used: int, updated_streak: int)
    """
    if secret_number is None:
        secret_number = generate_secret_number(1, 100)

    safe_print("\n=== PYTHON NUMBER GUESSING GAME ===")
    safe_print("I have selected a secret number between 1 and 100.")
    safe_print(f"You have {max_attempts} attempts to guess it!\n")

    attempts_used = 0

    while attempts_used < max_attempts:
        current_attempt_number = attempts_used + 1
        guess = get_valid_guess(
            current_attempt_number, max_attempts, input_func=input_func
        )
        attempts_used += 1
        remaining_attempts = max_attempts - attempts_used

        if guess == secret_number:
            # Player wins the round
            updated_streak = current_streak + 1
            attempt_word = "attempt" if attempts_used == 1 else "attempts"
            safe_print(
                f"\n🎉 Congratulations! You guessed the secret number {secret_number} "
                f"in {attempts_used} {attempt_word}!\n"
            )
            safe_print(f"Attempts used: {attempts_used}/{max_attempts}")
            safe_print(f"Attempts remaining: {remaining_attempts}")
            safe_print(f"Current winning streak: {updated_streak}\n")
            return True, attempts_used, updated_streak
        else:
            hint = get_hint(guess, secret_number)
            safe_print(f"\n{hint}")
            safe_print(f"Attempts remaining: {remaining_attempts}\n")

    # If all attempts exhausted without guessing correctly
    safe_print("GAME OVER!")
    safe_print(f"You've used all {max_attempts} attempts.")
    safe_print(f"The secret number was {secret_number}.\n")
    safe_print(f"Attempts used: {max_attempts}/{max_attempts}")
    safe_print("Attempts remaining: 0")
    safe_print("Current winning streak: 0\n")
    return False, attempts_used, 0


def get_replay_choice(input_func: Optional[Callable[[str], str]] = None) -> bool:
    """Prompt the player to decide whether to play another round.

    Validates that the input is 'y', 'yes', 'n', or 'no'.
    Re-prompts cleanly if an invalid choice is entered.
    """
    read_input = input_func if input_func is not None else input

    while True:
        choice = read_input("Would you like to play another round? (y/n): ").strip().lower()
        if choice in ("y", "yes"):
            return True
        elif choice in ("n", "no"):
            return False
        safe_print("\n[ERROR] Please enter 'y' for yes or 'n' for no.\n")


def display_session_summary(
    rounds_played: int, rounds_won: int, rounds_lost: int, best_streak: int
) -> None:
    """Display overall game statistics for the session."""
    win_rate = (rounds_won / rounds_played * 100) if rounds_played > 0 else 0.0
    safe_print("\n================ SESSION SUMMARY ================")
    safe_print(f"Total rounds played: {rounds_played}")
    safe_print(f"Total rounds won:    {rounds_won}")
    safe_print(f"Total rounds lost:   {rounds_lost}")
    safe_print(f"Overall win rate:    {win_rate:.1f}%")
    safe_print(f"Best winning streak: {best_streak}")
    safe_print("=================================================")
    safe_print("Thank you for playing the Python Number Guessing Game. Goodbye!\n")


def main(input_func: Optional[Callable[[str], str]] = None) -> None:
    """Main application loop controlling continuous play and session tracking."""
    winning_streak = 0
    best_streak = 0
    rounds_played = 0
    rounds_won = 0
    rounds_lost = 0

    while True:
        won, attempts_used, winning_streak = play_round(
            winning_streak, input_func=input_func
        )
        rounds_played += 1
        if won:
            rounds_won += 1
            if winning_streak > best_streak:
                best_streak = winning_streak
        else:
            rounds_lost += 1

        if not get_replay_choice(input_func=input_func):
            break

    display_session_summary(rounds_played, rounds_won, rounds_lost, best_streak)


if __name__ == "__main__":
    main()
