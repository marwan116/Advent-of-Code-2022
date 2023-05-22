from pathlib import Path
import sys
from io import StringIO

sample_input = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

# sample_input = """noop
# addx 3
# addx -5
# """

from collections import deque

if __name__ == "__main__":
    test_mode = sys.argv[-1] == "test"
    if test_mode:
        out = StringIO(sample_input)
    else:
        curr_dir = Path(__file__).parent
        out = open(curr_dir / "input.txt")
    
    x = deque([1])
    value_to_add = 0
    for cycle, line in enumerate(out, start=1):
        op, *ct = line.strip().split()
        if op == "noop":
            x.append(x[-1])
        elif op == "addx":
            x.append(x[-1])
            x.append(x[-1] + int(ct[0]))
        
    print(list(x))

    print(x[19], x[20]) # start of 20th cycle, end of 20th cycle
    print(x[59], x[60]) # start of 60th cycle, end of 60th cycle
    print(x[99], x[100]) # start of 100th cycle, end of 100th cycle
    print(x[139], x[140]) # start of 140th cycle, end of 140th cycle
    print(x[179], x[180]) # start of 180th cycle, end of 180th cycle
    print(x[219], x[220]) # start of 220th cycle, end of 220th cycle

    sum_of_strengths = x[19] * 20 + x[59] * 60 + x[99] * 100 + x[139] * 140 + x[179] * 180 + x[219] * 220
    print(sum_of_strengths)

    sprite_positions = [[v, v + 1, v + 2] for v in x]
    counter_positions = [(i % 40) + 1 for i, _ in enumerate(x)]

    for i, (counter_position, sprite_position) in enumerate(zip(counter_positions, sprite_positions)):
        if i % 40 == 0:
            print()
        if counter_position in sprite_position:
            print("#", end="")
        else:
            print(".", end="")