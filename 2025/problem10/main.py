import os
import math
import heapq
from typing import List, Tuple

from utils.args import parse_args
from utils.timer import timer
from utils.utils import print_matrix_with_path

"""
Preprocessing:
- Each line is a row of space-separated integers, so we just split on spaces and cast to int, keeping
  each row as a tuple.

Part 1:
- The safest row or column is just the one with the smallest sum, so we compute every row sum and every
  column sum in a single pass over the grid, tracking the running minimum row sum along the way and the
  per-column totals in a `cols_sum` accumulator. Once the grid has been scanned, the answer is the smaller
  of the best row sum and the smallest column sum.

Part 2:
- This is a shortest-path problem: find the cheapest sum of danger levels from (0, 0) to a fixed target,
  moving only right or down. We use Dijkstra's algorithm, treating each grid cell as a node whose "edge
  weight" is the danger level of the cell being entered, and only ever relaxing the two allowed neighbors
  (down and right).
- One tricky thing here is that Dijkstra is more general than we actually need: because we can only move
  right or down, every path to a cell (i, j) passes only through cells with smaller or equal row and column
  indices, so the grid is already a DAG processed in a natural order. `min_path_dp()` implements this
  observation directly, filling `dist[i][j] = grid[i][j] + min(dist[i-1][j], dist[i][j-1])` row by row
  instead of pulling from a priority queue, and produces the same distance and path as `dijkstra()`.
  Dijkstra still works correctly here (all weights are positive), it's just doing more bookkeeping than the
  restricted movement rules require.

Part 3:
- Same algorithm as part 2, just with the target changed from (14, 14) to the bottom-right corner of the
  grid, (rows - 1, cols - 1).
"""


TEST_DATA = parse_args()


@timer
def part1():
    grid = parse_file()

    cols_sum = [0 for _ in range(len(grid[0]))]
    min_row_sum = math.inf
    for i in range(len(grid)):
        row_sum = 0
        for j in range(len(grid[i])):
            row_sum += grid[i][j]
            cols_sum[j] += grid[i][j]

        if row_sum < min_row_sum:
            min_row_sum = row_sum

    min_col_sum = min(cols_sum)

    print(f"Danger level: {min(min_row_sum, min_col_sum)}")


@timer
def part2():
    grid = parse_file()
    start, end = (0, 0), (14, 14)

    dist, path = dijkstra(grid, start, end)

    print_matrix_with_path(grid, path)

    print(f"Danger lever from {start} to {end}: {dist}")


@timer
def part3():
    grid = parse_file()
    start, end = (0, 0), (len(grid) - 1, len(grid[0]) - 1)

    dist, path = dijkstra(grid, start, end)

    print_matrix_with_path(grid, path)

    print(f"Danger lever from {start} to {end}: {dist}")


def dijkstra(
    grid: List[Tuple[int]], start: Tuple[int], end: Tuple[int]
) -> Tuple[int, List[Tuple[int]]]:
    # Priority queue
    pq = []
    dist = dict()
    parent = dict()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            dist[(i, j)] = math.inf
            parent[(i, j)] = None

    dist[start] = grid[start[0]][start[1]]
    heapq.heappush(pq, (dist[start], start))

    while pq:
        d, u = heapq.heappop(pq)

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

        for d in ((1, 0), (0, 1)):
            v = (u[0] + d[0], u[1] + d[1])
            if v[0] >= len(grid) or v[1] >= len(grid[0]):
                continue

            w = grid[v[0]][v[1]]

            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

    return -1, []


def min_path_dp(
    grid: List[Tuple[int]], start: Tuple[int], end: Tuple[int]
) -> Tuple[int, List[Tuple[int]]]:
    """
    Same result as dijkstra(), but exploits the fact that moves are restricted to right/down: every
    path to (i, j) only passes through cells with smaller or equal row and column indices, so the grid
    can be filled as a DAG in row-major order without a priority queue.
    """
    rows, cols = len(grid), len(grid[0])

    dist = [[math.inf] * cols for _ in range(rows)]
    parent = dict()

    dist[start[0]][start[1]] = grid[start[0]][start[1]]

    for i in range(start[0], rows):
        for j in range(start[1], cols):
            if (i, j) == start:
                continue

            best, best_parent = math.inf, None
            if i > start[0] and dist[i - 1][j] < best:
                best, best_parent = dist[i - 1][j], (i - 1, j)
            if j > start[1] and dist[i][j - 1] < best:
                best, best_parent = dist[i][j - 1], (i, j - 1)

            dist[i][j] = best + grid[i][j]
            parent[(i, j)] = best_parent

    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = parent.get(curr)
    path.reverse()

    return dist[end[0]][end[1]], path


def parse_file() -> List[Tuple[int]]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    grid = []
    with open(abs_file_path, "r") as f:
        for line in f:
            grid.append(tuple(int(l) for l in line.strip().split(" ")))
    return grid


part1()
part2()
part3()
