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
    register_success = session.pop("register_success", None)
    return render_template(
        "index.html", meetings=all_meetings, register_success=register_success
    )


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        error = "VIRHE: salasanat eivät ole samat"
        return render_template("register.html", error=error)
    password_hash = generate_password_hash(password1)

    success = db.add_user(username, password_hash)
    if not success:
        error = "VIRHE: tunnus on jo varattu"
        return render_template("register.html", error=error)
    session["register_success"] = True
    return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = db.get_user_by_username(username)
    if not user:
        error = "VIRHE: käyttäjää ei ole olemassa"
        return render_template("index.html", error=error)
    user_id = user["id"]
    password_hash = user["password_hash"]
    if check_password_hash(password_hash, password):
        session["username"] = username
        session["user_id"] = user_id
        return redirect("/")
    else:
        error = "VIRHE: väärä tunnus tai salasana"
        return render_template("index.html", error=error)


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

    if (
        not title.strip()
        or not gear.strip()
        or not date.strip()
        or not description.strip()
    ):
        error = "Täytä kaikki kentät."
        return render_template("new_meeting.html", error=error)

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


@app.route("/search")
def search():
    query = request.args.get("query")
    results = meetings.search(query) if query else []
    return render_template("search.html", query=query, results=results)
