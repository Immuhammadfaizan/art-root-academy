CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    registration_id INTEGER REFERENCES registrations(id),
    name VARCHAR(100),
    email VARCHAR(100),
    payment_method VARCHAR(50),
    receipt_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM payments;
