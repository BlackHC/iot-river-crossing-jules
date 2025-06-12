import itertools

class GameState:
    def __init__(self, N: int, boat_capacity: int,
                 left_bank_individuals: set[str] | None = None,
                 right_bank_individuals: set[str] | None = None,
                 boat_on_left: bool = True):
        self.N = N
        self.boat_capacity = boat_capacity
        self.boat_on_left = boat_on_left

        self.actors = {f"a_{i+1}" for i in range(N)}
        self.agents = {f"A_{i+1}" for i in range(N)}
        self.all_individuals = self.actors.union(self.agents)

        if left_bank_individuals is None and right_bank_individuals is None:
            # Default initial setup
            if boat_on_left:
                self.left_bank = set(self.all_individuals)
                self.right_bank = set()
            else: # Typically used to construct a win state or specific scenario
                self.left_bank = set()
                self.right_bank = set(self.all_individuals)
        elif left_bank_individuals is not None and right_bank_individuals is not None:
            # Explicitly provided banks
            self.left_bank = set(left_bank_individuals) # Ensure it's a copy
            self.right_bank = set(right_bank_individuals) # Ensure it's a copy
        else:
            raise ValueError("Either both bank populations must be specified, or neither (for default initial setup).")

    @staticmethod
    def is_group_safe(group_individuals: set[str], all_actors_in_problem: set[str], all_agents_in_problem: set[str]) -> bool:
        """
        Checks if a group of individuals (on a bank or in a boat) is safe
        according to Actor-Agent rules.
        Rule: An actor (ax) can only be with other agents (Ay, Az) if its own agent (Ax) is also present.
              If Ax is not present, ax cannot be with any Ay (y!=x).
              If no actors are present, or only agents are present, it's safe by this rule.
        """
        actors_in_group = group_individuals.intersection(all_actors_in_problem)
        agents_in_group = group_individuals.intersection(all_agents_in_problem)

        if not actors_in_group: # No actors, so no violation possible by this rule
            return True

        for actor_id in actors_in_group: # e.g., "a1"
            own_agent_id = "A_" + actor_id[2:] # e.g., "A_1"
            if own_agent_id not in agents_in_group: # Actor's own agent is NOT present
                # Check if any *other* agent is present
                for other_agent_id in agents_in_group:
                    # No need to check other_agent_id != own_agent_id, because own_agent_id is not in agents_in_group
                    return False # Actor is with another agent, without its own agent present. Unsafe.
        return True

    def is_valid_state(self) -> bool:
        """
        Checks for overall state consistency and Actor-Agent safety rules on both banks.
        """
        # 1. Structural Validity Checks
        on_left_and_right = self.left_bank.intersection(self.right_bank)
        if len(on_left_and_right) > 0:
            return False # Someone is on both banks

        on_left_or_right = self.left_bank.union(self.right_bank)
        if on_left_or_right != self.all_individuals:
            return False # Some individuals are missing or extra individuals appeared

        # 2. Actor-Agent Safety Rules for each bank
        if not GameState.is_group_safe(self.left_bank, self.actors, self.agents):
            return False # Left bank is unsafe
        if not GameState.is_group_safe(self.right_bank, self.actors, self.agents):
            return False # Right bank is unsafe

        return True

    def is_win(self) -> bool:
        """Checks if all individuals are on the right bank and boat is also on right."""
        if not self.is_valid_state():
            return False
        return len(self.left_bank) == 0 and not self.boat_on_left and \
               len(self.right_bank) == 2 * self.N


    def __eq__(self, other):
        if not isinstance(other, GameState):
            return NotImplemented
        return (self.left_bank == other.left_bank and
                self.right_bank == other.right_bank and
                self.boat_on_left == other.boat_on_left and
                self.N == other.N and
                self.boat_capacity == other.boat_capacity)

    def __hash__(self):
        return hash((frozenset(self.left_bank), frozenset(self.right_bank),
                     self.boat_on_left, self.N, self.boat_capacity))

    def __str__(self):
        left_sorted = sorted(list(self.left_bank))
        right_sorted = sorted(list(self.right_bank))

        left_bank_str = str(left_sorted) if left_sorted else "[]"
        right_bank_str = str(right_sorted) if right_sorted else "[]"

        if self.boat_on_left:
            # Boat is on the Left bank, ready to move Right (L -> R)
            boat_str = "---B--->"
            # Position the boat graphic towards the left side of the gap
            boat_line = f"  {boat_str}            "
        else:
            # Boat is on the Right bank, ready to move Left (R -> L)
            boat_str = "<---B---"
            # Position the boat graphic towards the right side of the gap
            boat_line = f"            {boat_str}  "

        return (f"Left Bank:  {left_bank_str}\n"
                f"{boat_line}\n"
                f"Right Bank: {right_bank_str}")

    def get_valid_next_states(self) -> list['GameState']:
        """
        Generates all valid successor states from the current state for Actor-Agent puzzle.
        """
        valid_successors = []
        source_bank = self.left_bank if self.boat_on_left else self.right_bank

        for k_boat in range(1, self.boat_capacity + 1): # Number of people in boat
            for boat_occupants_tuple in itertools.combinations(source_bank, k_boat):
                boat_occupants_set = set(boat_occupants_tuple)

                # 1. Check boat safety
                if not GameState.is_group_safe(boat_occupants_set, self.actors, self.agents):
                    continue

                # 2. Create potential new bank configurations
                new_left_bank_set = set(self.left_bank)
                new_right_bank_set = set(self.right_bank)
                new_boat_on_left_val = not self.boat_on_left

                if self.boat_on_left: # Moving L -> R
                    new_left_bank_set -= boat_occupants_set
                    new_right_bank_set.update(boat_occupants_set)
                else: # Moving R -> L
                    new_right_bank_set -= boat_occupants_set
                    new_left_bank_set.update(boat_occupants_set)

                # 3. Create and validate the new state
                potential_next_state = GameState(N=self.N,
                                                 boat_capacity=self.boat_capacity,
                                                 left_bank_individuals=new_left_bank_set,
                                                 right_bank_individuals=new_right_bank_set,
                                                 boat_on_left=new_boat_on_left_val)

                if potential_next_state.is_valid_state():
                    valid_successors.append(potential_next_state)

        return valid_successors

