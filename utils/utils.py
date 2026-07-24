from typing import List


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\x1b[6;30;42m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


class tcolors:
    BLACK = "\33[30m"
    RED = "\33[31m"
    GREEN = "\33[32m"
    YELLOW = "\33[33m"
    BLUE = "\33[34m"
    VIOLET = "\33[35m"
    CYAN = "\33[36m"
    WHITE = "\33[37m"

    GRAY = "\33[90m"
    BRIGHT_RED = "\33[91m"
    BRIGHT_GREEN = "\33[92m"
    BRIGHT_YELLOW = "\33[93m"
    BRIGHT_BLUE = "\33[94m"
    BRIGHT_VIOLET = "\33[95m"
    BRIGHT_CYAN = "\33[96m"
    BRIGHT_WHITE = "\33[97m"

    ORANGE = "\33[38;5;208m"

    RESET = "\033[0m"


def print_matrix(matrix: List[List[str]]):
    for row in matrix:
        print("".join(row))
