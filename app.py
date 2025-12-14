from flask import Flask
from flask import request, render_template, redirect, abort, flash
from flask import session
import config
from werkzeug.security import check_password_hash, generate_password_hash
import db
import sqlite3
import meetings
import users
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = config.secret_key


@app.template_filter("finnish_datetime")
def finnish_datetime(value):
    dt = datetime.fromisoformat(value)
    return dt.strftime("%d.%m.%Y at %H:%M")


def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


@app.route("/")
def index():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    latest_meetings = meetings.get_latest_meetings(3)
    register_success = session.pop("register_success", None)
    return render_template(
        "index.html",
        meetings=latest_meetings,
        register_success=register_success,
        show_all_meetings_header=False,
    )


@app.route("/register")
def register():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    check_csrf()
    username = request.form["username"]
    if not username.strip():
        error = "Username cannot be blank"
        return render_template("register.html", error=error)
    password1 = request.form["password1"]
    if not password1.strip():
        error = "Password cannot be blank"
        return render_template("register.html", error=error)
    password2 = request.form["password2"]
    if password1 != password2:
        error = "Passwords don't match"
        return render_template("register.html", error=error)
    password_hash = generate_password_hash(password1)

    success = db.add_user(username, password_hash)
    if not success:
        error = "This username is already in use"
        return render_template("register.html", error=error)
    session["register_success"] = True
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        check_csrf()
        username = request.form.get("username")
        password = request.form.get("password")

        user = db.get_user_by_username(username)
        if not user:
            error = "This user doesn't exist"
            return render_template("index.html", error=error)
        user_id = user["id"]
        password_hash = user["password_hash"]
        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            error = "Wrong username or password"
            return render_template("index.html", error=error)
    return render_template("index.html")


@app.route("/logout", methods=["POST"])
def logout():
    check_csrf()
    session.pop("username", None)
    session.pop("user_id", None)
    session.pop("csrf_token", None)
    session["csrf_token"] = secrets.token_hex(16)
    return redirect("/")


@app.route("/new_meeting")
def new_meeting():
    if "username" not in session:
        return redirect("/login")
    return render_template("new_meeting.html")


@app.route("/create_meeting", methods=["POST"])
def create_meeting():
    check_csrf()
    title = request.form["title"]
    gear = request.form["gear"]
    date = request.form["date"]
    description = request.form["description"]
    tags_raw = request.form.get("tags", "")

    wind_speed = int(request.form.get("wind_speed", 1))
    user_id = session["user_id"]

    if (
        not title.strip()
        or not gear.strip()
        or not date.strip()
        or not description.strip()
    ):
        error = "Please fill all fields"
        return render_template("new_meeting.html", error=error)

    if len(title) > 100:
        error = "Title is too long (max 100 characters)"
        return render_template("new_meeting.html", error=error)

    try:
        meeting_date = datetime.fromisoformat(date)
        if meeting_date < datetime.now():
            error = "Date must be in the future"
            return render_template("new_meeting.html", error=error)
    except ValueError:
        error = "Invalid date format"
        return render_template("new_meeting.html", error=error)

    tag_names = [t.strip().lower() for t in tags_raw.split(",") if t.strip()]
    tags_str = ", ".join(tag_names)
    meeting_id = meetings.add_meeting(
        title, gear, date, description, user_id, wind_speed, tags_str
    )

    return redirect("/")


@app.route("/meeting/<int:meeting_id>")
def show_meeting(meeting_id):
    meeting = meetings.get_meeting(meeting_id)
    messages = meetings.get_messages(meeting_id)
    return render_template("show_meeting.html", meeting=meeting, messages=messages)


@app.route("/meeting/<int:meeting_id>/message", methods=["POST"])
def post_message(meeting_id):
    check_csrf()
    if "user_id" not in session:
        error = "You must be logged in to post a message."
        meeting = meetings.get_meeting(meeting_id)
        messages = meetings.get_messages(meeting_id)
        return render_template(
            "show_meeting.html", meeting=meeting, messages=messages, error=error
        )
    content = request.form.get("content", "").strip()
    if not content:
        error = "Message cannot be empty."
        meeting = meetings.get_meeting(meeting_id)
        messages = meetings.get_messages(meeting_id)
        return render_template(
            "show_meeting.html", meeting=meeting, messages=messages, error=error
        )
    meetings.add_message(meeting_id, session["user_id"], content)
    return redirect(f"/meeting/{meeting_id}")


@app.route("/edit_meeting/<int:meeting_id>", methods=["GET", "POST"])
def edit_meeting(meeting_id):
    if request.method == "POST":
        check_csrf()
    meeting = meetings.get_meeting(meeting_id)
    if meeting["user_id"] != session["user_id"]:
        return "Forbidden", 403
    return render_template("edit_meeting.html", meeting=meeting)


@app.route("/update_meeting", methods=["POST"])
def update_meeting():
    check_csrf()
    meeting_id = request.form["meeting_id"]
    meeting = meetings.get_meeting(int(meeting_id))
    if meeting["user_id"] != session["user_id"]:
        return "Forbidden", 403
    title = request.form["title"]
    gear = request.form["gear"]
    date = request.form["date"]

    description = request.form["description"]
    wind_speed = int(request.form.get("wind_speed", 1))
    tags_raw = request.form.get("tags", "")

    if (
        not title.strip()
        or not gear.strip()
        or not date.strip()
        or not description.strip()
    ):
        error = "Please fill all fields"
        return render_template("edit_meeting.html", meeting=meeting, error=error)

    if len(title) > 100:
        error = "Title is too long (max 100 characters)"
        return render_template("edit_meeting.html", meeting=meeting, error=error)

    try:
        meeting_date = datetime.fromisoformat(date)
        if meeting_date < datetime.now():
            error = "Date must be in the future"
            return render_template("edit_meeting.html", meeting=meeting, error=error)
    except ValueError:
        error = "Invalid date format"
        return render_template("edit_meeting.html", meeting=meeting, error=error)

    tag_names = [t.strip().lower() for t in tags_raw.split(",") if t.strip()]
    tags_str = ", ".join(tag_names)
    meetings.update_meeting(
        meeting_id, title, gear, date, description, wind_speed, tags_str
    )

    return redirect("/meeting/" + str(meeting_id))


@app.route("/search")
def search():
    if "username" not in session:
        return redirect("/login")
    query = request.args.get("query")
    tags = request.args.get("tags", "")
    tag_names = [t.strip().lower() for t in tags.split(",") if t.strip()]
    if tag_names:
        results = meetings.search_by_tags(tag_names)
    elif query:
        results = meetings.search(query)
    else:
        results = meetings.get_meetings()
    return render_template("search.html", query=query, tags=tags, results=results)


@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        error = "User not found"
        return render_template("index.html", error=error)
    meetings = users.get_meetings(user_id)
    return render_template("user.html", user=user, meetings=meetings)


@app.route("/delete_meeting/<int:meeting_id>", methods=["POST"])
def delete_meeting(meeting_id):
    check_csrf()
    meeting = meetings.get_meeting(meeting_id)
    if meeting["user_id"] != session["user_id"]:
        return "Forbidden", 403
    meetings.delete_meeting(meeting_id)
    return redirect("/")
