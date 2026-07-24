import os
from typing import List

from utils.args import parse_args
from utils.timer import timer

"""
Part 1:
- Nothing fancy here, we just sum up all 300 prices straight from the file.

Part 2:
- The trick is sorting the prices in ascending order, so the priciest items end up at the tail of the list.
  Slicing off the last 20 elements removes the 20 most expensive items in one shot, and we sum whatever's left.

Part 3:
- The key insight is that "add, subtract, add, subtract, ..." is just adding every price at an even index
  (1st, 3rd, 5th, ...) and subtracting every price at an odd index (2nd, 4th, 6th, ...). Python slicing does this
  cleanly: `prices[::2]` grabs every other price starting from the first, `prices[1::2]` grabs every other price
  starting from the second, and negating the second group before summing both gives the final price.

  Using the puzzle's own 6-item example (912372, 283723, 294281, 592382, 721395, 91238):
    prices[::2]  = [912372, 294281, 721395]   (1st, 3rd, 5th)
    prices[1::2] = [283723, 592382, 91238]    (2nd, 4th, 6th), negated
    sum: 912372 + 294281 + 721395 - 283723 - 592382 - 91238 = 960705
"""


TEST_DATA = parse_args()


@timer
def part1():
    prices = parse_file()
    print(f"Sum of the prices: {sum(prices)}")


@timer
def part2():
    prices = parse_file()
    prices = sorted(prices)[:-20]
    print(f"Sum of the prices: {sum(prices)}")


@timer
def part3():
    prices = parse_file()
    prices = prices[::2] + list(map(lambda x: -x, prices[1::2]))
    print(f"Sum of the prices: {sum(prices)}")


def parse_file() -> List[int]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    prices = []
    with open(abs_file_path, "r") as f:
        for line in f:
            prices.append(int(line.strip()))
    return prices


part1()
part2()
part3()
