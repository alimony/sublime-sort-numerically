import sublime
import sublime_plugin
import subprocess


class SortNumericallyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.sel()
        if len(regions) == 1 and regions[0].empty():
            # Selection is empty, use the entire buffer.
            regions = [sublime.Region(0, self.view.size())]
        for region in regions:
            p = subprocess.Popen(['sort', '-n'], bufsize=-1,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE)
            output, error = p.communicate(self.view.substr(region).encode('utf-8'))
            if error:
                sublime.error_message(error.decode('utf-8'))
            else:
                self.view.replace(edit, region, output.decode('utf-8'))
