# encoding: utf-8

'''
The sort_numerically() function lives in a separate file so it can be tested by tests.py
'''

from __future__ import unicode_literals

import re

LINE_ENDING_CHARACTER = '\n'


def convert(text):
    try:
        return float(text)
    except ValueError:
        return text


def alphanum_key(key):
    return [convert(c) for c in re.split('(-?[.0-9]+)', key)]


def sort_lines(input_lines):
    return sorted(input_lines, key=alphanum_key)
