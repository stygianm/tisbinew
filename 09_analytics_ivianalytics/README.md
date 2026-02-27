# 09_analytics_ivianalytics

Тестовое задание ivi — SQL для просмотров контента.

## Постановка задачи

content_watch + content: SVOD/AVOD, топ сериалов, organic→referral.
Источник: Hexlet ru-test-assignments analytics/ivi.

## Локальный запуск

1. Создать БД, выполнить schema.sql
2. Загрузить тестовые данные (из README ivi)
3. Выполнить queries.sql


# 1. Создаем базу данных (контейнер уже работает)
docker exec -it ivi-postgres psql -U postgres -c "CREATE DATABASE ivi_analytics;"

# 2. Копируем SQL файлы в контейнер
docker cp schema.sql ivi-postgres:/schema.sql
docker cp queries.sql ivi-postgres:/queries.sql

# 3. Создаем файл test_data.sql (если еще не создали)
# Создайте файл test_data.sql с данными из image.png

# 4. Копируем test_data.sql
docker cp test_data.sql ivi-postgres:/test_data.sql

# 5. Переключаемся на cmd для выполнения SQL файлов
cmd

# 6. Выполняем schema.sql (создание таблиц)
docker exec -i ivi-postgres psql -U postgres -d ivi_analytics < schema.sql

# 7. Выполняем test_data.sql (заполнение данными)
docker exec -i ivi-postgres psql -U postgres -d ivi_analytics < test_data.sql

# 8. Выполняем queries.sql (запросы)
docker exec -i ivi-postgres psql -U postgres -d ivi_analytics < queries.sql

# 9. Возвращаемся в PowerShell
exit

# 10. Для проверки можно зайти в psql и посмотреть результаты
docker exec -it ivi-postgres psql -U postgres -d ivi_analytics

# В psql выполните:
\dt  -- посмотреть таблицы
SELECT * FROM content;  -- посмотреть контент
SELECT * FROM content_watch LIMIT 5;  -- посмотреть просмотры
\q  -- выход