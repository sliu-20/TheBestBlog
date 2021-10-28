import os
import sqlite3
import re
from flask import Flask, render_template, request, session, redirect
import bcrypt

MAIN_DB = "blogs.db"

db = sqlite3.connect(MAIN_DB)
c = db.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS BLOGS (
    ROWID   INTEGER PRIMARY KEY,
    NAME    TEXT    NOT NULL,
    AUTHOR  TEXT    NOT NULL
);""")
c.execute("""
CREATE TABLE IF NOT EXISTS USERS (
    ROWID       INTEGER PRIMARY KEY,
    USERNAME    TEXT    NOT NULL,
    HASH        TEXT    NOT NULL
);""")
db.commit()
db.close()

app = Flask(__name__)
salt = bcrypt.gensalt()


@app.route("/blog")
def fetch_page():
    db = sqlite3.connect(MAIN_DB)
    c = db.cursor()

    filename = None
    if 'page' in request.args:
        c.execute("""SELECT ROWID FROM BLOGS WHERE NAME = ?;""",
                  (request.args['page'],))
        filename = str(c.fetchone()[0]) + ".txt"

    # db.commit() no edits
    db.close()

    return filename


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        if 'username' in request.form and 'password' in request.form:
            db = sqlite3.connect(MAIN_DB)
            c = db.cursor()
            c.execute("""SELECT USERNAME FROM USERS WHERE USERNAME = ?;""",
                      (request.form['username'],))
            exists = c.fetchone()
            if (exists == None):
                username = (request.form['username']).encode('utf-8')
                if re.match('^[a-zA-Z 0-9\_]*$', username.decode('utf-8')) == None:
                    db.close()
                    return render_template("login.html", action="/signup", name="Sign Up", error="Username can only contain alphanumeric characters and underscores.")
                if len(username) < 5 or len(username) > 15:
                    db.close()
                    return render_template("login.html", action="/signup", name="Sign Up", error="Usernames must be between 5 and 15 characters long")
                password = request.form['password']
                if ' ' in list(password) or '\\' in list(password):
                    db.close()
                    return render_template("login.html", action="/signup", name="Sign Up", error="Passwords cannot contain spaces or backslashes.")
                password = password.encode('utf-8')
                if len(password) > 7 and len(password) <= 50:
                    c.execute("""INSERT INTO USERS (USERNAME,HASH) VALUES (?,?)""",
                              (request.form['username'], bcrypt.hashpw(password, salt),))
                    db.commit()
                    c.execute(
                        """SELECT USERNAME FROM USERS WHERE USERNAME = ?;""", (request.form['username'],))
                    exists = c.fetchone()
                    db.close()
                    if (exists != None):
                        return render_template("login.html", action="/login", name="Login", error="Signed up successfully!")
                    else:
                        return render_template("login.html", action="/signup", name="Sign Up", error="Some error occurred. Please try signing up again.")
                else:
                    db.close()
                    return render_template("login.html", action="/signup", name="Sign Up", error="Password must be between 8 and 50 characters long")
            else:
                db.close()
                return render_template("login.html", action="/signup", name="Sign Up", error="Username already exists")
        else:
            return render_template("login.html", action="/signup", name="Sign Up", error="Some error occurred. Please try signing up again.")
    else:
        return render_template("login.html", action="/signup", name="Sign Up")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if 'username' in request.form and 'password' in request.form:
            db = sqlite3.connect(MAIN_DB)
            c = db.cursor()
            c.execute("""SELECT HASH FROM USERS WHERE USERNAME = ?;""",
                      ((request.form['username']).encode('utf-8'),))
            hashed = c.fetchone()  # [0]
            db.close()
            if (hashed == None):
                return render_template("login.html", name="Login", action="/login", error="User does not exist.")
            else:
                if bcrypt.checkpw((request.form['password']).encode('utf-8'), hashed[0]):
                    return "Logged in!"
                else:
                    return render_template("login.html", name="Login", action="/login", error="Password is incorrect")
        else:
            return render_template("login.html", name="Login", action="/login", error="An error occurred. Please try logging in again.")
    else:
        return render_template("login.html", action="/login", name="Login")


if __name__ == "__main__":
    app.debug = True
    app.run()
