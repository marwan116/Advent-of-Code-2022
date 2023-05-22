from pathlib import Path
import sys
from io import StringIO
from collections import defaultdict

sample_input = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


if __name__ == "__main__":
    test_mode = sys.argv[-1] == "test"
    if test_mode:
        out = StringIO(sample_input)
    else:
        curr_dir = Path(__file__).parent
        out = open(curr_dir / "input.txt")

    spaces = defaultdict(list)
    moves_list = []
    for line in out:
        move = {}
        if not line.strip():
            continue

        if line.startswith("move"):
            # move {} from {} to {}
            n_moves = int(line.split("move")[-1].split("from")[0].strip())
            from_stack = int(line.split("from")[-1].split("to")[0].strip())
            to_stack = int(line.split("to")[-1].strip())

            move["n_moves"] = n_moves
            move["from_stack"] = from_stack
            move["to_stack"] = to_stack
            moves_list.append(move)

        else:
            if '[' in line:
                for char_idx, char in enumerate(line):
                    if (char_idx + 1) % 2 == 0 and (char_idx + 1) % 4 != 0:
                        spaces[char_idx].append(char)
    
    stacks = [
        list(reversed(
            [
                char for char in vals if char != " "
            ]
        ))
        for vals in spaces.values()
    ]
    print(stacks)
    print(moves_list)

    for move in moves_list:
        n_moves = move["n_moves"]
        from_stack = move["from_stack"]
        to_stack = move["to_stack"]

        for _ in range(n_moves):
            item = stacks[from_stack - 1].pop()
            stacks[to_stack - 1].append(item)

    top_items = [stack[-1] for stack in stacks]
    print(''.join(top_items))
