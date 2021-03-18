from itertools import product, compress
from math import prod


def calculate_reliability(N: int, datafile: str, ps: list):
    with open(datafile, 'r') as data:
        table = data.readlines()[1:]
        table = [list(map(lambda x: int(x), elem.rstrip("\n").split(", "))) for elem in table]

    if len(table) - 2 != N:
        print("Incorrect topology!")
    else:
        if all([True if 0 <= p <= 1 else False for p in ps]):
            ixs = [i for i in range(len(table[0])) if table[0][i] == 1]
            states = [int('1' + '0' * (elem - 1) + '1' + '0' * ((len(table) - 1) - elem), 2) for elem in ixs]
            results = []
            while len(ixs) != 0:
                new_ixs = []
                new_states = []
                start = 0
                for index, i in enumerate(ixs):
                    new_ixs += [j for j in range(len(table[i])) if table[i][j] == 1 and bin(states[index])[2:][j] == '0']
                    new_states += [states[index] + int("0" * elem + "1" + "0" * ((len(table) - 1) - elem), 2)
                                   for elem in new_ixs[start:]]
                    start = len(new_ixs)
                states = new_states
                ixs = new_ixs
                results += [states[i] for i in range(len(ixs)) if ixs[i] == len(table) - 1]
                states = [state for state in states if state not in results]
                ixs = [ix for ix in ixs if ix != len(table) - 1]

            results = [int(bin(elem)[2:][1: -1], 2) for elem in results]
            P_sys = 0
            all_working_states = []
            for path in results:
                all_states = product(range(2), repeat=len(table) - 2)
                for state in all_states:
                    mask = int("".join(list(map(lambda x: str(x), state))), 2)
                    if path & mask == path:
                        all_working_states.append(mask)
            all_working_states = list(set(all_working_states))

            elements = [f'E{i}' for i in range(1, len(table) - 1)]
            print("\nAll possible paths from start to end:")
            for path in results:
                binary_filter = list(map(lambda x: int(x), list(bin(path)[2:])))
                new_path = compress(elements, binary_filter)
                print(" -> ".join(new_path))
            title_str = "| " + " | ".join([f'E{i}' for i in range(1, len(table) - 1)] + [""]) + "P".center(14) + "|"
            print("\nAll working states and their probabilities:")
            print(title_str)
            for state in all_working_states:
                binary = bin(state)[2:]
                binary_state = list(binary.rjust(len(table) - 2, '0'))
                element_probs = [p if binary_state[i] == '1' else 1 - p for i, p in enumerate(ps)]
                state_prob = prod(element_probs)
                print('-' * len(title_str))
                print("| " + "  | ".join(binary_state + [""]) + f"{state_prob:e}".center(14) + "|")
                P_sys += state_prob
            print(f"Number of all working states: {len(all_working_states)}")
            return P_sys
        else:
            print("Incorrect probabilities!")
