# 01_backend_avitotmbackend

Тестовое задание Avito TM — микросервис статистики для Trade Marketing.

## Постановка задачи

REST API для сохранения, получения и сброса статистики (просмотры, клики, стоимость).
Источник: [avito-tech/tm-backend-trainee](https://github.com/avito-tech/tm-backend-trainee)

## Локальный запуск

### Требования

- Python 3.11+
- PostgreSQL 15+

### Шаги

1. Создать БД PostgreSQL:
   ```bash
   createdb avitotm_stats
   ```

2. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустить приложение:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0
   ```

4. API доступен по адресу http://localhost:8000

### Примеры запросов

```bash
# Сохранить статистику
curl -X POST http://localhost:8000/api/v1/statistics \
  -H "Content-Type: application/json" \
  -d '{"date": "2025-02-27", "views": 100, "clicks": 10, "cost": 50.5}'

# Получить статистику
curl "http://localhost:8000/api/v1/statistics?from=2025-02-01&to=2025-02-28"

# Сбросить статистику
curl -X DELETE http://localhost:8000/api/v1/statistics
```

## Docker запуск

```bash
docker-compose up --build
```

API будет доступен на http://localhost:8000
