from pathlib import Path
import sys
from io import StringIO
from dataclasses import dataclass
from collections import Counter

sample_input = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
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
    
    points = [
        Point(x=0, y=0) for _ in range(10)
    ]

    tail = points[-1]

    tail_coords = Counter()
    for line in out:
        direction, num_moves = line.strip().split()
        num_moves = int(num_moves)

        for step in range(num_moves):
            head = points[0]
            if direction == "R":
                head.move_right()
            elif direction == "L":
                head.move_left()
            elif direction == "U":
                head.move_up()
            elif direction == "D":
                head.move_down()

            curr_point = head
            for point in points[1:]:

                if curr_point.is_touching(point):
                    # no need to move point if head is touching
                    pass
                
                elif curr_point.is_same_row(point):
                    if curr_point.x > point.x:
                        point.move_right()
                    else:
                        point.move_left()
                
                elif curr_point.is_same_col(point):
                    if curr_point.y > point.y:
                        point.move_up()
                    else:
                        point.move_down()
                
                else:
                    if curr_point.x > point.x:
                        point.move_right()
                    else:
                        point.move_left()
                    
                    if curr_point.y > point.y:
                        point.move_up()
                    else:
                        point.move_down()
                
                curr_point = point

            tail_coords[(point.x, point.y)] += 1


    num_points_visited = len(tail_coords)
    print(f"num_points_visited: {num_points_visited}")