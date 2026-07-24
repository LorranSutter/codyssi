import os
from typing import List
from dataclasses import dataclass

from utils.args import parse_args
from utils.timer import timer

"""
Preprocessing:
- Each line is "(reading) (base)", so we split on the space and keep the reading as a string (its digits
  depend on the base, so we can't parse it as an int yet) alongside its base as an int.

Part 1:
- The composition sum is just the sum of the base of every reading, no conversion needed.

Part 2:
- We convert each reading to base-10 using its recorded base and sum the results. Python's `int(str, base)`
  handles bases 2, 8, and 16 directly; base-10 readings are just `int(reading)`.

Part 3:
- Same sum as part 2, but the total then has to be re-expressed in the machine's custom base-65 alphabet
  instead of base-10.
- The trick is the standard base-conversion loop: repeatedly take the total modulo 65 to peel off the
  next digit (least significant first), map that digit through the alphabet string, then integer-divide
  the total by 65 and repeat until nothing's left. Since digits come out least-significant-first, we
  reverse them at the end to get the final string.

  For example, converting 3487996082 to base-65 (alphabet index 0-9 = digits, 10-35 = A-Z, 36-61 = a-z,
  62-64 = !@#):
      3487996082 % 65 = 12  -> alphabet[12] = "C", total //= 65 -> 53661478
        53661478 % 65 = 13  -> alphabet[13] = "D", total //= 65 -> 825561
          825561 % 65 = 61  -> alphabet[61] = "z", total //= 65 -> 12700
           12700 % 65 = 25  -> alphabet[25] = "P", total //= 65 -> 195
             195 % 65 = 0   -> alphabet[0]  = "0", total //= 65 -> 3
               3 % 65 = 3   -> alphabet[3]  = "3", total //= 65 -> 0
  Collected digits are "CDzP03" least-significant-first; reversing gives "30PzDC", matching the puzzle's
  own example.
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

    total = sum_readings(readings)

    print(f"Sum of the readings: {total}")


@timer
def part3():
    readings = parse_file()
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#"

    total = sum_readings(readings)

    base = len(alphabet)
    digits = []
    while total > 0:
        digits.append(alphabet[total % base])
        total //= base
    total = "".join(reversed(digits))

    print(f"Sum of the readings: {total}")


def sum_readings(readings: List[Reading]) -> int:
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

    return total


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
