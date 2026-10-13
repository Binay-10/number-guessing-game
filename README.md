# Python Number Guessing Game

An interactive, beginner-friendly console application built in Python where players guess a secret number between 1 and 100 within a strict 7-attempt limit, featuring smart directional hints, robust input validation, and session-wide winning streak tracking.

---

## 1. Project Title
**Python Number Guessing Game (Console Edition)**

---

## 2. Project Overview
The Python Number Guessing Game is a terminal-based game engineered to demonstrate fundamental computer science and Python programming principles. The computer selects a pseudo-random integer between 1 and 100 at the beginning of each round. The player is given up to seven attempts to guess the number. After each guess, the game evaluates the input, provides immediate directional hints ("Too Low!" or "Too High!"), reports remaining attempts, tracks consecutive winning streaks across rounds, and displays an end-of-session summary.

---

## 3. Problem Statement
Beginner programmers frequently struggle to integrate input validation, flow control loops, and state management cleanly. This project solves that challenge by providing an architecture that:
- Prevents game crashes from invalid or malicious console inputs.
- Enforces strict game boundary constraints (e.g., exactly seven valid guesses, no penalty for erroneous input).
- Maintains session statistics cleanly without using unnecessary global variables or overcomplicated object-oriented patterns.

---

## 4. Project Objectives
- Implement reliable random number generation within an inclusive range (`[1, 100]`).
- Design an input validation engine that catches non-numeric text, decimals, empty strings, and out-of-range integers without consuming attempts.
- Enforce a 7-attempt maximum game loop with accurate attempt and remaining-attempt counters.
- Provide a responsive conditional feedback/hint system.
- Track winning streaks and session metrics across multiple replay rounds.
- Deliver automated test coverage using Python's standard `unittest` framework.

---

## 5. Features
- **Deterministic Attempt Budget**: Exactly 7 valid guesses allowed per round.
- **Dynamic Hints**: Directional guidance (`-> Too Low! Try a higher number.` or `-> Too High! Try a lower number.`).
- **Zero-Penalty Validation**: Entering decimals, words, empty lines, or out-of-bounds numbers displays friendly error prompts without decrementing attempts.
- **Winning Streak Tracking**: Tracks consecutive round wins within an active game session; resets to 0 upon loss.
- **Session Analytics**: Tracks total rounds played, won, lost, overall win rate percentage, and highest streak achieved.
- **Replay Loop**: Seamless round transitions without restarting the Python interpreter.
- **Automated Test Suite**: 18 unit tests covering game logic, edge cases, input validation, and mocking.

---

## 6. Rules of the Game
1. The game selects a secret integer from 1 to 100 inclusive at the start of each round.
2. The player enters guesses into the terminal prompt.
3. Each valid number between 1 and 100 consumes one attempt.
4. If the guess is lower than the secret number, the game hints "Too Low!".
5. If the guess is higher than the secret number, the game hints "Too High!".
6. If the guess matches the secret number, the player wins immediately.
7. If seven valid guesses are exhausted without a match, the round ends in a loss, the secret number is revealed, and the streak resets.
8. Players can choose to play another round or exit with full session statistics.

---

## 7. Attempt-Limit Explanation
Why 7 attempts? Mathematically, the range from 1 to 100 contains 100 possible integers. Using binary search principles:
$$\lceil \log_2(100) \rceil = \lceil 6.64 \rceil = 7$$
With an optimal binary search strategy (guessing the midpoint each time), a player is guaranteed to be able to find any number between 1 and 100 in 7 attempts or fewer. This makes 7 attempts fair, challenging, and mathematically sound.

---

## 8. Hint System
The comparison engine performs clean three-way conditional branching:
- **`guess < secret_number`**: Outputs `-> Too Low! Try a higher number.` followed by remaining attempts.
- **`guess > secret_number`**: Outputs `-> Too High! Try a lower number.` followed by remaining attempts.
- **`guess == secret_number`**: Outputs a victory celebration and suppresses any directional hints.

---

## 9. Winning Streak and Scoring
The application maintains two levels of score tracking:
1. **Per-Round Metrics**:
   - Attempts used (e.g., `3/7`)
   - Attempts remaining (e.g., `4`)
