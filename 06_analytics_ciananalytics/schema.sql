-- Cian Analytics: Library DB schema (3NF)

CREATE TABLE IF NOT EXISTS work (
    id SERIAL PRIMARY KEY,
    name VARCHAR(500) NOT NULL
);

CREATE TABLE IF NOT EXISTS edition (
    id SERIAL PRIMARY KEY,
    work_id INT REFERENCES work(id),
    year INT,
    pages INT
);

CREATE TABLE IF NOT EXISTS copy (
    id SERIAL PRIMARY KEY,
    edition_id INT REFERENCES edition(id),
    inventory_num VARCHAR(50) UNIQUE
);

CREATE TABLE IF NOT EXISTS operation_log (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    copy_id INT REFERENCES copy(id),
    date_taken DATE,
    date_returned DATE
);
