# River Crossing Game Project

This project aims to explore the river crossing puzzle.

## Goals

- Implement the river crossing game as an environment to test sequences of moves for validity.
- Develop solvers for the river crossing game.
- Investigate optimal strategies for different `n` (number of missionaries/cannibals on one side) and `k` (boat capacity).
- Determine for which `n` and `k` values no solutions exist.

## To-Dos

- [ ] Create the game environment.
- [ ] Implement basic solver(s) (e.g., BFS, DFS).
- [ ] Develop methods to find and verify optimal strategies.
- [ ] Research and document `n` and `k` combinations with no solutions.
- [ ] Add comprehensive unit tests for all components.
- [ ] Consider creating visualizations for game states and solutions.
- [ ] Store project goals and to-dos in a structured way within the repository (this `README.md` is the first step).

## Project Components

*   **Game Environment (`game/environment.py`):**
    *   Defines the `GameState` including missionaries and cannibals on each side, and boat position.
    *   The boat capacity (`k`) is a configurable parameter of the `GameState`.
    *   Provides functionality to apply actions (moves) and determine valid next states.
*   **Solvers (`solvers/search.py`):**
    *   Includes Breadth-First Search (BFS) and Depth-First Search (DFS) algorithms to find solutions to the puzzle.
    *   BFS is used to find optimal (shortest) solutions.
*   **Documentation (`docs/`):**
    *   Includes analysis of unsolvable `n` and `k` combinations.
*   **Unit Tests (`tests/`):**
    *   Comprehensive tests for the game environment and solvers.
