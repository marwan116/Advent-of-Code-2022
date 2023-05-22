from dataclasses import dataclass
from functools import total_ordering
from io import StringIO
from pathlib import Path
import sys


@dataclass
@total_ordering
class Rock:
    value: int = 1

    def __lt__(self, other):
        if isinstance(other, Paper):
            return True
        return False
    
    def __eq__(self, other):
        if isinstance(other, Rock):
            return True
        return False

@dataclass
@total_ordering
class Paper:
    value: int = 2

    def __lt__(self, other):
        if isinstance(other, Scissors):
            return True
        return False
    
    def __eq__(self, other):
        if isinstance(other, Paper):
            return True
        return False
    

@dataclass
@total_ordering
class Scissors:
    value: int = 3

    def __lt__(self, other):
        if isinstance(other, Rock):
            return True
        return False
    
    def __eq__(self, other):
        if isinstance(other, Scissors):
            return True
        return False

opponent_map = {
    "A": Rock(),
    "B": Paper(),
    "C": Scissors()
}

my_map = {
    "X": Rock(),
    "Y": Paper(),
    "Z": Scissors()
}

score_map = {
    "Win": 6,
    "Tie": 3,
    "Lose": 0,
}

sample_input = """
A Y
B X
C Z
"""

pieces = [Rock(), Paper(), Scissors()]

target_result_map = {
    "X": "Lose",
    "Y": "Tie",
    "Z": "Win",
}

if __name__ == "__main__":
    test_mode = sys.argv[-1] == "test"
    if test_mode:
        out = StringIO(sample_input)
    else:
        curr_dir = Path(__file__).parent
        out = open(curr_dir / "input.txt")

    my_score = 0
    for line in out:
        if line.strip():
            opponent_move, my_move = line.split()
            opponent_piece = opponent_map[opponent_move]
            my_piece = my_map[my_move]

            if my_piece > opponent_piece:
                result = "Win"
            elif my_piece == opponent_piece:
                result = "Tie"
            else:
                result = "Lose"

            my_score += score_map[result] + my_piece.value    
    
    print(my_score)

    # new interpretation
    out.seek(0)

    my_new_score = 0
    for line in out:
        if line.strip():
            opponent_move, target_result_symbol = line.split()
            opponent_piece = opponent_map[opponent_move]
            target_result = target_result_map[target_result_symbol]

            if target_result == "Win":
                my_piece = next(piece for piece in pieces if piece > opponent_piece)
            elif target_result == "Tie":
                my_piece = next(piece for piece in pieces if piece == opponent_piece)
            elif target_result == "Lose":
                my_piece = next(piece for piece in pieces if piece < opponent_piece)

            my_new_score += score_map[target_result] + my_piece.value    
    
    print(my_new_score)
