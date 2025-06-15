import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game.environment import GameState

def solve_k4_n_greater_equal_6_heuristic(N: int) -> list[list[str]]:
    """
    Generates a sequence of moves to solve the Actor-Agent puzzle
    for K=4 and N>=6 using a specialized heuristic.

    The strategy is:
    1. Iteratively move pairs P_3 to P_N to the right bank using P_1 as a ferry.
       Each such pair P_i (where i is from 3 to N) takes 2 moves:
       - L->R: (a_i, A_i, a_1, A_1)
       - R->L: (a_1, A_1)
       This takes 2 * (N-2) moves.
    2. Solve the remaining P_1, P_2 on the left bank using the standard 5-move sequence.
       - L->R: (a_2, A_2)
       - R->L: (A_2)
       - L->R: (A_1, A_2)
       - R->L: (A_1)
       - L->R: (a_1, A_1)
       This takes 5 moves.
    Total moves = 2*(N-2) + 5 = 2N - 4 + 5 = 2N + 1.

    Args:
        N: The number of actor-agent pairs. Must be >= 2 for the formula to be meaningful.
           The problem statement targets N>=6 for this specific heuristic.
           The function handles N < 2 by returning an empty list.

    Returns:
        A list of moves, where each move is a list of strings representing
        the individuals on the boat for that move.
    """
    if N < 2:
        return []

    # Special case for N=2, direct 5-move sequence, aligns with 2N+1.
    # This structure is implicitly handled by the main logic if N=2,
    # as the loop for P_3 to P_N doesn't run.
    # Loop: range(3, 2 + 1) is empty. 2*(2-2) = 0 moves.
    # Then 5 moves for P_1, P_2. Total 5.

    moves = []

    # Part 1: Move pairs P_3 to P_N using P_1 as ferry
    # These are N-2 pairs if N >= 2. If N=2, this loop doesn't run.
    # Indices for actors/agents are 1-based.
    # P_1 is (a_1, A_1)
    # P_i is (a_i, A_i)
    for i in range(3, N + 1):
        actor_i = f"a_{i}"
        agent_i = f"A_{i}"
        actor_1 = f"a_1"
        agent_1 = f"A_1"

        # Move 1: L->R with (P_i, P_1)
        moves.append(sorted([actor_i, agent_i, actor_1, agent_1]))
        # Move 2: R->L with (P_1)
        moves.append(sorted([actor_1, agent_1]))

    # Part 2: Solve for P_1 and P_2 (which are now the only ones on Left, or all if N=2)
    # P_2 = (a_2, A_2), P_1 = (a_1, A_1)
    # Standard 5-move sequence:
    actor_2 = f"a_2"
    agent_2 = f"A_2"
    actor_1 = f"a_1"
    agent_1 = f"A_1"

    moves.append(sorted([actor_2, agent_2]))  # L->R: (a_2, A_2)
    moves.append(sorted([agent_2]))           # R->L: (A_2)
    moves.append(sorted([agent_1, agent_2]))  # L->R: (A_1, A_2)
    moves.append(sorted([agent_1]))           # R->L: (A_1)
    moves.append(sorted([actor_1, agent_1]))  # L->R: (a_1, A_1)

    return moves

