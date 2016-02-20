# This simple plugin is based on:
# http://www.codinghorror.com/blog/2007/12/sorting-for-humans-natural-sort-order.html

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

LINE_ENDING_CHARACTER = '\n'


class SortNumericallyCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        regions = self.view.sel()

        if len(regions) == 1 and regions[0].empty():
            # Selection is empty, use the entire buffer.
            regions = [sublime.Region(0, self.view.size())]

        for region in regions:
            input_lines = [self.view.substr(r) for r in self.view.lines(region)]
            sorted_lines = sort_lines(input_lines)

            output = LINE_ENDING_CHARACTER.join(sorted_lines)

            # If the end of the region had a line ending character, we re-add it here
            if self.view.substr(region).endswith(LINE_ENDING_CHARACTER):
                output += LINE_ENDING_CHARACTER

            self.view.replace(edit, region, output)
