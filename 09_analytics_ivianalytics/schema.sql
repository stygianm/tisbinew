-- ivi Analytics schema

CREATE TABLE IF NOT EXISTS content (
    content_id INT PRIMARY KEY,
    compilation_id INT,
    episode INT,
    paid_type VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS content_watch (
    watch_id BIGINT PRIMARY KEY,
    show_date TIMESTAMP,
    show_duration INT,
    platform INT,
    user_id INT,
    utm_medium VARCHAR(50),
    content_id INT REFERENCES content(content_id)
);
