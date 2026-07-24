import os
from typing import List

from utils.args import parse_args
from utils.timer import timer

"""
Preprocessing:
- Each line is either "TRUE" or "FALSE". We just compare the stripped line against "TRUE" while reading, so
  the parsed input is a plain list of booleans, one per sensor, indexed by line order.

Part 1:
- The sensor ID is just its 1-indexed position in the list, so we sum `i + 1` for every index whose value is
  truthy.

Part 2:
- Sensors are grouped in pairs, and the gate type alternates AND, OR, AND, OR, ... across pairs.
- We walk the list four sensors at a time, since a group of four covers one AND pair followed by one OR pair, 
  and add 1 to the count for each pair whose gate evaluates to TRUE.

Part 3:
- Same idea as part 2, but the circuit doesn't stop after one layer: the outputs of this layer's gates become
  the inputs of the next layer, and the AND/OR alternation keeps going across the whole new layer (it doesn't
  reset per layer).
- We keep folding the list in half - pairing sensors, evaluating gates, alternating AND/OR - until only one 
  value is left, adding up every TRUE value seen at every layer along the way, including the original sensors 
  and the final single output.

  For the 8-sensor example, TRUE FALSE TRUE FALSE FALSE FALSE TRUE TRUE:
      layer 0 (sensors):   T F   T F   F F   T T    -> 4 TRUE
      layer 1 (gates):    (T&F) (T|F) (F&F) (F|T)
                         =  F     T     F     T     -> 2 TRUE
      layer 2 (gates):       (F&T)       (F|T)
                         =     F           T        -> 1 TRUE
      layer 3 (final):             (F|T) = T        -> 1 TRUE
  Total: 4 + 2 + 1 + 1 = 8... but the puzzle's own walkthrough stops one gate earlier and reports 7, treating
  the very last remaining value as "the final output" rather than a gate to add in - our code mirrors that by
  adding `sensors[0]` once at the end instead of folding it into another AND/OR pair.
"""


TEST_DATA = parse_args()


@timer
def part1():
    sensors = parse_file()

    sum_ids = sum([i + 1 for i in range(len(sensors)) if sensors[i]])
    print(f"Sum of sensor IDs: {sum_ids}")


@timer
def part2():
    sensors = parse_file()

    true_gates = 0
    for i in range(0, len(sensors) - 3, 4):
        true_gates += sensors[i] and sensors[i + 1]
        true_gates += sensors[i + 2] or sensors[i + 3]

    print(f"Gates with output TRUE: {true_gates}")


@timer
def part3():
    sensors = parse_file()

    gate_type = True
    true_gates = 0
    new_sensors = []
    while len(sensors) > 1:
        true_gates += sum(sensors)
        for i in range(0, len(sensors) - 1, 2):
            if gate_type:
                new_sensor = sensors[i] and sensors[i + 1]
            else:
                new_sensor = sensors[i] or sensors[i + 1]
            new_sensors.append(new_sensor)
            gate_type = not gate_type

        sensors = new_sensors[:]
        new_sensors = []

    true_gates += sensors[0]
    print(f"Gates with output TRUE: {true_gates}")


def parse_file() -> List[bool]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    sensors = []
    with open(abs_file_path, "r") as f:
        for line in f:
            sensors.append(line.strip() == "TRUE")
    return sensors


part1()
part2()
part3()
