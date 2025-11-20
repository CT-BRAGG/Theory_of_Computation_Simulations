'''
Theory of Comp: Convert NFA to DFA
author: Carson Bragg
date: nov 10, 2025
'''

from typing import Final

# Global symbols for input alphabet, tape alphabet, and head moves
INPUT_ALPHABET: Final[list] = ['a', 'b']
TAPE_ALPHABET: Final[list] = ['a', 'b', '_']
MOVES: Final[list] = ['L', 'R']

def epsilon_closure(nfa, state_set):
    # Compute epsilon-closure for a set of NFA states
    closure = set(state_set)
    stack = list(state_set)

    while stack:
        state = stack.pop()
        key = (state, 'eps')

        if key in nfa['transitions']:
            next_states = nfa['transitions'][key]

            for nxt in next_states:
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)

    return closure

def move_nfa(nfa, state_set, symbol):
    # Compute NFA move set on a given input symbol
    result = set()

    for state in state_set:
        key = (state, symbol)
        if key in nfa['transitions']:
            next_states = nfa['transitions'][key]
            for nxt in next_states:
                result.add(nxt)

    return result

def nfa_to_dfa(nfa):
    # Convert NFA description to equivalent DFA description
    start_state = nfa['start_state']
    alphabet = nfa['alphabet']
    accept_states_nfa = set(nfa['accept_states'])

    # Compute start subset as epsilon-closure of NFA start state
    start_closure = epsilon_closure(nfa, {start_state})

    # Map subsets of NFA states to DFA state indices
    subset_to_index = {}
    subsets = []

    start_frozen = frozenset(start_closure)
    subset_to_index[start_frozen] = 0
    subsets.append(start_closure)

    # Store DFA transitions and accept states
    dfa_transitions = {}
    dfa_accept_states = set()

    index = 0
    while index < len(subsets):
        subset = subsets[index]
        current_index = index

        # Build transitions for each input symbol from current subset
        for symbol in alphabet:
            move_set = move_nfa(nfa, subset, symbol)
            if move_set:
                target_closure = epsilon_closure(nfa, move_set)
            else:
                target_closure = set()

            target_frozen = frozenset(target_closure)
            if target_frozen not in subset_to_index:
                new_index = len(subsets)
                subset_to_index[target_frozen] = new_index
                subsets.append(target_closure)
            next_index = subset_to_index[target_frozen]
            dfa_transitions[(current_index, symbol)] = next_index

        # Mark DFA state as accepting if subset contains an NFA accept state
        for s in subset:
            if s in accept_states_nfa:
                dfa_accept_states.add(current_index)
                break

        index += 1

    # Build DFA structure from collected data
    dfa_states = list(range(len(subsets)))
    dfa = {
        'states': dfa_states,
        'alphabet': list(alphabet),
        'start_state': 0,
        'accept_states': sorted(list(dfa_accept_states)),
        'transitions': dfa_transitions
    }

    return dfa

def dfa_to_tm_decider(dfa):
    # Convert DFA description to a Turing machine decider
    dfa_states = dfa['states']
    dfa_alphabet = dfa['alphabet']
    dfa_start = dfa['start_state']
    dfa_accept_states = set(dfa['accept_states'])

    # Reserve two extra states for accept and reject
    num_dfa_states = len(dfa_states)
    accept_state = num_dfa_states
    reject_state = num_dfa_states + 1

    tm_transitions = {}

    # Build TM transitions for every DFA state and input symbol
    for state in dfa_states:
        for symbol in INPUT_ALPHABET:
            if symbol in dfa_alphabet:
                key = (state, symbol)
                if key in dfa['transitions']:
                    nxt_st = dfa['transitions'][key]
                else:
                    nxt_st = reject_state
            else:
                nxt_st = reject_state

            tape_char = symbol
            direction = 'R'
            tm_transitions[(state, symbol)] = (nxt_st, tape_char, direction)

        # Handle blank symbol at the end of the input
        key_blank = (state, '_')
        tape_char_blank = '_'
        if state in dfa_accept_states:
            nxt_st_blank = accept_state
        else:
            nxt_st_blank = reject_state
        direction_blank = 'R'
        tm_transitions[key_blank] = (nxt_st_blank, tape_char_blank, direction_blank)

    # Build TM structure for the decider
    tm_states = list(range(num_dfa_states + 2))
    tm = {
        'num_states': len(tm_states),
        'start_state': dfa_start,
        'blank': '_',
        'transitions': tm_transitions,
        'accept_states': [accept_state],
        'reject_states': [reject_state]
    }

    return tm

