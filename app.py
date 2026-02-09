from flask import Flask, render_template, request, redirect
import sqlite3
import string
import random
from datetime import datetime, timedelta
from urllib.parse import urlparse

app = Flask(__name__)

# ------------------------
# Database Setup
# ------------------------
def init_db():
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE,
            clicks INTEGER DEFAULT 0,
            expiry_date TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ------------------------
# Helpers
# ------------------------
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc != ""

# ------------------------
# Routes
# ------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten():
    original_url = request.form["url"]
    custom_code = request.form.get("custom_code")
    expiry_days = request.form.get("expiry")

    if not is_valid_url(original_url):
        return "❌ Invalid URL! Must start with http:// or https://"

    short_code = custom_code if custom_code else generate_short_code()

    expiry_date = None
    if expiry_days:
        expiry_date = (datetime.now() + timedelta(days=int(expiry_days))).strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO urls (original_url, short_code, expiry_date)
            VALUES (?, ?, ?)
        """, (original_url, short_code, expiry_date))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "❌ Custom code already exists!"
    
    conn.close()
    return render_template("result.html", short_code=short_code)

@app.route("/delete/<short_code>")
def delete_url(short_code):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM urls WHERE short_code=?", (short_code,))
    conn.commit()
    conn.close()
    return redirect("/history")

@app.route("/history")
def history():
    search_query = request.args.get("search", "")
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    if search_query:
        cursor.execute("""
            SELECT original_url, short_code, clicks, expiry_date
            FROM urls
            WHERE short_code LIKE ?
        """, ('%' + search_query + '%',))
    else:
        cursor.execute("""
            SELECT original_url, short_code, clicks, expiry_date
            FROM urls
        """)

    data = cursor.fetchall()
    conn.close()
    return render_template("history.html", urls=data, search_query=search_query)

@app.route("/<short_code>")
def redirect_to_url(short_code):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT original_url, clicks, expiry_date
        FROM urls WHERE short_code=?
    """, (short_code,))
    result = cursor.fetchone()

    if result:
        original_url, clicks, expiry_date = result

        if expiry_date:
            if datetime.now() > datetime.strptime(expiry_date, "%Y-%m-%d %H:%M:%S"):
                conn.close()
                return "⏳ This link has expired."

        cursor.execute("UPDATE urls SET clicks=? WHERE short_code=?",
                       (clicks + 1, short_code))
        conn.commit()
        conn.close()
        return redirect(original_url)

    conn.close()
    return "❌ Invalid Short URL"

if __name__ == "__main__":
    app.run(debug=True)
