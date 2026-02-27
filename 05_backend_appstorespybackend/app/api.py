"""Apps CRUD API."""

from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import get_db

router = APIRouter()


class AppCreate(BaseModel):
    """Create app request."""

    name: str
    bundle_id: str
    store: Optional[str] = 'ios'


class AppUpdate(BaseModel):
    """Update app request."""

    name: Optional[str] = None
    store: Optional[str] = None


@router.post('/apps')
async def create_app(body: AppCreate):
    """Create app."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO apps (name, bundle_id, store) VALUES (%s, %s, %s) '
                'RETURNING id, name, bundle_id, store, created_at',
                (body.name, body.bundle_id, body.store),
            )
            row = cur.fetchone()
    return dict(row)


@router.get('/apps')
async def list_apps(limit: int = 50, offset: int = 0):
    """List apps."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT id, name, bundle_id, store, created_at FROM apps '
                'ORDER BY id LIMIT %s OFFSET %s',
                (limit, offset),
            )
            rows = cur.fetchall()
    return [dict(r) for r in rows]


@router.get('/apps/{app_id}')
async def get_app(app_id: int):
    """Get app by id."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT id, name, bundle_id, store, created_at FROM apps '
                'WHERE id = %s',
                (app_id,),
            )
            row = cur.fetchone()
    if not row:
        raise HTTPException(404, 'App not found')
    return dict(row)


@router.patch('/apps/{app_id}')
async def update_app(app_id: int, body: AppUpdate):
    """Update app."""
    updates = []
    params = []
    if body.name is not None:
        updates.append('name = %s')
        params.append(body.name)
    if body.store is not None:
        updates.append('store = %s')
        params.append(body.store)
    if not updates:
        return await get_app(app_id)
    params.append(app_id)
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f'UPDATE apps SET {", ".join(updates)} WHERE id = %s',
                params,
            )
            if cur.rowcount == 0:
                raise HTTPException(404, 'App not found')
    return await get_app(app_id)


@router.delete('/apps/{app_id}')
async def delete_app(app_id: int):
    """Delete app."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM apps WHERE id = %s', (app_id,))
            if cur.rowcount == 0:
                raise HTTPException(404, 'App not found')
    return {'status': 'ok'}
