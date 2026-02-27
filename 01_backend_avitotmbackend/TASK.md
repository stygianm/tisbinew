# Тестовое задание Avito TM Backend

**Источник:** [avito-tech/tm-backend-trainee](https://github.com/avito-tech/tm-backend-trainee)

Микросервис для счетчиков статистики с REST API.

## API методы

- **Сохранение статистики** — date, views, clicks, cost (опционально)
- **Показ статистики** — from, to, сортировка по дате
- **Сброс статистики** — удаление всех данных

## Формат ответа при показе

- date, views, clicks, cost, cpc (cost/clicks), cpm (cost/views*1000)
