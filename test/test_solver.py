#!/usr/bin/env python3

from unittest import TestCase

from textwrap import dedent
from solver import board_from_str


class SolverTest(TestCase):
    def test_parse(self):
        b = board_from_str(dedent("""
            3 1 .  . . .  . . .
            . . .  9 5 2  6 . .
            5 9 .  . 3 .  . . 2

            . . .  . 8 .  9 7 5
            . . .  2 . 1  . . .
            9 4 8  . 6 .  . . .

            8 . .  . 7 .  . 6 9
            . . 9  6 2 4  . . .
            . . .  . . .  . 3 4
        """))
        self.assertEqual(
            (4, 7, 8),
            tuple(sorted(b.find_all_possible(0, 3)))
        )

    def test_invalid(self):
        b = board_from_str("""
            5 . .  . 7 .  . . .
            3 4 .  1 5 .  . . 7
            . 9 .  . 3 6  . . .

            6 . .  . 2 1  . . 9
            2 . 4  9 8 7  1 . .
            . 1 .  . 4 5  . . .

            . . .  . . 3  . 2 6
            . . .  . . .  8 . .
            9 . .  . . .  3 4 .
        """)
        self.assertTrue(b.is_valid())
