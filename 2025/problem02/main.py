import os
import re
from typing import Tuple, List

from utils.args import parse_args
from utils.timer import timer

"""
Preprocessing:
- The input file is split into two blocks by a blank line: the three pricing functions (A, B, C, each a
  line with a single number embedded in it, e.g. "ADD 495") and the list of room qualities.
- Function values are pulled out with a regex and kept in order [A, B, C], and qualities are parsed 
  into ints.

Part 1:
- Every part shares the same pricing formula: take a value, raise it to the power from function C,
  multiply by function B, then add function A. `calculate_price()` just applies that chain directly.
- The only real work in part 1 is finding the median quality (sort, then pick the middle element, or
  average the two middle elements for an even-length list) and feeding it through the formula.

Part 2:
- Same pricing formula as part 1, but the input value changes: instead of pricing a single room, we sum
  up the qualities of every even room and price that total. So it's a filter-and-sum followed by the
  same `calculate_price()` call.

Part 3:
- This part runs the formula backwards. We're told the max the client can pay, and instead of computing
  a price from a quality, we need the highest quality whose price doesn't exceed that budget.
- The trick is inverting `calculate_price()` algebraically instead of searching:

    price = quality^C * B + A
    quality = ((price - A) / B)^(1/C)

- Plugging in the budget for `price` gives an upper bound on quality directly, in one shot, with no
  need to price every room and compare. From there it's just picking the largest actual room quality in
  the list that's still under that bound.
"""


TEST_DATA = parse_args()


@timer
def part1():
    # TODO: Implement part 1
    functions, qualities = parse_file()

    qualities.sort()
    length = len(qualities)
    if length % 2 == 0:
        median = (qualities[length // 2 - 1] + qualities[length // 2]) / 2
    else:
        median = qualities[length // 2]

    price = calculate_price(median, functions)

    print(f"Price in exponentialis pecunia: {price}")


@timer
def part2():
    # TODO: Implement part 2
    functions, qualities = parse_file()

    even_qualities = 0
    for quality in qualities:
        if quality % 2 == 0:
            even_qualities += quality

    price = calculate_price(even_qualities, functions)

    print(f"Price in exponentialis pecunia: {price}")


@timer
def part3():
    # TODO: Implement part 3
    functions, qualities = parse_file()
    max_price = 15000000000000
    max_quality = ((max_price - functions[0]) / functions[1]) ** (1 / functions[2])

    highest_quality = 0
    for quality in qualities:
        if quality <= max_quality and quality > highest_quality:
            highest_quality = quality

    print(f"Highest-quality affordable room: {highest_quality}")


def calculate_price(value: int, functions: List[int]) -> int:
    return value ** functions[2] * functions[1] + functions[0]


def parse_file() -> Tuple[List[int], List[int]]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    functions = []
    qualities = []
    with open(abs_file_path, "r") as f:
        functions, qualities = f.read().split("\n\n")

        functions = [
            int(re.search(r"(\d+)", f.strip())[0]) for f in functions.split("\n")
        ]
        qualities = [int(q.strip()) for q in qualities.split("\n")]

    return functions, qualities


part1()
part2()
part3()
