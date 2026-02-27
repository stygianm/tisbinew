-- Skypro Data Analyst schema

CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    course_id INT,
    user_id INT,
    order_date DATE,
    price DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    registration_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS ratings (
    rating_id SERIAL PRIMARY KEY,
    course_id INT,
    user_id INT,
    rating INT
);

CREATE TABLE IF NOT EXISTS user_courses (
    user_id INT,
    course_id INT,
    start_date DATE,
    end_date DATE
);

CREATE TABLE IF NOT EXISTS events (
    event_id SERIAL PRIMARY KEY,
    user_id INT,
    event_type VARCHAR(50),
    event_date DATE
);
