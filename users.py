import db


def get_user(user_id):
    sql = "SELECT username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None


def get_meetings(user_id):
    sql = """
        SELECT id, title, gear, date, description
        FROM meetings
        WHERE user_id = ?
        ORDER BY date DESC
    """
    return db.query(sql, [user_id])
