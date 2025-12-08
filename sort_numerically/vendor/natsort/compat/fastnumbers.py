# -*- coding: utf-8 -*-
"""
Interface for natsort to access fastnumbers functions without
having to worry if it is actually installed.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

try:
    # Modern, Python 3.8+, present on 3.12+
    from packaging.version import Version as StrictVersion
except Exception:
    try:
        # Older Python (≤3.11)
        from distutils.version import StrictVersion
    except Exception:
        # Last-ditch fallback (very old / embedded runtimes)
        class StrictVersion:
            def __init__(self, v):
                self._v = tuple(int(p) for p in v.split("."))

            def __lt__(self, other):
                return self._v < other._v

            def __eq__(self, other):
                return self._v == other._v


# If the user has fastnumbers installed, they will get great speed
# benefits. If not, we use the simulated functions that come with natsort.
try:
    # noinspection PyPackageRequirements
    from fastnumbers import __version__ as fn_ver
    from fastnumbers import fast_float, fast_int

    # Require >= version 2.0.0.
    if StrictVersion(fn_ver) < StrictVersion("2.0.0"):
        raise ImportError  # pragma: no cover
except ImportError:
    from natsort.compat.fake_fastnumbers import fast_float, fast_int  # noqa: F401
