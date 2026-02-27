"""TreeStore API routes."""

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.store import get_store

router = APIRouter()


@router.get('/items')
async def get_all() -> List[Dict[str, Any]]:
    """Return all items."""
    return get_store().getAll()


def _parse_id(item_id: str) -> int | str:
    """Parse item_id to int if numeric, else keep as str."""
    try:
        return int(item_id)
    except ValueError:
        return item_id


@router.get('/items/{item_id}')
async def get_item(item_id: str) -> Dict[str, Any]:
    """Return item by id."""
    parsed = _parse_id(item_id)
    item = get_store().getItem(parsed)
    if item is None:
        raise HTTPException(404, f'Item {parsed} not found')
    return item


@router.get('/items/{item_id}/children')
async def get_children(item_id: str) -> List[Dict[str, Any]]:
    """Return children of item."""
    return get_store().getChildren(_parse_id(item_id))


@router.get('/items/{item_id}/parents')
async def get_parents(item_id: str) -> List[Dict[str, Any]]:
    """Return chain of parents to root."""
    return get_store().getAllParents(_parse_id(item_id))
