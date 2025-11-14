import db


def add_meeting(title, gear, date, description, user_id):
    sql = "INSERT INTO meetings (title, gear, date, description, user_id) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [title, gear, date, description, user_id])
