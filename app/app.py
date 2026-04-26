from flask import Flask, request, jsonify
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

@app.route("/")
def home():
    return "Flask + PostgreSQL running with Docker Compose!"

@app.route("/notes", methods=["GET", "POST"])
def notes():
    conn = get_db_connection()
    cur = conn.cursor()

    # Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            content TEXT
        )
    """)

    if request.method == "POST":
        data = request.get_json()
        content = data.get("content")

        cur.execute("INSERT INTO notes (content) VALUES (%s)", (content,))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Note added!"})

    cur.execute("SELECT * FROM notes")
    notes = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(notes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
