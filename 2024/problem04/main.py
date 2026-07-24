import os
import math
import heapq
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

    print(unique_visited)
    print(f"Number of different locations: {len(unique_visited)}")


@timer
def part3():
    # TODO: Implement part 3
    # 231 incorrect
    paths = parse_file()
    graph = parse_graph(paths)

    for key in graph.keys():
        print(f"{key} -> {graph[key]}")

    total_time = 0
    for i, location in enumerate(graph.keys()):
        time, path = dijkstra(graph, "STT", location)
        total_time += time
        print(f"{i+1} Time between STT and {location}: {time}")
        print(f"   Path: {" ".join(path)}")

    print(f"Total time: {total_time}")


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


def dijkstra(
    graph: Dict[str, List[str]], start: str, end: str
) -> Tuple[int, List[str]]:
    # Priority queue
    pq = []
    dist = {loc: math.inf for loc in graph.keys()}
    parent = {coord: None for coord in graph.keys()}
    dist[start] = 0
    heapq.heappush(pq, (start, 0))

    while pq:
        u, d = heapq.heappop(pq)

        if u == end:
            # Reconstruct path
            path = []
            curr = end
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            return d, path

        # If this distance not the latest shortest one, skip it
        if d > dist[u]:
            continue

        for v in graph[u]:
            if dist[u] + 1 < dist[v]:
                dist[v] = dist[u] + 1
                parent[v] = u
                heapq.heappush(pq, (v, dist[v]))

    return -1, []


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
