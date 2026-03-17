"""Test configuration.

Ensure the `src/` directory is on `sys.path` so tests can import the
application package (`intuitive_openstack_manager`) consistently when running
from the repo root.
"""

import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
