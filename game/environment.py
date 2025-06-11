class GameState:
    def __init__(self, missionaries_left, cannibals_left, boat_on_left,
                 initial_missionaries=3, initial_cannibals=3):
        self.missionaries_left = missionaries_left
        self.cannibals_left = cannibals_left
        self.boat_on_left = boat_on_left
        self.initial_missionaries = initial_missionaries
        self.initial_cannibals = initial_cannibals
        self.missionaries_right = initial_missionaries - missionaries_left
        self.cannibals_right = initial_cannibals - cannibals_left

    def is_valid(self):
        """Checks if the current state is valid."""
        # Rule 1: Missionaries are not outnumbered by cannibals on the left bank
        if self.missionaries_left > 0 and self.missionaries_left < self.cannibals_left:
            return False
        # Rule 2: Missionaries are not outnumbered by cannibals on the right bank
        if self.missionaries_right > 0 and self.missionaries_right < self.cannibals_right:
            return False
        # Rule 3: Number of missionaries and cannibals must be non-negative
        if not (0 <= self.missionaries_left <= self.initial_missionaries and
                0 <= self.cannibals_left <= self.initial_cannibals and
                0 <= self.missionaries_right <= self.initial_missionaries and
                0 <= self.cannibals_right <= self.initial_cannibals):
            return False
        return True

    def is_win(self):
        """Checks if all missionaries and cannibals are on the right bank."""
        return self.missionaries_left == 0 and self.cannibals_left == 0 and \
               self.missionaries_right == self.initial_missionaries and \
               self.cannibals_right == self.initial_cannibals and \
               not self.boat_on_left

    def __eq__(self, other):
        if not isinstance(other, GameState):
            return NotImplemented
        return (self.missionaries_left == other.missionaries_left and
                self.cannibals_left == other.cannibals_left and
                self.boat_on_left == other.boat_on_left and
                self.initial_missionaries == other.initial_missionaries and
                self.initial_cannibals == other.initial_cannibals)

    def __hash__(self):
        return hash((self.missionaries_left, self.cannibals_left, self.boat_on_left,
                     self.initial_missionaries, self.initial_cannibals))

    def __str__(self):
        left_bank = f"L: M={self.missionaries_left}, C={self.cannibals_left}"
        right_bank = f"R: M={self.missionaries_right}, C={self.cannibals_right}"
        boat_pos = "<-B-" if self.boat_on_left else "-B->"
        return f"{left_bank} {boat_pos} {right_bank}"

# Possible actions: (missionaries_to_move, cannibals_to_move)
# Boat capacity is 2
POSSIBLE_ACTIONS = [
    (1, 0),  # 1 missionary
    (2, 0),  # 2 missionaries
    (0, 1),  # 1 cannibal
    (0, 2),  # 2 cannibals
    (1, 1)   # 1 missionary and 1 cannibal
]

def apply_action(state: GameState, action: tuple[int, int]) -> GameState | None:
    """
    Applies an action to the current state and returns a new state.
    Returns None if the action is invalid or results in an invalid state.
    """
    move_missionaries, move_cannibals = action
    people_in_boat = move_missionaries + move_cannibals

    if not (1 <= people_in_boat <= 2):
        # Invalid number of people in the boat
        return None

    if state.boat_on_left:
        # Moving from left to right
        if state.missionaries_left < move_missionaries or state.cannibals_left < move_cannibals:
            return None # Not enough people on the left bank

        new_ml = state.missionaries_left - move_missionaries
        new_cl = state.cannibals_left - move_cannibals
        new_boat_on_left = False
    else:
        # Moving from right to left
        if state.missionaries_right < move_missionaries or state.cannibals_right < move_cannibals:
            return None # Not enough people on the right bank

        new_ml = state.missionaries_left + move_missionaries
        new_cl = state.cannibals_left + move_cannibals
        new_boat_on_left = True

    new_state = GameState(new_ml, new_cl, new_boat_on_left,
                          state.initial_missionaries, state.initial_cannibals)

    if new_state.is_valid():
        return new_state
    else:
        return None

