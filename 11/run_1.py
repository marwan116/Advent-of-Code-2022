from pathlib import Path
import sys
from io import StringIO
import re
from dataclasses import dataclass
from typing import List
import operator
from collections import deque, Counter

sample_input = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

@dataclass
class Monkey:
    id: int
    starting_items: List[int]
    operation: str
    operation_value: int
    test_value: int
    true_monkey: int
    false_monkey: int

    def __post_init__(self):
        self.id = int(self.id)
        self.test_value = int(self.test_value)
        self.true_monkey = int(self.true_monkey)
        self.false_monkey = int(self.false_monkey)
        self.starting_items = deque([int(i) for i in self.starting_items.split(", ")])

        if self.operation == "*":
            self.operation = operator.mul
        elif self.operation == "+":
            self.operation = operator.add

    def run_operation(self, old):
        if self.operation_value == "old":
            val = old
        else:
            val = int(self.operation_value)

        return self.operation(old, val)

    def test(self, item):
        if item % self.test_value == 0:
            return self.true_monkey
        else:
            return self.false_monkey

if __name__ == "__main__":
    test_mode = sys.argv[-1] == "test"
    if test_mode:
        out = StringIO(sample_input)
    else:
        curr_dir = Path(__file__).parent
        out = open(curr_dir / "input.txt")
    
    pattern = r"""
Monkey (?P<id>.+?):
  Starting items: (?P<starting_items>.+)
  Operation: new = old (?P<operation>.) (?P<operation_value>.+)
  Test: divisible by (?P<test_value>.+)
    If true: throw to monkey (?P<true_monkey>.+)
    If false: throw to monkey (?P<false_monkey>.+)
    """.strip()

    text = out.read()

    match = re.finditer(pattern, text)
    
    monkey_list = [
        Monkey(**m.groupdict()) for m in match
    ]
    num_monkeys = len(monkey_list)
    monkeys = {m.id: m for m in monkey_list}
    
    round = 1
    item_inspection_counter = Counter()
    while True:
        for id in range(num_monkeys):
            monkey = monkeys[id]
            while True:
                try:
                    item = monkey.starting_items.popleft()
                except IndexError:
                    break
                item_inspection_counter[monkey.id] += 1
                print(f"Monkey {monkey.id} inspects an item with a worry level of {item}.")
                new_item = monkey.run_operation(item)
                new_item = new_item // 3
                dest_monkey = monkey.test(new_item)
                monkeys[dest_monkey].starting_items += [new_item]
                print(f"Item with worry level {new_item} is thrown to monkey {dest_monkey}")
            print("\n" * 2)
        
        print(f"{round=} {monkeys=}")
        
        round +=1
        if round == 21:
            break

    monkey_business = 1    
    for (id, ct) in (item_inspection_counter.most_common(n=2)):
        monkey_business *= ct
    print(monkey_business)