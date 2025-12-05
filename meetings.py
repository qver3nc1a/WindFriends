import db


def add_meeting(title, gear, date, description, user_id):
    sql = "INSERT INTO meetings (title, gear, date, description, user_id) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [title, gear, date, description, user_id])


def get_meetings():
    sql = """
        SELECT m.id, m.title, m.gear, m.date, m.description, u.username, u.id as user_id
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
                    users.id user_id,
                    users.username
    FROM meetings, users
    WHERE meetings.user_id = users.id AND meetings.id = ?"""
    return db.query(sql, [meeting_id])[0]


def update_meeting(meeting_id, title, gear, date, description):
    sql = """UPDATE meetings SET title = ?,
                                gear = ?,
                                date = ?,
                                description = ?
            WHERE id = ?"""
    db.execute(sql, [title, gear, date, description, meeting_id])


def search(query):
    sql = """
            SELECT m.id, m.title, m.gear, m.date, m.description, u.username
            FROM meetings m
            JOIN users u ON m.user_id = u.id
            WHERE m.title LIKE ? OR m.gear LIKE ? OR m.description LIKE ?
            ORDER BY m.date DESC
        """
    return db.query(sql, ["%" + query + "%", "%" + query + "%", "%" + query + "%"])


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
