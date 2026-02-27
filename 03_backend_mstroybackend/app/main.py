"""MStroy TreeStore REST API."""

from fastapi import FastAPI, HTTPException

from app.api import router as api_router

app = FastAPI(title='MStroy TreeStore API', version='1.0.0')


@app.get('/health')
async def health():
    """Health check."""
    return {'status': 'ok'}


app.include_router(api_router, prefix='/api/v1', tags=['treestore'])
