import os
from collections import deque
from typing import Dict, List

from utils.args import parse_args
from utils.timer import timer

"""
Part 1:
- Each line is just an edge between two location codes, so the unique locations are simply every
  code that shows up on either side of a "<->", collected into a set.

Part 2:
- This is a depth-limited traversal from STT: walk the graph outward, but stop following a branch
  once its depth passes 3. Every location touched along the way, regardless of how many separate
  branches reach it, gets added to a single `unique_visited` set, so the answer is just the size of
  that set once the traversal finishes.
- The traversal here is DFS rather than BFS, and that's fine specifically because we only care about
  reachability within a depth limit, not about the shortest distance to each location. Revisiting a
  node from a different branch is harmless: it just gets re-added to a set that already has it, and
  the recursion still bottoms out because depth is strictly increasing.
- Obs: DFS isn't the most efficient choice here though. Because it explores every branch fully before
  backtracking, it can re-walk the same node many times over from different paths before the depth cap
  kicks in. BFS would have been the better fit: it naturally expands outward one depth level at a time,
  so each location gets discovered once, at its true minimum depth, without the redundant re-visits.

Part 3:
- The naive approach is running a shortest-path search (Dijkstra) from STT to every other location.
  But since every edge has the same weight (1 hour) and there's no single destination to stop at, a
  single BFS from STT already gives the shortest distance to *every* location in one pass - Dijkstra's
  extra bookkeeping for weighted edges buys nothing here.
- So part 3 just runs one BFS from STT, and instead of stopping once we know each node's distance, we
  keep a running total: every time a location is popped off the queue, its distance is added to
  `total_dist`. Because BFS visits each node exactly once, and always via its shortest path, that sum
  is exactly the total time for one vehicle per location, each taking its shortest route.
"""


TEST_DATA = parse_args()


@timer
def part1():
    paths = parse_file()

    unique_locations = set()
    for path in paths:
        unique_locations.add(path[0])
        unique_locations.add(path[1])

    print(f"Number of unique locations: {len(unique_locations)}")


@timer
def part2():
    paths = parse_file()
    graph = parse_graph(paths)

    unique_visited = set()
    dfs("STT", graph, unique_visited, 0, 3)

    print(f"Number of different locations: {len(unique_visited)}")


@timer
def part3():
    paths = parse_file()
    graph = parse_graph(paths)

    total = bfs("STT", graph)

    print(f"Total time: {total}")


def dfs(
    location: str,
    graph: Dict[str, List[str]],
    unique_visited: set,
    depth: int,
    max_depth: int,
):
    if depth > max_depth:
        return

    unique_visited.add(location)

    for loc in graph[location]:
        dfs(loc, graph, unique_visited, depth + 1, max_depth)


def bfs(start: str, graph: Dict[str, List[str]]) -> int:
    visited = set()
    queue = deque()

    visited.add(start)
    queue.append((start, 0))

    total_dist = 0
    while queue:
        location, dist = queue.popleft()
        total_dist += dist

        for loc in graph[location]:
            if loc not in visited:
                visited.add(loc)
                queue.append((loc, dist + 1))

    return total_dist


def parse_graph(paths: List[List[str]]) -> Dict[str, List[str]]:
    graph = dict()
    for path in paths:
        if path[0] in graph:
            graph[path[0]].append(path[1])
        else:
            graph[path[0]] = [path[1]]
        if path[1] in graph:
            graph[path[1]].append(path[0])
        else:
            graph[path[1]] = [path[0]]

    return graph


def parse_file() -> List[List[str]]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    paths = []
    with open(abs_file_path, "r") as f:
        for line in f:
            line = line.strip().split(" <-> ")
            paths.append(line)
    return paths


part1()
part2()
part3()
