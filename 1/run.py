from io import StringIO
from pathlib import Path
import sys

sample_input = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000

"""

if __name__ == "__main__":
    test_mode = sys.argv[-1] == "test"
    
    if test_mode:
        out = StringIO(sample_input)
    else:
        curr_dir = Path(__file__).parent
        out = open(curr_dir / "input.txt")

    elf_calories = 0
    max_calories = elf_calories
    for line in out:
        if line.strip():
            elf_calories += int(line)
        else:
            max_calories = max(max_calories, elf_calories)
            elf_calories = 0

    print(max_calories)

    out.seek(0)

    top_three_elves = [0, 0, 0]
    elf_calories = 0
    for line in out:
        if line.strip():
            elf_calories += int(line)
        else:
            if elf_calories > top_three_elves[-1]:
                top_three_elves[-1] = elf_calories
                top_three_elves.sort(reverse=True) # O(n log n)
            elf_calories = 0

    print(sum(top_three_elves))