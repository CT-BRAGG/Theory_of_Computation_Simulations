'''
Theory of Comp: Validate TM
author: Carson Bragg
date: nov 10, 2025
'''

from itertools import product
from typing import Final

# Global symbols for input alphabet, tape alphabet, and head moves
INPUT_ALPHABET: Final[list] = ['a', 'b']
TAPE_ALPHABET: Final[list] = ['a', 'b', '_']
MOVES: Final[list] = ['L', 'R']

def build_trans_table(states):
    # Build all (state, tape_symbol) pairs for the transition table
    trans_table = []
    for s in states:
        for sym in TAPE_ALPHABET:
            trans_table.append((s, sym))
    return trans_table

def establish_rules(valid_next_states):
    # Build all possible (next_state, write_symbol, move) rules
    rules = []
    for nxt_st in valid_next_states:
        for tape_char in TAPE_ALPHABET:
            for direction in MOVES:
                rules.append((nxt_st, tape_char, direction))
    return rules

def enumerate_tms():
    # Infinite generator that enumerates Turing machines by number of states
    num_states = 1
    while True:
        states = list(range(num_states))
        valid_next_states = states + ['HALT']
        trans_table = build_trans_table(states)
        rules = establish_rules(valid_next_states)

        # Assign a rule to every (state, symbol) position
        for combo in product(rules, repeat=len(trans_table)):
            transitions = {}
            for pos, rule in zip(trans_table, combo):
                state, sym = pos
                nxt_st, tape_char, direction = rule
                transitions[(state, sym)] = (nxt_st, tape_char, direction)

            # Build TM description dictionary
            tm = {
                'num_states': num_states,
                'start_state': 0,
                'blank': '_',
                'transitions': transitions
            }
            yield tm

        num_states += 1

def print_tm(tm, index):
    # Print TM header information and full transition function
    print(f"TM #{index}")
    print(f"  States Count: {tm['num_states']}")
    print(f"  States: {list(range(tm['num_states']))}")
    print(f"  Start state: {tm['start_state']}")
    print(f"  Blank symbol: {tm['blank']}")
    print("  Transitions:")
    for item in sorted(tm['transitions'].items()):
        (state, sym), (nxt_st, tape_char, direction) = item
        if nxt_st == 'HALT':
            print(f"    δ(q{state}, {sym}) = HALT")
        else:
            print(f"    δ(q{state}, {sym}) = (q{nxt_st}, {tape_char}, {direction})")
    print()

def validate_tm(tm):
    # Check for required keys in TM description
    if 'num_states' not in tm:
        return 0
    if 'start_state' not in tm:
        return 0
    if 'blank' not in tm:
        return 0
    if 'transitions' not in tm:
        return 0

    num_states = tm['num_states']
    start_state = tm['start_state']
    blank = tm['blank']
    transitions = tm['transitions']

    # Basic type and range checks for number of states
    if not isinstance(num_states, int):
        return 0
    if num_states <= 0:
        return 0

    states = list(range(num_states))

    # Check start state, blank symbol, and transitions container
    if start_state not in states:
        return 0
    if blank not in TAPE_ALPHABET:
        return 0
    if not isinstance(transitions, dict):
        return 0

    # Check that each key is a valid (state, symbol) pair
    for key in transitions:
        if not isinstance(key, tuple):
            return 0
        if len(key) != 2:
            return 0

        state, sym = key

        if state not in states:
            return 0
        if sym not in TAPE_ALPHABET:
            return 0

    # Check that every (state, symbol) pair appears in transitions
    for s in states:
        for sym in TAPE_ALPHABET:
            if (s, sym) not in transitions:
                return 0

    # Check structure and contents of transition values
    for key in transitions:
        value = transitions[key]
        if not isinstance(value, tuple):
            return 0
        if len(value) != 3:
            return 0

        nxt_st, tape_char, direction = vaue

        if nxt_st != 'HALT' and nxt_st not in states:
            return 0
        if tape_char not in TAPE_ALPHABET:
            return 0
        if direction not in MOVES:
            return 0

    return 1

def make_invalid_missing_transition(tm):
    # Create TM copy with one transition removed
    invalid_transitions = dict(tm['transitions'])
    keys = list(invalid_transitions.keys())

    if keys:
        first_key = keys[0]
        del invalid_transitions[first_key]

    invalid_tm = {
        'num_states': tm['num_states'],
        'start_state': tm['start_state'],
        'blank': tm['blank'],
        'transitions': invalid_transitions
    }

    return invalid_tm

def make_invalid_blank_symbol(tm):
    # Create TM copy with an invalid blank symbol
    invalid_tm = {
        'num_states': tm['num_states'],
        'start_state': tm['start_state'],
        'blank': 'x',
        'transitions': dict(tm['transitions'])
    }

    return invalid_tm

def display_start_msg():
    # Print short description of program behavior
    print("\nThis program validates Turing machines over \n"+
            "the tape alphabet {a, b, _} by checking that\n"+
            "their states, transitions, and symbols are \n"+
            "well-formed. It then applies this validator to several\n"+
            "example machines and prints each machine definition\n"+
            "along with whether it is valid (1) or invalid (0).\n")

def main():
    # Build example machines and run validation
    machines = []
    tm_generator = enumerate_tms()

    display_start_msg()

    valid_tm_1 = next(tm_generator)
    valid_tm_2 = next(tm_generator)
    invalid_tm_1 = make_invalid_missing_transition(valid_tm_1)
    invalid_tm_2 = make_invalid_blank_symbol(valid_tm_2)

    machines.append(("Valid example 1", valid_tm_1))
    machines.append(("Valid example 2", valid_tm_2))
    machines.append(("Invalid example 1", invalid_tm_1))
    machines.append(("Invalid example 2", invalid_tm_2))

    index = 1
    for label, machine in machines:
        print(label)
        print_tm(machine, index)

        result = validate_tm(machine)
        print(f"  result: {result}\n")

        index += 1

if __name__ == "__main__":
    main()



