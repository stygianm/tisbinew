-- ivi Analytics: SQL queries (PostgreSQL диалект)

-- =====================================================
-- ЗАДАНИЕ 1.1: Просмотры по дням для SVOD/AVOD на платформах 10 и 11
-- =====================================================
SELECT 
    DATE(show_date) AS day,
    c.paid_type,
    COUNT(*) AS views_count,
    COUNT(DISTINCT user_id) AS unique_viewers
FROM content_watch cw
JOIN content c ON c.content_id = cw.content_id
WHERE cw.platform IN (10, 11)
  AND c.paid_type IN ('SVOD', 'AVOD')
  AND cw.show_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(show_date), c.paid_type
ORDER BY day DESC, c.paid_type;

-- =====================================================
-- ЗАДАНИЕ 1.2: Ежемесячный ТОП-5 сериалов и ТОП-5 единичного контента
-- =====================================================

-- ТОП-5 сериалов по количеству уникальных зрителей
WITH series_episodes AS (
    SELECT DISTINCT compilation_id
    FROM content
    WHERE compilation_id IS NOT NULL 
      AND episode IS NOT NULL
)
SELECT 
    c.compilation_id AS series_id,
    COUNT(DISTINCT cw.user_id) AS unique_viewers
FROM content_watch cw
JOIN content c ON cw.content_id = c.content_id
JOIN series_episodes se ON c.compilation_id = se.compilation_id
WHERE cw.show_date >= DATE_TRUNC('month', CURRENT_DATE)
  AND cw.show_date < DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'
GROUP BY c.compilation_id
ORDER BY unique_viewers DESC
LIMIT 5;

-- ТОП-5 единичного контента (фильмы, отдельные видео)
SELECT 
    cw.content_id,
    COUNT(DISTINCT cw.user_id) AS unique_viewers
FROM content_watch cw
JOIN content c ON cw.content_id = c.content_id
WHERE c.compilation_id IS NULL
  AND cw.show_date >= DATE_TRUNC('month', CURRENT_DATE)
  AND cw.show_date < DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'
GROUP BY cw.content_id
ORDER BY unique_viewers DESC
LIMIT 5;

-- =====================================================
-- ЗАДАНИЕ 1.3: Пользователи с organic → referral подряд
-- =====================================================
WITH user_sessions AS (
    SELECT 
        user_id,
        utm_medium,
        show_date,
        LAG(utm_medium) OVER (
            PARTITION BY user_id 
            ORDER BY show_date
        ) AS prev_medium,
        LAG(show_date) OVER (
            PARTITION BY user_id 
            ORDER BY show_date
        ) AS prev_show_date
    FROM content_watch
    WHERE DATE(show_date) = CURRENT_DATE - INTERVAL '1 day'
)
SELECT DISTINCT 
    user_id
FROM user_sessions
WHERE utm_medium = 'referral' 
  AND prev_medium = 'organic'
  AND EXTRACT(EPOCH FROM (show_date - prev_show_date)) < 3600
ORDER BY user_id;

-- =====================================================
-- ЗАДАНИЕ 2.1: Метрика "цепляемости" и "крутости" сериала
-- =====================================================
WITH episode_duration AS (
    SELECT 
        c.content_id,
        c.compilation_id,
        c.episode,
        AVG(cw.show_duration) AS avg_duration
    FROM content_watch cw
    JOIN content c ON cw.content_id = c.content_id
    WHERE c.compilation_id IS NOT NULL
    GROUP BY c.content_id, c.compilation_id, c.episode
),
completion_rates AS (
    SELECT 
        c.compilation_id,
        COUNT(DISTINCT CASE 
            WHEN cw.show_duration >= ed.avg_duration * 0.9 
            THEN cw.user_id 
        END) * 1.0 / NULLIF(COUNT(DISTINCT cw.user_id), 0) AS completion_rate
    FROM content_watch cw
    JOIN content c ON cw.content_id = c.content_id
    LEFT JOIN episode_duration ed ON cw.content_id = ed.content_id
    WHERE c.compilation_id IS NOT NULL
    GROUP BY c.compilation_id
),
binge_rates AS (
    SELECT 
        c1.compilation_id,
        COUNT(DISTINCT cw2.user_id) * 1.0 / NULLIF(COUNT(DISTINCT cw1.user_id), 0) AS binge_rate
    FROM content_watch cw1
    JOIN content c1 ON cw1.content_id = c1.content_id
    LEFT JOIN content_watch cw2 ON cw1.user_id = cw2.user_id
        AND cw2.show_date > cw1.show_date
        AND cw2.show_date <= cw1.show_date + INTERVAL '24 hours'
    WHERE c1.compilation_id IS NOT NULL
    GROUP BY c1.compilation_id
)
SELECT 
    cr.compilation_id AS series_id,
    ROUND(cr.completion_rate * 100, 2) AS completion_rate_percent,
    ROUND(br.binge_rate * 100, 2) AS binge_rate_percent,
    ROUND((cr.completion_rate * 0.4 + br.binge_rate * 0.6) * 100, 2) AS engagement_score
FROM completion_rates cr
JOIN binge_rates br ON cr.compilation_id = br.compilation_id
ORDER BY engagement_score DESC;

-- =====================================================
-- ЗАДАНИЕ 2.2: Рентген пользователей (RFM-анализ)
-- =====================================================
WITH user_metrics AS (
    SELECT 
        user_id,
        (CURRENT_DATE - MAX(show_date::date)) AS days_since_last_watch,
        COUNT(*) * 1.0 / NULLIF(
            EXTRACT(DAY FROM (MAX(show_date) - MIN(show_date))) + 1, 
            0
        ) AS avg_daily_views,
        SUM(show_duration) / 3600.0 AS total_watch_hours
    FROM content_watch
    GROUP BY user_id
),
user_segments AS (
    SELECT 
        user_id,
        days_since_last_watch,
        avg_daily_views,
        total_watch_hours,
        CASE 
            WHEN days_since_last_watch <= 7 THEN 'Active'
            WHEN days_since_last_watch <= 30 THEN 'Warm'
            ELSE 'Cold'
        END AS recency_segment,
        CASE 
            WHEN avg_daily_views >= 1 THEN 'Super Fan'
            WHEN avg_daily_views >= 0.3 THEN 'Regular'
            ELSE 'Casual'
        END AS frequency_segment,
        CASE 
            WHEN total_watch_hours >= 50 THEN 'Heavy'
            WHEN total_watch_hours >= 10 THEN 'Medium'
            ELSE 'Light'
        END AS monetary_segment
    FROM user_metrics
)
SELECT 
    CONCAT(recency_segment, ' / ', frequency_segment, ' / ', monetary_segment) AS segment,
    COUNT(*) AS users_count,
    ROUND(AVG(days_since_last_watch), 1) AS avg_recency_days,
    ROUND(AVG(avg_daily_views), 2) AS avg_daily_views,
    ROUND(AVG(total_watch_hours), 1) AS avg_watch_hours
FROM user_segments
GROUP BY recency_segment, frequency_segment, monetary_segment
ORDER BY 
    CASE recency_segment 
        WHEN 'Active' THEN 1 
        WHEN 'Warm' THEN 2 
        ELSE 3 
    END,
    users_count DESC;