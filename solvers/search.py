from collections import deque
import sys
import os

# Adjust path to import from parent directory's 'game' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.environment import GameState # apply_action and generate_possible_actions no longer needed here

def bfs_solve(initial_state: GameState) -> list[GameState] | None:
    """
    Solves the Missionaries and Cannibals problem using Breadth-First Search.
    BFS is guaranteed to find the shortest path in terms of the number of moves
    because it explores the state space layer by layer, and each move has a
    uniform cost (1 step).

    Args:
        initial_state: The starting state of the game.

    Returns:
        A list of GameState objects representing the path from the initial
        state to a winning state, or None if no solution is found.
    """
    if not initial_state.is_valid():
        return None
    if initial_state.is_win():
        return [initial_state]

    queue = deque([(initial_state, [initial_state])])  # Store (state, path_to_state)
    visited_states = {initial_state}

    while queue:
        current_state, current_path = queue.popleft()

        possible_next_states = current_state.get_valid_next_states()

        for next_state in possible_next_states:
            if next_state not in visited_states: # Check visited before further processing
                new_path = current_path + [next_state]
                if next_state.is_win():
                    return new_path

                visited_states.add(next_state)
                queue.append((next_state, new_path))

    return None # No solution found

def dfs_solve(initial_state: GameState) -> list[GameState] | None:
    """
    Solves the Missionaries and Cannibals problem using Depth-First Search (iterative).

    Args:
        initial_state: The starting state of the game.

    Returns:
        A list of GameState objects representing the path from the initial
        state to a winning state, or None if no solution is found.
    """
    if not initial_state.is_valid():
        return None
    if initial_state.is_win():
        return [initial_state]

    # Using a list as a stack: (state, path_to_state)
    stack = [(initial_state, [initial_state])]
    visited_states = {initial_state}

    while stack:
        current_state, current_path = stack.pop()

        possible_next_states = current_state.get_valid_next_states()

        # Explore neighbors (in reverse for stack to maintain similar order to old POSSIBlE_ACTIONS if desired, though not critical)
        # For DFS, the order of exploring children can affect the first solution found.
        # Original POSSIBLE_ACTIONS was [(1,0),(2,0),(0,1),(0,2),(1,1)].
        # get_valid_next_states order depends on generate_possible_actions.
        # If specific DFS path is desired for consistency with old tests, may need to reverse possible_next_states.
        # However, any valid path is acceptable for DFS.
        for next_state in possible_next_states: # Or reversed(possible_next_states)
            if next_state not in visited_states:
                new_path = current_path + [next_state]
                if next_state.is_win():
                    return new_path

                visited_states.add(next_state) # Mark visited before adding to stack
                stack.append((next_state, new_path))
            # No explicit check for "next_state in visited_states" here,
            # as it's handled by the "if next_state not in visited_states"
            # and standard DFS doesn't typically re-evaluate paths to already visited states.

    return None # No solution found

