# This simple plugin is based on:
# http://www.codinghorror.com/blog/2007/12/sorting-for-humans-natural-sort-order.html

import sublime
import sublime_plugin
import re


class SortNumericallyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.sel()
        if len(regions) == 1 and regions[0].empty():
            # Selection is empty, use the entire buffer.
            regions = [sublime.Region(0, self.view.size())]
        for region in regions:
            lines = [self.view.substr(r) for r in self.view.lines(region)]
            convert = lambda text: int(text) if text.isdigit() else text
            alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
            sorted_lines = sorted(lines, key=alphanum_key)

            # Determine the current line ending setting, so we can rejoin the
            # sorted lines using the correct line ending character.
            line_ending_character = '\n'  # Default.
            line_endings = self.view.line_endings()
            if line_endings == 'CR':
                line_ending_character = '\r'
            elif line_endings == 'Windows':
                line_ending_character = '\r\n'

            output = line_ending_character.join(sorted_lines)

            self.view.replace(edit, region, output)
