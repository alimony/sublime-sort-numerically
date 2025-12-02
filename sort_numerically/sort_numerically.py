# encoding: utf-8

'''
The sort_numerically() function lives in a separate file so it can be tested by tests.py
'''

from __future__ import unicode_literals

import os
import sys

def _add_vendor_to_path():
    base = os.path.dirname(__file__)
    vendor = os.path.join(base, "vendor")
    if vendor not in sys.path:
        sys.path.insert(0, vendor)

_add_vendor_to_path()

from natsort import realsorted  # noqa


def sort_lines(input_lines):
    return realsorted(input_lines)
