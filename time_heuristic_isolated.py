import sys
import os
import time

# Adjust sys.path to allow importing from solvers directory
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Attempt to import only the heuristic solver
try:
    from solvers.heuristic import solve_k4_n_greater_equal_6_heuristic
except ImportError as e:
    print(f"[{time.time():.2f} - time_heuristic_isolated] ImportError: {e}. Failed to import solve_k4_n_greater_equal_6_heuristic.")
    exit(1)
except Exception as ge:
    print(f"[{time.time():.2f} - time_heuristic_isolated] General Exception on import: {ge}")
    exit(1)

def main_time_test():
    N_test = 60
    K_val = 4 # Not used by heuristic directly, but context for the problem

    script_name = "time_heuristic_isolated.py"
    print(f"[{time.time():.2f} - {script_name}] STARTING HEURISTIC ISOLATION TEST for N={N_test}")

    # The heuristic function itself has internal prints, they will show up.
    # We are timing this specific call.
    start_execution_time = time.perf_counter()
    try:
        moves = solve_k4_n_greater_equal_6_heuristic(N_test)
    except Exception as e_solve:
        print(f"[{time.time():.2f} - {script_name}] EXCEPTION during solve_k4_n_greater_equal_6_heuristic: {e_solve}")
        end_execution_time = time.perf_counter()
        print(f"[{time.time():.2f} - {script_name}] Heuristic call failed in {end_execution_time - start_execution_time:.4f} seconds.")
        exit(1)
    end_execution_time = time.perf_counter()

    num_moves = len(moves)
    time_taken = end_execution_time - start_execution_time

    print(f"[{time.time():.2f} - {script_name}] solve_k4_n_greater_equal_6_heuristic for N={N_test} returned {num_moves} moves.")
    print(f"[{time.time():.2f} - {script_name}] Time taken for heuristic execution only: {time_taken:.4f} seconds.")

    expected_moves = 2 * N_test + 1
    if num_moves == expected_moves:
        print(f"[{time.time():.2f} - {script_name}] Move count ({num_moves}) matches expected ({expected_moves}).")
    else:
        print(f"[{time.time():.2f} - {script_name}] WARNING: Move count ({num_moves}) does NOT match expected ({expected_moves}).")

    print(f"[{time.time():.2f} - {script_name}] HEURISTIC ISOLATION TEST COMPLETE for N={N_test}")

if __name__ == '__main__':
    main_time_test()
