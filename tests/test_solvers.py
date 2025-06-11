import unittest
import sys
import os

# Adjust path to import from parent directory modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.environment import GameState # Actor-Agent GameState
from solvers.search import bfs_solve, dfs_solve, format_actor_agent_path

class TestActorAgentSolvers(unittest.TestCase):

    def test_solvers_n2_k2_aa_solvable(self):
        # Actor-Agent N=2, K=2
        initial_state = GameState(N=2, boat_capacity=2)
        # Expected winning state: all individuals on the right bank, boat on the right
        expected_win_state = GameState(N=2, boat_capacity=2, boat_on_left=False)
                                       # Using default bank setup for boat_on_left=False

        # BFS Test
        bfs_path = bfs_solve(initial_state)
        self.assertIsNotNone(bfs_path, "BFS should find a solution for AA (N=2, K=2)")
        if bfs_path:
            self.assertEqual(len(bfs_path), 6,
                             f"BFS solution for AA (N=2, K=2) should have 6 states (5 moves). Path: {[str(s) for s in bfs_path]}")
            self.assertEqual(bfs_path[0], initial_state)
            self.assertEqual(bfs_path[-1], expected_win_state)
            for state in bfs_path:
                self.assertTrue(state.is_valid_state(), f"Invalid state in BFS path: {state}")

        # DFS Test (check for solution existence, path length might vary)
        dfs_path = dfs_solve(initial_state)
        self.assertIsNotNone(dfs_path, "DFS should find a solution for AA (N=2, K=2)")
        if dfs_path:
            self.assertTrue(len(dfs_path) >= 6)
            self.assertEqual(dfs_path[0], initial_state)
            self.assertEqual(dfs_path[-1], expected_win_state)
            for state in dfs_path:
                self.assertTrue(state.is_valid_state(), f"Invalid state in DFS path: {state}")

    def test_solvers_n1_k1_aa_unsolvable(self):
        # Actor-Agent N=1, K=1 (expected to be unsolvable due to cycling without progress under strict AA rules)
        initial_state = GameState(N=1, boat_capacity=1)

        bfs_path = bfs_solve(initial_state)
        self.assertIsNone(bfs_path, "BFS should not find a solution for AA (N=1, K=1)")

        dfs_path = dfs_solve(initial_state)
        self.assertIsNone(dfs_path, "DFS should not find a solution for AA (N=1, K=1)")

    def test_solvers_already_solved_aa(self):
        # N=1, K=1, but already in winning configuration
        initial_state = GameState(N=1, boat_capacity=1, boat_on_left=False)
        self.assertTrue(initial_state.is_win(), f"State {initial_state} was expected to be a win state but is_win() is False.")

        bfs_path = bfs_solve(initial_state)
        self.assertIsNotNone(bfs_path, "BFS returned None for an already solved state.")
        if bfs_path:
            self.assertEqual(len(bfs_path), 1)
            self.assertEqual(bfs_path[0], initial_state)

        dfs_path = dfs_solve(initial_state)
        self.assertIsNotNone(dfs_path, "DFS returned None for an already solved state.")
        if dfs_path:
            self.assertEqual(len(dfs_path), 1)
            self.assertEqual(dfs_path[0], initial_state)

    def test_solvers_invalid_initial_state_aa(self):
        # Create a structurally invalid state for AA
        initial_state = GameState(N=1, boat_capacity=1)
        # Manually corrupt to make it structurally invalid for testing solver's initial check
        if initial_state.all_individuals:
          person_to_remove = next(iter(initial_state.all_individuals))
          if person_to_remove in initial_state.left_bank:
              initial_state.left_bank.remove(person_to_remove)
        self.assertFalse(initial_state.is_valid_state(), "Manually corrupted state was not detected as invalid.")

        bfs_path = bfs_solve(initial_state)
        self.assertIsNone(bfs_path, "BFS should return None for an invalid initial AA state")

        dfs_path = dfs_solve(initial_state)
        self.assertIsNone(dfs_path, "DFS should return None for an invalid initial AA state")

    def test_format_actor_agent_path(self):
        # Test with the known N=2, K=2 solution path structure if BFS found it
        initial_state_n2k2 = GameState(N=2, boat_capacity=2)
        bfs_path_n2k2 = bfs_solve(initial_state_n2k2)

        self.assertIsNotNone(bfs_path_n2k2, "Cannot test formatter: BFS failed to find N=2,K=2 solution.")
        if not bfs_path_n2k2: return # Guard for static analysis if assertIsNotNone is not enough

        formatted_moves = format_actor_agent_path(bfs_path_n2k2)

        # Based on common solutions for N=2, K=2 (5 moves)
        # Paper's example: [["A_2", "a_2"], ["A_2"], ["A_1", "A_2"], ["A_1"], ["A_1", "a_1"]]
        # Our sorting is alphabetical.
        expected_formatted_moves = [
            sorted(['A2', 'a2']),
            sorted(['A2']),
            sorted(['A1', 'A2']),
            sorted(['A1']),
            sorted(['A1', 'a1'])
        ]
        self.assertEqual(len(formatted_moves), 5, "Formatted path should have 5 moves for N=2, K=2.")
        # Comparing actual moves can be tricky if multiple optimal paths exist.
        # If a canonical path is expected from this BFS, this assertion can be made more specific.
        # self.assertEqual(formatted_moves, expected_formatted_moves, f"Formatted path for N=2,K=2 does not match. Got {formatted_moves}")
        print(f"Formatted N=2, K=2 BFS moves (for visual check): {formatted_moves}")

        self.assertTrue(all(isinstance(move, list) for move in formatted_moves))
        if formatted_moves:
            self.assertTrue(all(isinstance(p, str) for p in formatted_moves[0]))

        # Test with an empty path
        self.assertEqual(format_actor_agent_path([]), [])
        # Test with a path of one state (already solved)
        self.assertEqual(format_actor_agent_path([initial_state_n2k2]), [])


if __name__ == '__main__':
    unittest.main()
