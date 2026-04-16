import logging
import sqlite3
import sys

from flask import Flask, jsonify, render_template, request, url_for, redirect, flash

# Global counter for database connections initiated via get_db_connection()
db_connection_count = 0


def _configure_logging():
    """Timestamped logs to STDOUT (DEBUG+) and STDERR (ERROR+)."""
    log_format = "%(asctime)s %(levelname)s:%(name)s:%(message)s"
    date_format = "%m/%d/%Y, %H:%M:%S"
    formatter = logging.Formatter(log_format, datefmt=date_format)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers.clear()
    root.addHandler(stdout_handler)
    root.addHandler(stderr_handler)

    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.DEBUG)

    logging.getLogger("werkzeug").setLevel(logging.DEBUG)


_configure_logging()
logger = logging.getLogger("app")


def get_db_connection():
    """Connect to database.db; increments db_connection_count for metrics."""
    global db_connection_count
    db_connection_count += 1
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection


def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    connection.close()
    return post


app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"


def _database_ready():
    """Return True if DB file exists, connects, and posts table is usable."""
    try:
        conn = sqlite3.connect("database.db")
        conn.execute("SELECT 1 FROM posts LIMIT 1")
        conn.close()
        return True
    except sqlite3.Error:
        return False


@app.route("/healthz")
def healthz():
    if _database_ready():
        return jsonify(result="OK - healthy"), 200
    return jsonify(result="ERROR - unhealthy"), 500


@app.route("/metrics")
def metrics():
    connection = get_db_connection()
    row = connection.execute("SELECT COUNT(*) AS c FROM posts").fetchone()
    connection.close()
    post_count = int(row["c"]) if row else 0
    return jsonify(db_connection_count=db_connection_count, post_count=post_count), 200


@app.route("/")
def index():
    connection = get_db_connection()
    posts = connection.execute("SELECT * FROM posts").fetchall()
    connection.close()
    return render_template("index.html", posts=posts)


@app.route("/<int:post_id>")
def post(post_id):
    row = get_post(post_id)
    if row is None:
        logger.error('Article not found, 404 returned for id "%s"', post_id)
        return render_template("404.html"), 404
    logger.info('Article "%s" retrieved!', row["title"])
    return render_template("post.html", post=row)


@app.route("/about")
def about():
    logger.info('"About Us" page retrieved')
    return render_template("about.html")


@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            connection = get_db_connection()
            connection.execute(
                "INSERT INTO posts (title, content) VALUES (?, ?)", (title, content)
            )
            connection.commit()
            connection.close()
            logger.info('New article "%s" created!', title)
            return redirect(url_for("index"))

    return render_template("create.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3111")
