# Тестовое задание Avito Balance Backend

**Источник:** [avito-tech/autumn-2021-intern-assignment](https://github.com/avito-tech/autumn-2021-intern-assignment)

Микросервис для работы с балансом пользователей.

## API методы

- **Начисление средств** — user_id, amount
- **Списание средств** — user_id, amount
- **Перевод** — from_user_id, to_user_id, amount
- **Получение баланса** — user_id

## Требования

- Баланс не может быть отрицательным
- Данные хранятся в PostgreSQL
