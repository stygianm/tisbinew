# 08_analytics_skyproanalytics

Тестовое задание Skypro — SQL запросы для онлайн-образования.

## Постановка задачи

5 запросов: выручка, новые пользователи, оценки, активные, покупка без завершения.
Источник: Hexlet ru-test-assignments analytics/Skypro Data Analyst.

## Локальный запуск

1. Создать БД и выполнить schema.sql
2. Выполнить queries.sql (для запроса 4 подставить дату вместо :target_date)


# 1. ЗАПУСК КОНТЕЙНЕРА POSTGRESQL
# Запускаем контейнер с PostgreSQL на порту 5433 (так как 5432 занят)
docker run --name postgres-test -e POSTGRES_PASSWORD=postgres -d -p 5433:5432 postgres

# 2. ОСТАНОВКА И УДАЛЕНИЕ КОНТЕЙНЕРА (если нужно пересоздать)
docker stop postgres-test
docker rm postgres-test

# 3. ПОДКЛЮЧЕНИЕ К POSTGRESQL
# Войти в psql внутри контейнера
docker exec -it postgres-test psql -U postgres

# 4. СОЗДАНИЕ БАЗЫ ДАННЫХ
# Способ 1: через команду
docker exec -it postgres-test psql -U postgres -c "CREATE DATABASE skypro_test;"

# Способ 2: внутри psql
# CREATE DATABASE skypro_test;
# \c skypro_test;

# 5. КОПИРОВАНИЕ ФАЙЛОВ В КОНТЕЙНЕР
docker cp schema.sql postgres-test:/schema.sql
docker cp queries.sql postgres-test:/queries.sql
docker cp test_data.sql postgres-test:/test_data.sql
docker cp test_queries.sql postgres-test:/test_queries.sql

# 6. ВЫПОЛНЕНИЕ SQL-ФАЙЛОВ (через cmd, т.к. в PowerShell < не работает)
# Переключиться в cmd:
cmd

# Выполнить schema.sql (создание таблиц)
docker exec -i postgres-test psql -U postgres -d skypro_test < schema.sql

# Выполнить test_data.sql (заполнение тестовыми данными)
docker exec -i postgres-test psql -U postgres -d skypro_test < test_data.sql

# Выполнить queries.sql (основные запросы)
docker exec -i postgres-test psql -U postgres -d skypro_test < queries.sql

# Выполнить test_queries.sql (тестовые запросы)
docker exec -i postgres-test psql -U postgres -d skypro_test < test_queries.sql

# Вернуться в PowerShell:
exit

# 7. АЛЬТЕРНАТИВНЫЙ СПОСОБ: выполнение файлов внутри контейнера
docker exec -it postgres-test psql -U postgres -d skypro_test -f /schema.sql
docker exec -it postgres-test psql -U postgres -d skypro_test -f /test_data.sql
docker exec -it postgres-test psql -U postgres -d skypro_test -f /queries.sql

# 8. ПРОВЕРКА ДАННЫХ
# Посмотреть список таблиц
docker exec -it postgres-test psql -U postgres -d skypro_test -c "\dt"

# Выполнить произвольный SQL-запрос
docker exec -it postgres-test psql -U postgres -d skypro_test -c "SELECT * FROM users;"

# 9. ПОЛЕЗНЫЕ КОМАНДЫ ДЛЯ РАБОТЫ С КОНТЕЙНЕРОМ
# Посмотреть запущенные контейнеры
docker ps

# Посмотреть все контейнеры (включая остановленные)
docker ps -a

# Зайти в bash внутри контейнера
docker exec -it postgres-test bash

# Посмотреть логи контейнера
docker logs postgres-test

# Остановить контейнер
docker stop postgres-test

# Запустить остановленный контейнер
docker start postgres-test

# Удалить контейнер (предварительно остановив)
docker stop postgres-test
docker rm postgres-test

# 10. ЕСЛИ НУЖНО ПЕРЕСОЗДАТЬ ВСЁ С НУЛЯ
docker stop postgres-test
docker rm postgres-test
docker run --name postgres-test -e POSTGRES_PASSWORD=postgres -d -p 5433:5432 postgres
docker exec -it postgres-test psql -U postgres -c "CREATE DATABASE skypro_test;"
docker exec -i postgres-test psql -U postgres -d skypro_test < schema.sql
docker exec -i postgres-test psql -U postgres -d skypro_test < test_data.sql
