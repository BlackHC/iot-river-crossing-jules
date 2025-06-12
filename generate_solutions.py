import csv
import os
import sys

# Adjust sys.path to allow importing from game and solvers directories
# generate_solutions.py is in the root, so adding its directory to sys.path
# allows Python to find game/ and solvers/ as packages.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from game.environment import GameState
from solvers.search import bfs_solve, format_actor_agent_path

def get_all_solutions():
    """
    Generates solutions for the puzzle for n from 1 to 10.
    Determines primary_k based on n (2 if n<=3, else 3).
    Additionally, for n between 6 and 10, solves for k=4.
    Collects and returns a list of dictionaries containing solution details.
    """
    results = []
    for n in range(1, 11):  # Loop n from 1 to 10
        # Determine and process primary k
        primary_k = 2 if n <= 3 else 3
        print(f"Processing n={n}, k={primary_k}...")

        initial_state_pk = GameState(N=n, boat_capacity=primary_k)
        solution_states_pk = bfs_solve(initial_state_pk)

        if solution_states_pk:
            formatted_moves_pk = format_actor_agent_path(solution_states_pk)
            solvable_pk = True
            num_moves_pk = len(formatted_moves_pk)
            solution_str_pk = str(formatted_moves_pk)
        else:
            solvable_pk = False
            num_moves_pk = 0
            solution_str_pk = "NO_SOLUTION"

        results.append({
            'n': n,
            'k': primary_k,
            'solvable': solvable_pk,
            'num_moves': num_moves_pk,
            'solution_path': solution_str_pk
        })

        # If n is between 6 and 10 (inclusive), also solve for k=4
        if 6 <= n <= 10:
            secondary_k = 4
            print(f"Processing n={n}, k={secondary_k}...")

            initial_state_sk = GameState(N=n, boat_capacity=secondary_k)
            solution_states_sk = bfs_solve(initial_state_sk)

            if solution_states_sk:
                formatted_moves_sk = format_actor_agent_path(solution_states_sk)
                solvable_sk = True
                num_moves_sk = len(formatted_moves_sk)
                solution_str_sk = str(formatted_moves_sk)
            else:
                solvable_sk = False
                num_moves_sk = 0
                solution_str_sk = "NO_SOLUTION"

            results.append({
                'n': n,
                'k': secondary_k,
                'solvable': solvable_sk,
                'num_moves': num_moves_sk,
                'solution_path': solution_str_sk
            })

    return results

def write_to_csv(results_list, filename="solution.csv"):
    """
    Writes the given list of results to a CSV file.
    """
    if not results_list:
        print("No results to write.")
        return

    fieldnames = ["n", "k", "solvable", "num_moves", "solution_path"]
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results_list)
    print(f"Solutions written to {filename}")

if __name__ == "__main__":
    print("Starting solution generation...")
    all_solutions_data = get_all_solutions()
    write_to_csv(all_solutions_data, filename="solution.csv")
    print("Solution generation complete. Output written to solution.csv")
