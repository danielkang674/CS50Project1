import os
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# import requests
# res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "9tXuycx0QtIcjSYQXXDg", "isbns": "9781632168146"})
# print(res.json())

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("error.html", message="Error 404 Page Not Found")
    if request.method == "POST":
        un = request.form.get("userName")
        password = request.form.get("password")
        findUser = db.execute(
            "SELECT userid FROM users WHERE userid = :un AND password = :password",
        {"un":un, "password":password}).fetchone()
        if findUser is None:
            return render_template("error.html", message="Incorrect login")
        else:
            session[un] = un
    return render_template("login.html", message=session[un], user=session[un])


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("error.html", message="Error 404 Page Not Found")
    if request.method == "POST":
        un = request.form.get("userName")
        password = request.form.get("password")
        verifyPassword = request.form.get("verifyPassword")
        if un is None or password is None or verifyPassword is None:
            return render_template("error.html", message="Fill in all fields")
        elif password != verifyPassword:
            return render_template("error.html", message="Passwords do not match")
        try:
            db.execute(
            "INSERT INTO users (userid, password) VALUES (:userid, :password)",
            {"userid": un, "password": password})
            db.commit()
        except sqlalchemy.exc.IntegrityError:
            return render_template("error.html", message="Username already exists")
    return redirect(url_for('index'))

@app.route("/logout", methods=["POST"])
def logout():
    un = request.form.get("logout")
    del session[un]
    print(session)
    return redirect(url_for('index'))