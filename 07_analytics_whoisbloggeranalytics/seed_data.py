"""Seed test data for WhoIsBlogger analytics."""

import os
import random
from datetime import date, timedelta

import psycopg2

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/whoisblogger',
)


def main():
    """Insert sample data."""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute('DELETE FROM purchases')
    cur.execute('DELETE FROM users')
    cur.execute('DELETE FROM items')

    for i in range(1, 11):
        cur.execute(
            'INSERT INTO users (user_id, age) VALUES (%s, %s)',
            (i, random.choice([20, 30, 40])),
        )

    for i in range(1, 6):
        cur.execute(
            'INSERT INTO items (item_id, price) VALUES (%s, %s)',
            (i, round(random.uniform(10, 100), 2)),
        )

    for i in range(50):
        d = date.today() - timedelta(days=random.randint(0, 365))
        cur.execute(
            'INSERT INTO purchases (user_id, item_id, date) VALUES (%s, %s, %s)',
            (random.randint(1, 10), random.randint(1, 5), d),
        )

    conn.commit()
    cur.close()
    conn.close()
    print('Seed data inserted')


if __name__ == '__main__':
    main()
