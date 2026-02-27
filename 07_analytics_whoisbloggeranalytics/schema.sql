-- =====================================================
-- WHOISBLOGGER ANALYTICS: создание таблиц
-- =====================================================

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    age INTEGER NOT NULL
);

-- Таблица товаров
CREATE TABLE IF NOT EXISTS items (
    item_id SERIAL PRIMARY KEY,
    price DECIMAL(10,2) NOT NULL
);

-- Таблица покупок
CREATE TABLE IF NOT EXISTS purchases (
    purchase_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES items(item_id) ON DELETE CASCADE,
    date DATE NOT NULL
);