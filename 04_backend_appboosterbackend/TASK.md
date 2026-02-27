# Тестовое задание Appbooster Backend

**Источник:** [appbooster/test-assignments - backend.md](https://github.com/appbooster/test-assignments/blob/master/tasks/backend.md)

REST API для A/B тестов. По заголовку Device-Token возвращает распределение экспериментов.

## Эксперименты

1. **button_color**: #FF0000, #00FF00, #0000FF — по 33.3%
2. **price**: 10→75%, 20→10%, 50→5%, 5→10%

## Требования

- Девайс всегда в одной группе
- Новые эксперименты не показываются старым девайсам
- Страница статистики: эксперименты, кол-во девайсов, распределение
