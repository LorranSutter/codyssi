import os
from typing import List

from utils.args import parse_args
from utils.timer import timer

"""
Part 1:
- Straightforward: walk every character in every line and count the ones that are alphabetic with
  `str.isalpha()`.

Part 2:
- The key insight is that reductions can happen in any order without changing the final result, so there's
  no need to explore every possible reduction order - a single left-to-right greedy pass over each line
  gets the same answer.
- The pass keeps an index `i`. Whenever the character at `i` is a digit, it first checks the character to
  its left: if that's an alpha (or a hyphen, for part 2), the pair is deleted and `i` steps back one, since
  deleting shifts everything after it left, and stepping back lets us recheck what's now adjacent. If the
  left doesn't match, the same check happens on the right. If neither matches, we just move to the next
  index.
- `alphas` is the set of characters allowed to be consumed alongside a digit: letters, plus the hyphen when
  `hyphen=True`.
- Obs: this ends up as a lot of ifs and elses for what is a pretty simple sliding rule - there's probably a
  cleaner way to express it (e.g. with a stack), but it works and runs fast enough.

Part 3:
- Same reduction logic as part 2, just with the hyphen excluded from `alphas` - the delta is a single-line
  nudge to the set passed into `reduction()`.
"""


TEST_DATA = parse_args()


@timer
def part1():
    lines = parse_file()

    composition = 0
    for line in lines:
        for char in line:
            if char.isalpha():
                composition += 1

    print(f"File composition: {composition}")


@timer
def part2():
    lines = parse_file()

    total_chars = reduction(lines, True)

    print(f"Total remaining characters: {total_chars}")


@timer
def part3():
    lines = parse_file()

    total_chars = reduction(lines, False)

    print(f"Total remaining characters: {total_chars}")


def reduction(lines: List[str], hyphen: bool) -> int:
    alphas = set()
    if hyphen:
        alphas.add("-")
    for i in range(26):
        alphas.add(chr(i + 65))
        alphas.add(chr(i + 97))

    total_chars = 0
    for line in lines:
        i = 0
        while i < len(line):
            if line[i].isdigit():
                if i > 0 and line[i - 1] in alphas:
                    line = line[: i - 1] + line[i + 1 :]
                    i -= 1
                elif i >= 0 and i < len(line) - 1 and line[i + 1] in alphas:
                    line = line[:i] + line[i + 2 :]
                    if i > 0:
                        i -= 1
                else:
                    i += 1
            else:
                i += 1
        total_chars += len(line)

    return total_chars


def parse_file() -> List[str]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    lines = []
    with open(abs_file_path, "r") as f:
        for line in f:
            lines.append(line.strip())
    return lines


part1()
part2()
part3()
