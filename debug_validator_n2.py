import sys
import os
import time

# Adjust sys.path to allow importing
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from solvers.heuristic import solve_k4_n_greater_equal_6_heuristic, validate_solution
except ImportError as e:
    print(f"[{time.time():.2f} - debug_validator_n2] ImportError: {e}.")
    exit(1)
except Exception as ge:
    print(f"[{time.time():.2f} - debug_validator_n2] General Exception on import: {ge}")
    exit(1)

def main_debug_validator_test():
    N_test = 2
    K_val = 4
    script_name = "debug_validator_n2.py"
    print(f"[{time.time():.2f} - {script_name}] STARTING VALIDATOR DEBUG TEST for N={N_test}, K={K_val}")

    # 1. Generate moves (known to be fast)
    print(f"[{time.time():.2f} - {script_name}] Calling solve_k4_n_greater_equal_6_heuristic for N={N_test}...")
    # Heuristic function has its own prints, which will be verbose.
    # No need to time this separately as it's established as very fast.
    moves = solve_k4_n_greater_equal_6_heuristic(N_test)
    print(f"[{time.time():.2f} - {script_name}] Heuristic generated {len(moves)} moves for N={N_test}.")

    if not moves: # Should be 5 moves for N=2
        print(f"[{time.time():.2f} - {script_name}] FAIL: Heuristic produced NO MOVES for N={N_test}.")
        exit(1)

    # 2. Validate the generated moves
    print(f"[{time.time():.2f} - {script_name}] Calling validate_solution for N={N_test}, K={K_val} with {len(moves)} moves...")
    # validate_solution also has its own verbose prints.

    val_start_time = time.perf_counter()
    try:
        is_valid = validate_solution(N_test, K_val, moves)
    except Exception as e_validate:
        print(f"[{time.time():.2f} - {script_name}] EXCEPTION during validate_solution: {e_validate}")
        val_end_time = time.perf_counter()
        print(f"[{time.time():.2f} - {script_name}] validate_solution call failed in {val_end_time - val_start_time:.4f} seconds.")
        exit(1)
    val_end_time = time.perf_counter()

    print(f"[{time.time():.2f} - {script_name}] validate_solution returned: {is_valid}")
    print(f"[{time.time():.2f} - {script_name}] Time taken for validate_solution only: {val_end_time - val_start_time:.4f} seconds.")

    if is_valid:
        print(f"[{time.time():.2f} - {script_name}] VALIDATOR DEBUG TEST PASSED: Heuristic solution for N={N_test} is VALID.")
    else:
        print(f"[{time.time():.2f} - {script_name}] VALIDATOR DEBUG TEST FAILED: Heuristic solution for N={N_test} is INVALID.")
        # Moves would have been printed by validate_solution's internal logs if it reached that point.

    print(f"[{time.time():.2f} - {script_name}] VALIDATOR DEBUG TEST COMPLETE for N={N_test}, K={K_val}")

if __name__ == '__main__':
    main_debug_validator_test()
