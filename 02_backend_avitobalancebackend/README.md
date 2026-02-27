# 02_backend_avitobalancebackend

Тестовое задание Avito Balance — микросервис для работы с балансом пользователей.

## Постановка задачи

REST API: начисление, списание, перевод средств, получение баланса.
Источник: [avito-tech/autumn-2021-intern-assignment](https://github.com/avito-tech/autumn-2021-intern-assignment)

## Локальный запуск

1. `createdb avito_balance`
2. `pip install -r requirements.txt`
3. `uvicorn app.main:app --reload`

## Docker

```bash
docker-compose up --build
```

API: http://localhost:8001

### Примеры

```bash
curl -X POST http://localhost:8001/api/v1/deposit -H "Content-Type: application/json" -d '{"user_id":1,"amount":100}'
curl http://localhost:8001/api/v1/balance/1
curl -X POST http://localhost:8001/api/v1/transfer -H "Content-Type: application/json" -d '{"from_user_id":1,"to_user_id":2,"amount":50}'
```
