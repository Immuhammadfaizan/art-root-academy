-- Create the Email table if it doesn't already exist
CREATE TABLE IF NOT EXISTS Email (
    id INT PRIMARY KEY AUTO_INCREMENT,
    subject VARCHAR(120) NOT NULL,
    sender VARCHAR(120) NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    snippet VARCHAR(200) NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    category VARCHAR(50) DEFAULT 'inbox'
);

SELECT * FROM email
