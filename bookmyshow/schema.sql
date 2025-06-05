-- Updated schema for cinema ticket booking system with cities, cinemas, halls, movies, shows, and bookings

CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE cinemas (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city_id INT REFERENCES cities(id),
    location VARCHAR(255)
);

CREATE TABLE halls (
    id SERIAL PRIMARY KEY,
    cinema_id INT REFERENCES cinemas(id),
    name VARCHAR(100) NOT NULL
);

CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    duration_minutes INT NOT NULL,
    rating VARCHAR(10),
    release_date DATE
);

CREATE TABLE shows (
    id SERIAL PRIMARY KEY,
    movie_id INT REFERENCES movies(id),
    hall_id INT REFERENCES halls(id),
    show_time TIMESTAMP NOT NULL
);

CREATE TABLE seats (
    id SERIAL PRIMARY KEY,
    hall_id INT REFERENCES halls(id),
    seat_number VARCHAR(10) NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    show_id INT REFERENCES shows(id),
    seat_id INT REFERENCES seats(id),
    booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'CONFIRMED'
);

-- Indexes and constraints can be added as needed for performance and data integrity. 