import os
import re
from typing import List
from dataclasses import dataclass

from utils.args import parse_args
from utils.timer import timer

"""
Preprocessing:
-

Part 1:
-

Part 2:
-

Part 3:
-
"""


TEST_DATA = parse_args()


@dataclass
class Item:
    ID: int
    code: str
    quality: int
    cost: int
    materials: int


@timer
def part1():
    items = parse_file()

    items = sorted(items, key=lambda x: (x.quality, x.cost))
    total_materials = sum((x.materials for x in items[-5:]))

    print(f"Total materials for top 5 items: {total_materials}")


@timer
def part2():
    # TODO: Implement part 2
    lines = parse_file()
    pass


@timer
def part3():
    # TODO: Implement part 3
    lines = parse_file()
    pass


def parse_file() -> List[Item]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    items = []
    with open(abs_file_path, "r") as f:
        for line in f:
            line = re.search(
                r"(\d+)\s(\w+)\s\|\s\w+\s:\s(\d+),\s\w+\s:\s(\d+),\s\w+\s\w+\s:\s(\d+)",
                line.strip(),
            )
            groups = line.groups()
            items.append(Item(int(groups[0]), groups[1], *map(int, groups[2:])))
    return items


part1()
part2()
part3()
