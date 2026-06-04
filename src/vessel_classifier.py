# Vessel classifier - filter ships worth posting
import logging
import sys

sys.path.insert(0, str(__file__).rsplit("/", 2)[0])
from config import SKIP_TYPES, SHIP_MIN_LENGTH

logger = logging.getLogger(__name__)


def is_worthy(typename=None, length=None):
    if typename and typename.lower() in {t.lower() for t in SKIP_TYPES}:
        return False
    if length is not None and length < SHIP_MIN_LENGTH:
        return False
    good = {"cargo", "tanker", "passenger", "container", "bulk", "ro-ro"}
    if typename:
        for kw in good:
            if kw in typename.lower():
                return True
    return length is not None and length >= SHIP_MIN_LENGTH
