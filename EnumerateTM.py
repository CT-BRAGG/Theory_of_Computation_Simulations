"""
Theory of Comp: Enumerate TM
author: Carson Bragg
date: Nov 11, 2025
"""

from itertools import product
from typing import Final

INPUT_ALPHABET: Final[list] = ['a', 'b']           
TAPE_ALPHABET: Final[list] = ['a', 'b', '_']       
MOVES: Final[list] = ['L', 'R']                    
ENUMERATATION_COUNT: Final[int] = 20

def build_trans_table(states):
    # Constructs an empty table of transition functions
    # consiting of every combination of state and character
    # from the tape alphabet.
    trans_table = []
    
    for s in states:
        for sym in TAPE_ALPHABET:
            trans_table.append((s, sym))

    return trans_table

def establish_rules(valid_next_states):
    # Creates a list of all combinations of the tape 
    # character to be written, the direction to move
    # the tape head, and the state the tm changes to.
    rules = []

    for nxt_st in valid_next_states:
        for tape_char in TAPE_ALPHABET:
            for direction in MOVES:
                rules.append((nxt_st, tape_char, direction))

    return rules

def enumerate_tms():
    # Generator that enumerates all Turing machines over 
    # input alphabet {a, b} and tape alphabet {a, b, _}.
    #
    # Each machine is represented as a dict with:
    #      {
    #        'num_states': n,
    #        'start_state': 0,
    #        'blank': '_',
    #        'transitions': (state, symbol) >> (valid_next_state, write_symbol, move)
    #      }
    num_states = 1

    while True:
        # builds list of states from 0 to number of states
        states = list(range(num_states)) 
        valid_next_states = states + ['HALT']

        # builds an empty transition table of TM
        trans_table = build_trans_table(states)
        
        rules = establish_rules(valid_next_states)

        for combo in product(rules, repeat=len(trans_table)):
            transitions = {}
            for (pos, rule) in zip(trans_table, combo):
                state, sym = pos
                nxt_st, tape_Char, direction = rule
                transitions[(state, sym)] = (nxt_st, tape_char, direction)

            tm = {
                'num_states': num_states,
                'start_state': 0,
                'blank': '_',
                'transitions': transitions
            }
            yield tm

        num_states += 1

def print_tm(tm, index):
    # Prints out a single TM in a readable format.
    print(f"TM #{index}")
    print(f"  States Count: {tm['num_states']}")
    print(f"  States: {list(range(tm['num_states']))}")
    print(f"  Start state: {tm['start_state']}")
    print(f"  Blank symbol: {tm['blank']}")
    print("  Transitions:")

    # Sort by state then symbol
    for (state, sym), (nxt_st, tape_char, direction) in sorted(tm['transitions'].items()):
        if ns == 'HALT':
            print(f"    δ(q{state}, {sym}) = HALT")
        else:
            print(f"    δ(q{state}, {sym}) = (q{nxt_st}, {tape_char}, {direction})")
    print()

def main():
    # Starting point of Program Execution
    tm_generator = enumerate_tms()

    print(f"\nFirst {ENUMERATATION_COUNT} Turning "+
            "Machines with {a,b} as \nthe alphabet "+
            "and {a,b,_} as the tape alphabet.\n")

    for i in range(1, ENUMERATATION_COUNT+1):
        tm = next(tm_generator)
        print_tm(tm, i)

if __name__ == "__main__":
    main()
