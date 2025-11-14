from flask import Flask
from flask import request, render_template, redirect
from flask import session
import config
from werkzeug.security import check_password_hash, generate_password_hash
import db
import sqlite3
import meetings

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    all_meetings = meetings.get_meetings()
    return render_template("index.html", meetings=all_meetings)


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat <br /><a href='/register'>back</a>"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu <br /><a href='/'>back</a>"

    return "Tunnus luotu <br /><a href='/'>back</a>"


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    try:
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]
    except IndexError:
        return "VIRHE: käyttäjää ei ole olemassa <br /><a href='/'>back</a> <br /><a href='/register'>register</a>"

    if check_password_hash(password_hash, password):
        session["username"] = username
        session["user_id"] = user_id
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana <br /><a href='/'>back</a>"


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/new_meeting")
def new_meeting():
    return render_template("new_meeting.html")


@app.route("/create_meeting", methods=["POST"])
def create_meeting():
    title = request.form["title"]
    gear = request.form["gear"]
    date = request.form["date"]
    description = request.form["description"]
    user_id = session["user_id"]

    meetings.add_meeting(title, gear, date, description, user_id)

    return redirect("/")


@app.route("/meeting/<int:meeting_id>")
def show_meeting(meeting_id):
    meeting = meetings.get_meeting(meeting_id)
    return render_template("show_meeting.html", meeting=meeting)


@app.route("/edit_meeting/<int:meeting_id>")
def edit_meeting(meeting_id):
    meeting = meetings.get_meeting(meeting_id)
    return render_template("edit_meeting.html", meeting=meeting)


@app.route("/update_meeting", methods=["POST"])
def update_meeting():
    meeting_id = request.form["meeting_id"]
    title = request.form["title"]
    gear = request.form["gear"]
    date = request.form["date"]
    description = request.form["description"]

    meetings.update_meeting(meeting_id, title, gear, date, description)

    return redirect("/meeting/" + str(meeting_id))
