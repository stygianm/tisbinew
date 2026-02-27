-- =====================================================
-- WHOISBLOGGER ANALYTICS: ПРОСТОЙ РАБОЧИЙ КОД
-- =====================================================

-- 1. ОЧИСТКА
DROP TABLE IF EXISTS purchases, users, items CASCADE;

-- 2. СОЗДАНИЕ ТАБЛИЦ
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    age INTEGER NOT NULL
);

CREATE TABLE items (
    item_id SERIAL PRIMARY KEY,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE purchases (
    purchase_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    item_id INTEGER REFERENCES items(item_id),
    date DATE NOT NULL
);

-- 3. ТЕСТОВЫЕ ДАННЫЕ (ПРОСТЫЕ И ПОНЯТНЫЕ)
-- Пользователи
INSERT INTO users (age) VALUES
    (20), (22), (24), (19), (21),  -- 18-25
    (30), (32), (28), (29), (31),  -- 26-35
    (40), (45), (50), (55), (60);  -- 35+

-- Товары
INSERT INTO items (price) VALUES
    (100), (250), (500), (750), (1000);

-- Покупки
INSERT INTO purchases (user_id, item_id, date) VALUES
    (1, 1, '2024-01-15'),
    (1, 2, '2024-01-20'),
    (2, 3, '2024-02-10'),
    (3, 1, '2024-02-15'),
    (4, 4, '2024-03-05'),
    (5, 5, '2024-03-10'),
    (6, 2, '2024-04-12'),
    (7, 3, '2024-04-18'),
    (8, 1, '2024-05-22'),
    (9, 4, '2024-06-01'),
    (10, 5, '2024-06-15'),
    (11, 2, '2024-07-20'),
    (12, 3, '2024-08-10'),
    (13, 1, '2024-09-05'),
    (14, 4, '2024-10-15'),
    (15, 5, '2024-11-20');

-- 4. ПРОВЕРКА
SELECT 'users' AS table_name, COUNT(*) FROM users
UNION ALL
SELECT 'items', COUNT(*) FROM items
UNION ALL
SELECT 'purchases', COUNT(*) FROM purchases;

-- 5. А) Средняя сумма в месяц
-- 18-25 лет
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', p.date) AS month,
        SUM(i.price) AS total
    FROM purchases p
    JOIN users u ON u.user_id = p.user_id
    JOIN items i ON i.item_id = p.item_id
    WHERE u.age BETWEEN 18 AND 25
    GROUP BY DATE_TRUNC('month', p.date)
)
SELECT '18-25' AS age_group, ROUND(AVG(total)::numeric, 2) AS avg_monthly
FROM monthly;

-- 26-35 лет
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', p.date) AS month,
        SUM(i.price) AS total
    FROM purchases p
    JOIN users u ON u.user_id = p.user_id
    JOIN items i ON i.item_id = p.item_id
    WHERE u.age BETWEEN 26 AND 35
    GROUP BY DATE_TRUNC('month', p.date)
)
SELECT '26-35' AS age_group, ROUND(AVG(total)::numeric, 2) AS avg_monthly
FROM monthly;

-- 6. Б) Лучший месяц для 35+
SELECT
    TO_CHAR(p.date, 'YYYY-MM') AS month,
    SUM(i.price) AS revenue
FROM purchases p
JOIN users u ON u.user_id = p.user_id
JOIN items i ON i.item_id = p.item_id
WHERE u.age >= 35
GROUP BY TO_CHAR(p.date, 'YYYY-MM')
ORDER BY revenue DESC
LIMIT 1;

-- 7. В) Топ-1 товар за последний год
SELECT
    i.item_id,
    i.price,
    COUNT(*) AS sales,
    SUM(i.price) AS revenue
FROM purchases p
JOIN items i ON i.item_id = p.item_id
WHERE p.date >= '2024-01-01'
GROUP BY i.item_id, i.price
ORDER BY revenue DESC
LIMIT 1;

-- 8. Г) Топ-3 товара и их доля
WITH total_revenue AS (
    SELECT SUM(price) AS total FROM items
)
SELECT
    i.item_id,
    i.price,
    COUNT(p.purchase_id) AS sales,
    SUM(i.price) AS revenue,
    ROUND(100.0 * SUM(i.price) / (SELECT total FROM total_revenue), 2) AS share_percent
FROM items i
LEFT JOIN purchases p ON i.item_id = p.item_id
GROUP BY i.item_id, i.price
ORDER BY revenue DESC
LIMIT 3;