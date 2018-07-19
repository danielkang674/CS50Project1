import os
import requests
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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
    if isLoggedIn():
        return render_template("index.html")
    else:
        return render_template("index.html", user=session['userID'])

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
            session['userID'] = un
    return render_template("login.html", user=session['userID'])

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
    return render_template("signup.html", user=un)

@app.route("/logout", methods=["POST"])
def logout():
    session.pop('userID', None)
    return redirect(url_for('index'))

@app.route("/search", methods=["GET", "POST"])
def search():
    if isLoggedIn():
        return isLoggedIn()
    if request.method == "GET":
        return render_template("search.html", user=session['userID'])
    if request.method == "POST":
        search = request.form.get("searchBar")
        if search == "":
            return render_template("search.html", message="Enter a search term")
        findBook = db.execute(
            f"SELECT * FROM books WHERE isbn LIKE '%{search}%' OR title LIKE '%{search.capitalize()}%' OR author LIKE '%{search.capitalize()}%'").fetchmany(10)
        if not findBook:
            return render_template("search.html", message='No results')
        return render_template("search.html", results=findBook)

@app.route("/book/<string:isbn>", methods=["GET", "POST"])
def book(isbn):
    if isLoggedIn():
        return isLoggedIn()
    if request.method == "GET":
        bookInfo = db.execute(
            "SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
        if bookInfo is None:
            return render_template("book.html", bookInfo="Book does not exist")
        bookReviews = db.execute(
            "SELECT rating, review FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "9tXuycx0QtIcjSYQXXDg", "isbns": isbn})
        grReview = (res.json()['books'][0])
        return render_template("book.html", bookInfo=bookInfo, bookReviews=bookReviews, user=session['userID'], grReview=grReview)
    if request.method == "POST":
        rating = request.form.get("rating")
        review = request.form.get("review")
        user = db.execute(
            "SELECT isbn, userid FROM reviews WHERE isbn = :isbn AND userid = :userid",
            {"isbn": isbn, "userid": session['userID']}).fetchone()
        if user:
            return render_template("error.html", message="You've already reviewed this book!")
        db.execute(
            "INSERT INTO reviews (rating, review, isbn, userid) VALUES (:rating, :review, :isbn, :userid)",
            {"rating": rating, "review": review, "isbn": isbn, "userid": session['userID']})
        db.commit()
        return redirect(url_for('book', isbn=isbn))

@app.route("/api/<string:isbn>")
def api(isbn):
    bookInfo = db.execute(
            "SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if bookInfo is None:
        return jsonify({"error": "Could not find book"}), 404
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "9tXuycx0QtIcjSYQXXDg", "isbns": isbn})
    grReview = (res.json()['books'][0])
    bookjson = jsonify({
        "title": bookInfo.title, "author": bookInfo.author, "year": bookInfo.year, "isbn": bookInfo.isbn,
        "review_count": grReview['work_ratings_count'], "average_score": grReview['average_rating']})
    return bookjson

def isLoggedIn():
    if 'userID' not in session:
        return render_template("error.html", message="Please log in first!")