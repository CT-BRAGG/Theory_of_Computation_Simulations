'''
Theory of Comp: CFG Recognize Empty Language
author: Carson Bragg
date: nov 11, 2025
'''

from typing import Final

# Symbol used to represent epsilon on the right side of productions
EPSILON: Final[str] = 'eps'

def compute_generating_nonterminals(cfg):
    # Compute set of nonterminals that can derive some terminal string
    nonterminals = cfg['nonterminals']
    productions = cfg['productions']
    generating = set()
    changed = True

    # Repeat until no new generating nonterminals are found
    while changed:
        changed = False
        for non_term in nonterminals:
            # Skip nonterminals already known to be generating
            if non_term in generating:
                continue
            # Skip nonterminals without productions
            if non_term not in productions:
                continue

            right_side_list = productions[non_term]
            # Check each production for current nonterminal
            for right_side in right_side_list:
                # Nonterminal directly generates epsilon
                if len(right_side) == 1 and right_side[0] == EPSILON:
                    generating.add(non_term)
                    changed = True
                    break

                # Assume all nonterminals on right side are already generating
                all_symbols_good = True
                for sym in right_side:
                    if sym in nonterminals:
                        if sym not in generating:
                            all_symbols_good = False
                            break

                # Mark nonterminal as generating when all nonterminals on right side are generating
                if all_symbols_good:
                    generating.add(non_term)
                    changed = True
                    break

    return generating

def cfg_language_is_empty(cfg):
    # Decide whether CFG language is empty based on generating nonterminals
    generating = compute_generating_nonterminals(cfg)
    start_symbol = cfg['start_symbol']

    # Language is non-empty when start symbol can generate some string
    if start_symbol in generating:
        return 0

    # Language is empty when start symbol is not generating
    return 1

def print_cfg(cfg, index):
    # Print CFG structure in readable format
    print(f"CFG #{index}")
    print(f"  Nonterminals: {cfg['nonterminals']}")
    print(f"  Terminals: {cfg['terminals']}")
    print(f"  Start symbol: {cfg['start_symbol']}")
    print("  Productions:")

    productions = cfg['productions']
    # Walk through nonterminals that have productions
    for non_term in cfg['nonterminals']:
        if non_term in productions:
            right_side_list = productions[non_term]

            # Print each right side for current nonterminal
            for right_side in right_side_list:
                if len(right_side) == 1 and right_side[0] == EPSILON:
                    right_side_str = EPSILON
                else:
                    right_side_str = ''.join(right_side)

                print(f"    {non_term} -> {right_side_str}")
    print()

def display_start_msg():
    # Print description of program behavior and output format
    print("\nThis program determines whether a context-free \n"+
            "grammar (CFG) recognizes the empty language.\n"+
            "It uses a fixed-point algorithm to find all \n"+
            "nonterminals that can derive some terminal\n"+
            "string (including the empty string). If the \n"+
            "start symbol is not in this set, then the\n"+
            "language of the CFG is empty. The program then \n"+
            "applies this test to example grammars and\n"+
            "prints each grammar along with the result (1 for \n"+
            "empty language, 0 otherwise).\n")

def build_example_cfg_empty():
    # Build sample CFG whose language is empty
    nonterminals = ['S', 'A']
    terminals = ['a', 'b']
    start_symbol = 'S'

    productions = {}
    productions['S'] = [['A']]

    cfg = {
        'nonterminals': nonterminals,
        'terminals': terminals,
        'start_symbol': start_symbol,
        'productions': productions
    }
    return cfg

def build_example_cfg_nonempty():
    # Build sample CFG whose language is not empty
    nonterminals = ['S', 'A']
    terminals = ['a', 'b']
    start_symbol = 'S'

    productions = {}
    productions['S'] = [['A'], [EPSILON]]
    productions['A'] = [['a', 'A'], ['a']]

    cfg = {
        'nonterminals': nonterminals,
        'terminals': terminals,
        'start_symbol': start_symbol,
        'productions': productions
    }
    return cfg

def main():
    # Entry point for program execution
    display_start_msg()

    # Build list of example CFGs for testing
    cfgs = []
    cfg_empty = build_example_cfg_empty()
    cfg_nonempty = build_example_cfg_nonempty()

    cfgs.append(("CFG with empty language", cfg_empty))
    cfgs.append(("CFG with non-empty language", cfg_nonempty))

    # Run emptiness test on each CFG and print result
    index = 1
    for label, cfg in cfgs:
        print(label)
        print_cfg(cfg, index)
        result = cfg_language_is_empty(cfg)
        print(f"  result: {result}\n")
        index += 1

if __name__ == "__main__":
    main()

