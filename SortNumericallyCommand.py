# encoding: utf-8

import os
import sys

import sublime
import sublime_plugin

sys.path.append(os.path.dirname(sys.executable))

try:
    # This import method works in Sublime Text 2.
    from sort_numerically.sort_numerically import sort_lines
except ImportError:
    # While this works in Sublime Text 3.
    from .sort_numerically.sort_numerically import sort_lines

# The buffer always uses \n, whatever the line endings setting of the view says.
# That setting only applies when the file is saved.
LINE_ENDING_CHARACTER = '\n'


class SortNumericallyCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        # Work on a copy of the selection. Replacing whole lines can merge
        # selections that share a line. The copy stays valid, because sorting
        # does not change the length of the text.
        regions = list(self.view.sel())

        if len(regions) == 1 and regions[0].empty():
            # Selection is empty, use the entire buffer.
            regions = [sublime.Region(0, self.view.size())]

        for region in regions:
            lines = self.view.lines(region)
            input_lines = [self.view.substr(r) for r in lines]
            sorted_lines = sort_lines(input_lines)

            output = LINE_ENDING_CHARACTER.join(sorted_lines)

            # Replace whole lines, also when the selection starts or ends inside
            # a line. The line ending after the last line stays in place.
            whole_lines = sublime.Region(lines[0].begin(), lines[-1].end())

            self.view.replace(edit, whole_lines, output)
