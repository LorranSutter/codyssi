import os
import re
from typing import Tuple, List

from utils.args import parse_args
from utils.timer import timer

"""
Preprocessing:
- Each line is a coordinate pair written as "(x, y)", so we just regex out the two numbers and cast them
  to ints.

Part 1:
- We compute the Manhattan distance from the origin to every island and take max - min. Nothing more to
  it than a single pass over the list.

Part 2:
- Same distance function as part 1, but now we need the closest island to a given island rather than to
  the origin, and we need to handle ties (smaller x, then smaller y).
- We wrote get_closest_island() to do this generically: walk every candidate, track the running minimum, 
  and whenever a new candidate ties the current minimum, hand both to untie() to pick the winner. 
  That generic function is what makes part 3 a two-line change instead of a rewrite.
- One thing worth flagging: get_closest_island() skips d == 0, i.e. an island can't be "closest to itself".
  That's why we can call it with a coordinate that's already inside the list (as part 3 does) without it
  short-circuiting to a distance of 0.

Part 3:
- This is a nearest-neighbor greedy tour: repeatedly jump to the closest unvisited island, removing it from
  the pool, and add up the distance travelled.
- Since get_closest_island() already does "closest island to a point, with tie-breaking" generically, 
  part 3 just loops it, using the previous island as the next point and shrinking the coords list each iteration.
- Obs: this greedy approach doesn't find the optimal tour (that's the traveling salesman problem, and the
  puzzle explicitly says finding the true shortest path is too expensive with 50+ islands) - it's a
  heuristic that's "likely to be a short path", not guaranteed to be the shortest one.
"""


TEST_DATA = parse_args()


@timer
def part1():
    coords = parse_file()

    dists = tuple(manhattan_dist((0, 0), coord) for coord in coords)
    min_dist = min(dists)
    max_dist = max(dists)

    print(f"Diff max and min dists: {max_dist-min_dist}")


@timer
def part2():
    coords = parse_file()

    closest_coord, _ = get_closest_island((0, 0), coords)
    _, min_dist = get_closest_island(closest_coord, coords)

    print(f"Shortest dist: {min_dist}")


@timer
def part3():
    coords = parse_file()

    total_dist = 0
    current_coord = (0, 0)
    while coords:
        closest_island, min_dist = get_closest_island(current_coord, coords)
        coords.remove(closest_island)
        current_coord = closest_island
        total_dist += min_dist

    print(f"Total dist: {total_dist}")


def manhattan_dist(p1: List[int] | Tuple[int], p2: List[int] | Tuple[int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def get_closest_island(coord, coords) -> Tuple[List[int], int]:
    min_dist = 1000
    closest_coord = (0, 0)
    for c in coords:
        d = manhattan_dist(coord, c)
        if d > 0 and d <= min_dist:
            if d == min_dist:
                c = untie(closest_coord, c)
            min_dist = d
            closest_coord = c
    return closest_coord, min_dist


def untie(p1: List[int] | Tuple[int], p2: List[int] | Tuple[int]) -> Tuple[int]:
    if p1[0] == p2[0]:
        if p1[1] < p2[1]:
            return p1
        else:
            return p2
    if p1[0] < p2[0]:
        return p1
    else:
        return p2


def parse_file() -> List[str]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    coords = []
    with open(abs_file_path, "r") as f:
        for line in f:
            line = re.search(r"\((-*\d+),\s*(-*\d+)\)", line)
            line = tuple(map(int, line.groups()))
            coords.append(line)
    return coords


part1()
part2()
part3()
