import os
from collections import defaultdict, deque
from typing import List, Tuple
from dataclasses import dataclass

from utils.args import parse_args
from utils.timer import timer

"""
Preprocessing:
- Each artifact line is `code | ID`. The last two lines of the file are a separate pair of
  artifacts to recheck later (part 3), so we pop the blank separator line and split the file into
  the main artifact list and this two-artifact recheck list up front.

Part 1:
- We build a binary search tree by inserting artifacts one at a time in file order: each artifact
  compares its ID against the current node and walks left (smaller) or right (greater-or-equal)
  until it finds an empty slot to sit in. The root is layer 1, its children are layer 2, and so on.
- Once the tree is built, a BFS walk (a queue of `(node, level)` pairs) visits every node exactly
  once while naturally tracking which layer it's on. We sum IDs per layer as we go, then multiply
  the biggest layer sum by the number of occupied layers.

Part 2:
- Inserting the new artifact (ID 500000) is the same walk `add_child` does, except instead of just
  landing on a node we record every code visited along the way. `find_sequence` walks from the
  root, comparing the new ID against each node's ID, appending that node's code to the sequence,
  and stepping left or right until it hits an empty slot.

Part 3:
- The key insight is that the least common ancestor of two nodes in a BST is exactly the point
  where their search paths from the root diverge. Both artifacts are found by the same walk as
  part 2, so we reuse `find_sequence` to get each one's path from the root, then walk both paths
  in lockstep and keep the last code where they still agreed.
- Obs: this works because it computes both paths independently, but it could be done in one pass by
  walking the tree once and comparing both target IDs against each node at the same time - the LCA
  is the last node where both IDs still land on the same side.
"""


TEST_DATA = parse_args()


@dataclass
class Artifact:
    ID: int
    code: str


class TreeNode:
    def __init__(self, node: Artifact):
        self.data = node
        self.left = None
        self.right = None

    def add_child(self, node: Artifact):
        if node.ID < self.data.ID:
            if not self.left:
                self.left = TreeNode(node)
            else:
                self.left.add_child(node)
        else:
            if not self.right:
                self.right = TreeNode(node)
            else:
                self.right.add_child(node)

    def print_tree(self, level=0):
        """Recursively prints the tree with visual indentation."""
        indent = "  " * level
        print(f"{level}{indent}└── ({self.data.code},{self.data.ID})")
        for child in [self.left, self.right]:
            if child:
                child.print_tree(level + 1)


@timer
def part1():
    artifacts, _ = parse_file()

    root = make_tree(artifacts)
    # root.print_tree()

    queue = deque([(root, 1)])

    level_sum = defaultdict(int)
    while queue:
        v, level = queue.popleft()

        level_sum[level] += v.data.ID

        if v.left:
            queue.append((v.left, level + 1))
        if v.right:
            queue.append((v.right, level + 1))

    max_level = max(level_sum.keys())
    max_sum = max(level_sum.items(), key=lambda item: item[1])[1]

    print(f"Product max sum and layers: {max_level * max_sum}")


@timer
def part2():
    artifacts, _ = parse_file()
    new_id = 500000

    root = make_tree(artifacts)
    # root.print_tree()

    sequence = "-".join(find_sequence(root, new_id))

    print(f"Sequence: {sequence}")


@timer
def part3():
    artifacts, artifacts_recheck = parse_file()

    root = make_tree(artifacts)
    # root.print_tree()

    sequence1 = find_sequence(root, artifacts_recheck[0].ID)
    sequence2 = find_sequence(root, artifacts_recheck[1].ID)

    least_common_ancestor = ""
    for code1, code2 in zip(sequence1, sequence2):
        if code1 != code2:
            break
        least_common_ancestor = code1

    print(f"Least common ancestor: {least_common_ancestor}")


def make_tree(artifacts: List[Artifact]) -> TreeNode:
    root = TreeNode(artifacts[0])
    for artifact in artifacts[1:]:
        root.add_child(artifact)

    return root


def find_sequence(root: TreeNode, ID: int) -> List[str]:
    sequence = []
    node = root
    while node:
        sequence.append(node.data.code)
        if ID < node.data.ID:
            if not node.left:
                break
            else:
                node = node.left
        else:
            if not node.right:
                break
            else:
                node = node.right

    return sequence


def parse_file() -> Tuple[List[Artifact], List[Artifact]]:
    file_name = "input_sample.txt" if TEST_DATA else "input.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    artifacts = []
    artifacts_recheck = []
    with open(abs_file_path, "r") as f:
        artifacts_raw = f.read().split("\n")
        artifacts_raw.pop(-3)

        for a in artifacts_raw[:-2]:
            code, ID = a.strip().split(" | ")
            artifacts.append(Artifact(int(ID), code))
        for a in artifacts_raw[-2:]:
            code, ID = a.strip().split(" | ")
            artifacts_recheck.append(Artifact(int(ID), code))

    return artifacts, artifacts_recheck


part1()
part2()
part3()
