"""Test that database initialization is idempotent."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data.db import init_db


def test_init_twice_no_error():
    """Calling init() twice should not fail (idempotent)."""
    init_db()
    init_db()
