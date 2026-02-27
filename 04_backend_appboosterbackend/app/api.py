"""Experiments API."""

import hashlib
from typing import Dict

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.database import get_db

router = APIRouter()

# Button color: equal 33.3% each
BUTTON_OPTIONS = ['#FF0000', '#00FF00', '#0000FF']

# Price: 10->75%, 20->10%, 50->5%, 5->10%
PRICE_OPTIONS = (
    ['10'] * 75 + ['20'] * 10 + ['50'] * 5 + ['5'] * 10
)


def _assign_button(device_token: str) -> str:
    """Assign button color by deterministic hash."""
    h = int(hashlib.md5(device_token.encode()).hexdigest(), 16) % 3
    return BUTTON_OPTIONS[h]


def _assign_price(device_token: str) -> str:
    """Assign price by deterministic hash."""
    h = int(hashlib.md5(device_token.encode()).hexdigest(), 16) % 100
    return PRICE_OPTIONS[h]


@router.get('/experiments')
async def get_experiments(request: Request) -> Dict[str, str]:
    """Return experiments for device (Device-Token header)."""
    token = request.headers.get('Device-Token') or request.headers.get(
        'device-token'
    )
    if not token:
        return {}
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT experiment_key, option_value FROM device_assignments '
                'WHERE device_token = %s',
                (token,),
            )
            rows = cur.fetchall()
    if rows:
        return {r['experiment_key']: r['option_value'] for r in rows}
    button = _assign_button(token)
    price = _assign_price(token)
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO device_assignments VALUES (%s, %s, %s), (%s, %s, %s)',
                (token, 'button_color', button, token, 'price', price),
            )
    return {'button_color': button, 'price': price}


@router.get('/statistics', response_class=HTMLResponse)
async def statistics():
    """Statistics page."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT experiment_key, option_value, COUNT(*) as cnt
                FROM device_assignments
                GROUP BY experiment_key, option_value
            ''')
            rows = cur.fetchall()
    data: Dict[str, Dict[str, int]] = {}
    for r in rows:
        key = r['experiment_key']
        if key not in data:
            data[key] = {}
        data[key][r['option_value']] = r['cnt']
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT COUNT(DISTINCT device_token) FROM device_assignments'
            )
            total_devices = cur.fetchone()['count'] or 0
    html = '<html><head><title>Statistics</title></head><body>'
    html += '<h1>A/B Experiments Statistics</h1>'
    html += f'<p>Total devices: {total_devices}</p>'
    html += '<table border="1"><tr><th>Experiment</th><th>Option</th><th>Count</th><th>%</th></tr>'
    for key, opts in data.items():
        exp_total = sum(opts.values())
        for opt, cnt in opts.items():
            pct = round(cnt * 100 / exp_total, 1) if exp_total else 0
            html += f'<tr><td>{key}</td><td>{opt}</td><td>{cnt}</td><td>{pct}%</td></tr>'
    html += '</table></body></html>'
    return html
