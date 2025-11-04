# simple Flask app that stores and reads a message from MySQL
from flask import Flask, jsonify, request
import os
import pymysql
from time import sleep

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASS = os.getenv("DB_PASS", "apppassword")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_PORT = int(os.getenv("DB_PORT", 3306))

app = Flask(__name__)

def get_db_connection(retries=5, wait=2):
    """Try to connect to mysql a few times (useful because db may be initializing)."""
    for i in range(retries):
        try:
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS,
                                   database=DB_NAME, port=DB_PORT, cursorclass=pymysql.cursors.DictCursor)
            return conn
        except Exception as e:
            if i + 1 == retries:
                raise
            sleep(wait)

@app.route("/")
def index():
    return jsonify({"message": "Hello from Flask", "db_host": DB_HOST})

@app.route("/init")
def init_db():
    """Create a simple table if not exists."""
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    message VARCHAR(255) NOT NULL
                ) ENGINE=InnoDB;
            """)
            conn.commit()
    return jsonify({"status":"ok","detail":"table created"})


@app.route("/add", methods=["POST"])
def add_note():
    data = request.json or {}
    msg = data.get("message", "default message")
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO notes (message) VALUES (%s)", (msg,))
            conn.commit()
            inserted_id = cur.lastrowid
    return jsonify({"status":"ok","id": inserted_id, "message": msg})


@app.route("/notes")
def list_notes():
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, message FROM notes")
            rows = cur.fetchall()
    return jsonify(rows)
