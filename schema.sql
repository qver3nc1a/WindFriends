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
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    wind_speed INTEGER,
    tags TEXT
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    meeting_id INTEGER REFERENCES meetings(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);