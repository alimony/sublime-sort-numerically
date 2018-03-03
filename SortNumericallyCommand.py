# encoding: utf-8

import os
import sys

import sublime
import sublime_plugin

sys.path.append(os.path.dirname(sys.executable))

try:
    # This import method works in Sublime Text 2.
    from sort_numerically import sort_lines
except ImportError:
    # While this works in Sublime Text 3.
    from .sort_numerically import sort_lines


class SortNumericallyCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        regions = self.view.sel()

        if len(regions) == 1 and regions[0].empty():
            # Selection is empty, use the entire buffer.
            regions = [sublime.Region(0, self.view.size())]

        for region in regions:
            input_lines = [self.view.substr(r) for r in self.view.lines(region)]
            sorted_lines = sort_lines(input_lines)

            # Fetch the actual line ending characters used, assuming the same is
            # used througout the entire region.
            first_line = self.view.substr(self.view.full_line(0))
            stripped_line = first_line.rstrip()
            line_ending_length = len(first_line) - len(stripped_line)
            line_ending = first_line[len(first_line) - line_ending_length:]

            output = line_ending.join(sorted_lines)

            # If the end of the region had a line ending character, we re-add it here
            if self.view.substr(region).endswith(line_ending):
                output += line_ending

            self.view.replace(edit, region, output)
