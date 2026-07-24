import os
from typing import List

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
    # 623
    sensors = parse_file()

    gate_type = True
    true_gates = 0
    new_sensors = []
    while len(sensors) > 1:
        print(sensors)
        true_gates += sum(sensors)
        print(f"True gates: {true_gates}")
        for i in range(0, len(sensors) - 1, 2):
            if gate_type:
                new_sensor = sensors[i] and sensors[i + 1]
            else:
                new_sensor = sensors[i] or sensors[i + 1]
            new_sensors.append(new_sensor)
            gate_type = not gate_type

        sensors = new_sensors[:]
        new_sensors = []

    print(sensors)
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
