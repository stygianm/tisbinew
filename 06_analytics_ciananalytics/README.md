# 06_analytics_ciananalytics

Тестовое задание Cian — SQL запросы для библиотечной БД.

## Постановка задачи

Схема 3НФ: work, edition, copy, operation_log.
Источник: Hexlet ru-test-assignments analytics/Cian.

## Локальный запуск

1. Создать БД PostgreSQL
2. Выполнить schema.sql
3. Выполнить queries.sql или запустить Python:

```bash
pip install psycopg2-binary
python run_queries.py
```

## Docker

```bash
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:15
psql -h localhost -U postgres -f schema.sql
psql -h localhost -U postgres -f queries.sql
```