2. **Session Metrics**:
   - Current Winning Streak: Increments by 1 on every won round; resets to 0 on a loss.
   - Best Winning Streak: Preserves the highest streak achieved during the session.
   - Total Rounds Played, Won, and Lost.
   - Win Rate Percentage: $\frac{\text{Rounds Won}}{\text{Rounds Played}} \times 100\%$.

---

## 10. Technology Stack
- **Language**: Python 3.10+ (Tested on Python 3.13)
- **Standard Library Modules**: `random`, `unittest`, `unittest.mock`, `typing`, `io`, `sys`
- **External Dependencies**: None (100% pure standard library)

---

## 11. Python Concepts Demonstrated
1. **Variables & Data Types**: Strings, integers, booleans, tuples, and lists.
2. **Random Module**: Utilizing `random.randint(1, 100)` for secret number generation.
3. **Console Input/Output**: Using `input()` for prompts and formatted `f-strings` for dynamic text.
4. **Type Parsing & Casting**: Parsing strings to integers using `int()` and inspecting with `float()`.
5. **Control Flow (Loops)**: Using `while` loops for repeated guessing and replay mechanisms.
6. **Conditional Branching**: Structured `if`, `elif`, and `else` blocks for hint determination.
7. **Exception Handling**: Catching `ValueError` cleanly to eliminate unexpected program crashes.
8. **Modular Function Design**: Single-responsibility functions (`generate_secret_number`, `validate_guess`, `get_hint`, `play_round`, etc.).
9. **Unit Testing & Mocking**: Writing robust test fixtures and using `unittest.mock.patch` for input simulation and deterministic RNG testing.

---

## 12. Project Structure
```text
number-guessing-game/
│
├── number_guessing_game.py          # Main executable game application
├── README.md                        # Complete project documentation
├── .gitignore                       # Git exclusion rules for clean repository
│
├── tests/
│   └── test_number_guessing_game.py # 18 automated unit and integration tests
│
└── screenshots/                     # Verified execution evidence
    ├── 01_game_start_and_low_hint.png
    ├── 02_high_hint_and_remaining_attempts.png
    ├── 03_successful_guess.png
    ├── 04_game_over_and_secret_reveal.png
    ├── 05_invalid_input_validation.png
    └── 06_replay_and_winning_streak.png
```

---

## 13. Prerequisites
- Operating System: Windows 10/11, macOS, or Linux.
- Python: Version 3.10 or higher.
  Check your Python installation:
  ```bash
  python --version
  ```

---

## 14. Installation and Setup
1. Clone or download the repository to your local machine:
   ```bash
   git clone https://github.com/<your-username>/number-guessing-game.git
   cd number-guessing-game
   ```
2. No virtual environment or third-party package installation (`pip install`) is required, as the project uses only the Python standard library.

---

## 15. How to Run the Game
Execute the game using standard Python:
```bash
python number_guessing_game.py
```

On Windows, you can also use the Python Launcher:
```bash
py number_guessing_game.py
```

---

## 16. Sample Gameplay
```text
=== PYTHON NUMBER GUESSING GAME ===
I have selected a secret number between 1 and 100.
You have 7 attempts to guess it!

[Attempt 1/7] Enter your guess: 50

-> Too Low! Try a higher number.
Attempts remaining: 6

[Attempt 2/7] Enter your guess: 75

-> Too High! Try a lower number.
Attempts remaining: 5

[Attempt 3/7] Enter your guess: 63

🎉 Congratulations! You guessed the secret number 63 in 3 attempts!

Attempts used: 3/7
Attempts remaining: 4
Current winning streak: 1

Would you like to play another round? (y/n): n

================ SESSION SUMMARY ================
Total rounds played: 1
Total rounds won:    1
Total rounds lost:   0
Overall win rate:    100.0%
Best winning streak: 1
=================================================
Thank you for playing the Python Number Guessing Game. Goodbye!
```

---

## 17. Input Validation and Error Handling
The game incorporates bulletproof input validation to guarantee seamless UX:

| Input Scenario | Sample Input | Game Response | Attempt Consumed? |
| :--- | :--- | :--- | :---: |
| **Empty string / spaces** | ` ` | `[ERROR] Input cannot be empty. Please enter a number.` | No |
| **Decimal / Floating point** | `45.5` | `[ERROR] Please enter a whole number, not a decimal.` | No |
| **Non-numeric text** | `apple` | `[ERROR] Invalid input! Please enter a whole number between 1 and 100.` | No |
| **Below minimum range** | `0` or `-15` | `[ERROR] Your guess must be between 1 and 100.` | No |
| **Above maximum range** | `101` | `[ERROR] Your guess must be between 1 and 100.` | No |
| **Valid integer** | `42` | Generates hint or winning message | **Yes** |

