"""Database configuration and models."""

import os
from contextlib import contextmanager
from typing import Generator

import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/avitotm_stats',
)


def get_connection():
    """Get database connection."""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


@contextmanager
def get_db() -> Generator:
    """Database connection context manager."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Initialize database schema."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS stat_records (
                    id SERIAL PRIMARY KEY,
                    date DATE NOT NULL UNIQUE,
                    views BIGINT DEFAULT 0,
                    clicks BIGINT DEFAULT 0,
                    cost DECIMAL(12, 2) DEFAULT 0
                )
            ''')
