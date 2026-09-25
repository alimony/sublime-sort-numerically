#!/usr/bin/env python3
# encoding: utf-8

'''Run some basic tests on various lists of input lines, and on the command.'''

from __future__ import unicode_literals

if __name__ == '__main__':
    import sys
    import types
    import unittest
    from sort_numerically.sort_numerically import sort_lines

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

    # Stand-ins for the parts of the Sublime Text API that the command uses, so
    # that it can run outside the editor.

    class Region(object):

        def __init__(self, a, b):
            self.a = a
            self.b = b

        def begin(self):
            return min(self.a, self.b)

        def end(self):
            return max(self.a, self.b)

        def empty(self):
            return self.a == self.b

    class TextCommand(object):

        def __init__(self, view):
            self.view = view

    class View(object):
        '''A buffer with one selection. Like in Sublime Text, the buffer always
        uses line feeds, whatever line endings the file is saved with.'''

        def __init__(self, text, selection=(0, 0)):
            self.text = text
            self.selection = [Region(*selection)]

        def sel(self):
            return self.selection

        def size(self):
            return len(self.text)

        def substr(self, region):
            return self.text[region.begin():region.end()]

        def lines(self, region):
            # The lines that the region touches, without their line endings. A
            # line that starts where a non-empty region ends is left out.
            lines = []
            start = self.text.rfind('\n', 0, region.begin()) + 1
            while True:
                end = self.text.find('\n', start)
                if end == -1:
                    end = len(self.text)
                lines.append(Region(start, end))
                start = end + 1
                if end >= region.end() or start == region.end():
                    return lines

        def replace(self, edit, region, text):
            self.text = self.text[:region.begin()] + text + self.text[region.end():]

    sys.modules['sublime'] = types.SimpleNamespace(Region=Region)
    sys.modules['sublime_plugin'] = types.SimpleNamespace(TextCommand=TextCommand)
    from SortNumericallyCommand import SortNumericallyCommand

    class TestSortNumericallyCommand(unittest.TestCase):

        def run_command(self, text, selection=(0, 0)):
            view = View(text, selection)
            SortNumericallyCommand(view).run(edit=None)
            return view.text

        def test_keeps_final_line_ending(self):
            self.assertEqual(self.run_command('3\n1\n2\n'), '1\n2\n3\n')

        def test_does_not_add_final_line_ending(self):
            self.assertEqual(self.run_command('3\n1\n2'), '1\n2\n3')

        def test_trailing_whitespace_on_first_line(self):
            self.assertEqual(
                self.run_command('file10  \nfile2\nfile1\n'),
                'file1\nfile2\nfile10  \n',
            )

        def test_whitespace_only_first_line(self):
            self.assertEqual(
                self.run_command('  \nb2\nb10\nb1\n'),
                '  \nb1\nb2\nb10\n',
            )

        def test_trailing_whitespace_on_first_line_outside_selection(self):
            text = 'header  \n10\n2\n1\nfooter\n'
            selection = (text.index('10'), text.index('footer'))
            self.assertEqual(
                self.run_command(text, selection),
                'header  \n1\n2\n10\nfooter\n',
            )

        def test_selection_starting_and_ending_inside_lines(self):
            text = '10 a\n2 b\n1 c'
            selection = (text.index(' a'), text.index(' c'))
            self.assertEqual(self.run_command(text, selection), '1 c\n2 b\n10 a')

        def test_selection_ending_at_start_of_line(self):
            text = '3\n1\n2\n0\n'
            selection = (0, text.index('0'))
            self.assertEqual(self.run_command(text, selection), '1\n2\n3\n0\n')

    unittest.main(argv=['TestSortNumerically'])
