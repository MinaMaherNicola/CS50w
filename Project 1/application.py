import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps

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

def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def hasher(word):
    result = 0
    for i in range(len(word)):
        result += ord(word[i])
    result *= len(word)
    return result

@app.route("/")
def index():
    session.clear()
    return render_template("login.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", e = "ENTER YOUR USERNAME!")

        elif not request.form.get("password"):
            return render_template("error.html", e = "ENTER YOUR PASSWORD!")

        else:
            password = request.form.get("password")
            hash = hasher(password)
            user = request.form.get("username")

            userData = db.get_bind().execute(text("SELECT * FROM users WHERE username = :username"), username = user).fetchone()

            if not userData:
                return render_template("error.html", e="THERE IS NO SUCH USERNAME")

            elif str(hash) != str(userData[2]):
                return render_template("error.html", e="WRONG PASSWORD!")
            else:
                session["user_id"] = userData[0]
                return redirect(url_for("search"))
    else:
        return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", e="PLEASE PROVIDE A USER NAME!")

        elif not request.form.get("password"):
            return render_template("error.html", e="PLEASE PROVIDE A PASSWORD!")

        elif len(request.form.get("password")) < 8:
            return render_template("error.html", e="PLEASE PROVIDE A PASSWORD WITH 8 CHARACTERS OR MORE!")

        elif not request.form.get("confirmpassword"):
            return render_template("error.html", e="PLEASE CONFIRM YOUR PASSWORD!")

        elif not request.form.get("email"):
            return render_template("error.html", e="PLEASE CONFIRM AN EMAIL!")

        elif not request.form.get("confirmpassword") == request.form.get("password"):
            return render_template("error.html", e="YOUR PASSWORD DOESN\'T MATCH!")

        else:
            user = request.form.get("username")
            hash = hasher(request.form.get("password"))
            email = request.form.get("email")
            allUsers = db.get_bind().execute(text("SELECT username FROM users"))
            row = allUsers.fetchone()
            repeated = False
            if row:
                for i in range(len(row)):
                    if user == row[i]:
                        repeated = True
                        return render_template("error.html", e="USERNAME IS ALREADY TAKEN!")

            if repeated == False:
                new_user_id = db.get_bind().execute(text("INSERT INTO users (username, password, email)" + "VALUES (:username, :password, :email)"), username=user, password=hash, email=email)
                userId = db.get_bind().execute(text("SELECT id FROM users WHERE username = :username"), username=user).fetchone()
                session["user_id"] = userId[0]
                return redirect(url_for("search"))
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

titleVar = []

@app.route("/search", methods=["POST", "GET"])
@login_required
def search():
    if request.method == "POST":
        search = request.form.get("search")
        if not search:
            return render_template("error.html", e="PLEASE ENTER DESIRED BOOK!", user_id=session["user_id"])
        else:
            row = db.get_bind().execute(text("SELECT * FROM books WHERE isbn = :isbn"), isbn=search).fetchone()
            if not row:
                row = db.get_bind().execute(text("SELECT * FROM books WHERE title = :title"), title=search).fetchone()
            if not row:
                row = db.get_bind().execute(text("SELECT * FROM books WHERE author = :author"), author=search).fetchone()
            if row:
                res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "gc0ZZOko8DcWkNBzgIKg", "isbns": "9781632168146"}).json()
                data = []

                for i in range(len(row)):
                    data.append(row[i])

                data.append(res['books'][0]['average_rating'])
                holder = data[0]
                data[0] = data[1]
                data[1] = holder

                titleVar.append(data[0])

                rev = db.get_bind().execute(text("SELECT * FROM reviews WHERE booktitle = :title"), title=titleVar[0]).fetchall()

                if rev:
                    return render_template("bookpage.html", data=data, user_id=session["user_id"], reviews=rev)

                else:
                    return render_template("bookpage.html", data=data, user_id=session["user_id"])
    else:
        return render_template("search.html", user_id=session["user_id"])

@app.route("/submitReview", methods=["POST", "GET"])
@login_required
def submitReview():
    if request.method == "POST":
        reviewData = []
        if request.form.get("review") and request.form.get("rating"):
            user = db.get_bind().execute(text("SELECT * FROM users WHERE id = :id"), id=session["user_id"]).fetchone()

            reviewCheck = db.get_bind().execute(text("SELECT * FROM reviews WHERE username = :username"), username=user[1]).fetchone()
            if reviewCheck:
                if titleVar[0] == reviewCheck[1]:
                    return render_template("error.html", e="YOU CAN'T REVIEW THE SAME BOOK TWICE!", user_id=session["user_id"])
                else:
                    reviewData.append(user[1])
                    reviewData.append(request.form.get("review"))
                    reviewData.append(titleVar[0])
                    reviewData.append(request.form.get("rating"))
                    db.get_bind().execute(text("INSERT INTO reviews (username, booktitle, review, rating)" + "VALUES (:username, :title, :review, :rating)"), username=reviewData[0], title=reviewData[2], review=reviewData[1], rating=reviewData[3])
                    return render_template("search.html", user_id=session["user_id"], success=True)
            else:
                reviewData.append(user[1])
                reviewData.append(request.form.get("review"))
                reviewData.append(titleVar[0])
                reviewData.append(request.form.get("rating"))
                db.get_bind().execute(text("INSERT INTO reviews (username, booktitle, review, rating)" + "VALUES (:username, :title, :review, :rating)"), username=reviewData[0], title=reviewData[2], review=reviewData[1], rating=reviewData[3])
                return render_template("search.html", user_id=session["user_id"], success=True)
        else:
            return render_template("error.html", e="PLEASE FILL THE REVIEW AND RATE THE BOOK!", user_id=session["user_id"])
    else:
        return render_template("search.html", user_id=session["user_id"])