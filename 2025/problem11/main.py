import os
from typing import List, Tuple
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
    # TODO: Implement part 3
    lines = parse_file()
    pass


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
