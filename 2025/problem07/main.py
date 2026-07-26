import os
from typing import List, Tuple

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
    freqs, swaps, test_index = parse_file()

    for s in swaps:
        freqs[s[0] - 1], freqs[s[1] - 1] = freqs[s[1] - 1], freqs[s[0] - 1]

    print(f"Frequency: {freqs[test_index-1]}")


@timer
def part2():
    freqs, swaps, test_index = parse_file()
    swaps.append(swaps[0])

    for i in range(len(swaps) - 1):
        freqs[swaps[i + 1][0] - 1], freqs[swaps[i][1] - 1], freqs[swaps[i][0] - 1] = (
            freqs[swaps[i][1] - 1],
            freqs[swaps[i][0] - 1],
            freqs[swaps[i + 1][0] - 1],
        )

    print(f"Frequency: {freqs[test_index-1]}")


@timer
def part3():
    # TODO: Implement part 3
    lines = parse_file()
    pass


def parse_file() -> Tuple[List[int], List[Tuple[int]], int]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    frequencies = []
    swaps = []
    test_index = 0
    with open(abs_file_path, "r") as f:
        frequencies, swaps, test_index = f.read().split("\n\n")
        frequencies = [int(f.strip()) for f in frequencies.split("\n")]
        swaps = [tuple(map(int, s.strip().split("-"))) for s in swaps.split("\n")]
        test_index = int(test_index)
    return frequencies, swaps, test_index


part1()
part2()
# part3()
