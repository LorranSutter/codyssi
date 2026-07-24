import os
from typing import List

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
