import csv
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from solvers.heuristic import solve_k4_heuristic_2N_minus_3, validate_solution
from game.environment import GameState # Needed for BFS
from solvers.search import bfs_solve, format_actor_agent_path # Needed for BFS

def generate_k4_solutions_and_write_csv():
    # This function content remains the same as the last successful run that produced solutions_k4.csv
    results = []
    k_value = 4
    output_filename = "solutions_k4.csv"
    print(f"Starting K={k_value} solution generation for N=6 to N=60 using heuristic (2N-3 strategy)...")
    print("Solution VALIDATION IS ENABLED.")
    for n_value in range(6, 61):
        start_time = time.time()
        heuristic_moves = solve_k4_heuristic_2N_minus_3(n_value)
        solvable_status = False
        num_moves_heuristic = 0
        solution_str_heuristic = "NO_SOLUTION_BY_HEURISTIC"
        if n_value < 2 and not heuristic_moves:
            solvable_status = False
            num_moves_heuristic = 0
            solution_str_heuristic = "N/A_FOR_N<2"
        elif heuristic_moves:
            num_moves_heuristic = len(heuristic_moves)
            is_valid_solution = validate_solution(n_value, k_value, heuristic_moves)
            if is_valid_solution:
                solvable_status = True
                solution_str_heuristic = str(heuristic_moves)
            else:
                solution_str_heuristic = "INVALID_HEURISTIC_SOLUTION"
                print(f"  N={n_value}, K={k_value}: CORRECTED HEURISTIC SOLUTION INVALID for N={n_value} after validation.")
        else:
             print(f"  N={n_value}, K={k_value}: Heuristic produced NO moves (unexpected for N>=2).")
        end_time = time.time()
        time_taken = end_time - start_time
        if n_value % 5 == 0 or n_value == 60 or n_value == 6:
             print(f"  N={n_value}, K={k_value}: Solvable: {solvable_status}, Moves: {num_moves_heuristic}, Time: {time_taken:.4f}s")
        results.append({
            'n': n_value, 'k': k_value, 'solver': 'heuristic_2N-3',
            'solvable': solvable_status, 'num_moves': num_moves_heuristic,
            'solution_path': solution_str_heuristic, 'time_seconds': round(time_taken, 4)
        })
    fieldnames = ["n", "k", "solver", "solvable", "num_moves", "solution_path", "time_seconds"]
    try:
        with open(output_filename, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"\nSolutions written to {output_filename} (N=6 to N=60, validated, 2N-3 strategy).")
    except IOError:
        print(f"Error: Could not write to CSV file {output_filename}.")

def compare_heuristic_with_bfs_for_small_n():
    k_value = 4
    # Adjusted range for BFS comparison: N=6 to N=10.
    # N=15 was suggested as "maybe", N=10 is safer for BFS performance.
    comparison_range_n = range(6, 11)

    print("\n" + "="*70)
    print(f"Comparing heuristic (2N-3) with BFS Optimal for K={k_value}, N={min(comparison_range_n)} to N={max(comparison_range_n)}")
    print("="*70 + "\n")
    print(f"{'N':<3} | {'Heuristic (2N-3)':<18} | {'BFS Optimal':<12} | {'Difference (BFS-Heur)':<20} | {'BFS Time (s)':<12}")
    print("-" * 70)

    for n_value in comparison_range_n:
        heuristic_moves_list = solve_k4_heuristic_2N_minus_3(n_value)
        heuristic_moves_count = len(heuristic_moves_list)

        # Ensure heuristic solution is valid before comparing (it should be based on previous step)
        if not validate_solution(n_value, k_value, heuristic_moves_list):
            print(f"{n_value:<3} | {heuristic_moves_count:<18} | {'Heuristic Invalid':<12} | {'N/A':<20} | {'N/A':<12}")
            print("-" * 70)
            continue

        print(f"N={n_value}: Calculating BFS... (K={k_value})")
        bfs_start_time = time.time()
        initial_state_bfs = GameState(N=n_value, boat_capacity=k_value)
        bfs_solution_path_states = bfs_solve(initial_state_bfs) # UNCOMMENTED
        bfs_duration = time.time() - bfs_start_time

        bfs_moves_count_str = "NO_SOLUTION"
        bfs_moves_count_val = -1
        difference_str = "N/A"

        if bfs_solution_path_states:
            formatted_bfs_moves = format_actor_agent_path(bfs_solution_path_states) # UNCOMMENTED
            bfs_moves_count_val = len(formatted_bfs_moves)
            bfs_moves_count_str = str(bfs_moves_count_val)
            # print(f"  N={n_value}: BFS found solution with {bfs_moves_count_val} moves in {bfs_duration:.2f}s.")
        # else:
            # print(f"  N={n_value}: BFS found NO solution in {bfs_duration:.2f}s.")

        if bfs_moves_count_val != -1: # If BFS found a solution
             difference = bfs_moves_count_val - heuristic_moves_count
             difference_str = str(difference)
             if difference < 0:
                 difference_str += " (Heuristic longer)"
             elif difference == 0:
                 difference_str += " (Optimal)"
             else: # difference > 0
                 difference_str += " (Heuristic shorter but BFS is optimal)"


        print(f"{n_value:<3} | {heuristic_moves_count:<18} | {bfs_moves_count_str:<12} | {difference_str:<20} | {bfs_duration:<12.2f}")
        print("-" * 70)

if __name__ == "__main__":
    generate_k4_solutions_and_write_csv()
    compare_heuristic_with_bfs_for_small_n() # Now this will run active BFS
    print("\nScript execution for CSV generation and BFS comparison complete.")
