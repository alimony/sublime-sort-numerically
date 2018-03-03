#!/usr/bin/env python3
# encoding: utf-8

'''Run some basic tests on various lists of input lines.'''

from __future__ import unicode_literals

if __name__ == '__main__':
    import unittest
    from sort_numerically import sort_lines

    class TestSortNumerically(unittest.TestCase):

        def test_simple_noop(self):
            input_lines = [
                '1',
                '2',
                '3',
            ]
            expected_output_lines = [
                '1',
                '2',
                '3',
            ]
            self.assertEqual(sort_lines(input_lines), expected_output_lines)

        def test_simple_noop_with_alpha(self):
            input_lines = [
                '1 a',
                '2 b',
                '3 c',
            ]
            expected_output_lines = [
                '1 a',
                '2 b',
                '3 c',
            ]
            self.assertEqual(sort_lines(input_lines), expected_output_lines)

        def test_simple_sort(self):
            input_lines = [
                '1',
                '3',
                '2',
            ]
            expected_output_lines = [
                '1',
                '2',
                '3',
            ]
            self.assertEqual(sort_lines(input_lines), expected_output_lines)

        def test_simple_sort_with_alpha(self):
            input_lines = [
                '1 a',
                '3 b',
                '2 c',
            ]
            expected_output_lines = [
                '1 a',
                '2 c',
                '3 b',
            ]
            self.assertEqual(sort_lines(input_lines), expected_output_lines)

        def test_sort_with_decimals(self):
            input_lines = [
                '1.5',
                '1',
                '2.5',
                '2',
            ]
            expected_output_lines = [
                '1',
                '1.5',
                '2',
                '2.5',
            ]
            self.assertEqual(sort_lines(input_lines), expected_output_lines)

        def test_sort_with_multiple_int_groups(self):
            input_lines = [
                '1 1',
                '3 2',
                '2 3',
            ]
            expected_output_lines = [
                '1 1',
                '2 3',
                '3 2',
            ]
            self.assertEqual(sort_lines(input_lines), expected_output_lines)

        def test_sort_with_negatives(self):
            input_lines = [
                '1',
                '-2',
                '2',
                '-1',
                '3',
            ]
            expected_output_lines = [
                '-2',
                '-1',
                '1',
                '2',
                '3',
            ]
            self.assertEqual(sort_lines(input_lines), expected_output_lines)

        def test_sort_with_negative_decimals(self):
            input_lines = [
                '2',
                '1.2',
                '1',
                '0',
                '-1',
                '-1.2',
                '-2',
            ]
            expected_output_lines = [
                '-2',
                '-1.2',
                '-1',
                '0',
                '1',
                '1.2',
                '2',
            ]
            self.assertEqual(sort_lines(input_lines), expected_output_lines)

        def test_sort_with_negatives_and_alpha(self):
            input_lines = [
                '1 a',
                '-2 b',
                '2 c',
                '-1 d',
                '3 e',
            ]
            expected_output_lines = [
                '-2 b',
                '-1 d',
                '1 a',
                '2 c',
                '3 e',
            ]
            self.assertEqual(sort_lines(input_lines), expected_output_lines)

        def test_sort_with_alphanumeric_partial_formatting(self):
            input_lines = [
                '2 a',
                '1 b2',
                '1 b.',
            ]
            expected_output_lines = [
                '1 b2',
                '1 b.',
                '2 a',
            ]
            self.assertEqual(sort_lines(input_lines), expected_output_lines)

    unittest.main(argv=['TestSortNumerically'])
