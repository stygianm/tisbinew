"""Tests for TreeStore."""

from tree_store import TreeStore

ITEMS = [
    {'id': 1, 'parent': 'root'},
    {'id': 2, 'parent': 1, 'type': 'test'},
    {'id': 3, 'parent': 1, 'type': 'test'},
    {'id': 4, 'parent': 2, 'type': 'test'},
    {'id': 5, 'parent': 2, 'type': 'test'},
    {'id': 6, 'parent': 2, 'type': 'test'},
    {'id': 7, 'parent': 4, 'type': None},
    {'id': 8, 'parent': 4, 'type': None},
]


def test_get_all():
    """Test getAll returns all items."""
    ts = TreeStore(ITEMS)
    assert ts.getAll() == ITEMS


def test_get_item():
    """Test getItem returns item by id."""
    ts = TreeStore(ITEMS)
    assert ts.getItem(7) == {'id': 7, 'parent': 4, 'type': None}
    assert ts.getItem(999) is None


def test_get_children():
    """Test getChildren returns direct children."""
    ts = TreeStore(ITEMS)
    assert ts.getChildren(4) == [
        {'id': 7, 'parent': 4, 'type': None},
        {'id': 8, 'parent': 4, 'type': None},
    ]
    assert ts.getChildren(5) == []


def test_get_all_parents():
    """Test getAllParents returns parent chain to root."""
    ts = TreeStore(ITEMS)
    assert ts.getAllParents(7) == [
        {'id': 4, 'parent': 2, 'type': 'test'},
        {'id': 2, 'parent': 1, 'type': 'test'},
        {'id': 1, 'parent': 'root'},
    ]
