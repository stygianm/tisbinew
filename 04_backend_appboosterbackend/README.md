# 04_backend_appboosterbackend

Тестовое задание Appbooster — REST API для A/B тестов.

## Постановка задачи

По заголовку Device-Token возвращаются значения экспериментов (button_color, price).
Источник: [appbooster/test-assignments](https://github.com/appbooster/test-assignments/blob/master/tasks/backend.md)

## Локальный запуск

1. `createdb appbooster`
2. `pip install -r requirements.txt`
3. `uvicorn app.main:app --reload`

## Docker

```bash
docker-compose up --build
```

API: http://localhost:8002
Статистика: http://localhost:8002/api/v1/statistics
