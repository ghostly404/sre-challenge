import logging
from flask import Flask, session, redirect, url_for, request, render_template, abort
import psycopg2 #postgress
import os
import psycopg2.extras #extra postgress utility

app = Flask(__name__)
app.secret_key = b"192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"
app.logger.setLevel(logging.INFO)


def get_db_connection(): #connectie met de postgresdatabase
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) #psycopg2 werkt met cursor daarom nodig
    return conn, cursor


def is_authenticated():
    if "username" in session:
        return True
    return False


def authenticate(username, password):
    #iets aangepast zodat de connectie met postgres werkt ipv sqlite
    conn, cur = get_db_connection()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()

    for user in users:
        if user["username"] == username and user["password"] == password:
            app.logger.info(f"the user '{username}' logged in successfully with password '{password}'")
            session["username"] = username
            return True

    app.logger.warning(f"the user '{ username }' failed to log in '{ password }'")
    abort(401)


@app.route("/")
def index():
    return render_template("index.html", is_authenticated=is_authenticated())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if authenticate(username, password):
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route("/healthz")
def healthz():
        return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
