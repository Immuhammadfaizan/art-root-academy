CREATE TABLE registrations (
    id SERIAL AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    dob DATE NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    contact_method VARCHAR(50) NOT NULL,
    course_category VARCHAR(50) NOT NULL,
    course VARCHAR(255) NOT NULL,
    referral VARCHAR(255),
    experience VARCHAR(3),
    experience_details TEXT,
    payment_method VARCHAR(50) NOT NULL,
    agree ENUM('Agree', 'Disagree') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM registrations;