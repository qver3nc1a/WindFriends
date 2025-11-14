import db


def add_meeting(title, gear, date, description, user_id):
    sql = "INSERT INTO meetings (title, gear, date, description, user_id) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [title, gear, date, description, user_id])


def get_meetings():
    sql = "SELECT id, title FROM meetings ORDER BY id DESC"
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
