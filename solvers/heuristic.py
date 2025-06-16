import sys
import os
import time

# solve_k4_n_greater_equal_6_heuristic is now solve_k4_heuristic_2N_minus_3

def solve_k4_heuristic_2N_minus_3(N: int) -> list[list[str]]:
    func_name = "solve_k4_heuristic_2N_minus_3"
    # print(f"[{time.time():.2f} - {func_name}] START for N={N}")

    if N < 2:
        # This strategy requires at least 2 pairs.
        # For N=0 or N=1, it's typically no solution or trivial.
        # The problem targets N>=6, but the formula works for N>=2.
        return []

    moves = []

    # Part 1: Iteratively move pairs P_3 to P_N to the right bank using P_1 as a ferry.
    # This takes 2 * (N-2) moves.
    # This part only runs if N >= 3.
    if N >= 3:
        for i in range(3, N + 1):
            actor_i = f"a_{i}"
            agent_i = f"A_{i}"
            actor_1 = f"a_1" # P_1 is the ferry pair
            agent_1 = f"A_1"
            # Move P_i and P_1 to Right
            moves.append(sorted([actor_i, agent_i, actor_1, agent_1]))
            # Return P_1 to Left
            moves.append(sorted([actor_1, agent_1]))

    # Part 2: Move the final two pairs (P_1 and P_2) from Left to Right.
    # If N=2, Part 1 is skipped (0 moves), and this part constitutes the whole solution.
    # P_1 = (a_1, A_1), P_2 = (a_2, A_2)
    actor_1 = f"a_1"
    agent_1 = f"A_1"
    actor_2 = f"a_2"
    agent_2 = f"A_2"
    # Send P_1 and P_2 to Right in one go.
    moves.append(sorted([actor_1, agent_1, actor_2, agent_2])) # This is 1 move.

    # Total moves: 2*(N-2) + 1 = 2N - 4 + 1 = 2N - 3 (for N>=2)
    # If N=2, Part 1 is 0 moves. Part 2 is 1 move. Total 1. Formula: 2*2-3=1. Correct.
    # If N=3, Part 1 is 2*(3-2)=2 moves. Part 2 is 1 move. Total 3. Formula: 2*3-3=3. Correct.

    # print(f"[{time.time():.2f} - {func_name}] END for N={N}. Total moves: {len(moves)}.")
    return moves

def validate_solution(N: int, K: int, moves: list[list[str]]) -> bool:
    # GameState import is local to this function
    from game.environment import GameState
    func_name = "validate_solution"
    # print(f"[{time.time():.2f} - {func_name}] START for N={N}, K={K}, {len(moves)} moves.")

    if N == 0: return not moves # Empty moves list is a win for N=0

    initial_check_state = GameState(N=N, boat_capacity=K)
    if not moves: # No moves provided
        return initial_check_state.is_win()

    current_state = GameState(N=N, boat_capacity=K)
    if not current_state.is_valid_state():
        # This print is important if initial state itself is bad.
        print(f"[{time.time():.2f} - {func_name}] Initial state for N={N}, K={K} is INVALID.")
        return False

    for i, move_individuals_list in enumerate(moves):
        move_individuals_set = set(move_individuals_list)

        if not (1 <= len(move_individuals_set) <= K):
            print(f"[{time.time():.2f} - {func_name}] N={N} Move {i+1} FAIL: Invalid boat size {len(move_individuals_set)} for K={K}.")
            return False
        source_bank = current_state.left_bank if current_state.boat_on_left else current_state.right_bank
        if not move_individuals_set.issubset(source_bank):
            print(f"[{time.time():.2f} - {func_name}] N={N} Move {i+1} FAIL: Individuals {sorted(list(move_individuals_set - source_bank))} not on source bank {sorted(list(source_bank))}.")
            return False
        if not GameState.is_group_safe(move_individuals_set, current_state.actors, current_state.agents):
            print(f"[{time.time():.2f} - {func_name}] N={N} Move {i+1} FAIL: Boat group {sorted(list(move_individuals_set))} unsafe.")
            return False

        new_left_bank_set = set(current_state.left_bank)
        new_right_bank_set = set(current_state.right_bank)
        new_boat_on_left_val = not current_state.boat_on_left
        if current_state.boat_on_left: # L->R
            new_left_bank_set -= move_individuals_set
            new_right_bank_set.update(move_individuals_set)
        else: # R->L
            new_right_bank_set -= move_individuals_set
            new_left_bank_set.update(move_individuals_set)

        next_state = GameState(N=N, boat_capacity=K, left_bank_individuals=new_left_bank_set, right_bank_individuals=new_right_bank_set, boat_on_left=new_boat_on_left_val)
        if not next_state.is_valid_state():
            print(f"[{time.time():.2f} - {func_name}] N={N} Move {i+1} ({sorted(list(move_individuals_set))}) FAIL: Resulting state invalid.")
            # To give more detail on why next_state is invalid:
            if not GameState.is_group_safe(next_state.left_bank, next_state.actors, next_state.agents):
                 print(f"  Reason: New left bank {sorted(list(next_state.left_bank))} is unsafe.")
            if not GameState.is_group_safe(next_state.right_bank, next_state.actors, next_state.agents):
                 print(f"  Reason: New right bank {sorted(list(next_state.right_bank))} is unsafe.")
            on_left_and_right = next_state.left_bank.intersection(next_state.right_bank)
            if len(on_left_and_right) > 0:
                 print(f"  Reason: Individuals on both banks: {sorted(list(on_left_and_right))}")
            on_left_or_right = next_state.left_bank.union(next_state.right_bank)
            if on_left_or_right != next_state.all_individuals:
                 print(f"  Reason: Individuals missing or extra. Expected: {sorted(list(next_state.all_individuals))}, Got: {sorted(list(on_left_or_right))}")
            return False
        current_state = next_state

    if not current_state.is_win():
        print(f"[{time.time():.2f} - {func_name}] N={N} END: Final state is NOT a win.")
        return False
    return True

if __name__ == '__main__':
    pass # Keep __main__ minimal
