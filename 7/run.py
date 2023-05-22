from pathlib import Path
import sys
from io import StringIO
from dataclasses import dataclass
from collections import defaultdict
from typing import Tuple, List, Union

sample_input = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

@dataclass(frozen=True)
class File:
    path: Tuple[str]
    size: int

@dataclass(frozen=True)
class Directory:
    path: Tuple[str]


if __name__ == "__main__":
    test_mode = sys.argv[-1] == "test"
    if test_mode:
        out = StringIO(sample_input)
    else:
        curr_dir = Path(__file__).parent
        out = open(curr_dir / "input.txt")
    
    path = []
    dirs = defaultdict(list)
    for line in out:
        if line.startswith("$"):
            if "cd" in line:
                curr_dir = line.split("cd ")[-1].strip()
                if curr_dir == "..":
                    path.pop()
                else:
                    path.append(curr_dir)
        
        else:
            if line.startswith("dir"):
                dir = line.split("dir ")[-1].strip()
                dirs[Directory(path=tuple(path))].append(
                    Directory(path=tuple(path + [dir]))
                )
            else:
                size, filename = line.split()
                dirs[Directory(path=tuple(path))].append(
                    File(path=tuple(path + [filename]), size=int(size))
                )


dirs = dict(dirs)

cache = {}
def sum_contents(objects: List[Union[File, Directory]]):
    size = 0
    for object in objects:
        if isinstance(object, File):
            size += object.size
        elif isinstance(object, Directory):
            if object in cache:
                size += cache[object]
            else:
                content_size = sum_contents(dirs[object])
                cache[object] = content_size
                size += content_size
        else:
            raise ValueError(f"Unknown object type: {object}")
    return size
  
dir_sizes = {}
for dir, objects in dict(dirs).items():
    dir_sizes[dir] = sum_contents(objects)

# part 1
print(sum(size for size in dir_sizes.values() if size <= 100000))


total_space = 70_000_000
space_required_for_update = 30_000_000

space_used = dir_sizes[Directory(path=("/",))]
space_left = total_space - space_used

space_to_empty = max(space_required_for_update - space_left, 0)
print(space_to_empty)

candidates = [
    dir for dir, size in dir_sizes.items() if size >= space_to_empty   
]

# part 2
smallest_dir = min(candidates, key=dir_sizes.get)
print(smallest_dir, dir_sizes[smallest_dir])
