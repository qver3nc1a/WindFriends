CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE meetings (
    id INTEGER PRIMARY KEY,
    title TEXT,
    gear TEXT,
    date DATETIME,
    description TEXT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
)