if __name__ == '__main__':
    # Example Usage and Basic Test
    initial_state = GameState(3, 3, True)
    print(f"Initial State: {initial_state}, Valid: {initial_state.is_valid()}")

    action_to_try = (1, 1) # Move 1M, 1C from Left to Right
    print(f"\nTrying action: Move {action_to_try[0]}M, {action_to_try[1]}C from Left to Right")
    next_state = apply_action(initial_state, action_to_try)
    if next_state:
        print(f"Next State: {next_state}, Valid: {next_state.is_valid()}, Win: {next_state.is_win()}")
    else:
        print("Action resulted in an invalid state or was not possible.")

    if next_state:
        action_to_try_back = (1,0) # Move 1M from Right to Left
        print(f"\nTrying action: Move {action_to_try_back[0]}M, {action_to_try_back[1]}C from Right to Left")
        state_after_return = apply_action(next_state, action_to_try_back)
        if state_after_return:
            print(f"State after return: {state_after_return}, Valid: {state_after_return.is_valid()}, Win: {state_after_return.is_win()}")
        else:
            print("Return action resulted in an invalid state or was not possible.")

    print("\nTesting winning state:")
    # M=0, C=0, B=F | M=3, C=3
    winning_state = GameState(0,0, False)
    print(f"Winning State: {winning_state}, Valid: {winning_state.is_valid()}, Win: {winning_state.is_win()}")

    print("\nTesting losing state (more cannibals on one side):")
    # M=1, C=2, B=T | M=2, C=1
    losing_state_left = GameState(1,2, True)
    print(f"Losing State (left): {losing_state_left}, Valid: {losing_state_left.is_valid()}")

    # M=2, C=1, B=F | M=1, C=2
    losing_state_right = GameState(2,1, False)
    print(f"Losing State (right): {losing_state_right}, Valid: {losing_state_right.is_valid()}")

    # M=1, C=1, B=F | M=2, C=2  (boat on right)
    # Action: move 2C from L to R
    # Initial: 3M, 3C, B=L
    # Action: (0,2) L->R
    # State: 3M, 1C, B=R | 0M, 2C (Valid)
    s1 = apply_action(initial_state, (0,2))
    print(f"\nStep 1: {s1}")
    if s1:
        # Action: (0,1) R->L
        # State: 3M, 2C, B=L | 0M, 1C (Valid)
        s2 = apply_action(s1, (0,1))
        print(f"Step 2: {s2}")
        if s2:
            # Action: (0,2) L->R
            # State: 3M, 0C, B=R | 0M, 3C (Valid)
            s3 = apply_action(s2, (0,2))
            print(f"Step 3: {s3}")
            if s3:
                 # Action: (0,1) R->L
                 # State: 3M, 1C, B=L | 0M, 2C (Valid) - This is s1, cycle. But it's s2.
                 s4 = apply_action(s3, (0,1))
                 print(f"Step 4: {s4}") # Should be 3M,1C,L -- 0M,2C. Oh, it's s1. No, s2.
                 if s4:
                    # Action: (2,0) L->R
                    # State: 1M, 1C, B=R | 2M, 2C (Valid)
                    s5 = apply_action(s4, (2,0))
                    print(f"Step 5: {s5}")
                    if s5:
                        # Action: (1,1) R->L
                        # State: 2M, 2C, B=L | 1M, 1C (Valid)
                        s6 = apply_action(s5, (1,1))
                        print(f"Step 6: {s6}")
                        if s6:
                            # Action: (2,0) L->R
                            # State: 0M, 2C, B=R | 3M, 1C (Valid)
                            s7 = apply_action(s6, (2,0))
                            print(f"Step 7: {s7}")
                            if s7:
                                # Action: (0,1) R->L
                                # State: 0M, 3C, B=L | 3M, 0C (Valid)
                                s8 = apply_action(s7, (0,1))
                                print(f"Step 8: {s8}")
                                if s8:
                                    # Action: (0,2) L->R
                                    # State: 0M, 1C, B=R | 3M, 2C (Valid)
                                    s9 = apply_action(s8, (0,2))
                                    print(f"Step 9: {s9}")
                                    if s9:
                                        # Action: (0,1) R->L
                                        # State: 0M, 2C, B=L | 3M, 1C (Valid) - This is s7
                                        s10 = apply_action(s9, (0,1))
                                        print(f"Step 10: {s10}")
                                        if s10:
                                            # Action: (0,2) L->R
                                            # State: 0M, 0C, B=R | 3M, 3C (WIN!)
                                            s11 = apply_action(s10, (0,2))
                                            print(f"Step 11: {s11}, Win: {s11.is_win() if s11 else 'Invalid'}")