def format_configuration(state, tape, head_position):
    # Format configuration string for current TM state and tape
    tape_str = ''.join(tape)
    pointer_chars = []

    '''
    Code below can display a caret under the tape head position
    for i in range(len(tape)):
        if i == head_position:
            pointer_chars.append('\t^')
        else:
            pointer_chars.append(' ')
    pointer_str = ''.join(pointer_chars)
    '''

    return f"state={state}, tape={tape_str}, head pos={head_position}"

def simulate_tm(tm, input_string, max_steps=None):
    # Simulate TM execution on a given input string
    tape = []

    for ch in input_string:
        tape.append(ch)
    tape.append(tm['blank'])

    head = 0
    state = tm['start_state']
    accept_states = set(tm.get('accept_states', []))
    reject_states = set(tm.get('reject_states', []))

    configurations = []
    steps = 0

    while True:
        # Record configuration before each transition
        configurations.append(format_configuration(state, tape, head))

        # Check accept and reject conditions
        if state in accept_states:
            return 1, configurations
        if state in reject_states:
            return 0, configurations

        # Enforce optional step limit
        if max_steps is not None and steps >= max_steps:
            return 0, configurations

        # Extend tape if head moves beyond current bounds
        if head < 0:
            tape.insert(0, tm['blank'])
            head = 0
        if head >= len(tape):
            tape.append(tm['blank'])

        # Read current symbol and apply transition rule
        current_symbol = tape[head]
        key = (state, current_symbol)
        if key not in tm['transitions']:
            return 0, configurations

        nxt_st, tape_char, direction = tm['transitions'][key]
        tape[head] = tape_char

        # Move head according to direction
        if direction == 'R':
            head += 1
        else:
            head -= 1

        # Update current state and step counter
        state = nxt_st
        steps += 1

def build_example_nfa():
    # Build example NFA for conversion and testing
    states = [0, 1, 2]
    alphabet = ['a', 'b']
    start_state = 0
    accept_states = [2]
    transitions = {}

    # Transitions for example NFA
    transitions[(0, 'a')] = [0, 1]
    transitions[(0, 'b')] = [0]
    transitions[(1, 'b')] = [2]

    nfa = {
        'states': states,
        'alphabet': alphabet,
        'start_state': start_state,
        'accept_states': accept_states,
        'transitions': transitions
    }

    return nfa

def print_dfa(dfa):
    # Print DFA description in a readable format
    print("DFA states:", dfa['states'])
    print("DFA start state:", dfa['start_state'])
    print("DFA accept states:", dfa['accept_states'])
    print("DFA transitions:")

    sorted_items = sorted(dfa['transitions'].items())

    for key, value in sorted_items:
        state, symbol = key
        print(f"\tδ({state}, {symbol}) = {value}")
    print()

def print_tm(tm):
    # Print TM decider description in a readable format
    print("TM number of states:", tm['num_states'])
    print("TM start state:", tm['start_state'])
    print("TM accept states:", tm.get('accept_states', []))
    print("TM reject states:", tm.get('reject_states', []))
    print("TM transitions:")

    sorted_items = sorted(tm['transitions'].items())

    for key, value in sorted_items:
        state, read_symbol = key
        nxt_st, tape_char, direction = value
        print(f"\tδ({state}, {read_symbol}) = ({nxt_st}, {tape_char}, {direction})")
    print()

def display_start_msg():
    # Display short description of program behavior
    print(f"\nThis program converts a nondeterministic \n"+
            "finite automaton (NFA) into an equivalent \n"+
            "deterministic finite automaton (DFA), then \n"+
            "builds a Turing Machine decider (TM-D) from \n"+
            "that DFA. It can also simulate the TM-D on an\n"+
            "input string and print each tape configuration\n"+
            "step by step to show how the machine processes \n"+
            "the string.\n")

def main():
    # Drive NFA to DFA conversion, TM construction, and simulation
    display_start_msg()

    nfa = build_example_nfa()
    dfa = nfa_to_dfa(nfa)
    tm = dfa_to_tm_decider(dfa)

    print("Constructed DFA from NFA:")
    print_dfa(dfa)

    print("Constructed TM decider from DFA:")
    print_tm(tm)

    input_string = "abb"
    print(f"Simulating TM on input: {input_string}\n")

    result, configurations = simulate_tm(tm, input_string)

    for i, cfg in enumerate(configurations):
        print(f"\tStep {i+1}: {cfg}")

    print("\tResult:", result)

if __name__ == "__main__":
    main()

