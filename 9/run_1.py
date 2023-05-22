from pathlib import Path
import sys
from io import StringIO
from dataclasses import dataclass
from collections import Counter

sample_input = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
@dataclass
class Point:
    x: int
    y: int

    def move_right(self):
        self.x += 1
    
    def move_left(self):
        self.x -= 1
    
    def move_up(self):
        self.y += 1
    
    def move_down(self):
        self.y -= 1
    
    def is_touching(self, other):
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1
    
    def is_same_row(self, other):
        return self.y == other.y

    def is_same_col(self, other):
        return self.x == other.x

if __name__ == "__main__":
    test_mode = sys.argv[-1] == "test"
    if test_mode:
        out = StringIO(sample_input)
    else:
        curr_dir = Path(__file__).parent
        out = open(curr_dir / "input.txt")
    
    head = Point(x=0, y=0)
    tail = Point(x=0, y=0)
    tail_coords = Counter()
    for line in out:
        direction, num_moves = line.strip().split()
        num_moves = int(num_moves)

        for step in range(num_moves):
            if direction == "R":
                head.move_right()
            elif direction == "L":
                head.move_left()
            elif direction == "U":
                head.move_up()
            elif direction == "D":
                head.move_down()

            if head.is_touching(tail):
                # no need to move tail if head is touching
                pass
            
            elif head.is_same_row(tail):
                if head.x > tail.x:
                    tail.move_right()
                else:
                    tail.move_left()
            
            elif head.is_same_col(tail):
                if head.y > tail.y:
                    tail.move_up()
                else:
                    tail.move_down()
            
            else:
                if head.x > tail.x:
                    tail.move_right()
                else:
                    tail.move_left()
                
                if head.y > tail.y:
                    tail.move_up()
                else:
                    tail.move_down()

            tail_coords[(tail.x, tail.y)] += 1


    num_points_visited = len(tail_coords)
    print(f"num_points_visited: {num_points_visited}")