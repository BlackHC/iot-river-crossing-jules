class GameState:
    def __init__(self, missionaries_left, cannibals_left, boat_on_left,
                 initial_missionaries=3, initial_cannibals=3, boat_capacity=2):
        self.missionaries_left = missionaries_left
        self.cannibals_left = cannibals_left
        self.boat_on_left = boat_on_left
        self.initial_missionaries = initial_missionaries
        self.initial_cannibals = initial_cannibals
        self.boat_capacity = boat_capacity
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
                self.initial_cannibals == other.initial_cannibals and
                self.boat_capacity == other.boat_capacity)

    def __hash__(self):
        return hash((self.missionaries_left, self.cannibals_left, self.boat_on_left,
                     self.initial_missionaries, self.initial_cannibals, self.boat_capacity))

    def __str__(self):
        left_bank = f"L: M={self.missionaries_left}, C={self.cannibals_left}"
        right_bank = f"R: M={self.missionaries_right}, C={self.cannibals_right}"
        boat_pos = "<-B-" if self.boat_on_left else "-B->"
        return f"{left_bank} {boat_pos} {right_bank} (Cap: {self.boat_capacity})"

    def get_valid_next_states(self) -> list['GameState']:
        """
        Generates all valid successor states from the current state.
        """
        possible_next_states = []
        actions = generate_possible_actions(self.boat_capacity)

        for action in actions:
            new_state = apply_action(self, action) # self is the current state
            if new_state: # apply_action returns None if move is invalid or leads to invalid state
                possible_next_states.append(new_state)
        return possible_next_states

def generate_possible_actions(boat_capacity: int) -> list[tuple[int, int]]:
    """
    Generates a list of possible actions (number of missionaries, number of cannibals)
    that can be taken in a boat with a given capacity.

    Args:
        boat_capacity: The maximum number of people the boat can hold.

    Returns:
        A list of tuples (m, c) representing valid actions.
    """
    actions = []
    for m in range(boat_capacity + 1):  # Missionaries from 0 to boat_capacity
        for c in range(boat_capacity + 1 - m):  # Cannibals from 0 to boat_capacity - m
            if m + c > 0 and m + c <= boat_capacity:
                actions.append((m, c))
    return actions

def apply_action(state: GameState, action: tuple[int, int]) -> GameState | None:
    """
    Applies an action to the current state and returns a new state.
    Returns None if the action is invalid or results in an invalid state.
    """
    move_missionaries, move_cannibals = action
    people_in_boat = move_missionaries + move_cannibals

    if not (1 <= people_in_boat <= state.boat_capacity): # Use state.boat_capacity
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
                          state.initial_missionaries, state.initial_cannibals, state.boat_capacity)

    if new_state.is_valid():
        return new_state
    else:
        return None

if __name__ == '__main__':
    # Example Usage and Basic Test
    initial_state = GameState(3, 3, True, boat_capacity=2)
    print(f"Initial State: {initial_state}, Valid: {initial_state.is_valid()}")

    action_to_try = (1, 1) # Move 1M, 1C from Left to Right. Boat capacity 2.
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
    winning_state = GameState(0,0, False, initial_missionaries=3, initial_cannibals=3, boat_capacity=2)
    print(f"Winning State: {winning_state}, Valid: {winning_state.is_valid()}, Win: {winning_state.is_win()}")

    print("\nTesting losing state (more cannibals on one side):")
    # M=1, C=2, B=T | M=2, C=1
    losing_state_left = GameState(1,2, True, boat_capacity=2)
    print(f"Losing State (left): {losing_state_left}, Valid: {losing_state_left.is_valid()}")

    # M=2, C=1, B=F | M=1, C=2
    losing_state_right = GameState(2,1, False, boat_capacity=2)
    print(f"Losing State (right): {losing_state_right}, Valid: {losing_state_right.is_valid()}")

    # M=1, C=1, B=F | M=2, C=2  (boat on right)
    # Action: move 2C from L to R
    # The manual step-by-step example below can be simplified or adapted
    # to use get_valid_next_states for demonstration if desired.
    # For now, its direct use of apply_action is still fine as apply_action itself is unchanged.

    # Example of using get_valid_next_states:
    print(f"\nPossible next states from initial state ({initial_state}):")
    for i, next_s in enumerate(initial_state.get_valid_next_states()):
        print(f"Option {i+1}: {next_s}")

    # The long chain of s1, s2... s11 is a specific path test.
    # It can remain as is, as it tests apply_action directly.
    # If we wanted to test get_valid_next_states more, we might pick one of its outputs.

    print("\nTesting generate_possible_actions:") # This function remains useful internally
    print(f"Actions for boat_capacity=1: {generate_possible_actions(1)}")
    # Expected: [(0,1), (1,0)] or [(1,0),(0,1)]
    print(f"Actions for boat_capacity=2: {generate_possible_actions(2)}")
    # Expected: [(0,1), (0,2), (1,0), (1,1), (2,0)] in some order
    print(f"Actions for boat_capacity=3: {generate_possible_actions(3)}")
