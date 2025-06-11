from collections import deque
import sys
import os

# Adjust path to import from parent directory's 'game' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.environment import GameState # Only GameState is needed now

def bfs_solve(initial_state: GameState) -> list[GameState] | None:
    """
    Solves a river crossing puzzle using Breadth-First Search.
    Works for any GameState that implements get_valid_next_states(), is_win(), is_valid().
    BFS is guaranteed to find the shortest path in terms of the number of moves.
    """
    if not initial_state.is_valid_state(): # Use the new method name
        return None
    if initial_state.is_win():
        return [initial_state]

    queue = deque([(initial_state, [initial_state])])
    visited_states = {initial_state}

    while queue:
        current_state, current_path = queue.popleft()

        possible_next_states = current_state.get_valid_next_states()

        for next_state in possible_next_states:
            if next_state not in visited_states:
                new_path = current_path + [next_state]
                if next_state.is_win():
                    return new_path

                visited_states.add(next_state)
                queue.append((next_state, new_path))

    return None

def dfs_solve(initial_state: GameState) -> list[GameState] | None:
    """
    Solves a river crossing puzzle using Depth-First Search (iterative).
    Works for any GameState that implements get_valid_next_states(), is_win(), is_valid().
    """
    if not initial_state.is_valid_state(): # Use the new method name
        return None
    if initial_state.is_win():
        return [initial_state]

    stack = [(initial_state, [initial_state])]
    visited_states = {initial_state}

    while stack:
        current_state, current_path = stack.pop()
        possible_next_states = current_state.get_valid_next_states()

        for next_state in possible_next_states:
            if next_state not in visited_states:
                new_path = current_path + [next_state]
                if next_state.is_win():
                    return new_path

                visited_states.add(next_state)
                stack.append((next_state, new_path))

    return None

def format_actor_agent_path(path: list[GameState]) -> list[list[str]]:
    """
    Formats a solution path (list of GameState objects) for the Actor-Agent puzzle
    into a list of moves, where each move is represented by a sorted list of
    individuals on the boat.
    """
    if not path or len(path) < 2:
        return []

    formatted_moves = []
    for i in range(len(path) - 1):
        current_state = path[i]
        next_state = path[i+1]

        boat_occupants: set[str]
        if current_state.boat_on_left: # Boat moved L -> R
            boat_occupants = current_state.left_bank.difference(next_state.left_bank)
        else: # Boat moved R -> L
            boat_occupants = current_state.right_bank.difference(next_state.right_bank)

        # Sort alphabetically for consistent output order.
        # Example: "A1", "a1" if both were on boat.
        sorted_occupants = sorted(list(boat_occupants))
        formatted_moves.append(sorted_occupants)

    return formatted_moves

