"""Database for app catalog."""

import os
from contextlib import contextmanager
from typing import Generator

import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/appstorespy',
)


def get_connection():
    """Get database connection."""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


@contextmanager
def get_db() -> Generator:
    """Database context manager."""
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
    """Create tables."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS apps (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    bundle_id VARCHAR(255) UNIQUE NOT NULL,
                    store VARCHAR(50) DEFAULT 'ios',
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')
