import os
from typing import List
from collections import defaultdict

from utils.args import parse_args
from utils.timer import timer

"""
Preprocessing:
- Each letter maps to a value: lowercase 'a'-'z' get 1-26, uppercase 'A'-'Z' get 27-52. We build that
  mapping once with `data_to_value`, so both part 2 and part 3 can just look a character up instead of
  recomputing its value from scratch.

Part 1:
- The corrupted entries are just non-alphabetical symbols mixed into the log, so counting the uncorrupted
  data is a matter of filtering the string down to `isalpha()` characters and counting what's left.

Part 2:
- Same filter as part 1, but instead of counting the uncorrupted characters we look up each one's value
  in `data_to_value` and sum them.

Part 3:
- The trick here is that a corrupted character's value only depends on the character right before it, so
  we can walk the log left to right and always have that preceding value on hand - no need for a second
  pass. If the preceding character was itself corrupted, we already amended it on the previous step, so
  `preceeding_value` always holds a real value by the time we need it.
- To amend a corrupted character: take the preceding value, compute `value * 2 - 5`, then wrap it into the
  1-52 range by adding or subtracting 52 (never more than once, since the formula can't overshoot the
  range by more than a single cycle).
- Worked example, following the sample log sheet 't#UD$...':
    't' is alpha, value 20 -> running total includes 20, preceding_value = 20
    '#' is corrupted, preceding_value = 20 -> 20 * 2 - 5 = 35, already in [1, 52] -> value 35
    'U' is alpha, value 47 -> preceding_value = 47
    'D' is alpha, value 30 -> preceding_value = 30
    '$' is corrupted, preceding_value = 30 -> 30 * 2 - 5 = 55, over 52 -> 55 - 52 = 3 -> value 3
  and so on for the rest of the sheet, summing every value (amended or original) as we go.
"""


TEST_DATA = parse_args()

data_to_value = defaultdict(int)
for i in range(26):
    data_to_value[chr(97 + i)] = i + 1
    data_to_value[chr(65 + i)] = 27 + i


@timer
def part1():
    data = parse_file()

    uncorrupted_data_count = sum((1 for d in data if d.isalpha()))

    print(f"Number of uncorrupted data values: {uncorrupted_data_count}")


@timer
def part2():
    data = parse_file()

    total_value = sum(data_to_value[d] for d in data if d.isalpha())

    print(f"Sum of uncorrupted data values: {total_value}")


@timer
def part3():
    data = parse_file()

    total_value = data_to_value[data[0]]
    preceeding_value = data_to_value[data[0]]
    for i in range(1, len(data)):
        if data[i].isalpha():
            preceeding_value = data_to_value[data[i]]
            total_value += preceeding_value
        else:
            corrupted_value = preceeding_value * 2 - 5
            if corrupted_value < 1:
                corrupted_value += 52
            elif corrupted_value > 52:
                corrupted_value -= 52

            total_value += corrupted_value
            preceeding_value = corrupted_value

    print(f"Total value of the data log sheet: {total_value}")


def parse_file() -> List[str]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    data = []
    with open(abs_file_path, "r") as f:
        data = f.read().strip()
    return data


part1()
part2()
part3()
