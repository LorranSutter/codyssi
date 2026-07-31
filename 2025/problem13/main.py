import os
import re
import math
from collections import deque
from typing import Dict, List, Tuple

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


@timer
def part1():
    graph = parse_file()

    dists = bfs("STT", graph)
    # No need to sort

    prod_longestst_dists = math.prod(dists[-3:])

    print(f"Product of the 3 longestst dists: {prod_longestst_dists}")


@timer
def part2():
    graph = parse_file()

    dists = bfs("STT", graph, True)
    dists.sort()

    prod_longestst_dists = math.prod(dists[-3:])

    print(f"Product of the 3 longestst dists: {prod_longestst_dists}")


@timer
def part3():
    # TODO: Implement part 3
    lines = parse_file()
    pass


def bfs(
    start: str, graph: Dict[str, List[Tuple[str, int]]], weighted: bool = False
) -> List[int]:
    visited = set()
    queue = deque()

    visited.add(start)
    queue.append((start, 0))

    dists = []
    while queue:
        location, dist = queue.popleft()
        dists.append(dist)

        if location not in graph:
            continue

        for loc in graph[location]:
            if loc[0] not in visited:
                visited.add(loc[0])
                queue.append((loc[0], dist + (loc[1] if weighted else 1)))

    return dists


def parse_file() -> Dict[str, List[Tuple[str, int]]]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    graph = dict()
    with open(abs_file_path, "r") as f:
        for line in f:
            line = re.search(r"(\w+)\s->\s(\w+)\s\|\s(\d+)", line)
            source, dest, length = line.groups()
            if source in graph:
                graph[source].append((dest, int(length)))
            else:
                graph[source] = [(dest, int(length))]
    return graph


part1()
part2()
part3()
