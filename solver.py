#!/usr/bin/env python3

import sys

from typing import List, IO, Iterator, Set, Tuple, Iterable, Optional
from copy import deepcopy


class Board(object):
    """
    A board represents the 9 x 9 squares of a sudoku board
    """
    def __init__(self, items: List[List[int]]) -> None:
        self.items = items

    def print(self, output: IO = sys.stdout) -> None:
        """
        Prints the current board onto output, stdout by default.
        """
        for i, row in enumerate(self.items):
            if i in (3, 6):
                output.write("\n")
            s: List[str] = []
            for j in range(0, 9, 3):
                s.append(" ".join(_dot_or_num(x) for x in row[j:j+3]))
            output.write("  ".join(s) + "\n")

    def yield_box(self, x: int, y: int) -> Iterator[int]:
        """
        Yields all the values in the box where the item with coordinates x, y
        is located but not the x, y item.
        """
        x_start = x // 3 * 3
        y_start = y // 3 * 3
        for i in range(x_start, x_start + 3):
            for j in range(y_start, y_start + 3):
                if i == x and j == y:
                    continue
                yield self.items[i][j]

    def yield_row(self, x: int, y: int) -> Iterator[int]:
        """
        Yields all the values in the row where the item with coordinates x, y
        is lcoated but not the x, y item.
        """
        for i, value in enumerate(self.items[x]):
            if i == y:
                continue
            yield value

    def yield_column(self, x: int, y: int) -> Iterator[int]:
        """
        Yields all the values in the column where the item with coordinates
        x, y is located but not the x, y item.
        """
        for a in range(9):
            if a == x:
                continue
            yield self.items[a][y]

    def find_all_possible(self, x: int, y: int):
        """
        Yields all valid values that the item with coordinates x, y could take
        """
        other: Set[int] = set()
        for i in self._all_others(x, y):
            if i != 0:
                other.add(i)
        for i in range(1, 10):
            if i not in other:
                yield i

    def is_valid(self) -> bool:
        """
        Returns True if all the constraints of the board are satisfied;
        no duplicates in any row, column or box, else False.
        """
        for row in self.items:
            s: Set[int] = set()
            for item in row:
                if not item:
                    continue
                if item in s:
                    return False
                s.add(item)
        for x in range(9):
            s = set()
            for y in range(9):
                item = self.items[x][y]
                if item:
                    if item in s:
                        return False
                    s.add(item)
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                s = set()
                for k in range(3):
                    for l in range(3):
                        item = self.items[i+k][j+l]
                        if item:
                            if item in s:
                                return False
                            s.add(item)
        return True

    def _all_others(self, x: int, y: int):
        """
        Yield all the items in the same box, row and column as the item
        with coordinates x, y.
        """
        yield from self.yield_box(x, y)
        yield from self.yield_row(x, y)
        yield from self.yield_column(x, y)


def _dot_or_num(i: int):
    "Returns a string representation of integer i, or '.' if i is 0"
    return "." if i == 0 else str(i)


def read_input(file_name: str) -> Board:
    """
    Reads and returns a board from the file with file_name.
    """
    with open(file_name, "r") as f:
        return board_from_lines(f)


def board_from_lines(lines: Iterable[str]) -> Board:
    """
    Reads and returns a board from the string returned when iterating over
    lines.
    """
    items: List[List[int]] = []
    for i, line in enumerate(lines):
        line = line.strip().replace(" ", "").replace(".", "0")
        if not line:
            # ignore empty lines, they are just there for formatting
            continue
        if len(line) != 9:
            raise Exception(
                f"Line {i+1} in does not contain 9 items as "
                "expected: {line}"
            )
        items.append(list(int(i) for i in line))
    return Board(items)


def board_from_str(input: str) -> Board:
    """
    Reads and returns a board from the provided multiline string.
    """
    return board_from_lines(input.split("\n"))


def solve(board: Board) -> Optional[Board]:
    """
    Attempt to solve board. Return None if board can never be solved.
    if a solution is found, return the Board representing the solution
    """

    while True:
        list_of_possibles: List[Tuple[Tuple[int, int], Tuple[int, ...]]] = []
        # figure out which values are possible in each empty slot on the board
        for x in range(9):
            for y in range(9):
                if not board.items[x][y]:
                    all_possible = tuple(board.find_all_possible(x, y))
                    if not all_possible:
                        return None
                    list_of_possibles.append(((x, y), all_possible))

        if not list_of_possibles:
            # our board is full of values. Win!
            return board

        # figure out if there are any slots that only has a single possibility
        singles = [x for x in list_of_possibles if len(x[1]) == 1]
        if singles:
            for (x, y), all_possible in singles:
                board.items[x][y] = all_possible[0]
                if not board.is_valid():
                    return None
        else:
            # pick the first slot slot and try the different possible values
            coordinates, possibles = list_of_possibles[0]
            for i in possibles:
                b = deepcopy(board)
                b.items[coordinates[0]][coordinates[1]] = i
                ret = solve(b)
                if ret:
                    return ret
            return None
    return None


if __name__ == '__main__':
    board = read_input("hard2.txt")
    board.print()
    result = solve(board)
    if not result:
        print("Did not find a solution")
        sys.exit(1)
    else:
        print("The solution:")
        result.print()
