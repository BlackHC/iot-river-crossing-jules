import sys
import os
import time

# Adjust sys.path to allow importing from game and solvers directories
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from solvers.heuristic import solve_k4_n_greater_equal_6_heuristic, validate_solution
    # from game.environment import GameState # GameState is used by validate_solution
except ImportError as e:
    print(f"[{time.time():.2f} - debug_heuristic_n6] ImportError: {e}. Check paths.")
    # Attempt to list contents for debugging path issues from script's perspective
    try:
        print(f"[{time.time():.2f} - debug_heuristic_n6] CWD: {os.getcwd()}")
        if os.path.exists("solvers"):
            print(f"[{time.time():.2f} - debug_heuristic_n6] Contents of ./solvers/: {os.listdir('./solvers/')}")
        else:
            print(f"[{time.time():.2f} - debug_heuristic_n6] ./solvers/ directory NOT FOUND from CWD.")
        if os.path.exists("game"):
             print(f"[{time.time():.2f} - debug_heuristic_n6] Contents of ./game/: {os.listdir('./game/')}")
        else:
            print(f"[{time.time():.2f} - debug_heuristic_n6] ./game/ directory NOT FOUND from CWD.")
    except Exception as list_e:
        print(f"[{time.time():.2f} - debug_heuristic_n6] Error listing directories: {list_e}")
    exit(1)
except Exception as ge:
    print(f"[{time.time():.2f} - debug_heuristic_n6] General Exception on import: {ge}")
    exit(1)


def main_debug_test():
    N_test = 2
    K_val = 4

    script_name = "debug_heuristic_n6.py"
    print(f"[{time.time():.2f} - {script_name}] STARTING DEBUG TEST for N={N_test}, K={K_val}")

    print(f"[{time.time():.2f} - {script_name}] Calling solve_k4_n_greater_equal_6_heuristic...")
    try:
        moves = solve_k4_n_greater_equal_6_heuristic(N_test)
    except Exception as e_solve:
        print(f"[{time.time():.2f} - {script_name}] EXCEPTION during solve_k4_n_greater_equal_6_heuristic: {e_solve}")
        exit(1)

    print(f"[{time.time():.2f} - {script_name}] solve_k4_n_greater_equal_6_heuristic returned {len(moves)} moves.")

    if not moves:
        print(f"[{time.time():.2f} - {script_name}] Heuristic produced NO MOVES for N={N_test}. Exiting debug test.")
        # This would be an issue for N=6
        exit(1)

    print(f"[{time.time():.2f} - {script_name}] Calling validate_solution...")
    try:
        is_valid = validate_solution(N_test, K_val, moves)
    except Exception as e_validate:
        print(f"[{time.time():.2f} - {script_name}] EXCEPTION during validate_solution: {e_validate}")
        exit(1)

    print(f"[{time.time():.2f} - {script_name}] validate_solution returned: {is_valid}")

    if is_valid:
        print(f"[{time.time():.2f} - {script_name}] DEBUG TEST PASSED: Heuristic solution for N={N_test} is VALID.")
    else:
        print(f"[{time.time():.2f} - {script_name}] DEBUG TEST FAILED: Heuristic solution for N={N_test} is INVALID.")
        print(f"    Moves: {moves}")

    print(f"[{time.time():.2f} - {script_name}] DEBUG TEST COMPLETE for N={N_test}, K={K_val}")

if __name__ == '__main__':
    main_debug_test()
