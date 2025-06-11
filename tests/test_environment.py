import unittest
import sys
import os

# Adjust path to import from parent directory's 'game' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.environment import GameState, apply_action, POSSIBLE_ACTIONS

class TestGameState(unittest.TestCase):

    def test_initialization(self):
        state = GameState(3, 3, True, initial_missionaries=3, initial_cannibals=3)
        self.assertEqual(state.missionaries_left, 3)
        self.assertEqual(state.cannibals_left, 3)
        self.assertTrue(state.boat_on_left)
        self.assertEqual(state.missionaries_right, 0)
        self.assertEqual(state.cannibals_right, 0)
        self.assertEqual(state.initial_missionaries, 3)
        self.assertEqual(state.initial_cannibals, 3)

        state_custom = GameState(2, 1, False, initial_missionaries=5, initial_cannibals=4)
        self.assertEqual(state_custom.missionaries_left, 2)
        self.assertEqual(state_custom.cannibals_left, 1)
        self.assertFalse(state_custom.boat_on_left)
        self.assertEqual(state_custom.missionaries_right, 3) # 5 - 2
        self.assertEqual(state_custom.cannibals_right, 3)   # 4 - 1

    def test_is_valid(self):
        # Standard initial state (3,3)
        state1 = GameState(3, 3, True)
        self.assertTrue(state1.is_valid())

        # All on right bank (winning state is valid before checking win condition)
        state2 = GameState(0, 0, False)
        self.assertTrue(state2.is_valid())

        # Missionaries outnumbered on left
        state_invalid_left = GameState(1, 2, True)
        self.assertFalse(state_invalid_left.is_valid())
        state_invalid_left_boat_right = GameState(1, 2, False) # Same bank state, boat elsewhere
        self.assertFalse(state_invalid_left_boat_right.is_valid())


        # Missionaries outnumbered on right
        state_invalid_right = GameState(2, 1, True) # M=2,C=1 on Left; M=1,C=2 on Right
        self.assertFalse(state_invalid_right.is_valid())
        state_invalid_right_boat_left = GameState(2, 1, False) # Same bank state, boat elsewhere
        self.assertFalse(state_invalid_right_boat_left.is_valid())

        # Only cannibals on a bank (valid)
        state_only_c_left = GameState(0, 2, True)
        self.assertTrue(state_only_c_left.is_valid())
        state_only_c_right = GameState(3, 1, True) # M=3,C=1 on Left; M=0,C=2 on Right
        self.assertTrue(state_only_c_right.is_valid())

        # Negative numbers (should not happen with apply_action, but test constructor effect)
        # GameState constructor doesn't directly prevent this if numbers are wrong, relies on calculation
        # However, initial_missionaries/cannibals are used for right side calculation
        # Let's test states that could arise from bad subtractions if apply_action was flawed
        state_neg_m = GameState(-1, 3, True, 3, 3)
        self.assertFalse(state_neg_m.is_valid()) # Fails due to negative counts
        state_neg_c = GameState(3, -1, True, 3, 3)
        self.assertFalse(state_neg_c.is_valid()) # Fails due to negative counts

        # More people than initial (e.g. M_left > initial_M)
        state_overflow_m = GameState(4, 3, True, 3, 3)
        self.assertFalse(state_overflow_m.is_valid()) # Fails due to M_left > initial_M
        state_overflow_c = GameState(3, 4, True, 3, 3)
        self.assertFalse(state_overflow_c.is_valid()) # Fails due to C_left > initial_C

        # Valid intermediate state: (2M, 2C, Left), Boat Right, (1M, 1C, Right)
        state_intermediate = GameState(2,2,False, initial_missionaries=3, initial_cannibals=3)
        self.assertTrue(state_intermediate.is_valid()) # 2M,2C Left | 1M,1C Right

    def test_is_win(self):
        # Standard winning state (3,3)
        win_state = GameState(0, 0, False, initial_missionaries=3, initial_cannibals=3)
        self.assertTrue(win_state.is_win())

        # Not winning: initial state
        initial_state = GameState(3, 3, True)
        self.assertFalse(initial_state.is_win())

        # Not winning: boat on wrong side
        state_boat_wrong = GameState(0, 0, True)
        self.assertFalse(state_boat_wrong.is_win())

        # Not winning: some people still on left
        state_some_left = GameState(1, 1, False)
        self.assertFalse(state_some_left.is_win())

        # Winning state for (2,2) game
        win_state_22 = GameState(0,0,False, initial_missionaries=2, initial_cannibals=2)
        self.assertTrue(win_state_22.is_win())
        self.assertFalse(GameState(0,0,False, initial_missionaries=3, initial_cannibals=2).is_win()) # Mismatch initial

    def test_apply_action(self):
        initial_state = GameState(3, 3, True) # 3M, 3C, Boat L

        # 1. Valid move: (1M, 1C) L -> R
        # Expected: 2M, 2C, Boat R | 1M, 1C
        action1 = (1, 1)
        next_state1 = apply_action(initial_state, action1)
        self.assertIsNotNone(next_state1)
        self.assertEqual(next_state1.missionaries_left, 2)
        self.assertEqual(next_state1.cannibals_left, 2)
        self.assertFalse(next_state1.boat_on_left)
        self.assertEqual(next_state1.missionaries_right, 1)
        self.assertEqual(next_state1.cannibals_right, 1)
        self.assertTrue(next_state1.is_valid())

        # 2. From next_state1 (2M,2C, B_R | 1M,1C), move (1M) R -> L
        # Expected: 3M, 2C, Boat L | 0M, 1C
        action2 = (1, 0)
        next_state2 = apply_action(next_state1, action2)
        self.assertIsNotNone(next_state2)
        self.assertEqual(next_state2.missionaries_left, 3)
        self.assertEqual(next_state2.cannibals_left, 2)
        self.assertTrue(next_state2.boat_on_left)
        self.assertEqual(next_state2.missionaries_right, 0)
        self.assertEqual(next_state2.cannibals_right, 1)
        self.assertTrue(next_state2.is_valid())

        # 3. Invalid move: too many people in boat (3C)
        action_too_many = (0, 3) # Not in POSSIBLE_ACTIONS, but test apply_action directly
        self.assertIsNone(apply_action(initial_state, action_too_many))
        action_zero = (0,0)
        self.assertIsNone(apply_action(initial_state, action_zero))


        # 4. Invalid move: not enough people on bank
        # State: 1M, 1C, Boat L | 2M, 2C. Try to move 2M from Left.
        state_low_pop = GameState(1,1, True, initial_missionaries=3, initial_cannibals=3)
        action_not_enough_m = (2,0)
        self.assertIsNone(apply_action(state_low_pop, action_not_enough_m))
        action_not_enough_c = (0,2)
        self.assertIsNone(apply_action(state_low_pop, action_not_enough_c))
        action_not_enough_both = (1,1) # This one is valid for state_low_pop
        self.assertIsNotNone(apply_action(state_low_pop,action_not_enough_both))


        # 5. Move leading to invalid state (missionaries outnumbered)
        # State: 3M, 3C, Boat L. Action: (0C, 2C) L -> R
        # Result: 3M, 1C, Boat R | 0M, 2C (This state is valid)
        s1 = apply_action(initial_state, (0,2))
        self.assertIsNotNone(s1)
        self.assertEqual(s1.missionaries_left, 3)
        self.assertEqual(s1.cannibals_left, 1)
        self.assertFalse(s1.boat_on_left)

        # From s1 (3M, 1C, Boat R | 0M, 2C). Action: (0M, 1C) R -> L
        # Result: 3M, 2C, Boat L | 0M, 1C (This state is valid)
        s2 = apply_action(s1, (0,1))
        self.assertIsNotNone(s2)
        self.assertEqual(s2.missionaries_left, 3)
        self.assertEqual(s2.cannibals_left, 2)
        self.assertTrue(s2.boat_on_left)

        # From s2 (3M, 2C, Boat L | 0M, 1C). Action: (1M, 0C) L -> R
        # Result: 2M, 2C, Boat R | 1M, 1C (This state is valid)
        # This is next_state1, which is fine.

        # Let's find a move that directly leads to an invalid state:
        # Initial: 3M, 3C, Boat L. Action: (1M, 0C) L->R
        # State: 2M, 3C, Boat R | 1M, 0C. This is invalid (2M, 3C on left)
        action_leads_to_invalid = (1,0)
        self.assertIsNone(apply_action(initial_state, action_leads_to_invalid))

        # Initial: 3M, 3C, Boat L. Action: (0M, 1C) L->R
        # State: 3M, 2C, Boat R | 0M, 1C. This is valid.
        # Let this be s_tmp1
        s_tmp1 = apply_action(initial_state, (0,1))
        self.assertIsNotNone(s_tmp1)
        self.assertEqual(s_tmp1.missionaries_left, 3)
        self.assertEqual(s_tmp1.cannibals_left, 2)
        self.assertFalse(s_tmp1.boat_on_left) # Boat on Right
        self.assertEqual(s_tmp1.missionaries_right, 0)
        self.assertEqual(s_tmp1.cannibals_right, 1)

        # From s_tmp1 (3M,2C, B_R | 0M,1C). Action (1M,0C) R->L
        # State: (3M+1M), (2C+0C), B_L | (0M-1M), (1C-0C) -> this logic is wrong in comment
        # State: (M_L+1M), (C_L+0C), B_L. M_R will be M_Initial - (M_L+1M)
        # (3+1)M, 2C, B_L -> 4M, 2C on left. Right: (3-4)=-1M, (3-2)=1C. This is invalid by numbers.
        # apply_action checks for enough people on source bank (right)
        # s_tmp1 has 0M, 1C on right. So (1,0) R->L is not possible.
        self.assertIsNone(apply_action(s_tmp1, (1,0))) # Not enough M on right bank.

    def test_state_equality_and_hash(self):
        s1 = GameState(3,3,True,3,3)
        s2 = GameState(3,3,True,3,3)
        s3 = GameState(2,3,True,3,3)
        s4 = GameState(3,3,False,3,3)
        s5 = GameState(3,3,True,4,3) # Different initial counts

        self.assertEqual(s1, s2)
        self.assertNotEqual(s1, s3)
        self.assertNotEqual(s1, s4)
        self.assertNotEqual(s1, s5)
        self.assertNotEqual(s3, s4)

        self.assertEqual(hash(s1), hash(s2))
        # It's not strictly required for non-equal objects to have different hashes,
        # but good hash functions usually achieve this. We mainly care that equal objects have equal hashes.
        # self.assertNotEqual(hash(s1), hash(s3)) # Can't guarantee this

        # Test with a set
        state_set = {s1, s2}
        self.assertEqual(len(state_set), 1)
        state_set.add(s3)
        self.assertEqual(len(state_set), 2)
        state_set.add(s4)
        self.assertEqual(len(state_set), 3)
        state_set.add(s5)
        self.assertEqual(len(state_set), 4)


if __name__ == '__main__':
    unittest.main()