---

## 18. Testing Instructions
Run the automated test suite with standard `unittest` discovery:
```bash
python -m unittest discover -s tests -v
```

Or target the test module directly:
```bash
python tests/test_number_guessing_game.py
```

---

## 19. Sample Test Cases
The test suite implements 18 comprehensive test scenarios:
- **TEST 1**: `test_01_secret_number_range` — Validates random numbers strictly stay between 1 and 100 across 500 iterations.
- **TEST 2**: `test_02_lower_guess_hint` — Confirms guess < secret yields "Too Low!".
- **TEST 3**: `test_03_higher_guess_hint` — Confirms guess > secret yields "Too High!".
- **TEST 4**: `test_04_correct_guess_wins_and_ends_round` — Confirms exact guess concludes round with victory.
- **TEST 5**: `test_05_first_attempt_win` — Confirms single-guess victory handling and streak increment.
- **TEST 6**: `test_06_seventh_attempt_win` — Confirms win on the 7th attempt.
- **TEST 7**: `test_07_maximum_attempts_ends_in_loss` — Confirms 7 wrong guesses trigger Game Over.
- **TEST 8**: `test_08_no_eighth_guess` — Ensures no 8th prompt is offered once 7 attempts expire.
- **TEST 9**: `test_09_invalid_text_rejected` — Ensures letters/symbols do not decrement attempt count.
- **TEST 10**: `test_10_empty_input_handled_safely` — Ensures empty/whitespace lines prompt user again safely.
- **TEST 11**: `test_11_decimal_input_rejected` — Ensures float inputs are rejected with decimal notice.
- **TEST 12**: `test_12_out_of_range_values_rejected` — Ensures `< 1` and `> 100` are blocked.
- **TEST 13**: `test_13_remaining_attempts_calculated_correctly` — Validates attempt arithmetic.
- **TEST 14**: `test_14_winning_streak_increments` — Verifies streak increments across consecutive rounds.
- **TEST 15**: `test_15_streak_reset_on_loss` — Verifies streak resets to 0 on defeat.
- **TEST 16**: `test_16_replay_flow` — Verifies replay prompt accepts `y`/`yes`/`n`/`no` and reprompts on bad inputs.
- **TEST 17**: `test_17_session_exit` — Verifies clean program exit and summary display.
- **TEST 18**: `test_18_random_number_mocking` — Uses `unittest.mock.patch` for deterministic testing without hardcoding.

---

## 20. Screenshots Section
The `screenshots/` directory contains visual execution evidence:
- **`01_game_start_and_low_hint.png`**: Game introduction, attempt counter, and "Too Low!" hint.
- **`02_high_hint_and_remaining_attempts.png`**: "Too High!" hint with decremented remaining attempts.
- **`03_successful_guess.png`**: Winning screen with singular/plural attempt grammar and streak update.
- **`04_game_over_and_secret_reveal.png`**: Game Over message, secret number reveal, and streak reset.
- **`05_invalid_input_validation.png`**: Demonstrations of non-numeric, decimal, empty, and out-of-bounds error handling.
- **`06_replay_and_winning_streak.png`**: Multi-round gameplay displaying consecutive streaks and session summary.

---

## 21. Learning Outcomes
- Designing defensive programs that never crash on irregular user inputs.
- Utilizing loops and sentinel variables to maintain consistent game state.
- Structuring automated unit tests using mocking techniques to evaluate interactive terminal applications.
- Authoring production-ready documentation and clean Git repository configurations.

---

## 22. Limitations
- Console/terminal environment only (no graphical interface by design).
- Session statistics are stored in memory and reset when the terminal session ends.

---

## 23. Future Enhancements
- Configurable difficulty settings (Easy: 1-50 in 6 attempts, Hard: 1-500 in 9 attempts).
- Persistent high-score leaderboard saved to JSON.
- Two-player turn-based guessing mode.

---

## 24. Author Information
- **Author**: Student Developer
- **Course**: Python Programming Fundamentals
- **Project**: Number Guessing Game Console Application

---

## 25. License
This project is open-source and distributed under the [MIT License](https://opensource.org/licenses/MIT).
