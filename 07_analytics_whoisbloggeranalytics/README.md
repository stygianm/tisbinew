# 07_analytics_whoisbloggeranalytics

Тестовое задание WhoIsBlogger — SQL метрики для Users/Purchases/Items.

## Постановка задачи

А–Г: средние суммы, месяц макс. выручки, топ товар, топ-3 с долей.
Источник: Hexlet ru-test-assignments analytics/WhoIsBlogger.

## Локальный запуск

1. `createdb whoisblogger`
2. `psql -d whoisblogger -f schema.sql`
3. `pip install psycopg2-binary && python seed_data.py`
4. `psql -d whoisblogger -f queries.sql`

## Docker

```bash
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:15
docker cp schema.sql 0469071d8e14:/schema.sql
docker exec -it 0469071d8e14 psql -U postgres -f /schema.sql
docker cp queries.sql 0469071d8e14:/queries.sql
docker exec -it 0469071d8e14 psql -U postgres -f /queries.sql

```
