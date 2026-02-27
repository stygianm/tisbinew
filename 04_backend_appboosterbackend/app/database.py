"""Database for experiments and device assignments."""

import os
from contextlib import contextmanager
from typing import Generator

import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/appbooster',
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
                CREATE TABLE IF NOT EXISTS device_assignments (
                    device_token VARCHAR(255) NOT NULL,
                    experiment_key VARCHAR(100) NOT NULL,
                    option_value TEXT NOT NULL,
                    PRIMARY KEY (device_token, experiment_key)
                )
            ''')
