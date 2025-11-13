from flask import Flask
from flask import request, render_template, redirect
from flask import session
import config
from werkzeug.security import check_password_hash, generate_password_hash
import db
import sqlite3

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    return render_template("index.html")


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

    sql = "SELECT password_hash FROM users WHERE username = ?"
    try:
        password_hash = db.query(sql, [username])[0][0]
    except IndexError:
        return "VIRHE: käyttäjää ei ole olemassa <br /><a href='/'>back</a> <br /><a href='/register'>register</a>"

    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana <br /><a href='/'>back</a>"


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
