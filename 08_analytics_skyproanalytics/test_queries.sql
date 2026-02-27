-- 1. Выручка по курсам (без ограничения по дате)
SELECT
    course_id,
    SUM(price) AS revenue
FROM orders
GROUP BY course_id
ORDER BY revenue DESC;

-- 2. Новые пользователи по дням (за всё время)
SELECT
    registration_date::date AS day,
    COUNT(*) AS new_users
FROM users
GROUP BY registration_date::date
ORDER BY day DESC;

-- 3. Курсы со средней оценкой (все, без HAVING для проверки)
SELECT
    c.course_name,
    ROUND(AVG(r.rating)::numeric, 2) AS avg_rating,
    COUNT(*) AS ratings_count
FROM courses c
JOIN ratings r ON r.course_id = c.course_id
GROUP BY c.course_id, c.course_name
ORDER BY avg_rating DESC;

-- 4. Активные пользователи на конкретную дату (например, '2024-02-20')
SELECT
    COUNT(DISTINCT user_id) AS active_users
FROM user_courses
WHERE start_date <= '2024-02-20'
  AND (end_date IS NULL OR end_date >= '2024-02-20');

-- 5. Пользователи: купили, но не завершили за 30 дней
WITH purchases AS (
    SELECT DISTINCT user_id, event_date AS purchase_date
    FROM events
    WHERE event_type = 'course_purchase'
)
SELECT
    COUNT(DISTINCT p.user_id) AS users_count,
    -- Для детализации:
    p.user_id,
    p.purchase_date
FROM purchases p
LEFT JOIN events e ON e.user_id = p.user_id
    AND e.event_type = 'course_complete'
    AND e.event_date <= p.purchase_date + INTERVAL '30 days'
WHERE e.user_id IS NULL
GROUP BY p.user_id, p.purchase_date;