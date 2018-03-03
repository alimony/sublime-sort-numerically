# encoding: utf-8

'''
The sort_numerically() function lives in a separate file so it can be tested by tests.py
'''

from __future__ import unicode_literals

# from natsort import realsorted
from natsort import realsorted


def sort_lines(input_lines):
    return realsorted(input_lines)
