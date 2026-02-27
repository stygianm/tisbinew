"""API routes for statistics."""

from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.database import get_db

router = APIRouter()


class StatSaveRequest(BaseModel):
    """Request model for saving statistics."""

    date: date
    views: Optional[int] = 0
    clicks: Optional[int] = 0
    cost: Optional[float] = 0.0


@router.post('/statistics')
async def save_statistics(body: StatSaveRequest):
    """Save or aggregate statistics for a date."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO stat_records (date, views, clicks, cost)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (date) DO UPDATE SET
                    views = stat_records.views + EXCLUDED.views,
                    clicks = stat_records.clicks + EXCLUDED.clicks,
                    cost = stat_records.cost + EXCLUDED.cost
            ''', (body.date, body.views, body.clicks, body.cost))
    return {'status': 'ok'}


@router.get('/statistics')
async def get_statistics(
    from_date: date = Query(..., alias='from'),
    to_date: date = Query(..., alias='to'),
    sort_by: str = Query('date', regex='^(date|views|clicks|cost|cpc|cpm)$'),
):
    """Get statistics for date range."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT date, views, clicks, cost
                FROM stat_records
                WHERE date >= %s AND date <= %s
                ORDER BY date
            ''', (from_date, to_date))
            rows = cur.fetchall()

    result = []
    for row in rows:
        clicks = int(row['clicks']) or 1
        views = int(row['views']) or 1
        cost = float(row['cost']) or 0
        cpc = round(cost / clicks, 2)
        cpm = round(cost / views * 1000, 2) if views else 0
        result.append({
            'date': str(row['date']),
            'views': row['views'],
            'clicks': row['clicks'],
            'cost': str(row['cost']),
            'cpc': str(cpc),
            'cpm': str(cpm),
        })

    if sort_by and sort_by != 'date':
        result.sort(key=lambda x: float(x.get(sort_by, 0)))

    return result


@router.delete('/statistics')
async def reset_statistics():
    """Delete all statistics."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE stat_records')
    return {'status': 'ok'}
