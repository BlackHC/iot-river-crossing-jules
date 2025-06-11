import unittest
import sys
import os

# Adjust path to import from parent directory's 'game' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.environment import GameState, apply_action, POSSIBLE_ACTIONS

class TestGameState(unittest.TestCase):

    def test_initialization(self):
        state = GameState(3, 3, True, initial_missionaries=3, initial_cannibals=3, boat_capacity=2)
        self.assertEqual(state.missionaries_left, 3)
        self.assertEqual(state.cannibals_left, 3)
        self.assertTrue(state.boat_on_left)
        self.assertEqual(state.boat_capacity, 2)
        self.assertEqual(state.missionaries_right, 0)
        self.assertEqual(state.cannibals_right, 0)
        self.assertEqual(state.initial_missionaries, 3)
        self.assertEqual(state.initial_cannibals, 3)

        state_custom = GameState(2, 1, False, initial_missionaries=5, initial_cannibals=4, boat_capacity=3)
        self.assertEqual(state_custom.missionaries_left, 2)
        self.assertEqual(state_custom.cannibals_left, 1)
        self.assertFalse(state_custom.boat_on_left)
        self.assertEqual(state_custom.boat_capacity, 3)
        self.assertEqual(state_custom.missionaries_right, 3) # 5 - 2
        self.assertEqual(state_custom.cannibals_right, 3)   # 4 - 1

    def test_is_valid(self):
        # Standard initial state (3,3), cap 2
        state1 = GameState(3, 3, True, boat_capacity=2)
        self.assertTrue(state1.is_valid())

        # All on right bank (winning state is valid before checking win condition)
        state2 = GameState(0, 0, False, boat_capacity=2)
        self.assertTrue(state2.is_valid())

        # Missionaries outnumbered on left
        state_invalid_left = GameState(1, 2, True, boat_capacity=2)
        self.assertFalse(state_invalid_left.is_valid())
        state_invalid_left_boat_right = GameState(1, 2, False, boat_capacity=2) # Same bank state, boat elsewhere
        self.assertFalse(state_invalid_left_boat_right.is_valid())


        # Missionaries outnumbered on right
        state_invalid_right = GameState(2, 1, True, boat_capacity=2) # M=2,C=1 on Left; M=1,C=2 on Right
        self.assertFalse(state_invalid_right.is_valid())
        state_invalid_right_boat_left = GameState(2, 1, False, boat_capacity=2) # Same bank state, boat elsewhere
        self.assertFalse(state_invalid_right_boat_left.is_valid())

        # Only cannibals on a bank (valid)
        state_only_c_left = GameState(0, 2, True, boat_capacity=2)
        self.assertTrue(state_only_c_left.is_valid())
        state_only_c_right = GameState(3, 1, True, boat_capacity=2) # M=3,C=1 on Left; M=0,C=2 on Right
        self.assertTrue(state_only_c_right.is_valid())

        # Negative numbers (should not happen with apply_action, but test constructor effect)
        state_neg_m = GameState(-1, 3, True, 3, 3, boat_capacity=2)
        self.assertFalse(state_neg_m.is_valid()) # Fails due to negative counts
        state_neg_c = GameState(3, -1, True, 3, 3, boat_capacity=2)
        self.assertFalse(state_neg_c.is_valid()) # Fails due to negative counts

        # More people than initial (e.g. M_left > initial_M)
        state_overflow_m = GameState(4, 3, True, 3, 3, boat_capacity=2)
        self.assertFalse(state_overflow_m.is_valid()) # Fails due to M_left > initial_M
        state_overflow_c = GameState(3, 4, True, 3, 3, boat_capacity=2)
        self.assertFalse(state_overflow_c.is_valid()) # Fails due to C_left > initial_C

        # Valid intermediate state: (2M, 2C, Left), Boat Right, (1M, 1C, Right), cap 2
        state_intermediate = GameState(2,2,False, initial_missionaries=3, initial_cannibals=3, boat_capacity=2)
        self.assertTrue(state_intermediate.is_valid()) # 2M,2C Left | 1M,1C Right

    def test_is_win(self):
        # Standard winning state (3,3), cap 2
        win_state = GameState(0, 0, False, initial_missionaries=3, initial_cannibals=3, boat_capacity=2)
        self.assertTrue(win_state.is_win())

        # Not winning: initial state
        initial_state = GameState(3, 3, True, boat_capacity=2)
        self.assertFalse(initial_state.is_win())

        # Not winning: boat on wrong side
        state_boat_wrong = GameState(0, 0, True, boat_capacity=2)
        self.assertFalse(state_boat_wrong.is_win())

        # Not winning: some people still on left
        state_some_left = GameState(1, 1, False, boat_capacity=2)
        self.assertFalse(state_some_left.is_win())

        # Winning state for (2,2) game, cap 2
        win_state_22 = GameState(0,0,False, initial_missionaries=2, initial_cannibals=2, boat_capacity=2)
        self.assertTrue(win_state_22.is_win())
        # Mismatch initial counts, still uses default boat_capacity=2 for this instance
        self.assertFalse(GameState(0,0,False, initial_missionaries=3, initial_cannibals=2, boat_capacity=2).is_win())

    def test_apply_action(self):
        initial_state = GameState(3, 3, True, boat_capacity=2) # 3M, 3C, Boat L, Cap 2

        # 1. Valid move: (1M, 1C) L -> R with cap 2
        # Expected: 2M, 2C, Boat R | 1M, 1C. Cap 2.
        action1 = (1, 1)
        next_state1 = apply_action(initial_state, action1)
        self.assertIsNotNone(next_state1)
        self.assertEqual(next_state1.missionaries_left, 2)
        self.assertEqual(next_state1.cannibals_left, 2)
        self.assertFalse(next_state1.boat_on_left)
        self.assertEqual(next_state1.missionaries_right, 1)
        self.assertEqual(next_state1.cannibals_right, 1)
        self.assertEqual(next_state1.boat_capacity, 2)
        self.assertTrue(next_state1.is_valid())

        # 2. From next_state1 (2M,2C, B_R | 1M,1C, cap 2), move (1M) R -> L
        # Expected: 3M, 2C, Boat L | 0M, 1C. Cap 2.
        action2 = (1, 0)
        next_state2 = apply_action(next_state1, action2)
        self.assertIsNotNone(next_state2)
        self.assertEqual(next_state2.missionaries_left, 3)
        self.assertEqual(next_state2.cannibals_left, 2)
        self.assertTrue(next_state2.boat_on_left)
        self.assertEqual(next_state2.missionaries_right, 0)
        self.assertEqual(next_state2.cannibals_right, 1)
        self.assertEqual(next_state2.boat_capacity, 2)
        self.assertTrue(next_state2.is_valid())

        # 3. Invalid move: too many people in boat for capacity 2
        action_too_many_cap2 = (0, 3) # 3 people, cap is 2. This action tuple itself is invalid for generate_possible_actions for k=2
                                      # but apply_action should still reject it if passed directly.
        self.assertIsNone(apply_action(initial_state, action_too_many_cap2))
        action_zero = (0,0) # 0 people
        self.assertIsNone(apply_action(initial_state, action_zero))

        # Test with boat_capacity = 3
        initial_state_cap3 = GameState(3,3,True, boat_capacity=3)
        action_3_people = (2,1) # 3 people, valid for cap 3
        next_state_cap3_move = apply_action(initial_state_cap3, action_3_people)
        self.assertIsNotNone(next_state_cap3_move, "Should allow 3 people if boat_capacity is 3")
        if next_state_cap3_move: # Check state if move was successful
            self.assertEqual(next_state_cap3_move.missionaries_left, 1) # 3-2
            self.assertEqual(next_state_cap3_move.cannibals_left, 2)    # 3-1
            self.assertFalse(next_state_cap3_move.boat_on_left)
            self.assertEqual(next_state_cap3_move.boat_capacity, 3)

        action_4_people_cap3 = (2,2) # 4 people, cap is 3. Invalid.
        self.assertIsNone(apply_action(initial_state_cap3, action_4_people_cap3))


        # 4. Invalid move: not enough people on bank (cap 2)
        state_low_pop = GameState(1,1, True, initial_missionaries=3, initial_cannibals=3, boat_capacity=2)
        action_not_enough_m = (2,0)
        self.assertIsNone(apply_action(state_low_pop, action_not_enough_m))
        action_not_enough_c = (0,2)
        self.assertIsNone(apply_action(state_low_pop, action_not_enough_c))
        action_valid_for_low_pop = (1,1)
        self.assertIsNotNone(apply_action(state_low_pop,action_valid_for_low_pop))


        # 5. Move leading to invalid state (missionaries outnumbered) (cap 2)
        s1 = apply_action(initial_state, (0,2)) # (3,3,L,c2) -> (0,2) -> (3,1,R,c2) | (0,2) Valid
        self.assertIsNotNone(s1)
        self.assertEqual(s1.missionaries_left, 3)
        self.assertEqual(s1.cannibals_left, 1)

        s2 = apply_action(s1, (0,1)) # (3,1,R,c2) -> (0,1)R->L -> (3,2,L,c2) | (0,1) Valid
        self.assertIsNotNone(s2)
        self.assertEqual(s2.missionaries_left, 3)
        self.assertEqual(s2.cannibals_left, 2)

        # Initial: (3,3,L,c2). Action: (1M,0C) L->R
        # State: (2M,3C,R,c2) | (1M,0C). Invalid (2M,3C on left)
        action_leads_to_invalid = (1,0)
        self.assertIsNone(apply_action(initial_state, action_leads_to_invalid))

        # Test for not enough on bank from R to L
        s_tmp1 = apply_action(initial_state, (0,1)) # (3,3,L,c2) -> (0,1)L->R -> (3,2,R,c2) | (0,1)
        self.assertIsNotNone(s_tmp1)
        self.assertEqual(s_tmp1.missionaries_right, 0) # 0M on right bank
        self.assertEqual(s_tmp1.cannibals_right, 1)   # 1C on right bank

        self.assertIsNone(apply_action(s_tmp1, (1,0)), "Should be None, not enough M on right bank for (1,0) R->L")

    def test_state_equality_and_hash(self):
        s1 = GameState(3,3,True,3,3, boat_capacity=2)
        s2 = GameState(3,3,True,3,3, boat_capacity=2)
        s3 = GameState(2,3,True,3,3, boat_capacity=2) # Diff M_left
        s4 = GameState(3,3,False,3,3, boat_capacity=2) # Diff boat_on_left
        s5 = GameState(3,3,True,4,3, boat_capacity=2) # Diff initial_M
        s6 = GameState(3,3,True,3,3, boat_capacity=3) # Diff boat_capacity

        self.assertEqual(s1, s2)
        self.assertNotEqual(s1, s3)
        self.assertNotEqual(s1, s4)
        self.assertNotEqual(s1, s5)
        self.assertNotEqual(s1, s6) # Test boat_capacity difference
        self.assertNotEqual(s3, s4)

        self.assertEqual(hash(s1), hash(s2))
        self.assertNotEqual(hash(s1), hash(s6)) # Should be different due to boat_capacity

        state_set = {s1, s2}
        self.assertEqual(len(state_set), 1)
        state_set.add(s3)
        self.assertEqual(len(state_set), 2)
        state_set.add(s4)
        self.assertEqual(len(state_set), 3)
        state_set.add(s5)
        self.assertEqual(len(state_set), 4)
        state_set.add(s6)
        self.assertEqual(len(state_set), 5) # Added s6 with different capacity

    def test_get_valid_next_states(self):
        # Standard case: 3M, 3C, Boat L, Cap 2
        state = GameState(3, 3, True, initial_missionaries=3, initial_cannibals=3, boat_capacity=2)
        next_states = state.get_valid_next_states()
        self.assertIsInstance(next_states, list)
        for s_next in next_states:
            self.assertIsInstance(s_next, GameState)

        # Expected next states from (3,3,L,k=2):
        # Move (1M,1C) L->R: results in (2,2,R) - Valid
        # Move (0M,1C) L->R: results in (3,2,R) - Valid
        # Move (0M,2C) L->R: results in (3,1,R) - Valid
        # Move (1M,0C) L->R: results in (2,3,R) - Invalid (M outnumbered on L) -> should not be in list
        # Move (2M,0C) L->R: results in (1,3,R) - Invalid (M outnumbered on L) -> should not be in list

        # Let's check the specific states expected (order might vary based on generate_possible_actions)
        expected_next_configs = [
            (2,2,False), # from (1,1) L->R
            (3,2,False), # from (0,1) L->R
            (3,1,False)  # from (0,2) L->R
        ]
        actual_next_configs = sorted([(s.missionaries_left, s.cannibals_left, s.boat_on_left) for s in next_states])
        expected_next_configs_sorted = sorted(expected_next_configs)

        self.assertEqual(len(next_states), 3)
        self.assertEqual(actual_next_configs, expected_next_configs_sorted)

        # Test with capacity 1 from (3,3,L)
        state_k1 = GameState(3, 3, True, initial_missionaries=3, initial_cannibals=3, boat_capacity=1)
        next_states_k1 = state_k1.get_valid_next_states()
        # Possible moves: (1,0) or (0,1)
        # (1,0) L->R -> (2,3,R) - Invalid (M outnumbered on L)
        # (0,1) L->R -> (3,2,R) - Valid
        self.assertEqual(len(next_states_k1), 1)
        if len(next_states_k1) == 1:
            self.assertEqual((next_states_k1[0].missionaries_left, next_states_k1[0].cannibals_left, next_states_k1[0].boat_on_left), (3,2,False))

        # Test from a state with no valid moves
        # Example: M=1, C=1, Boat R. Initial M=1, C=1. Capacity 1. (M=0,C=0 on left, M=1,C=1 on right)
        # From (0,0,R, init_m=1, init_c=1, cap=1), only (1,0) or (0,1) can return R->L
        # (1,0) R->L -> (1,0,L). Valid.
        # (0,1) R->L -> (0,1,L). Valid.
        # This is not a "no moves" state.

        # A state that is valid, but any move leads to invalid.
        # (M=1, C=0, Boat_L | M=2, C=3, Boat_Cap=2) -> This state itself is invalid (2M,3C on right)
        # Consider (M=0,C=1, Boat_R | M=3,C=2, Boat_Cap=2). This state is valid.
        # Moves from R->L:
        # (1,0) -> (1,1,L) Valid
        # (0,1) -> (0,2,L) Valid
        # (2,0) -> (2,1,L) Valid
        # (0,2) -> (0,3,L) Valid
        # (1,1) -> (1,2,L) Valid
        # Still not a "no moves" state.
        # A true "no moves" state for M&C is rare if the state itself is valid, unless it's a win state already on the wrong side.
        # Let's use the (1M,1C,L, k=1) case. If it moves (0,1) L->R, state is (1,0,R).
        # state_no_progress = GameState(1,0,False, initial_missionaries=1, initial_cannibals=1, boat_capacity=1)
        # From (1,0,R), only (1,0) R->L or (0,0) (invalid by count)
        # (1,0) R->L -> (1,1,L). This is a valid move.
        # It seems my earlier reasoning that (1,1,k=1) is unsolvable is because it leads to cycles, not stuck states.

        # A state from which no valid moves can be made (because all lead to invalid states):
        # (M=1, C=1, BoatL | M=2, C=2, k=2). State is valid.
        # Moves L->R:
        # (1,0) -> (0,1,R | M=3,C=2). Left bank C>M. Invalid.
        # (0,1) -> (1,0,R | M=2,C=3). Right bank C>M. Invalid.
        # (1,1) -> (0,0,R | M=3,C=3). Valid. (Ah, this one has a valid move)

        # Let's try state (2,2,L, initial_M=2, initial_C=2, k=2)
        # Move (1,0) L->R -> (1,2,R). Invalid on Left.
        # Move (2,0) L->R -> (0,2,R). Valid.
        # Move (0,1) L->R -> (2,1,R). Invalid on Right.
        # Move (0,2) L->R -> (2,0,R). Valid.
        # Move (1,1) L->R -> (1,1,R). Valid.
        # Still not a good "no moves" example.
        # For now, testing non-empty list is primary. Test empty list if a clear scenario is found.
        # A winning state on the wrong side:
        state_win_wrong_side = GameState(0,0,True, initial_missionaries=3, initial_cannibals=3, boat_capacity=2)
        self.assertTrue(state_win_wrong_side.is_valid())
        self.assertFalse(state_win_wrong_side.is_win()) # Boat on left
        next_states_win_wrong_side = state_win_wrong_side.get_valid_next_states()
        # No one on left to move. So, no valid L->R moves.
        self.assertEqual(len(next_states_win_wrong_side), 0, "Should be no valid moves from a winning configuration on the wrong side of the river")


if __name__ == '__main__':
    unittest.main()
