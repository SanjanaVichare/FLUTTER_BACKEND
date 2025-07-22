from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# PostgreSQL connection string from Render
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def home():
    return "✅ Flask Backend is Running!"

# --- Login API ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    login_id = data.get('login_id')
    password = data.get('password')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, email, role FROM users
        WHERE login_id = %s AND password = %s AND status = 'active'
    """, (login_id, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return jsonify({
            "status": "success",
            "user": {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "role": user[3]
            }
        })
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

# --- Car Search Log Insert ---
@app.route('/api/car_search_log', methods=['POST'])
def insert_car_search_log():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO car_search_logs (emp_id, emp_name, chasis_no, searched_at, location, device_info)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data['emp_id'],
        data['emp_name'],
        data['chasis_no'],
        data['searched_at'],
        data['location'],
        data['device_info']
    ))

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "success", "message": "Search log inserted."})

# --- Get Car Search Logs ---
@app.route('/api/car_search_logs', methods=['GET'])
def get_car_logs():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM car_search_logs ORDER BY searched_at DESC")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()

    logs = [dict(zip(columns, row)) for row in rows]
    return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True)
