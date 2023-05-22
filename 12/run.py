from pathlib import Path
import sys
from io import StringIO
from dataclasses import dataclass
from typing import Tuple
from string import ascii_lowercase

sample_input = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".strip()

Coords = Tuple[int, int]

@dataclass(frozen=True)
class Node:
    level: str
    x: int
    y: int

    @property
    def level_value(self):
        level = self.level

        if level == "S":
            return 0
        
        elif level == "E":
            return ascii_lowercase.index("z") + 2
        
        else:
            return ascii_lowercase.index(level) + 1
    
    def is_start(self):
        return self.level == "S"
    
    def is_end(self):
        return self.level == "E"

    def move(self, direction: str) -> Coords:
        x, y = self.x, self.y
        if direction == "up":
            y -= 1
        elif direction == "down":
            y += 1
        elif direction == "left":
            x -= 1
        elif direction == "right":
            x += 1
        else:
            raise ValueError("Invalid direction")
        return (x, y)


def get_eligible_directions(node):
    eligible_directions = []
    for direction in ["up", "down", "left", "right"]:
        # get new coordinates
        new_coords = node.move(direction)

        # check if new coordinates are in grid
        if new_coords in grid:
            
            # get new node
            new_node = grid[new_coords]
            
            # if new node accessible, add to paths
            if new_node.level_value - node.level_value <= 1:
                eligible_directions.append(direction)

    return eligible_directions

cache = {}

def get_shortest_path(node, path=[]):
    # if node is end, return path
    if node.is_end():
        return path

    # get eligible directions
    eligible_directions = get_eligible_directions(node)

    # if no eligible directions, return None
    if not eligible_directions:
        return None

    # if eligible directions, get shortest path
    shortest_path = None
    for direction in eligible_directions:
        # get new coordinates
        new_coords = node.move(direction)

        # get new node
        new_node = grid[new_coords]

        # if new node is already in path, skip
        if new_node in path:
            continue

        # get new path
        new_path = path + [new_node]

        # get shortest path from new node
        if new_node in cache:
            if cache[new_node]:
                new_shortest_path = new_path + cache[new_node]
            else:
                new_shortest_path = None
        else:
            new_shortest_path = get_shortest_path(new_node, new_path)
            if new_shortest_path:
                cache[new_node] = new_shortest_path[len(path) + 1:]
            else:
                cache[new_node] = None

        # if new shortest path is shorter than current shortest path, update shortest path
        if new_shortest_path:
            if not shortest_path or len(new_shortest_path) < len(shortest_path):
                shortest_path = new_shortest_path

    return shortest_path


if __name__ == "__main__":
    test_mode = sys.argv[-1] == "test"
    if test_mode:
        out = StringIO(sample_input)
    else:
        curr_dir = Path(__file__).parent
        out = open(curr_dir / "input.txt")
    
    # Read input
    grid = {
        (col_idx, row_idx): Node(level=char, x=col_idx, y=row_idx)
        for row_idx, line in enumerate(out.readlines())
        for col_idx, char in enumerate(line.strip())
    }

    print(grid)

    # Find the shortest path to the end marked at E starting from S
    # The path can only move in the 4 directions (up, down, left, right)
    # next step can only be 1 character away at most from the current position

    starting_node = [node for node in grid.values() if node.is_start()][0]

    node = starting_node
    sys.setrecursionlimit(10000)
    path = get_shortest_path(node, path=[])

    print(path)
    print(len(path))
            

        

