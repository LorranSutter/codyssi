import os
from typing import List, Tuple

from utils.args import parse_args
from utils.timer import timer

"""
Preprocessing:
- The input file has three blocks separated by blank lines: the starting frequencies, the swap instructions
  (`X-Y` pairs), and the test index. Track numbers in the puzzle are 1-indexed, so we keep the parsed swap
  pairs 1-indexed too and just subtract 1 whenever we index into the `freqs` list.

Part 1:
- This one is a straight simulation: walk the swap instructions in order and swap the two tracks each one
  references. Nothing more to it.

Part 2:
- The trick is noticing that the "3-swap" only ever needs X and Y from the current instruction plus Z, the
  first number of the *next* instruction - so there's no need to build explicit (X, Y, Z) triples up front.
- We can just slide a window over two consecutive swap lines at a time and rotate three values using the
  pair we're on plus the next pair's X. Wrapping the last line back to the first is handled by appending a
  copy of `swaps[0]` to the end of the list before looping, so the final iteration naturally pairs the last
  instruction with the first one.
- The rotation itself is a single simultaneous tuple assignment: given X, Y from the current pair and Z from
  the next pair's first track, we send old X to Y, old Y to Z, and old Z to X, all from the pre-swap values.
  Using the first example's first two swap lines (4-8 then 5-8, so X=4, Y=8, Z=5) on
  159, 527, 827, 596, 296, 413, 45, 796, 853, 778:
    old freqs[X-1] = 596, freqs[Y-1] = 796, freqs[Z-1] = 296
    new freqs[Z-1] = old freqs[Y-1] = 796  ->  track 5 becomes 796
    new freqs[Y-1] = old freqs[X-1] = 596  ->  track 8 becomes 596
    new freqs[X-1] = old freqs[Z-1] = 296  ->  track 4 becomes 296
  which gives 159, 527, 827, 296, 796, 413, 45, 596, 853, 778 - matching the puzzle's own trace.

Part 3:
- This is the block-swap version of part 1: instead of swapping single tracks at X and Y, we swap two runs
  of consecutive tracks starting at X and Y. The block length is capped twice - first so the two blocks
  can't overlap (bounded by the distance between X and Y), then again so the second block can't run past
  the last track.
- Worked example straight from the block-swap explanation: list 34, 12, 67, 15, 98 (5 tracks), instruction
  2-4. The distance between the starts caps the length at 4-2=2. A length-2 block starting at track 4 covers
  tracks 4-5, which fits exactly inside the 5 tracks, so no further shrinking is needed and size stays 2.
- That gives us block A = tracks 2-3 (12, 67) and block B = tracks 4-5 (15, 98). We swap position by
  position - first track of each block, then second track of each block:
    swap track 2 <-> track 4:  34, 15, 67, 12, 98
    swap track 3 <-> track 5:  34, 15, 98, 12, 67
  which lands on 34, 15, 98, 12, 67, the same result the puzzle gives for this instruction.
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
    freqs, swaps, test_index = parse_file()

    for s in swaps:
        s = sorted(s)
        size = s[1] - s[0]
        if s[1] + size > len(freqs) - 1:
            size = len(freqs) - s[1] + 1

        freqs[s[0] - 1 : s[0] - 1 + size], freqs[s[1] - 1 : s[1] - 1 + size] = (
            freqs[s[1] - 1 : s[1] - 1 + size],
            freqs[s[0] - 1 : s[0] - 1 + size],
        )

    print(f"Frequency: {freqs[test_index-1]}")


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
part3()
