# Actor-Agent River Crossing Puzzle Project

This project implements and explores the "Actor-Agent River Crossing" puzzle. This version of the puzzle, with its specific safety constraints (actors needing their agents when other agents are present), is based on the problem description found in the paper "The Illusion of Thinking: Understanding the Strengths and Limitations of Reasoning Models via the Lens of Problem Complexity."

## Goals

- Implement the Actor-Agent river crossing game as an environment to test sequences of moves for validity.
- Develop solvers (BFS, DFS) for this specific version of the river crossing game.
- Investigate optimal strategies for different `N` (number of actor-agent pairs) and `K` (boat capacity) values.
- Determine for which `N` and `K` values no solutions exist for the Actor-Agent puzzle.

## Project Status & To-Dos

- [x] Create the game environment for Actor-Agent puzzle (`game/environment.py`).
    - [x] State representation (banks, boat, N, K).
    - [x] Actor-Agent safety rules (`is_group_safe`, `is_valid_state`).
    - [x] Action generation and application (`get_valid_next_states`).
- [x] Implement basic solver(s) (`solvers/search.py`).
    - [x] Breadth-First Search (BFS).
    *   [x] Depth-First Search (DFS).
    *   [x] Solution path formatting (`format_actor_agent_path`).
- [x] Add comprehensive unit tests for all components (`tests/`).
- [ ] Develop methods to find and verify optimal strategies (BFS provides this).
- [ ] Research and document `N` and `K` combinations with no solutions *specifically for the Actor-Agent puzzle*.
- [ ] Consider creating visualizations for game states and solutions.
- [ ] Refine output formatting to exactly match paper's move representation if needed (e.g., "A_2" vs "A2").

## Project Components

*   **Game Environment (`game/environment.py`):**
    *   Defines `GameState` for the Actor-Agent puzzle, tracking individuals (e.g., "a1", "A1") on left/right banks.
    *   Configurable with `N` (number of actor-agent pairs) and `boat_capacity` (K).
    *   Enforces Actor-Agent safety rules: an actor `ax` can only be with other agents (`Ay`, `Az`) if its own agent `Ax` is also present. This is checked for banks and boat occupants.
    *   Provides `get_valid_next_states()` to generate all valid successor states.
*   **Solvers (`solvers/search.py`):**
    *   Includes Breadth-First Search (BFS) and Depth-First Search (DFS) algorithms to find solutions.
    *   BFS finds an optimal (shortest) solution in terms of the number of moves.
    *   Includes `format_actor_agent_path` to convert a solution path (list of `GameState` objects) into the paper's specified list-of-lists format for moves (e.g., `[['A2', 'a2'], ['A2'], ...]`, using alphabetical sorting for individuals within each move).
*   **Documentation (`docs/`):**
    *   `docs/no_solutions.md` currently details some general M&C unsolvable conditions. This may need updating or a new file for Actor-Agent specific conditions.
*   **Unit Tests (`tests/`):**
    *   `tests/test_environment.py` contains tests for `GameState`, including initialization, safety rules (`is_group_safe`, `is_valid_state`), win condition, and `get_valid_next_states`.
    *   `tests/test_solvers.py` contains tests for BFS and DFS solvers with various Actor-Agent scenarios (e.g., N=2 K=2 solvable, N=1 K=1 unsolvable), and tests for `format_actor_agent_path`.
