-- Тестовые данные для skypro_test

-- Пользователи
INSERT INTO users (name, email, registration_date) VALUES
('Иван Петров', 'ivan@email.com', '2024-01-10 10:00:00'),
('Мария Сидорова', 'maria@email.com', '2024-01-15 15:30:00'),
('Петр Иванов', 'petr@email.com', '2024-02-01 09:00:00'),
('Анна Смирнова', 'anna@email.com', '2024-02-05 14:20:00'),
('Сергей Козлов', 'sergey@email.com', '2024-02-10 11:00:00');

-- Курсы
INSERT INTO courses (course_name) VALUES
('Python для начинающих'),
('SQL для аналитиков'),
('Data Science с нуля'),
('Веб-разработка на Django');

-- Оценки
INSERT INTO ratings (course_id, user_id, rating) VALUES
(1, 1, 5), (1, 2, 4), (1, 3, 5), (1, 4, 4), (1, 5, 5),
(2, 1, 5), (2, 2, 5), (2, 3, 4), (2, 4, 5), (2, 5, 4), (2, 1, 5),
(3, 2, 3), (3, 3, 4), (3, 4, 3);

-- Заказы
INSERT INTO orders (course_id, user_id, order_date, price) VALUES
(1, 1, '2024-01-15', 5000),
(2, 2, '2024-01-20', 6000),
(1, 3, '2024-02-01', 5000),
(3, 4, '2024-02-05', 8000),
(2, 5, '2024-02-10', 6000),
(1, 2, '2024-02-15', 5000);

-- Курсы пользователей
INSERT INTO user_courses (user_id, course_id, start_date, end_date) VALUES
(1, 1, '2024-01-15', '2024-03-15'),
(2, 2, '2024-01-20', NULL),
(3, 1, '2024-02-01', '2024-04-01'),
(4, 3, '2024-02-05', NULL),
(5, 2, '2024-02-10', '2024-04-10'),
(2, 1, '2024-02-15', NULL);

-- События
INSERT INTO events (user_id, event_type, event_date) VALUES
(1, 'registration', '2024-01-10'),
(1, 'course_purchase', '2024-01-15'),
(1, 'course_complete', '2024-03-15'),
(2, 'registration', '2024-01-15'),
(2, 'course_purchase', '2024-01-20'),
(3, 'registration', '2024-02-01'),
(3, 'course_purchase', '2024-02-01'),
(4, 'registration', '2024-02-05'),
(4, 'course_purchase', '2024-02-05'),
(5, 'registration', '2024-02-10'),
(5, 'course_purchase', '2024-02-10'),
(2, 'course_purchase', '2024-02-15');