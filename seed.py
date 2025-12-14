import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM meetings")
db.execute("DELETE FROM messages")

user_count = 1000
meeting_count = 10**5
message_count = 10**6

for i in range(1, user_count + 1):
    db.execute(
        "INSERT INTO users (username) VALUES (?)",
        ["user" + str(i)],
    )

for i in range(1, meeting_count + 1):
    title = random.choice(
        [
            "cool meeting",
            "amazing meeting",
            "windy meetup",
            "chill meetup",
            "dawn surfing",
        ]
    )
    gear = random.choice(
        [
            "Wingfoil",
            "Superboard",
            "Surfboard",
            "Hydrofoil",
            "Windsurf",
        ]
    )
    description = random.choice(
        [
            "Amazing surfing session at the beach",
            "Evening ride, bring marshmallows!!",
            "Beginner-friendly meetup, rented gear",
            "Windsurfing and sup if conditions allow",
            "Gear sharing welcome",
        ]
    )
    user_id = random.randint(1, user_count)
    wind_speed = random.randint(1, 5)
    tags_pool = ["beginner", "advanced", "chill", "energetic", "waves", "fun"]
    tags = ",".join(random.sample(tags_pool, k=random.randint(1, 3)))
    db.execute(
        """
        INSERT INTO meetings (title, gear, date, description, user_id, wind_speed, tags)
        VALUES (?, ?, datetime('now'), ?, ?, ?, ?)
        """,
        [title, gear, description, user_id, wind_speed, tags],
    )

for i in range(1, message_count + 1):
    user_id = random.randint(1, user_count)
    meeting_id = random.randint(1, meeting_count)
    db.execute(
        """
        INSERT INTO messages (content, created_at, user_id, meeting_id)
        VALUES (?, datetime('now'), ?, ?)
        """,
        ["message" + str(i), user_id, meeting_id],
    )

db.commit()
db.close()
