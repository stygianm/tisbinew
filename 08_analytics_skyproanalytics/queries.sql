-- 1. Выручка по курсам за последний месяц (последние 30 дней)
SELECT
    course_id,
    SUM(price) AS revenue
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'  -- Исправлено: теперь действительно последние 30 дней
GROUP BY course_id
ORDER BY revenue DESC;  -- Добавлена сортировка для удобства

-- 2. Новые пользователи по дням за 7 дней
SELECT
    registration_date::date AS day,
    COUNT(*) AS new_users
FROM users
WHERE registration_date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY registration_date::date
ORDER BY day DESC;  -- Исправлено: теперь сначала последние дни

-- 3. Курсы со средней оценкой (кол-во оценок > 10)
SELECT
    c.course_name,
    ROUND(AVG(r.rating)::numeric, 2) AS avg_rating,  -- Добавлено округление для читаемости
    COUNT(*) AS ratings_count  -- Добавлено для информации
FROM courses c
JOIN ratings r ON r.course_id = c.course_id
GROUP BY c.course_id, c.course_name
HAVING COUNT(*) > 10
ORDER BY avg_rating DESC;

-- 4. Активные пользователи на указанную дату
-- Замени '2024-01-15' на нужную дату
SELECT
    COUNT(DISTINCT user_id) AS active_users
FROM user_courses
WHERE start_date <= '2024-01-15'  -- Замените на нужную дату
  AND (end_date IS NULL OR end_date >= '2024-01-15');

-- 5. Пользователи: купили, но не завершили за 30 дней
-- Улучшенная версия с лучшей производительностью
WITH purchases AS (
    SELECT DISTINCT user_id, event_date AS purchase_date
    FROM events
    WHERE event_type = 'course_purchase'
)
SELECT
    COUNT(DISTINCT p.user_id) AS users_count
FROM purchases p
LEFT JOIN events e ON e.user_id = p.user_id
    AND e.event_type = 'course_complete'
    AND e.event_date <= p.purchase_date + INTERVAL '30 days'
WHERE e.user_id IS NULL;