"""Appstorespy App Catalog API."""

from fastapi import FastAPI

from app.api import router as api_router
from app.database import init_db

app = FastAPI(title='Appstorespy API', version='1.0.0')


@app.on_event('startup')
async def startup():
    """Initialize database."""
    init_db()


@app.get('/health')
async def health():
    """Health check."""
    return {'status': 'ok'}


app.include_router(api_router, prefix='/api/v1', tags=['apps'])
