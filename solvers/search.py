from collections import deque
import sys
import os

# Adjust path to import from parent directory's 'game' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.environment import GameState, POSSIBLE_ACTIONS, apply_action

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

        for action in POSSIBLE_ACTIONS:
            next_state = apply_action(current_state, action)

            if next_state and next_state not in visited_states:
                # apply_action is expected to return None or a valid state.
                # So, if next_state is not None, it is assumed to be valid.
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

        # Optimization: If we've found a path that reaches current_state via a shorter route,
        # and then re-added current_state to the stack, we might explore longer paths.
        # However, for basic DFS, we usually mark visited when popped or when pushed.
        # For this problem, marking when pushed (as done below for next_state) is common to avoid cycles.
        # If we only add to visited when *popped*, we might re-explore.
        # Current implementation adds to visited *before* pushing.

        # Explore neighbors
        for action in POSSIBLE_ACTIONS:
            next_state = apply_action(current_state, action)

            if next_state and next_state not in visited_states:
                # apply_action is expected to return None or a valid state.
                # So, if next_state is not None, it is assumed to be valid.
                new_path = current_path + [next_state]
                if next_state.is_win():
                    return new_path

                visited_states.add(next_state) # Mark visited before adding to stack
                stack.append((next_state, new_path))
            elif next_state and next_state in visited_states:
                # Optional: Could check if new_path is shorter to this visited state,
                # but standard DFS doesn't guarantee shortest path.
                # For this problem, we just need *a* solution.
                pass

    return None # No solution found

if __name__ == '__main__':
    # Test the solvers
    start_state = GameState(3, 3, True) # Initial state: 3M, 3C, Boat on Left

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
    won_state = GameState(0,0,False, initial_missionaries=3, initial_cannibals=3)
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
    invalid_start_state = GameState(1,2,True, initial_missionaries=3, initial_cannibals=3)
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
    print("Attempting BFS solver for 2M, 2C, Boat Left...")
    start_state_2m2c = GameState(2, 2, True, initial_missionaries=2, initial_cannibals=2)
    bfs_solution_path_2m2c = bfs_solve(start_state_2m2c)

    if bfs_solution_path_2m2c:
        print("BFS Solution Found for 2M, 2C:")
        for i, state in enumerate(bfs_solution_path_2m2c):
            print(f"Step {i}: {state}")
        expected_optimal_length_2m2c = 6 # 5 moves
        if start_state_2m2c.initial_missionaries == 2 and start_state_2m2c.initial_cannibals == 2:
            assert len(bfs_solution_path_2m2c) == expected_optimal_length_2m2c, \
                f"BFS solution length {len(bfs_solution_path_2m2c)} for (2M,2C) does not match known optimal of {expected_optimal_length_2m2c} states."
            print(f"\nBFS solution for (2M,2C) has {len(bfs_solution_path_2m2c)-1} moves, which is the known optimal.")
    else:
        print("No solution found by BFS for 2M, 2C.")

    print("\nAttempting DFS solver for 2M, 2C, Boat Left...")
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

    # Consider an initial state that leads to no solution: GameState(1,0,True,1,0) is already solved.
    # GameState(0,1,True,0,1) is also solved.
    # GameState(1,1,True, initial_missionaries=1, initial_cannibals=2) boat on left.
    # M=1, C=1, B=L | M=0, C=1. Valid.
    # Try to move (0,1) L->R: M=1,C=0, B=R | M=0,C=2 -> Invalid.
    # Try to move (1,0) L->R: M=0,C=1, B=R | M=1,C=1 -> Valid.
    #   Now: M=0,C=1, B=R | M=1,C=1
    #   Try to move (0,1) R->L: M=0,C=2, B=L | M=1,C=0 -> Invalid
    #   Try to move (1,0) R->L: M=1,C=1, B=L | M=0,C=1 -> Back to start.
    #   Try to move (1,1) R->L: M=1,C=2, B=L | M=0,C=0 -> Invalid.
    # This state (1M,1C,L | 0M,1C) is unsolvable.
    print("\n" + "="*30 + "\n")
    print("Attempting BFS for an unsolvable state (1M,1C,L where total C=2):")
    unsolvable_state = GameState(1,1,True, initial_missionaries=1, initial_cannibals=2)
    print(f"Initial state: {unsolvable_state}, Valid: {unsolvable_state.is_valid()}")
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
