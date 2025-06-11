import unittest
import sys
import os

# Adjust path to import from parent directory modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.environment import GameState
from solvers.search import bfs_solve, dfs_solve

class TestSolvers(unittest.TestCase):

    def test_bfs_solve_standard_3m_3c(self):
        # Standard 3 Missionaries, 3 Cannibals, boat capacity 2
        # GameState defaults to initial_missionaries=3, initial_cannibals=3
        initial_state = GameState(3, 3, True)
        solution_path = bfs_solve(initial_state)

        self.assertIsNotNone(solution_path, "BFS should find a solution for (3,3)")
        self.assertIsInstance(solution_path, list)
        self.assertTrue(all(isinstance(s, GameState) for s in solution_path))

        # Known optimal solution length is 12 states (11 moves)
        self.assertEqual(len(solution_path), 12, "BFS solution for (3,3) should have 12 states")

        # Check if first state is initial and last state is win state
        self.assertEqual(solution_path[0], initial_state)
        self.assertTrue(solution_path[-1].is_win())

        # Check path validity (all states in path must be valid)
        for state in solution_path:
            self.assertTrue(state.is_valid(), f"State {state} in BFS path for (3,3) is invalid")

    def test_dfs_solve_standard_3m_3c(self):
        initial_state = GameState(3, 3, True)
        solution_path = dfs_solve(initial_state)

        self.assertIsNotNone(solution_path, "DFS should find a solution for (3,3)")
        self.assertIsInstance(solution_path, list)
        self.assertTrue(all(isinstance(s, GameState) for s in solution_path))

        # DFS doesn't guarantee shortest path, so don't assert length unless specific seed/ordering
        self.assertTrue(len(solution_path) >= 12, "DFS solution for (3,3) should have at least 12 states")

        self.assertEqual(solution_path[0], initial_state)
        self.assertTrue(solution_path[-1].is_win())

        for state in solution_path:
            self.assertTrue(state.is_valid(), f"State {state} in DFS path for (3,3) is invalid")

    def test_bfs_solve_2m_2c(self):
        initial_state = GameState(2, 2, True, initial_missionaries=2, initial_cannibals=2)
        solution_path = bfs_solve(initial_state)

        self.assertIsNotNone(solution_path, "BFS should find a solution for (2,2)")
        self.assertIsInstance(solution_path, list)
        # Known optimal for 2M, 2C is 5 moves (6 states)
        self.assertEqual(len(solution_path), 6, "BFS solution for (2,2) should have 6 states")
        self.assertTrue(solution_path[-1].is_win())
        for state in solution_path:
            self.assertTrue(state.is_valid(), f"State {state} in BFS path for (2,2) is invalid")

    def test_dfs_solve_2m_2c(self):
        initial_state = GameState(2, 2, True, initial_missionaries=2, initial_cannibals=2)
        solution_path = dfs_solve(initial_state)
        self.assertIsNotNone(solution_path, "DFS should find a solution for (2,2)")
        self.assertIsInstance(solution_path, list)
        self.assertTrue(len(solution_path) >= 6) # DFS path length for (2,2)
        self.assertTrue(solution_path[-1].is_win())
        for state in solution_path:
            self.assertTrue(state.is_valid(), f"State {state} in DFS path for (2,2) is invalid")

    def test_solvers_unsolvable_4m_4c(self):
        # 4M, 4C, k=2 is known to be unsolvable
        initial_state = GameState(4, 4, True, initial_missionaries=4, initial_cannibals=4)

        bfs_solution = bfs_solve(initial_state)
        self.assertIsNone(bfs_solution, "BFS should return None for unsolvable (4,4) case")

        dfs_solution = dfs_solve(initial_state)
        self.assertIsNone(dfs_solution, "DFS should return None for unsolvable (4,4) case")

    def test_solvers_already_solved_state(self):
        # Initial state is already the winning state
        # (0M, 0C, Boat Right) for a (3M,3C) game.
        initial_state = GameState(0, 0, False, initial_missionaries=3, initial_cannibals=3)
        self.assertTrue(initial_state.is_win())

        bfs_solution = bfs_solve(initial_state)
        self.assertIsNotNone(bfs_solution)
        self.assertEqual(len(bfs_solution), 1)
        self.assertEqual(bfs_solution[0], initial_state)

        dfs_solution = dfs_solve(initial_state)
        self.assertIsNotNone(dfs_solution)
        self.assertEqual(len(dfs_solution), 1)
        self.assertEqual(dfs_solution[0], initial_state)

    def test_solvers_invalid_initial_state(self):
        # Initial state where missionaries are outnumbered (1M, 2C on left)
        initial_state = GameState(1, 2, True, initial_missionaries=3, initial_cannibals=3)
        self.assertFalse(initial_state.is_valid()) # Ensure it's actually invalid for test setup

        bfs_solution = bfs_solve(initial_state)
        self.assertIsNone(bfs_solution, "BFS should return None for an invalid initial state")

        dfs_solution = dfs_solve(initial_state)
        self.assertIsNone(dfs_solution, "DFS should return None for an invalid initial state")

if __name__ == '__main__':
    unittest.main()
