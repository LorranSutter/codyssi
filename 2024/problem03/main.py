import os
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
class Reading:
    reading: str
    base: int


@timer
def part1():
    readings = parse_file()
    composition = sum([reading.base for reading in readings])

    print(f"Composition sum: {composition}")


@timer
def part2():
    readings = parse_file()

    total = 0
    for reading in readings:
        match reading.base:
            case 2:
                total += int(reading.reading, 2)
            case 8:
                total += int(reading.reading, 8)
            case 16:
                total += int(reading.reading, 16)
            case _:
                total += int(reading.reading)

    print(f"Sum of the readings: {total}")


@timer
def part3():
    readings = parse_file()
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#"

    total = 0
    for reading in readings:
        match reading.base:
            case 2:
                total += int(reading.reading, 2)
            case 8:
                total += int(reading.reading, 8)
            case 16:
                total += int(reading.reading, 16)
            case _:
                total += int(reading.reading)

    total = convert_to_base(total, alphabet)
    print(f"Sum of the readings: {total}")


def convert_to_base(num: int, alphabet: str) -> str:
    if num == 0:
        return alphabet[0]

    base = len(alphabet)
    digits = []
    while num > 0:
        digits.append(alphabet[num % base])
        num //= base

    return "".join(reversed(digits))


def parse_file() -> List[Reading]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    readings = []
    with open(abs_file_path, "r") as f:
        for line in f:
            line = line.strip().split(" ")
            readings.append(Reading(line[0], int(line[1])))
    return readings


part1()
part2()
part3()
