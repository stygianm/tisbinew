-- Cian Analytics: SQL queries

-- 1. Произведения, издававшиеся более 5 раз
SELECT w.id, w.name, COUNT(e.id) AS edition_count
FROM work w
JOIN edition e ON e.work_id = w.id
GROUP BY w.id, w.name
HAVING COUNT(e.id) > 5;

-- 2. Экземпляры без привязки к изданию
SELECT c.id, c.inventory_num
FROM copy c
WHERE c.edition_id IS NULL;

-- 3. Последние 3 произведения на пользователя + сколько раз брали
WITH log_with_work AS (
    SELECT ol.user_id, ol.copy_id, ol.date_taken, ed.work_id
    FROM operation_log ol
    JOIN copy c ON c.id = ol.copy_id
    JOIN edition ed ON ed.id = c.edition_id
),
last_three AS (
    SELECT user_id, copy_id, date_taken, work_id,
           ROW_NUMBER() OVER (
               PARTITION BY user_id ORDER BY date_taken DESC
           ) AS rn
    FROM log_with_work
),
borrow_counts AS (
    SELECT user_id, work_id, COUNT(*) AS cnt
    FROM log_with_work
    GROUP BY user_id, work_id
)
SELECT lt.user_id, w.name AS work_name, lt.date_taken, bc.cnt AS total_borrows
FROM last_three lt
JOIN work w ON w.id = lt.work_id
JOIN borrow_counts bc ON bc.user_id = lt.user_id AND bc.work_id = lt.work_id
WHERE lt.rn <= 3;

-- 4. Рейтинг 10 неблагонадежных пользователей (просрочки)
-- ИСПРАВЛЕНО: убрал INTERVAL и сравниваю с числом 30
SELECT user_id,
       COUNT(*) AS overdue_count
FROM operation_log
WHERE date_returned IS NOT NULL
  AND (date_returned - date_taken) > 30  -- Здесь было INTERVAL '30 days'
GROUP BY user_id
ORDER BY overdue_count DESC
LIMIT 10;
