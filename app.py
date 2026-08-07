from flask import Flask, request, jsonify, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps
import os

# Tell Flask to look for templates in the current directory
app = Flask(__name__, template_folder=os.path.abspath('.'))
app.secret_key = 'super_secret_cis_key_2026' 

def get_db_connection():
    conn = sqlite3.connect('app.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized. Please log in."}), 401
        return f(*args, **kwargs)
    return decorated_function

# =========================================
# UI SERVING ROUTES (PHASE 5)
# =========================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

# =========================================
# AUTHENTICATION ROUTES (PHASE 2)
# =========================================
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO Users (name, email, password_hash, department, skills) VALUES (?, ?, ?, ?, ?)',
            (data['name'], data['email'], generate_password_hash(data['password']), data['department'], data.get('skills', ''))
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "User registered successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE email = ?', (data.get('email'),)).fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], data.get('password')):
        session['user_id'] = user['user_id']
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# =========================================
# CRUD & SEARCH ROUTES (PHASE 3)
# =========================================
@app.route('/api/projects', methods=['GET', 'POST'])
def handle_projects():
    conn = get_db_connection()
    if request.method == 'POST':
        if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
        data = request.get_json()
        conn.execute('INSERT INTO Projects (title, description, required_skills, creator_id) VALUES (?, ?, ?, ?)',
                     (data['title'], data['description'], data['required_skills'], session['user_id']))
        conn.commit()
        conn.close()
        return jsonify({"message": "Project created!"}), 201

    skill_filter = request.args.get('skill')
    if skill_filter:
        projects = conn.execute('SELECT * FROM Projects WHERE required_skills LIKE ?', ('%' + skill_filter + '%',)).fetchall()
    else:
        projects = conn.execute('SELECT * FROM Projects').fetchall()
    conn.close()
    return jsonify([dict(p) for p in projects]), 200

@app.route('/api/apply', methods=['POST'])
@login_required
def apply_project():
    data = request.get_json()
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO Applications (project_id, applicant_id, status) VALUES (?, ?, ?)',
                     (data['project_id'], session['user_id'], 'Pending'))
        conn.commit()
        conn.close()
        return jsonify({"message": "Application submitted successfully!"}), 201
    except:
        return jsonify({"error": "Database error or already applied"}), 400

# =========================================
# DASHBOARD API (PHASE 5)
# =========================================
@app.route('/api/dashboard', methods=['GET'])
@login_required
def get_dashboard_data():
    conn = get_db_connection()
    # Get all applications sent to this creator's projects
    apps = conn.execute('''
        SELECT a.application_id, a.status, u.name, u.department, u.skills, p.title 
        FROM Applications a
        JOIN Users u ON a.applicant_id = u.user_id
        JOIN Projects p ON a.project_id = p.project_id
        WHERE p.creator_id = ?
    ''', (session['user_id'],)).fetchall()
    conn.close()
    return jsonify({"applications": [dict(a) for a in apps]})

@app.route('/api/applications/<int:app_id>', methods=['PUT'])
@login_required
def update_application(app_id):
    status = request.get_json().get('status')
    conn = get_db_connection()
    conn.execute('UPDATE Applications SET status = ? WHERE application_id = ?', (status, app_id))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Application {status}"})

if __name__ == '__main__':
    app.run(debug=True)