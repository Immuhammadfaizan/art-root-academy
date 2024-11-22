CREATE TABLE user_data (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL,
    terms_agreed BOOLEAN DEFAULT FALSE NOT NULL
);

select * from user_data;
