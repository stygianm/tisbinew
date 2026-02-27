"""TreeStore class for tree structure operations."""

from typing import Any, Dict, List


class TreeStore:
    """Store for tree-structured items with O(1) access."""

    def __init__(self, items: List[Dict[str, Any]]) -> None:
        """Initialize tree store with items.

        Builds index for O(1) access by id and parent.
        """
        self._items = items
        self._by_id: Dict[Any, Dict[str, Any]] = {
            item['id']: item for item in items
        }
        self._children: Dict[Any, List[Dict[str, Any]]] = {}
        for item in items:
            parent = item.get('parent')
            if parent not in self._children:
                self._children[parent] = []
            self._children[parent].append(item)

    def getAll(self) -> List[Dict[str, Any]]:
        """Return all items in original order."""
        return self._items

    def getItem(self, item_id: Any) -> Dict[str, Any] | None:
        """Return item by id or None."""
        return self._by_id.get(item_id)

    def getChildren(self, item_id: Any) -> List[Dict[str, Any]]:
        """Return direct children of item."""
        return self._children.get(item_id, [])

    def getAllParents(self, item_id: Any) -> List[Dict[str, Any]]:
        """Return chain of parents from item to root."""
        result: List[Dict[str, Any]] = []
        item = self._by_id.get(item_id)
        while item and item.get('parent') != 'root':
            parent_id = item['parent']
            parent = self._by_id.get(parent_id)
            if parent:
                result.append(parent)
            item = parent
        return result
