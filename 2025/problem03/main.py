import os
import re
from typing import List

from utils.args import parse_args
from utils.timer import timer

"""
Preprocessing:
- Each line holds two ranges, but they don't always mean the same thing across parts: in part 1 every
  range is its own pile, while in part 2 and 3 a pair of ranges on one line forms a single pile.
- To keep one parser for all three parts, we flatten every line into two consecutive entries in `box_ranges`,
  so a pile's two ranges always sit at `box_ranges[2i]` and `box_ranges[2i + 1]`.

Part 1:
- Every range is counted on its own, so the size of a range `a-b` is just `b - a + 1`. Summing that over
  every range in the file gives the total.

Part 2:
- Now a pile is the *union* of its two ranges, not just their sum. If the ranges overlap (or touch),
  boxes are being double counted by adding the range sizes directly, since a shared number should only be
  counted once.
- The trick is to check whether the ranges overlap first: if they do, the union is just one contiguous 
  span from the pile's minimum to its maximum; if they don't, there's no overlap to correct for, so the 
  sizes can simply be added.
    range_1 = 6-8, range_2 = 8-10
    these overlap (8 is in both), so the union spans 6 to 10: 10 - 6 + 1 = 5 boxes
    range_1 = 3-4, range_2 = 7-8
    these don't overlap, so we just add the sizes: 2 + 2 = 4 boxes

Part 3:
- Same grouping idea as part 2, but now we're combining two *adjacent piles* (4 ranges total) into one
  set and counting how many unique labels it holds, sliding that 4-range window one pile at a time across
  the whole file and keeping the largest set size seen.
- Building an explicit set of every labelled number (rather than reasoning about overlaps like in part 2) 
  is a little brute force, but with only two piles and small ranges to combine, it's simple and fast enough.
"""


TEST_DATA = parse_args()


@timer
def part1():
    box_ranges = parse_file()

    total_boxes = 0
    for box_range in box_ranges:
        total_boxes += box_range[1] - box_range[0] + 1

    print(f"Total boxes: {total_boxes}")


@timer
def part2():
    box_ranges = parse_file()

    total_boxes = 0
    for i in range(0, len(box_ranges) - 1, 2):
        range_1 = box_ranges[i]
        range_2 = box_ranges[i + 1]

        if overlaps(range_1, range_2):
            box_range = set(range_1 + range_2)
            total_boxes += max(box_range) - min(box_range) + 1
        else:
            total_boxes += range_1[1] - range_1[0] + 1
            total_boxes += range_2[1] - range_2[0] + 1

    print(f"Total boxes: {total_boxes}")


@timer
def part3():
    box_ranges = parse_file()

    max_unique_labeled = 0
    for i in range(0, len(box_ranges) - 2, 2):
        box_set = set()
        for j in range(4):
            box_set.update(set(range(box_ranges[i + j][0], box_ranges[i + j][1] + 1)))

        num_unique_labels = len(box_set)

        if num_unique_labels > max_unique_labeled:
            max_unique_labeled = num_unique_labels

    print(f"Max uniquely labelled boxes: {max_unique_labeled}")


def overlaps(range_1: List[int], range_2: List[int]) -> bool:
    return range_1[0] <= range_2[1] and range_2[0] <= range_1[1]


def parse_file() -> List[List[int]]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    box_ranges = []
    with open(abs_file_path, "r") as f:
        for line in f:
            line = re.search(r"(\d+)-(\d+)\s+(\d+)-(\d+)", line.strip())
            line = list(map(int, line.groups()))
            box_ranges.append([line[0], line[1]])
            box_ranges.append([line[2], line[3]])

    return box_ranges


part1()
part2()
part3()
