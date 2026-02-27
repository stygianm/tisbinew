"""Avito Balance microservice - FastAPI application."""

from fastapi import FastAPI

from app.api import router as api_router
from app.database import init_db

app = FastAPI(title='Avito Balance API', version='1.0.0')


@app.on_event('startup')
async def startup():
    """Initialize database on startup."""
    init_db()


@app.get('/health')
async def health():
    """Health check endpoint."""
    return {'status': 'ok'}


app.include_router(api_router, prefix='/api/v1', tags=['balance'])
