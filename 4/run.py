from pathlib import Path
import sys
from io import StringIO

sample_input = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""


if __name__ == "__main__":
    test_mode = sys.argv[-1] == "test"
    if test_mode:
        out = StringIO(sample_input)
    else:
        curr_dir = Path(__file__).parent
        out = open(curr_dir / "input.txt")
    
    count_fully_contained = 0
    for line in out:
        left, right = line.split(",")
        min_left, max_left = map(int, left.split("-"))
        min_right, max_right = map(int, right.split("-"))
        if min_left <= min_right and max_left >= max_right:
            print("left fully contains right")
            print(f"left: {min_left}, {max_left}, right: {min_right}, {max_right}")
            count_fully_contained +=1 
            print("\n" * 2)
            continue
        
        if min_right <= min_left and max_right >= max_left:
            print("right fully contains left")
            print(f"right: {min_right}, {max_right}, left: {min_left}, {max_left}")
            count_fully_contained +=1
            print("\n" * 2)
            continue
    
    print(count_fully_contained)

    out.seek(0)

    # Part 2
    count_overlapping = 0
    for line in out:
        left, right = line.split(",")
        min_left, max_left = map(int, left.split("-"))
        min_right, max_right = map(int, right.split("-"))
        if (max_left < min_right) or (min_left > max_right):
            print("left and right are disjoint")
            print(f"left: {min_left}, {max_left}, right: {min_right}, {max_right}")
            print("\n" * 2)
        else:
            count_overlapping +=1 
    
    print(count_overlapping)