# Old M&C related functions are now fully removed.

if __name__ == '__main__':
    print("Actor-Agent River Crossing Puzzle State Definition & Next States")

    # Initial state for N=2, K=2
    initial_state_aa = GameState(N=2, boat_capacity=2)
    print(f"\nInitial State (N={initial_state_aa.N}, K={initial_state_aa.boat_capacity}):\n{initial_state_aa}")
    print(f"Is valid: {initial_state_aa.is_valid_state()}")
    print(f"Is win: {initial_state_aa.is_win()}")

    # Manually construct a winning state for N=2, K=2
    win_state_aa = GameState(N=2, boat_capacity=2, boat_on_left=False)
    print(f"\nConstructed Winning State (N={win_state_aa.N}, K={win_state_aa.boat_capacity}):\n{win_state_aa}")
    print(f"Is valid: {win_state_aa.is_valid_state()}")
    print(f"Is win: {win_state_aa.is_win()}")

    # Test get_valid_next_states from initial state
    # print(f"\n--- Testing get_valid_next_states from: {initial_state_aa} ---")
    # The initial state string itself will be printed above, so this specific line might be verbose.
    # We'll still print the next states.
    print(f"\n--- Testing get_valid_next_states from initial N={initial_state_aa.N}, K={initial_state_aa.boat_capacity} state ---")
    next_possible_states = initial_state_aa.get_valid_next_states()
    print(f"Found {len(next_possible_states)} valid next states:")
    for i, state in enumerate(next_possible_states):
        print(f"State {i+1} (Valid: {state.is_valid_state()}):\n{state}")

    # Example of a state that would be structurally invalid (for is_valid_state test)
    corrupted_state_missing = GameState(N=2, boat_capacity=2)
    if "a_1" in corrupted_state_missing.left_bank: # Adjusted for new ID format
      corrupted_state_missing.left_bank.remove("a_1")
    print(f"\nCorrupted State ('a_1' missing, N={corrupted_state_missing.N}, K={corrupted_state_missing.boat_capacity}):\n{corrupted_state_missing}")
    print(f"Is valid (now includes safety): {corrupted_state_missing.is_valid_state()}")

    corrupted_state_duplicate = GameState(N=2, boat_capacity=2)
    # Ensure 'a_1' is in all_individuals and not on right_bank before adding
    if "a_1" in corrupted_state_duplicate.all_individuals and \
       "a_1" in corrupted_state_duplicate.left_bank and \
       "a_1" not in corrupted_state_duplicate.right_bank:
        corrupted_state_duplicate.right_bank.add("a_1") # This makes 'a_1' on both banks
    print(f"\nCorrupted State ('a_1' on both banks if N>=1, N={corrupted_state_duplicate.N}, K={corrupted_state_duplicate.boat_capacity}):\n{corrupted_state_duplicate}")
    print(f"Is valid (now includes safety): {corrupted_state_duplicate.is_valid_state()}")