import os
import operator
import numpy as np
import numpy.typing as npt
from itertools import cycle
from typing import List, Tuple

from utils.args import parse_args
from utils.timer import timer

"""
Preprocessing:
- The file is three blocks separated by blank lines: the grid, the instructions, and the flow-control
  actions. Instructions are kept as raw tuples of tokens (e.g. `("SHIFT", "ROW", "1", "BY", "3")` or
  `("ADD", "7", "ROW", "3")`) instead of being parsed into a structured form up front, so `execute()`
  can just pattern-match on the first token and grab whichever positions it needs.

Part 1:
- Plain simulation: load the grid into a numpy array and run every instruction through `execute()` in
  file order.
- Shifts are just `np.roll`, which does the cyclic wraparound for free. The "clamp back into [0, 1073741823]"
  rule turns out to be exactly what Python/numpy's `%` operator already does - adding or subtracting 
  1073741824 until a value is back in range is the same as taking it mod 1073741824 - so `grid_op` 
  never needs a manual add/sub loop, just `% max_value` after every ADD/SUB/MULTIPLY.
- Once every instruction has run, `get_max` sums along both axes and takes the largest row or column sum.

Part 2:
- Same grid mechanics, but now the instruction list is treated as a queue driven by the flow-control
  actions instead of being walked straight through: `TAKE` pops the front instruction into `taken`,
  `CYCLE` appends `taken` back onto the end of the queue, and `ACT` runs `taken` through the same
  `execute()` from part 1. Only the actions listed in the file are performed, once, in order.

Part 3:
- Same queue-driven simulation as part 2, but the action list is now consumed on a loop
  (`itertools.cycle`) instead of once, since the flow-control actions repeat until every instruction has
  been taken and acted on.
- The one shortcut worth calling out: once a `TAKE` empties the instruction queue, every action after
  that must still eventually be the `ACT` that runs it - but any `CYCLE` in between does nothing, because
  appending the sole remaining instruction to an empty queue and then immediately `TAKE`-ing it straight
  back out is a no-op. The code exploits this by checking, at the top of every loop iteration, whether 
  the queue is already empty; if it is, it skips straight to executing whatever is in `taken` and stops, 
  instead of simulating the rest of the guaranteed `CYCLE`/`TAKE`/`ACT` dance around it.
"""


TEST_DATA = parse_args()
OPS = {"ADD": operator.add, "SUB": operator.sub, "MULTIPLY": operator.mul}


@timer
def part1():
    grid, instructions, _ = parse_file()
    grid = np.array(grid)

    for instruction in instructions:
        execute(grid, instruction)

    max_sum = get_max(grid)

    print(f"Largest sum: {max_sum}")


@timer
def part2():
    grid, instructions, actions = parse_file()
    grid = np.array(grid)

    taken = ()
    for action in actions:
        match action:
            case "TAKE":
                taken = instructions.pop(0)
            case "CYCLE":
                instructions.append(taken)
            case "ACT":
                execute(grid, taken)

    max_sum = get_max(grid)

    print(f"Largest sum: {max_sum}")


@timer
def part3():
    grid, instructions, actions = parse_file()
    grid = np.array(grid)

    taken = ()
    for action in cycle(actions):
        if len(instructions) <= 0:
            # Execute the last instruction in taken
            execute(grid, taken)
            break

        match action:
            case "TAKE":
                taken = instructions.pop(0)
            case "CYCLE":
                instructions.append(taken)
            case "ACT":
                execute(grid, taken)

    max_sum = get_max(grid)

    print(f"Largest sum: {max_sum}")


def grid_shift(
    grid: npt.NDArray,
    row_col: str,
    id: int,
    number: int,
):
    if row_col == "ROW":
        grid[id, :] = np.roll(grid[id, :], number)
    elif row_col == "COL":
        grid[:, id] = np.roll(grid[:, id], number)


def grid_op(
    grid: npt.NDArray,
    row_col_all: str,
    id: int,
    number: int,
    op: str,
    max_value: int = 1073741824,
):
    if row_col_all == "ROW":
        grid[id, :] = OPS[op](grid[id, :], number) % max_value
    elif row_col_all == "COL":
        grid[:, id] = OPS[op](grid[:, id], number) % max_value
    elif row_col_all == "ALL":
        grid[:, :] = OPS[op](grid, number) % max_value


def get_max(grid: npt.NDArray) -> int:
    max_col_sum = grid.sum(axis=0).max()
    max_row_sum = grid.sum(axis=1).max()

    return max(max_col_sum, max_row_sum)


def execute(grid: npt.NDArray, instruction: str):
    match instruction[0]:
        case "ADD" | "SUB" | "MULTIPLY":
            id = 0
            if instruction[2] != "ALL":
                id = int(instruction[3]) - 1
            grid_op(
                grid,
                instruction[2],
                id,
                int(instruction[1]),
                instruction[0],
            )
        case "SHIFT":
            grid_shift(
                grid,
                instruction[1],
                int(instruction[2]) - 1,
                int(instruction[4]),
            )


def parse_file() -> Tuple[List[List[int]], List[Tuple[str]], Tuple[str]]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    grid = []
    instructions = []
    actions = []
    with open(abs_file_path, "r") as f:
        grid_raw, instructions_raw, actions_raw = f.read().split("\n\n")

        for row in grid_raw.split("\n"):
            row = (r.strip() for r in row.split(" "))
            grid.append(list(map(int, row)))

        for instruction in instructions_raw.split("\n"):
            instructions.append(tuple(instruction.strip().split(" ")))

        actions = tuple(a.strip() for a in actions_raw.split("\n"))

    return grid, instructions, actions


part1()
part2()
part3()