if __name__ == '__main__':
    print("Actor-Agent Puzzle Solver Tests")
    print("="*40)

    # Test Case 1: N=2, K=2 (Solvable, known solution is 5 moves / 6 states)
    print("\n--- Testing N=2, K=2 (Solvable) ---")
    initial_state_n2_k2 = GameState(N=2, boat_capacity=2)
    print(f"Initial State: {initial_state_n2_k2}")

    print("\nAttempting BFS for N=2, K=2...")
    bfs_solution_n2_k2 = bfs_solve(initial_state_n2_k2)
    if bfs_solution_n2_k2:
        print(f"BFS Solution Found for N=2, K=2 ({len(bfs_solution_n2_k2)-1} moves):")
        # for i, state in enumerate(bfs_solution_n2_k2):
        #     print(f"Step {i}: {state}")

        formatted_bfs_moves = format_actor_agent_path(bfs_solution_n2_k2)
        print(f"Formatted BFS Moves: {formatted_bfs_moves}")
        # Expected paper example: [["A_2", "a_2"], ["A_2"], ["A_1", "A_2"], ["A_1"], ["A_1", "a_1"]]
        # My sorting will be alphabetical: e.g., ["A2", "a2"] or ["A1", "A2"] or ["A1", "a1"]
        # The paper uses _ my code uses no underscore. Let's adapt expected to my format.
        expected_moves_n2_k2_paper_adapted = [
            sorted(["A2", "a2"]), # (a2,A2)R
            sorted(["A2"]),       # (A2)L
            sorted(["A1", "A2"]), # (A1,A2)R
            sorted(["A1"]),       # (A1)L
            sorted(["A1", "a1"])  # (a1,A1)R
        ]
        # Note: The exact set of individuals might differ if multiple paths of same length exist.
        # The key is the length for BFS.
        assert len(formatted_bfs_moves) == 5, "BFS N=2,K=2: Expected 5 moves."
        if formatted_bfs_moves == expected_moves_n2_k2_paper_adapted:
            print("BFS N=2,K=2 path matches adapted paper example.")
        else:
            print(f"BFS N=2,K=2 path does not exactly match adapted paper example. Expected: {expected_moves_n2_k2_paper_adapted}")

        expected_len_n2_k2_states = 6
        assert len(bfs_solution_n2_k2) == expected_len_n2_k2_states, \
            f"BFS N=2,K=2: Expected {expected_len_n2_k2_states} states, got {len(bfs_solution_n2_k2)}"
        print(f"BFS path length for N=2, K=2 is {len(bfs_solution_n2_k2)} states, which is the expected optimal.")

    else:
        print("BFS: No solution found for N=2, K=2.")

    print("\nAttempting DFS for N=2, K=2...")
    dfs_solution_n2_k2 = dfs_solve(initial_state_n2_k2)
    if dfs_solution_n2_k2:
        print(f"DFS Solution Found for N=2, K=2 ({len(dfs_solution_n2_k2)-1} moves).")
        formatted_dfs_moves = format_actor_agent_path(dfs_solution_n2_k2)
        print(f"Formatted DFS Moves: {formatted_dfs_moves}")
        print(f"DFS path length for N=2, K=2 is {len(dfs_solution_n2_k2)} states.")
    else:
        print("DFS: No solution found for N=2, K=2.")

    # Test Case 2: N=1, K=1 (Should be Unsolvable by current AA rules)
    print("\n--- Testing N=1, K=1 (Unsolvable) ---")
    initial_state_n1_k1 = GameState(N=1, boat_capacity=1)
    print(f"Initial State: {initial_state_n1_k1}")

    print("\nAttempting BFS for N=1, K=1...")
    bfs_solution_n1_k1 = bfs_solve(initial_state_n1_k1)
    if bfs_solution_n1_k1:
        print(f"BFS Solution Found for N=1, K=1 ({len(bfs_solution_n1_k1)-1} moves) - THIS IS UNEXPECTED!")
        formatted_n1_k1 = format_actor_agent_path(bfs_solution_n1_k1)
        print(f"Formatted N1K1 Moves: {formatted_n1_k1}")
    else:
        print("BFS: No solution found for N=1, K=1 (as expected for strict AA rules).")

    # Test Case 3: Already solved state
    print("\n--- Testing Already Solved State (N=1, K=1) ---")
    solved_state_n1_k1 = GameState(N=1, boat_capacity=1, boat_on_left=False)
    print(f"Initial State (already solved): {solved_state_n1_k1}")
    assert solved_state_n1_k1.is_win(), "Constructed solved state is not a win state!"

    bfs_solved_path = bfs_solve(solved_state_n1_k1)
    if bfs_solved_path:
        assert len(bfs_solved_path) == 1, "Path for already solved state should be 1"
        print("BFS correctly found path of length 1 for already solved state.")
        formatted_solved_moves = format_actor_agent_path(bfs_solved_path)
        assert formatted_solved_moves == [], "Formatted moves for already solved state should be empty."
        print("Formatted moves for already solved path is correctly empty.")
    else:
        print("BFS failed for already solved state.")

    # Test Case 4: Invalid initial state (structurally)
    print("\n--- Testing Invalid Initial State (N=1, K=1) ---")
    invalid_initial_state = GameState(N=1, boat_capacity=1)
    if invalid_initial_state.all_individuals:
      person_to_remove = next(iter(invalid_initial_state.all_individuals))
      if person_to_remove in invalid_initial_state.left_bank:
          invalid_initial_state.left_bank.remove(person_to_remove)
      # No need to check right bank for default init state
    print(f"Initial State (corrupted): {invalid_initial_state}")
    assert not invalid_initial_state.is_valid_state(), "Corrupted state was not invalid!"

    bfs_invalid_path = bfs_solve(invalid_initial_state)
    if bfs_invalid_path is None:
        print("BFS correctly returned None for invalid initial state.")
    else:
        print("BFS returned a path for invalid initial state (error).")