def validate_solution(N: int, K: int, moves: list[list[str]]) -> bool:
    """
    Validates a sequence of moves for the Actor-Agent puzzle.

    Args:
        N: Number of actor-agent pairs.
        K: Boat capacity.
        moves: A list of moves, where each move is a list of strings (individuals).

    Returns:
        True if the solution is valid (all moves are legal and leads to a win state),
        False otherwise.
    """
    if N == 0: # Special case for N=0
        return not moves # Empty moves list is a win for N=0

    initial_check_state = GameState(N=N, boat_capacity=K)
    if not moves: # No moves provided
        return initial_check_state.is_win()

    current_state = GameState(N=N, boat_capacity=K)

    if not current_state.is_valid_state():
        # This should not happen with the default GameState constructor
        print(f"Error: Initial state for N={N}, K={K} is surprisingly invalid.")
        return False

    for i, move_individuals_list in enumerate(moves):
        move_individuals_set = set(move_individuals_list)

        # Check 0: Boat capacity (must not be empty, must not exceed K)
        if not (1 <= len(move_individuals_set) <= K):
            print(f"Validation Fail (Move {i+1} - '{move_individuals_list}'): Invalid number of people in boat ({len(move_individuals_set)} for capacity {K}).")
            return False

        # Check 1: Are the individuals in the boat actually on the source bank?
        source_bank = current_state.left_bank if current_state.boat_on_left else current_state.right_bank
        if not move_individuals_set.issubset(source_bank):
            print(f"Validation Fail (Move {i+1} - '{move_individuals_list}'): Individuals {move_individuals_set - source_bank} not on source bank. Source bank: {sorted(list(source_bank))}")
            return False

        # Check 2: Is the boat group safe?
        if not GameState.is_group_safe(move_individuals_set, current_state.actors, current_state.agents):
            print(f"Validation Fail (Move {i+1} - '{move_individuals_list}'): Boat group unsafe.")
            return False

        # Create potential new bank configurations
        new_left_bank_set = set(current_state.left_bank) # Make copies
        new_right_bank_set = set(current_state.right_bank) # Make copies
        new_boat_on_left_val = not current_state.boat_on_left

        if current_state.boat_on_left: # Moving L -> R
            new_left_bank_set -= move_individuals_set
            new_right_bank_set.update(move_individuals_set)
        else: # Moving R -> L
            new_right_bank_set -= move_individuals_set
            new_left_bank_set.update(move_individuals_set)

        # Create the new GameState object for validation
        next_state = GameState(N=N,
                               boat_capacity=K,
                               left_bank_individuals=new_left_bank_set,
                               right_bank_individuals=new_right_bank_set,
                               boat_on_left=new_boat_on_left_val)

        if not next_state.is_valid_state():
            print(f"Validation Fail (Move {i+1} - '{move_individuals_list}') leads to an invalid state:")
            print(f"  Attempted state details - Left: {sorted(list(next_state.left_bank))}, Right: {sorted(list(next_state.right_bank))}, Boat on Left: {next_state.boat_on_left}")
            # Provide more specific reasons for invalidity
            if not GameState.is_group_safe(next_state.left_bank, next_state.actors, next_state.agents):
                 print(f"  Reason: New left bank {sorted(list(next_state.left_bank))} is unsafe.")
            if not GameState.is_group_safe(next_state.right_bank, next_state.actors, next_state.agents):
                 print(f"  Reason: New right bank {sorted(list(next_state.right_bank))} is unsafe.")
            # Could also check structural integrity if is_valid_state had sub-checks exposed
            return False

        current_state = next_state

    if not current_state.is_win():
        print(f"Validation Fail: Final state after all {len(moves)} moves is not a win state.")
        # print(f"Final state dump: {current_state}") # GameState.__str__ is verbose
        print(f"  Final state details - Left: {sorted(list(current_state.left_bank))}, Right: {sorted(list(current_state.right_bank))}, Boat on Left: {current_state.boat_on_left}")
        return False

    return True

# Update the if __name__ == '__main__' block:
if __name__ == '__main__':
    print("Testing solve_k4_n_greater_equal_6_heuristic and validate_solution:")

    # Test cases: N values to test. K is fixed to 4.
    # The heuristic is primarily for N>=6, but the formula 2N+1 works for N>=2.
    # solve_k4_n_greater_equal_6_heuristic returns [] for N<2.
    test_cases_n_values = [0, 1, 2, 3, 6]
    K_val = 4

    for n_val in test_cases_n_values:
        print(f"--- Testing for N={n_val}, K={K_val} ---")

        heuristic_moves = solve_k4_n_greater_equal_6_heuristic(n_val)

        expected_num_moves = 0
        if n_val >= 2:
            expected_num_moves = 2 * n_val + 1

        print(f"N={n_val}: Heuristic generated {len(heuristic_moves)} moves. Expected {expected_num_moves} (if N>=2, else 0).")

        if n_val < 2: # Covers N=0 and N=1
            if heuristic_moves: # Should be empty for N<2 from heuristic
                print(f"  WARN: Heuristic produced {len(heuristic_moves)} moves for N={n_val}, expected [].")

            # Validate the empty move list returned by heuristic for N<2
            is_valid_lt_2 = validate_solution(n_val, K_val, heuristic_moves) # heuristic_moves is []
            expected_validation_result = (n_val == 0) # Only N=0 with empty moves is a win

            print(f"  Validation for N={n_val} (heuristic produced []): {'PASS' if is_valid_lt_2 == expected_validation_result else 'FAIL'}")
            if is_valid_lt_2 != expected_validation_result:
                 print(f"    Detail: validate_solution({n_val}, {K_val}, []) returned {is_valid_lt_2}, expected {expected_validation_result}")
        else: # N >= 2
            if len(heuristic_moves) != expected_num_moves:
                 print(f"  WARN: Move count mismatch for N={n_val}! Got {len(heuristic_moves)}, Expected {expected_num_moves}.")

            if not heuristic_moves: # Should not happen for N>=2 from heuristic
                print(f"  FAIL: Heuristic produced no moves for N={n_val} (>=2).")
                # No point in validating empty moves if we expected some.
            else:
                # Validate the moves generated by the heuristic for N>=2
                is_valid = validate_solution(n_val, K_val, heuristic_moves)
                print(f"  Validation for N={n_val} heuristic solution: {'PASS' if is_valid else 'FAIL'}")
                if not is_valid:
                    # Avoid printing very long move lists if they fail.
                    # print(f"    Heuristic solution for N={n_val} that failed: {heuristic_moves}")
                    pass # Error messages from validate_solution should give enough detail.
        print("-" * 20)

    print("\nBasic tests complete for heuristic and validation.")
