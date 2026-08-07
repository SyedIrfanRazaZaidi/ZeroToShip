from flask import Flask, request, jsonify, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps
import os

app = Flask(__name__, template_folder=os.path.abspath('.'))
app.secret_key = 'super_secret_professional_key_2026'

def get_db_connection():
    conn = sqlite3.connect('app.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized. Please log in to perform this action."}), 401
        return f(*args, **kwargs)
    return decorated_function

# =========================================
# PHASE 4/5: UI SERVING ROUTES
# =========================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

# =========================================
# PHASE 2: AUTHENTICATION ROUTES
# =========================================
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # Compulsory field backend validation
    if not all([data.get('name'), data.get('email'), data.get('password'), data.get('department'), data.get('skills')]):
        return jsonify({"error": "All fields are compulsory."}), 400

    try:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO Users (name, email, password_hash, department, skills) VALUES (?, ?, ?, ?, ?)',
            (data['name'], data['email'], generate_password_hash(data['password']), data['department'], data['skills'])
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Account created! You can now log in."}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "An account with this email already exists."}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE email = ?', (data.get('email'),)).fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], data.get('password')):
        session['user_id'] = user['user_id']
        session['name'] = user['name']
        return jsonify({"message": f"Welcome back, {user['name']}!"}), 200
    return jsonify({"error": "Invalid email or password."}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully."})

@app.route('/api/me', methods=['GET'])
def get_current_user():
    if 'user_id' in session:
        return jsonify({"logged_in": True, "name": session['name']})
    return jsonify({"logged_in": False})

# =========================================
# PHASE 3: CRUD & SEARCH ROUTES
# =========================================
@app.route('/api/projects', methods=['GET', 'POST'])
def handle_projects():
    conn = get_db_connection()
    if request.method == 'POST':
        if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
        data = request.get_json()
        
        # Compulsory field backend validation
        if not all([data.get('title'), data.get('description'), data.get('required_skills')]):
            return jsonify({"error": "Project title, description, and skills are compulsory."}), 400

        conn.execute('INSERT INTO Projects (title, description, required_skills, creator_id) VALUES (?, ?, ?, ?)',
                     (data['title'], data['description'], data['required_skills'], session['user_id']))
        conn.commit()
        conn.close()
        return jsonify({"message": "Project successfully published to the marketplace!"}), 201

    # GET Route with Filtering
    skill_filter = request.args.get('skill')
    if skill_filter:
        projects = conn.execute('''
            SELECT p.*, u.name as creator_name FROM Projects p 
            JOIN Users u ON p.creator_id = u.user_id 
            WHERE p.required_skills LIKE ? ORDER BY p.project_id DESC
        ''', ('%' + skill_filter + '%',)).fetchall()
    else:
        projects = conn.execute('''
            SELECT p.*, u.name as creator_name FROM Projects p 
            JOIN Users u ON p.creator_id = u.user_id 
            ORDER BY p.project_id DESC
        ''').fetchall()
    conn.close()
    return jsonify([dict(p) for p in projects]), 200

@app.route('/api/apply', methods=['POST'])
@login_required
def apply_project():
    data = request.get_json()
    try:
        conn = get_db_connection()
        # Prevent applying to own project
        project = conn.execute('SELECT creator_id FROM Projects WHERE project_id = ?', (data['project_id'],)).fetchone()
        if project['creator_id'] == session['user_id']:
            return jsonify({"error": "You cannot apply to your own project."}), 400
            
        conn.execute('INSERT INTO Applications (project_id, applicant_id, status) VALUES (?, ?, ?)',
                     (data['project_id'], session['user_id'], 'Pending Review'))
        conn.commit()
        conn.close()
        return jsonify({"message": "Application submitted successfully!"}), 201
    except:
        return jsonify({"error": "Database error or application already exists."}), 400

@app.route('/api/dashboard', methods=['GET'])
@login_required
def get_dashboard_data():
    conn = get_db_connection()
    apps = conn.execute('''
        SELECT a.application_id, a.status, u.name, u.department, u.skills, p.title 
        FROM Applications a
        JOIN Users u ON a.applicant_id = u.user_id
        JOIN Projects p ON a.project_id = p.project_id
        WHERE p.creator_id = ?
        ORDER BY a.application_id DESC
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
    return jsonify({"message": f"Application marked as {status}"})

if __name__ == '__main__':
    app.run(debug=True)