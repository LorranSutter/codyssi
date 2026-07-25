import os
from typing import List

from utils.args import parse_args
from utils.timer import timer

"""
Part 1:
- Each character's memory cost is just its position in the alphabet, so this is a straight lookup-and-sum. We
  build a `char_to_memory` table once (A-Z -> 1-26, and while we're at it 0-9 -> their own value, since parts
  2 and 3 will introduce digits into the messages).

Part 2:
- The trick here is that the "lossy" compression keeps a fixed number of characters at each end - `len // 10`,
  rounded down - and replaces everything in between with a single number representing how many characters were
  dropped.
- So for each line we just slice the first and last `lossy` characters and glue the removed count between them.

    Take VJAANCPKKLZSSSSSSSSS (20 chars). lossy = 20 // 10 = 2, so we keep the first 2 and last 2 characters:

        VJ AANCPKKLZSSSSSSSS SS
        ^^                   ^^
        kept                 kept
           ^^^^^^^^^^^^^^^^^^
           16 characters removed

    giving VJ16SS. The removed count itself becomes digit characters in the message, which is why the table
    above bothered to price 0-9 as well.

Part 3:
- This is classic run-length encoding: walk each line, and whenever the character changes, flush the count and
  character seen so far and start a new run. We track `last` and `letter_count`, appending `f"{letter_count}
  {last}"` to the output every time a run ends, plus once more after the loop for the final run.

    OONNHHHHHANNNHHHHHHHH becomes:

        OO -> 2O
        NN -> 2N
        HHHHH -> 5H
        A -> 1A
        NNN -> 3N
        HHHHHHHH -> 8H

    i.e. 2O2N5H1A3N8H, same as the puzzle example.
"""


TEST_DATA = parse_args()

char_to_memory = {chr(num): num - 64 for num in range(65, 91)}
for i in range(10):
    char_to_memory[str(i)] = i


@timer
def part1():
    messages = parse_file()

    total_memory = 0
    for message in messages:
        total_memory += calculate_total_memory(message)

    print(f"Total memory units: {total_memory}")


@timer
def part2():
    messages = parse_file()

    total_memory = 0
    for message in messages:
        lossy = len(message) // 10
        middle_size = len(message) - 2 * lossy
        message = message[:lossy] + str(middle_size) + message[-lossy:]
        total_memory += calculate_total_memory(message)

    print(f"Total memory units: {total_memory}")


@timer
def part3():
    messages = parse_file()

    total_memory = 0
    for message in messages:
        new_message = ""
        last = message[0]
        letter_count = 0
        for m in message:
            if m == last:
                letter_count += 1
            else:
                new_message += f"{letter_count}{last}"
                last = m
                letter_count = 1
        new_message += f"{letter_count}{last}"
        total_memory += calculate_total_memory(new_message)

    print(f"Total memory units: {total_memory}")


def calculate_total_memory(message: str) -> int:
    return sum(char_to_memory[m] for m in message)


def parse_file() -> List[str]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    messages = []
    with open(abs_file_path, "r") as f:
        for line in f:
            messages.append(line.strip())
    return messages


part1()
part2()
part3()
