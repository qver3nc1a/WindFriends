def add_user(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    try:
        execute(sql, [username, password_hash])
        return True
    except sqlite3.IntegrityError:
        return False


def get_user_by_username(username):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = query(sql, [username])
    if result:
        return result[0]
    return None


import sqlite3
from flask import g


def get_connection():
    con = sqlite3.connect("database.db", timeout=10)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con


def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    con.close()


def last_insert_id():
    return g.last_insert_id


def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result


def add_message(meeting_id, user_id, content):
    sql = "INSERT INTO messages (meeting_id, user_id, content) VALUES (?, ?, ?)"
    execute(sql, [meeting_id, user_id, content])


def get_messages_for_meeting(meeting_id):
    sql = """
        SELECT messages.id, messages.content, messages.created_at, users.username, users.id as user_id
        FROM messages
        LEFT JOIN users ON messages.user_id = users.id
        WHERE messages.meeting_id = ?
        ORDER BY messages.created_at ASC
    """
    return query(sql, [meeting_id])
