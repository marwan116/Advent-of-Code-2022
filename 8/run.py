from pathlib import Path
import sys
from io import StringIO
from dataclasses import dataclass

sample_input = """30373
25512
65332
33549
35390
"""

@dataclass(frozen=True)
class Tree:
    x: int
    y: int
    height: int
    
    @property
    def is_edge(self):
        return self.x == 0 or self.y == 0

    def is_visible_from(self, other):
        if not isinstance(other, Tree):
            return NotImplemented()
        
        return self.height > other.height


if __name__ == "__main__":
    test_mode = sys.argv[-1] == "test"
    if test_mode:
        out = StringIO(sample_input)
    else:
        curr_dir = Path(__file__).parent
        out = open(curr_dir / "input.txt")
    
    trees = {}
    max_x = 0
    max_y = 0
    for row_idx, line in enumerate(out):
        max_y = max(max_y, row_idx)
        for col_idx, num in enumerate(line.strip()):
            max_x = max(max_x, col_idx)

            trees[(col_idx, row_idx)] = (
                Tree(
                    x=col_idx,
                    y=row_idx,
                    height=int(num),
                )
            )

    num_visible_from_edge = 0
    for coord, tree in trees.items():
        if tree.is_edge:
            num_visible_from_edge +=1
        else:
            visible_from_left = all(
                tree.is_visible_from(trees[(x, tree.y)])
                for x in range(tree.x)
            )
            
            visible_from_top = all(
                tree.is_visible_from(trees[(tree.x, y)])
                for y in range(tree.y)
            )

            visible_from_right = all(
                tree.is_visible_from(trees[(x, tree.y)])
                for x in range(tree.x + 1, max_x + 1)
            )

            visible_from_bottom = all(
                tree.is_visible_from(trees[(tree.x, y)])
                for y in range(tree.y + 1, max_y + 1)   
            )

            num_visible_from_edge += int(
                visible_from_left
                or visible_from_top
                or visible_from_right
                or visible_from_bottom
            )

    print(num_visible_from_edge)


    max_scenic_score = 0
    for coord, tree in trees.items():
        
        if tree.is_edge:
            # given scenic score will be 0
            continue

        num_visible_to_left = 0
        for x in reversed(range(tree.x)):
            num_visible_to_left += 1
            if not tree.is_visible_from(trees[(x, tree.y)]):
                break

        num_visible_to_top = 0
        for y in reversed(range(tree.y)):
            num_visible_to_top += 1
            if not tree.is_visible_from(trees[(tree.x, y)]):
                break
        
        num_visible_to_right = 0
        for x in range(tree.x + 1, max_x + 1):
            num_visible_to_right += 1
            if not tree.is_visible_from(trees[(x, tree.y)]):
                break
        
        num_visible_to_bottom = 0
        for y in range(tree.y + 1, max_y + 1):
            num_visible_to_bottom += 1
            if not tree.is_visible_from(trees[(tree.x, y)]):
                break
        
        scenic_core = (
            num_visible_to_left
            * num_visible_to_top
            * num_visible_to_right
            * num_visible_to_bottom
        )
        max_scenic_score = max(max_scenic_score, scenic_core)
        
    print(max_scenic_score)