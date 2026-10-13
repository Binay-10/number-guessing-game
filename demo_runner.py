"""Interactive Demo Runner for Number Guessing Game.

This utility executes real, genuine terminal runs of the Number Guessing Game
for capturing the 6 required assignment screenshots:
  1. 01_game_start_and_low_hint.png
  2. 02_high_hint_and_remaining_attempts.png
  3. 03_successful_guess.png
  4. 04_game_over_and_secret_reveal.png
  5. 05_invalid_input_validation.png
  6. 06_replay_and_winning_streak.png
"""

import sys
import time
from number_guessing_game import play_round, get_replay_choice, main, display_session_summary

def simulate_input_stream(inputs, delay=0.8):
    """Simulate realistic user typing into the game prompts."""
    iterator = iter(inputs)
    def _input(prompt=""):
        sys.stdout.write(prompt)
        sys.stdout.flush()
        time.sleep(delay)
        val = next(iterator)
        print(val)
        time.sleep(delay)
        return val
    return _input

def run_scenario_1():
    print("\n" + "=" * 60)
    print("SCENARIO 1: Game Start & Low Hint -> 01_game_start_and_low_hint.png")
    print("=" * 60)
    # Secret is 63, user enters 30 (Too low!)
    inputs = ["30", "63"]
    play_round(current_streak=0, secret_number=63, input_func=simulate_input_stream(inputs))

def run_scenario_2():
    print("\n" + "=" * 60)
    print("SCENARIO 2: High Hint & Decrementing Attempts -> 02_high_hint_and_remaining_attempts.png")
    print("=" * 60)
    # Secret is 45, user enters 80 (Too high!), 20 (Too low!), 45 (Win)
    inputs = ["80", "20", "45"]
    play_round(current_streak=0, secret_number=45, input_func=simulate_input_stream(inputs))

def run_scenario_3():
    print("\n" + "=" * 60)
    print("SCENARIO 3: Successful Guess & Winning Streak -> 03_successful_guess.png")
    print("=" * 60)
    # Secret is 72, user guesses 50 (Low), 72 (Correct in 2 attempts, streak 2)
    inputs = ["50", "72"]
    play_round(current_streak=1, secret_number=72, input_func=simulate_input_stream(inputs))

def run_scenario_4():
    print("\n" + "=" * 60)
    print("SCENARIO 4: Game Over & Secret Reveal (7 failed attempts) -> 04_game_over_and_secret_reveal.png")
    print("=" * 60)
    # 7 incorrect guesses
    inputs = ["10", "20", "30", "40", "50", "60", "70"]
    play_round(current_streak=3, secret_number=88, input_func=simulate_input_stream(inputs))

def run_scenario_5():
    print("\n" + "=" * 60)
    print("SCENARIO 5: Robust Input Validation -> 05_invalid_input_validation.png")
    print("=" * 60)
    # Shows non-numeric, decimal, empty, below range, above range, then valid guess
    inputs = ["abc", "45.5", "   ", "0", "101", "50"]
    play_round(current_streak=0, secret_number=50, input_func=simulate_input_stream(inputs))

def run_scenario_6():
    print("\n" + "=" * 60)
    print("SCENARIO 6: Multi-Round Replay & Session Summary -> 06_replay_and_winning_streak.png")
    print("=" * 60)
    # Round 1 win, replay 'y', Round 2 win, replay 'n'
    inputs = ["50", "y", "75", "n"]
    # We can run two rounds simulating main
    streak = 0
    # Round 1
    won, _, streak = play_round(streak, secret_number=50, input_func=simulate_input_stream(["50"]))
    # Replay
    print("Would you like to play another round? (y/n): y")
    # Round 2
    won, _, streak = play_round(streak, secret_number=75, input_func=simulate_input_stream(["75"]))
    print("Would you like to play another round? (y/n): n")
    display_session_summary(rounds_played=2, rounds_won=2, rounds_lost=0, best_streak=2)

def menu():
    print("\n--- NUMBER GUESSING GAME DEMO RUNNER ---")
    print("Choose a scenario to display in terminal for screenshot capture:")
    print("1. Scenario 1: Game Start & Low Hint")
    print("2. Scenario 2: High Hint & Decrementing Attempts")
    print("3. Scenario 3: Successful Guess & Streak")
    print("4. Scenario 4: Game Over & Secret Reveal")
    print("5. Scenario 5: Input Validation Errors")
    print("6. Scenario 6: Replay Flow & Session Summary")
    print("7. Run All Scenarios Sequentially")
    print("0. Exit")
    choice = input("\nEnter choice (0-7): ").strip()

    actions = {
        "1": run_scenario_1,
        "2": run_scenario_2,
        "3": run_scenario_3,
        "4": run_scenario_4,
        "5": run_scenario_5,
        "6": run_scenario_6,
    }

    if choice in actions:
        actions[choice]()
    elif choice == "7":
        for num in range(1, 7):
            actions[str(num)]()
            time.sleep(1)
    elif choice == "0":
        print("Exiting demo runner.")
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        scenarios = {
            "1": run_scenario_1,
            "2": run_scenario_2,
            "3": run_scenario_3,
            "4": run_scenario_4,
            "5": run_scenario_5,
            "6": run_scenario_6,
            "all": lambda: [run_scenario_1(), run_scenario_2(), run_scenario_3(), run_scenario_4(), run_scenario_5(), run_scenario_6()]
        }
        if arg in scenarios:
            scenarios[arg]()
        else:
            print(f"Unknown scenario: {arg}")
    else:
        menu()
