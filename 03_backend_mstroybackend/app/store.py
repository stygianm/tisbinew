"""TreeStore singleton with default data."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tree_store import TreeStore  # noqa: E402

DEFAULT_ITEMS = [
    {'id': 1, 'parent': 'root'},
    {'id': 2, 'parent': 1, 'type': 'test'},
    {'id': 3, 'parent': 1, 'type': 'test'},
    {'id': 4, 'parent': 2, 'type': 'test'},
    {'id': 5, 'parent': 2, 'type': 'test'},
    {'id': 6, 'parent': 2, 'type': 'test'},
    {'id': 7, 'parent': 4, 'type': None},
    {'id': 8, 'parent': 4, 'type': None},
]

_store: TreeStore | None = None


def get_store() -> TreeStore:
    """Return singleton TreeStore instance."""
    global _store
    if _store is None:
        _store = TreeStore(DEFAULT_ITEMS)
    return _store
