import db


def add_meeting(title, gear, date, description, user_id, wind_speed, tags_str=""):
    """Create a meeting and return its id. Stores tags as a comma-separated string."""
    sql = "INSERT INTO meetings (title, gear, date, description, user_id, wind_speed, tags) VALUES (?, ?, ?, ?, ?, ?, ?)"
    con = db.get_connection()
    cur = con.execute(
        sql, [title, gear, date, description, user_id, wind_speed, tags_str]
    )
    con.commit()
    meeting_id = cur.lastrowid
    con.close()
    return meeting_id


def add_meeting_tags(meeting_id, tag_names):
    """Simplified: store tags as comma-separated string in meetings.tags."""
    tags_str = ", ".join(sorted({t.strip().lower() for t in tag_names if t.strip()}))
    sql = "UPDATE meetings SET tags = ? WHERE id = ?"
    db.execute(sql, [tags_str, meeting_id])


def get_meetings():
    sql = """
        SELECT m.id, m.title, m.gear, m.date, m.description, m.tags, u.username, u.id as user_id
        FROM meetings m
        JOIN users u ON m.user_id = u.id
        ORDER BY m.date DESC
    """
    return db.query(sql)


def get_meeting(meeting_id):
    sql = """SELECT meetings.id,
                    meetings.title,
                    meetings.gear,
                    meetings.date,
                    meetings.description,
                    meetings.wind_speed,
                    meetings.tags,
                    users.id user_id,
                    users.username
    FROM meetings, users
    WHERE meetings.user_id = users.id AND meetings.id = ?"""
    return db.query(sql, [meeting_id])[0]


def update_meeting(meeting_id, title, gear, date, description, wind_speed, tags_str=""):
    sql = """UPDATE meetings SET title = ?,
                                gear = ?,
                                date = ?,
                                description = ?,
                                wind_speed = ?,
                                tags = ?
            WHERE id = ?"""
    db.execute(sql, [title, gear, date, description, wind_speed, tags_str, meeting_id])


def set_meeting_tags(meeting_id, tag_names):
    """Replace tags string for a meeting."""
    add_meeting_tags(meeting_id, tag_names)


def search(query):
    sql = """
            SELECT m.id, m.title, m.gear, m.date, m.description, m.tags, u.username, u.id as user_id
            FROM meetings m
            JOIN users u ON m.user_id = u.id
            WHERE m.title LIKE ? OR m.gear LIKE ? OR m.description LIKE ?
            ORDER BY m.date DESC
        """
    return db.query(sql, ["%" + query + "%", "%" + query + "%", "%" + query + "%"])


def search_by_tags(tag_names):
    if not tag_names:
        return get_meetings()
    tag = str(tag_names[0]).strip()
    if not tag:
        return get_meetings()
    sql = """
        SELECT m.id, m.title, m.gear, m.date, m.description, m.tags, u.username, u.id as user_id
        FROM meetings m
        JOIN users u ON m.user_id = u.id
        WHERE m.tags LIKE ?
        ORDER BY m.date DESC
    """
    return db.query(sql, [f"%{tag}%"])


def delete_meeting(meeting_id):
    sql = "DELETE FROM meetings WHERE id = ?"
    db.execute(sql, [meeting_id])


def get_latest_meetings(limit=3):
    sql = """
        SELECT m.id, m.title, m.gear, m.date, m.description, u.username, u.id as user_id
        FROM meetings m
        JOIN users u ON m.user_id = u.id
        ORDER BY m.date DESC
        LIMIT ?
    """
    return db.query(sql, [limit])


def add_message(meeting_id, user_id, content):
    db.add_message(meeting_id, user_id, content)


def get_messages(meeting_id):
    return db.get_messages_for_meeting(meeting_id)
