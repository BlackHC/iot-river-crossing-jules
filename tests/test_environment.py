import unittest
import sys
import os

# Adjust path to import from parent directory's 'game' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# GameState is now for Actor-Agent
from game.environment import GameState

class TestActorAgentGameState(unittest.TestCase):

    def test_initialization_actor_agent(self):
        # Test default initialization (all on left)
        state_n2_k2_default = GameState(N=2, boat_capacity=2)
        self.assertEqual(state_n2_k2_default.N, 2)
        self.assertEqual(state_n2_k2_default.boat_capacity, 2)
        self.assertTrue(state_n2_k2_default.boat_on_left)
        self.assertEqual(state_n2_k2_default.actors, {"a1", "a2"})
        self.assertEqual(state_n2_k2_default.agents, {"A1", "A2"})
        self.assertEqual(state_n2_k2_default.all_individuals, {"a1", "A1", "a2", "A2"})
        self.assertEqual(state_n2_k2_default.left_bank, {"a1", "A1", "a2", "A2"})
        self.assertEqual(state_n2_k2_default.right_bank, set())

        # Test initialization with boat on right (e.g., for a win state)
        state_n1_k1_boat_right = GameState(N=1, boat_capacity=1, boat_on_left=False)
        self.assertFalse(state_n1_k1_boat_right.boat_on_left)
        self.assertEqual(state_n1_k1_boat_right.left_bank, set())
        self.assertEqual(state_n1_k1_boat_right.right_bank, {"a1", "A1"})

        # Test initialization with specified banks
        left_b = {"a1", "A2"}
        right_b = {"A1", "a2"}
        state_n2_k2_custom = GameState(N=2, boat_capacity=2,
                                       left_bank_individuals=left_b,
                                       right_bank_individuals=right_b,
                                       boat_on_left=True)
        self.assertEqual(state_n2_k2_custom.left_bank, left_b)
        self.assertEqual(state_n2_k2_custom.right_bank, right_b)
        # Ensure it makes copies
        self.assertIsNot(state_n2_k2_custom.left_bank, left_b)
        left_b.add("a3") # Modify original after creation
        self.assertNotEqual(state_n2_k2_custom.left_bank, left_b)


    def test_is_group_safe_static(self):
        actors_n2 = {"a1", "a2"}
        agents_n2 = {"A1", "A2"}
        actors_n3 = {"a1", "a2", "a3"}
        agents_n3 = {"A1", "A2", "A3"}

        # Safe groups
        self.assertTrue(GameState.is_group_safe({"a1", "A1"}, actors_n2, agents_n2))
        self.assertTrue(GameState.is_group_safe({"a1", "A1", "A2"}, actors_n2, agents_n2)) # a1 with own agent, A2 fine
        self.assertTrue(GameState.is_group_safe({"A1", "A2"}, actors_n2, agents_n2)) # Only agents
        self.assertTrue(GameState.is_group_safe({"a1"}, actors_n2, agents_n2)) # Actor alone
        self.assertTrue(GameState.is_group_safe({"A1"}, actors_n2, agents_n2)) # Agent alone
        self.assertTrue(GameState.is_group_safe(set(), actors_n2, agents_n2)) # Empty group
        self.assertTrue(GameState.is_group_safe({"a1", "a2", "A1", "A2"}, actors_n2, agents_n2)) # All together

        # Unsafe groups
        self.assertFalse(GameState.is_group_safe({"a1", "A2"}, actors_n2, agents_n2)) # a1 with A2, without A1
        self.assertFalse(GameState.is_group_safe({"a1", "a2", "A1"}, actors_n3, agents_n3)) # a2 with A1, without A2
        self.assertFalse(GameState.is_group_safe({"a1", "A2", "A3"}, actors_n3, agents_n3)) # a1 with A2,A3 without A1

        # More complex cases
        self.assertTrue(GameState.is_group_safe({"a1","A1","a2","A2","A3"}, actors_n3, agents_n3)) # N=3, a1,a2,A1,A2,A3 safe
        self.assertFalse(GameState.is_group_safe({"a1","A2","a3","A3"}, actors_n3, agents_n3)) # a1 with A2 (no A1) unsafe

    def test_is_valid_state_actor_agent(self):
        # Structurally valid and safe
        s_initial_n2k2 = GameState(N=2, boat_capacity=2) # All on left, safe
        self.assertTrue(s_initial_n2k2.is_valid_state())

        s_win_n2k2 = GameState(N=2, boat_capacity=2, boat_on_left=False) # All on right, safe
        self.assertTrue(s_win_n2k2.is_valid_state())

        s_mixed_safe = GameState(N=2, boat_capacity=2,
                                 left_bank_individuals={"a1", "A1"},
                                 right_bank_individuals={"a2", "A2"},
                                 boat_on_left=True)
        self.assertTrue(s_mixed_safe.is_valid_state())

        # Structurally valid BUT unsafe (bank rules)
        s_unsafe_bank = GameState(N=2, boat_capacity=2,
                                  left_bank_individuals={"a1", "A2"},
                                  right_bank_individuals={"A1", "a2"},
                                  boat_on_left=True)
        self.assertFalse(s_unsafe_bank.is_valid_state(), f"State {s_unsafe_bank} should be invalid due to bank safety.")

        s_unsafe_one_actor = GameState(N=2, boat_capacity=2,
                                       left_bank_individuals={"a1", "A2", "a2"},
                                       right_bank_individuals={"A1"},
                                       boat_on_left=True)
        # Left bank: a1 with A2 (bad), a2 alone (ok). Overall left unsafe.
        self.assertFalse(s_unsafe_one_actor.is_valid_state(), f"State {s_unsafe_one_actor} should be invalid.")


        # Structurally invalid
        s_missing_person = GameState(N=2, boat_capacity=2)
        s_missing_person.left_bank.remove("a1") # a1 is missing
        self.assertFalse(s_missing_person.is_valid_state())

        s_extra_person = GameState(N=2, boat_capacity=2, left_bank_individuals={"a1","A1","a2","A2","a3"}, right_bank_individuals=set())
        self.assertFalse(s_extra_person.is_valid_state()) # a3 is not part of N=2

        s_person_on_both_banks = GameState(N=2, boat_capacity=2, left_bank_individuals={"a1","A1"}, right_bank_individuals={"a1","a2","A2"})
        self.assertFalse(s_person_on_both_banks.is_valid_state())


    def test_is_win_actor_agent(self):
        # Valid winning state
        s_win = GameState(N=2, boat_capacity=2, boat_on_left=False)
        self.assertTrue(s_win.is_win())

        # Not winning: initial state
        s_initial = GameState(N=2, boat_capacity=2)
        self.assertFalse(s_initial.is_win())

        # Not winning: boat on wrong side (all on right, but boat on left)
        s_boat_wrong = GameState(N=2, boat_capacity=2,
                                 left_bank_individuals=set(),
                                 right_bank_individuals={"a1","A1","a2","A2"},
                                 boat_on_left=True)
        self.assertFalse(s_boat_wrong.is_win())

        # Not winning: some people still on left
        s_some_left = GameState(N=2, boat_capacity=2,
                                left_bank_individuals={"a1"},
                                right_bank_individuals={"A1","a2","A2"},
                                boat_on_left=False)
        self.assertFalse(s_some_left.is_win())

        # Not winning: unsafe "winning" bank configuration (should be caught by is_valid_state in is_win)
        s_unsafe_win_config = GameState(N=2, boat_capacity=2, boat_on_left=False)
        s_unsafe_win_config.right_bank = {"a1", "A2", "a2", "A1"} # Structurally fine
        # Manually make right bank unsafe for this test (a1 with A2, a2 with A1 - actually safe if both pairs there)
        # Let's make it: a1, A2, a2 (A1 missing from right bank)
        s_unsafe_win_config.right_bank = {"a1", "A2", "a2"}
        s_unsafe_win_config.all_individuals = {"a1", "A1", "a2", "A2"} # Keep this consistent for structural check
        # This state is structurally invalid because A1 is missing. is_valid_state() catches this.
        self.assertFalse(s_unsafe_win_config.is_win())


    def test_get_valid_next_states_actor_agent(self):
        # N=2, K=2, Initial State (all on left, boat left)
        # Left: {a1,A1,a2,A2}, Right: {}, Boat: L
        s_initial_n2k2 = GameState(N=2, boat_capacity=2)
        next_states = s_initial_n2k2.get_valid_next_states()

        # Expected moves from (a1,A1,a2,A2 | --- L, k=2):
        # Boat: (a1,A1) -> L:{a2,A2} R:{a1,A1} B:R. Valid.
        # Boat: (a2,A2) -> L:{a1,A1} R:{a2,A2} B:R. Valid.
        # Boat: (a1,a2) -> unsafe boat.
        # Boat: (A1,A2) -> L:{a1,a2} R:{A1,A2} B:R. Valid.
        # Boat: (a1,A2) -> unsafe boat.
        # Boat: (a2,A1) -> unsafe boat.
        # Boat: (A1)    -> L:{a1,a2,A2} R:{A1} B:R. Valid. (Left bank: a1 with A2 (no A1)-unsafe, a2 with A2 (ok)) -> Left bank unsafe!
        # Boat: (A2)    -> L:{a1,A1,a2} R:{A2} B:R. Valid. (Left bank: a2 with A1 (no A2)-unsafe, a1 with A1 (ok)) -> Left bank unsafe!
        # Boat: (a1)    -> L:{A1,a2,A2} R:{a1} B:R. Valid. (Left bank: a2 with A1 (no A2), A1, A2) -> Left bank unsafe!
        # Boat: (a2)    -> L:{a1,A1,A2} R:{a2} B:R. Valid. (Left bank: a1 with A2 (no A1), A1, A2) -> Left bank unsafe!

        # Re-evaluating safe moves for N=2, K=2 from initial state:
        # L:{a1,A1,a2,A2} | R:{} Boat:L K=2
        # 1. Move (a1,A1) L->R. Boat safe. New L:{a2,A2} (safe). New R:{a1,A1} (safe). Valid.
        # 2. Move (a2,A2) L->R. Boat safe. New L:{a1,A1} (safe). New R:{a2,A2} (safe). Valid.
        # 3. Move (A1,A2) L->R. Boat safe. New L:{a1,a2} (safe). New R:{A1,A2} (safe). Valid.
        # 4. Move (a1,A2) L->R. Boat unsafe (a1 with A2, no A1).
        # 5. Move (a2,A1) L->R. Boat unsafe (a2 with A1, no A2).
        # 6. Move (a1,a2) L->R. Boat safe. New L:{A1,A2} (safe). New R:{a1,a2} (safe). Valid.
        # Single person moves:
        # 7. Move (A1) L->R. Boat safe. New L:{a1,a2,A2} (a1 w A2 (no A1), a2 w A2 (ok)) -> L unsafe.
        # 8. Move (A2) L->R. Boat safe. New L:{a1,A1,a2} (a2 w A1 (no A2), a1 w A1 (ok)) -> L unsafe.
        # 9. Move (a1) L->R. Boat safe. New L:{A1,a2,A2} (a2 w A2 (ok)) -> L safe. New R:{a1} safe. Valid.
        #10. Move (a2) L->R. Boat safe. New L:{A1,a1,A2} (a1 w A1 (ok)) -> L safe. New R:{a2} safe. Valid.

        # Total valid next states = 6.
        self.assertEqual(len(next_states), 6)
        for s_next in next_states:
            self.assertIsInstance(s_next, GameState)
            self.assertTrue(s_next.is_valid_state())

        # Test from a state with no valid moves: N=1, K=1, all on left.
        # L:{a1,A1} | R:{} Boat:L K=1
        # Move (a1) L->R. Boat safe. New L:{A1} (safe). New R:{a1} (safe). Valid.
        # Move (A1) L->R. Boat safe. New L:{a1} (safe). New R:{A1} (safe). Valid.
        # So, this state has moves.

        # A state that is a win state but boat on wrong side: (N=1, K=1)
        # L:{} | R:{a1,A1} Boat:L K=1
        s_win_boat_left = GameState(N=1, boat_capacity=1,
                                    left_bank_individuals=set(),
                                    right_bank_individuals={"a1","A1"},
                                    boat_on_left=True)
        self.assertTrue(s_win_boat_left.is_valid_state()) # Valid because banks are safe
        self.assertFalse(s_win_boat_left.is_win()) # Not win because boat on left
        next_states_from_win_boat_left = s_win_boat_left.get_valid_next_states()
        # Boat is on Left, Left bank is empty. No one to move.
        self.assertEqual(len(next_states_from_win_boat_left), 0)


    def test_state_equality_and_hash_actor_agent(self):
        # Using Actor-Agent GameState
        s1 = GameState(N=2, boat_capacity=2, boat_on_left=True)
        s2 = GameState(N=2, boat_capacity=2, boat_on_left=True) # Equal to s1
        s3 = GameState(N=2, boat_capacity=2, boat_on_left=False) # Different boat position
        s4 = GameState(N=1, boat_capacity=2, boat_on_left=True) # Different N
        s5 = GameState(N=2, boat_capacity=1, boat_on_left=True) # Different K

        left_b = {"a1", "A1"}
        right_b = {"a2", "A2"}
        s6 = GameState(N=2, boat_capacity=2,
                       left_bank_individuals=left_b,
                       right_bank_individuals=right_b,
                       boat_on_left=True) # Different bank setup

        self.assertEqual(s1, s2)
        self.assertNotEqual(s1, s3)
        self.assertNotEqual(s1, s4)
        self.assertNotEqual(s1, s5)
        self.assertNotEqual(s1, s6)

        self.assertEqual(hash(s1), hash(s2))
        # For non-equal objects, hashes *should ideally* be different but not strictly required.
        # We mainly care that equal objects have equal hashes.
        # self.assertNotEqual(hash(s1), hash(s3)) # This might collide but unlikely for these changes

        state_set = {s1, s2, s3, s4, s5, s6}
        self.assertEqual(len(state_set), 5) # s1 and s2 are the same

if __name__ == '__main__':
    unittest.main()
