# 03_backend_mstroybackend

Тестовое задание ООО МСтрой — класс TreeStore с REST API.

## Постановка задачи

TreeStore для работы с древовидной структурой. Источник: Hexlet ru-test-assignments.

## Локальный запуск

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: http://localhost:8000

## Запуск тестов

```bash
python -m pytest test_tree_store.py -v
```

## Docker

```bash
docker build -t mstroy .
docker run -p 8000:8000 mstroy
```
