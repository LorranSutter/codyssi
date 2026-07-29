import os
import math
from typing import List
from dataclasses import dataclass

from utils.args import parse_args
from utils.timer import timer

"""
Preprocessing:
- Each line is just "{number} {base}", so we parse it straight into a `Num` dataclass holding the raw digit
  string and its base as an int.

- The `alphabet` string is the digit-to-value lookup for the whole file: 0-9, then A-Z, then a-z, then the
  six extra symbols !@#$%^ tacked on the end, for 68 characters total. It does double duty across the three
  parts: `parse_to_base_10` only ever needs the first 62 of them (the puzzle caps input bases at 62), while
  `parse_to_base_n` slices off the first `base` characters of it to emit digits for bases up to 68 in part 2.

Part 1:
- Nothing fancy here: convert every line to base 10 with its own base and keep the largest.
  `parse_to_base_10` walks the digit string left to right, and since the leftmost character carries the
  highest place value, it multiplies each digit by `base` raised to its distance from the right end -
  exactly the manual pencil-and-paper base conversion.

Part 2:
- Same as part 1, but instead of taking the max of the base-10 values we sum them, then convert that sum
  to base 68 with `parse_to_base_n`. That function is the classic remainder method: repeatedly divide by
  68, stash the remainder as a digit, and reverse the collected digits at the end since they come out
  least-significant-first. This is exactly where the six extra alphabet symbols earn their keep, since base
  68 needs six digits beyond a-z.

Part 3:
- The trick is realizing the question is really "what's the smallest base whose N-digit ceiling can hold
  this sum", so it pays to first find a formula for that ceiling instead of searching base by base.

- I started by looking for a pattern in the maximum value representable with N digits in base 2:
    1    -> 1  = 2^1 - 1
    11   -> 3  = 2^2 - 1
    111  -> 7  = 2^3 - 1
    1111 -> 15 = 2^4 - 1
  the max base-10 value written with N digits in base 2 is 2^N - 1. The same pattern holds for base 16:
    F    -> 15    = 16^1 - 1
    FF   -> 255   = 16^2 - 1
    FFF  -> 4095  = 16^3 - 1
    FFFF -> 65535 = 16^4 - 1
  which makes sense once you write it out: with every digit maxed at base-1, the value is
    (base-1) * (base^(N-1) + base^(N-2) + ... + base^0) = (base-1) * (base^N - 1) / (base-1) = base^N - 1

- So the smallest base that fits `sum_base_10` in N digits is the smallest base with base^N - 1 >=
  sum_base_10, i.e. base >= (sum_base_10 + 1)^(1/N). Taking the ceiling of that root gives the answer
  directly, no search needed.
"""


@dataclass
class Num:
    num: str
    base: int


TEST_DATA = parse_args()

alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^"
alphabet_to_num = {char: i for i, char in enumerate(alphabet)}


@timer
def part1():
    nums = parse_file()

    base_10 = (parse_to_base_10(num.num, num.base) for num in nums)

    print(f"Largest number: {max(base_10)}")


@timer
def part2():
    nums = parse_file()

    base_10 = (parse_to_base_10(num.num, num.base) for num in nums)
    sum_base_10 = sum(base_10)
    base_68 = parse_to_base_n(sum_base_10, 68)

    print(f"Base-68 sum: {base_68}")


@timer
def part3():
    nums = parse_file()
    N = 4

    base_10 = (parse_to_base_10(num.num, num.base) for num in nums)
    sum_base_10 = sum(base_10)

    min_base = math.ceil((sum_base_10 + 1) ** (1 / N))

    print(f"Smallest base: {min_base}")


def parse_to_base_10(num: str, base: int) -> int:
    result = 0
    for i in range(len(num)):
        result += alphabet_to_num[num[i]] * base ** (len(num) - 1 - i)

    return result


def parse_to_base_n(num: int, base: int) -> str:
    local_alphabet = alphabet[:base]

    digits = []
    while num > 0:
        digits.append(local_alphabet[num % base])
        num //= base

    return "".join(reversed(digits))


def parse_file() -> List[Num]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    nums = []
    with open(abs_file_path, "r") as f:
        for line in f:
            num, base = line.strip().split(" ")
            nums.append(Num(num, int(base)))
    return nums


part1()
part2()
part3()
