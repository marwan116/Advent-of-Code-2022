from io import StringIO
from pathlib import Path
import sys
from string import ascii_lowercase, ascii_uppercase


sample_input = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

a_to_z = ascii_lowercase
A_to_Z = ascii_uppercase

if __name__ == "__main__":
    test_mode = sys.argv[-1] == "test"
    if test_mode:
        out = StringIO(sample_input)
    else:
        curr_dir = Path(__file__).parent
        out = open(curr_dir / "input.txt")

    priority_sum = 0
    for line in out:
        if line.strip():
            rucksack = line.strip()
            compartment1, compartment2 = rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:]
            common = set(compartment1).intersection(compartment2)
            for letter in common:
                if letter in a_to_z:
                    priority = a_to_z.index(letter) + 1
                else:
                    priority = A_to_Z.index(letter) + 27
                priority_sum += priority

    print(priority_sum)

    out.seek(0)
    
    group = []
    new_priority_sum = 0
    i = 0
    for line in out:
        if line.strip():
            group.append(line.strip())
            i += 1
        else:
            continue
        if i % 3 == 0:
            common = set(group[0]).intersection(group[1])
            common = common.intersection(group[2])
            if len(common) > 1:
                print(common, group)
                raise ValueError("Not possible")
            else:
                label = list(common)[0]
                if label in a_to_z:
                    priority = a_to_z.index(label) + 1
                else:
                    priority = A_to_Z.index(label) + 27
                new_priority_sum += priority
            group = []

    print(new_priority_sum)
        