if __name__ == '__main__':
    # Test the solvers
    # Standard game: 3 Missionaries, 3 Cannibals, Boat Capacity 2
    start_state = GameState(3, 3, True, initial_missionaries=3, initial_cannibals=3, boat_capacity=2)

    print("Attempting BFS solver...")
    bfs_solution_path = bfs_solve(start_state)

    if bfs_solution_path:
        print("BFS Solution Found:")
        for i, state in enumerate(bfs_solution_path):
            print(f"Step {i}: {state}")
        # The path includes the initial state, so #moves = path_length - 1
        # Known optimal for 3M, 3C, boat_cap=2 is 11 moves. So path length is 12.
        expected_optimal_length = 12
        if start_state.initial_missionaries == 3 and start_state.initial_cannibals == 3:
            assert len(bfs_solution_path) == expected_optimal_length, \
                f"BFS solution length {len(bfs_solution_path)} does not match known optimal of {expected_optimal_length} states."
            print(f"\nBFS solution for (3M,3C) has {len(bfs_solution_path)-1} moves, which is the known optimal.")
    else:
        print("No solution found by BFS.")

    print("\n" + "="*30 + "\n")

    print("Attempting DFS solver...")
    # For DFS, to prevent extremely long non-optimal paths,
    # re-initialize visited_states if you run it after BFS on the same start_state object
    # or ensure GameState's hash/eq are robust if it were mutable (it's not currently).
    # Since visited_states is local to each function, this is fine.
    dfs_solution_path = dfs_solve(start_state)

    if dfs_solution_path:
        print("DFS Solution Found:")
        for i, state in enumerate(dfs_solution_path):
            print(f"Step {i}: {state}")
    else:
        print("No solution found by DFS.")

    # Test case: Already won state
    print("\n" + "="*30 + "\n")
    print("Testing already won state:")
    won_state = GameState(0,0,False, initial_missionaries=3, initial_cannibals=3, boat_capacity=2)
    print(f"Initial state: {won_state}, Is Win? {won_state.is_win()}")
    bfs_won_path = bfs_solve(won_state)
    if bfs_won_path:
        print("BFS solution for won state:")
        for s in bfs_won_path: print(s)
    else:
        print("BFS: No solution for won state (error).")

    dfs_won_path = dfs_solve(won_state)
    if dfs_won_path:
        print("DFS solution for won state:")
        for s in dfs_won_path: print(s)
    else:
        print("DFS: No solution for won state (error).")

    # Test case: Impossible state (e.g., more people than exist)
    # GameState constructor would prevent this, apply_action would also.
    # Let's test an invalid starting state that *can* be constructed.
    print("\n" + "="*30 + "\n")
    print("Testing invalid initial state (1M, 2C on left):")
    # For a 3M, 3C game with boat_capacity=2
    invalid_start_state = GameState(1,2,True, initial_missionaries=3, initial_cannibals=3, boat_capacity=2)
    print(f"Initial state: {invalid_start_state}, Is Valid? {invalid_start_state.is_valid()}")

    bfs_invalid_path = bfs_solve(invalid_start_state)
    if bfs_invalid_path is None:
        print("BFS correctly returned None for invalid start.")
    else:
        print(f"BFS returned a path for invalid start (error): {bfs_invalid_path}")

    dfs_invalid_path = dfs_solve(invalid_start_state)
    if dfs_invalid_path is None:
        print("DFS correctly returned None for invalid start.")
    else:
        print(f"DFS returned a path for invalid start (error): {dfs_invalid_path}")

    # Test with different initial numbers (e.g. 2M, 2C)
    # The known optimal for 2M, 2C, boat_cap=2 is 5 moves (path length 6)
    print("\n" + "="*30 + "\n")
    print("Attempting BFS solver for 2M, 2C, Boat Left (cap=2)...")
    start_state_2m2c = GameState(2, 2, True, initial_missionaries=2, initial_cannibals=2, boat_capacity=2)
    bfs_solution_path_2m2c = bfs_solve(start_state_2m2c)

    if bfs_solution_path_2m2c:
        print("BFS Solution Found for 2M, 2C:")
        for i, state in enumerate(bfs_solution_path_2m2c):
            print(f"Step {i}: {state}")
        expected_optimal_length_2m2c = 6 # 5 moves
        if start_state_2m2c.initial_missionaries == 2 and start_state_2m2c.initial_cannibals == 2 and start_state_2m2c.boat_capacity == 2:
            assert len(bfs_solution_path_2m2c) == expected_optimal_length_2m2c, \
                f"BFS solution length {len(bfs_solution_path_2m2c)} for (2M,2C) k=2 does not match known optimal of {expected_optimal_length_2m2c} states."
            print(f"\nBFS solution for (2M,2C) k=2 has {len(bfs_solution_path_2m2c)-1} moves, which is the known optimal.")
    else:
        print("No solution found by BFS for 2M, 2C.")

    print("\nAttempting DFS solver for 2M, 2C, Boat Left...")
    # start_state_2m2c is already defined with cap=2
    dfs_solution_path_2m2c = dfs_solve(start_state_2m2c)
    if dfs_solution_path_2m2c:
        print("DFS Solution Found for 2M, 2C:")
        for i, state in enumerate(dfs_solution_path_2m2c):
            print(f"Step {i}: {state}")
    else:
        print("No solution found by DFS for 2M, 2C.")

    # Test an unsolvable scenario if one is easily constructible
    # For M&C, standard (3,3) is solvable. (1,2) with boat cap 2 might be unsolvable
    # if initial state is (1,2,L) -> move (0,1) -> (1,1,R) -> move (0,1) -> (1,2,L) ... cycle
    # Or if only 1M, 1C and boat capacity 2.
    # (1M, 1C, L) -> move (1,0) -> (0,1,R) -> cannot move back M or C alone without violating rules.
    # -> move (1,1) -> (0,0,R) WIN. This is solvable.

    # Consider an initial state that leads to no solution:
    # Using the (1M,1C,L | initial_M=1, initial_C=2, boat_cap=2) example from before
    print("\n" + "="*30 + "\n")
    print("Attempting BFS for an unsolvable state (1M,1C,L where total M=1, C=2, cap=2):")
    unsolvable_state = GameState(1,1,True, initial_missionaries=1, initial_cannibals=2, boat_capacity=2)
    print(f"Initial state: {unsolvable_state}, Valid: {unsolvable_state.is_valid()}") # Should be valid
    bfs_unsolvable = bfs_solve(unsolvable_state)
    if bfs_unsolvable is None:
        print("BFS correctly returned None for unsolvable state.")
    else:
        print(f"BFS returned a path for unsolvable state (error): {bfs_unsolvable}")

    dfs_unsolvable = dfs_solve(unsolvable_state)
    if dfs_unsolvable is None:
        print("DFS correctly returned None for unsolvable state.")
    else:
        print(f"DFS returned a path for unsolvable state (error): {dfs_unsolvable}")
