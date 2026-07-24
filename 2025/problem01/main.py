import os
from typing import List, Tuple

from utils.args import parse_args
from utils.timer import timer

"""
Preprocessing:
- The file has 600 magnitude lines followed by one line of 599 "+"/"-" symbols. `parse_file()` reads the
  magnitudes into a list and the signs into a second list, and returns both along with the magnitude count
  so the calculation functions don't need to re-derive it.

Part 1:
- This is just a running sum: start from the first magnitude (the initial offset) and add or subtract each
  following magnitude depending on its matching sign, in file order. `calculate_offset()` does exactly this
  with a single loop.

Part 2:
- Same as part 1, but the sign sequence is meant to be read in reverse: the last symbol now corresponds to
  the first correction instead of the first symbol. We get this for free by reversing the `signs` list in
  place before calling `calculate_offset()` again - the rest of the logic is untouched.

Part 3:
- The trick here is realizing every reading is actually two lines glued together: the tens digit and the
  ones digit.
- So before applying corrections, we collapse each consecutive pair of magnitudes into a single two-digit 
  number with `10 * mags[i] + mags[i + 1]`, which also halves how many readings there are. The signs still 
  get reversed exactly as in part 2, since that instruction is still in effect - only the magnitudes needed 
  re-parsing.

  For example, with mags=[8,1,5,5,7,6,5,4,3,1] and signs="-++-++-++" reversed to "++-++-++-":
    pairs: (8,1) -> 81, (5,5) -> 55, (7,6) -> 76, (5,4) -> 54, (3,1) -> 31
    offset: 81 + 55 + 76 - 54 + 31 = 189
  which matches the reversed signs "+ + - +" applied to the four corrections after the initial 81.
"""


TEST_DATA = parse_args()


@timer
def part1():
    mags, signs, mags_length = parse_file()

    offset = calculate_offset(mags_length, mags, signs)

    print(f"Compass offset: {offset}")


@timer
def part2():
    mags, signs, mags_length = parse_file()

    signs.reverse()
    offset = calculate_offset(mags_length, mags, signs)

    print(f"Compass offset: {offset}")


@timer
def part3():
    mags, signs, mags_length = parse_file()

    signs.reverse()
    mags = [10 * mags[i] + mags[i + 1] for i in range(0, mags_length - 1, 2)]
    mags_length //= 2
    offset = calculate_offset(mags_length, mags, signs)

    print(f"Compass offset: {offset}")


def calculate_offset(mags_length: int, magnetudes: List[int], signs: List[str]) -> int:
    offset = magnetudes[0]
    for i in range(mags_length - 1):
        if signs[i] == "-":
            offset -= magnetudes[i + 1]
        else:
            offset += magnetudes[i + 1]
    return offset


def parse_file() -> Tuple[List[int], List[str], int]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    mags_length = 10 if TEST_DATA else 600

    mags = []
    signs = []
    with open(abs_file_path, "r") as f:
        for _ in range(mags_length):
            mags.append(int(f.readline().strip()))

        signs = [sign for sign in f.readline().strip()]

    return mags, signs, mags_length


part1()
part2()
part3()
