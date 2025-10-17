from flask import Flask, request, jsonify
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env file

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")  # Get API key

# -----------------------------
# Helper: Connect to Database
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------
# Middleware: Verify API Key
# -----------------------------
def check_api_key(req):
    key = req.headers.get('x-api-key')
    return key == API_KEY

# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def home():
    return jsonify({"message": "Welcome to My Secure SQLite3 API"}), 200

@app.route('/students', methods=['GET'])
def get_students():
    if not check_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()

    data = [dict(row) for row in students]
    return jsonify(data), 200

@app.route('/add_student', methods=['POST'])
def add_student():
    if not check_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    course = data.get('course')

    conn = get_db_connection()
    conn.execute('INSERT INTO students (name, age, course) VALUES (?, ?, ?)', (name, age, course))
    conn.commit()
    conn.close()

    return jsonify({"message": "✅ Student added successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
