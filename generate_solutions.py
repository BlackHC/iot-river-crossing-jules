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
    Determines k based on n (k=2 if n<=3, else k=3).
    Collects and returns a list of dictionaries containing solution details.
    """
    results = []
    for n in range(1, 11):  # Loop n from 1 to 10
        k = 2 if n <= 3 else 3
        print(f"Processing n={n}, k={k}...")

        initial_state = GameState(N=n, boat_capacity=k)
        solution_states = bfs_solve(initial_state)

        if solution_states:
            formatted_moves = format_actor_agent_path(solution_states)
            solvable = True
            num_moves = len(formatted_moves)
            solution_str = str(formatted_moves)
        else:
            solvable = False
            num_moves = 0
            solution_str = "NO_SOLUTION"

        results.append({
            'n': n,
            'k': k,
            'solvable': solvable,
            'num_moves': num_moves,
            'solution_path': solution_str
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
    write_to_csv(all_solutions_data, filename="solution.csv") # Ensure filename is "solution.csv"
    print("Solution generation complete. Output written to solution.csv")
