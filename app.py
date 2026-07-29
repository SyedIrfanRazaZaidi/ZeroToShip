from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_cis_key_2026' 

def get_db_connection():
    conn = sqlite3.connect('app.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------------------
# DATA INTEGRITY GUARD (From Phase 2)
# -----------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized. Please log in."}), 401
        return f(*args, **kwargs)
    return decorated_function

# -----------------------------------------
# AUTHENTICATION ROUTES (From Phase 2)
# -----------------------------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    department = data.get('department')
    skills = data.get('skills', '')

    if not all([name, email, password, department]):
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO Users (name, email, password_hash, department, skills) VALUES (?, ?, ?, ?, ?)',
            (name, email, hashed_password, department, skills)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409
    finally:
        conn.close()

    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE email = ?', (email,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['user_id']
        return jsonify({"message": "Login successful!"}), 200
    
    return jsonify({"error": "Invalid email or password"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/project/<int:project_id>/edit', methods=['PUT'])
@login_required 
def edit_project(project_id):
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM Projects WHERE project_id = ?', (project_id,)).fetchone()

    if not project:
        conn.close()
        return jsonify({"error": "Project not found"}), 404

    if project['creator_id'] != session['user_id']:
        conn.close()
        return jsonify({"error": "Forbidden: You can only edit your own projects"}), 403

    data = request.get_json()
    new_title = data.get('title', project['title'])
    
    conn.execute(
        'UPDATE Projects SET title = ? WHERE project_id = ?',
        (new_title, project_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Project updated successfully!"}), 200


# =========================================
# NEW PHASE 3 ROUTES BELOW
# =========================================

# 1. CRUD API & SKILL SEARCH ROUTING
@app.route('/api/projects', methods=['GET', 'POST'])
def handle_projects():
    conn = get_db_connection()
    
    # CREATE A PROJECT (Requires Login)
    if request.method == 'POST':
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized. Please log in."}), 401
            
        data = request.get_json()
        title = data.get('title')
        description = data.get('description', '')
        required_skills = data.get('required_skills', '')
        
        if not title:
            return jsonify({"error": "Project title is required"}), 400
            
        conn.execute(
            'INSERT INTO Projects (title, description, required_skills, creator_id) VALUES (?, ?, ?, ?)',
            (title, description, required_skills, session['user_id'])
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Project created successfully!"}), 201

    # READ PROJECTS & SKILL SEARCH
    if request.method == 'GET':
        skill_filter = request.args.get('skill')
        
        if skill_filter:
            # Searches for projects containing the requested skill tag
            projects = conn.execute(
                'SELECT * FROM Projects WHERE required_skills LIKE ?', 
                ('%' + skill_filter + '%',)
            ).fetchall()
        else:
            # Returns all projects if no filter is applied
            projects = conn.execute('SELECT * FROM Projects').fetchall()
            
        conn.close()
        # Convert database rows to JSON dictionaries
        projects_list = [dict(p) for p in projects]
        return jsonify(projects_list), 200

# DELETE A PROJECT
@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM Projects WHERE project_id = ?', (project_id,)).fetchone()
    
    if not project:
        conn.close()
        return jsonify({"error": "Project not found"}), 404
        
    # DATA INTEGRITY GUARD: Ensures users can only delete their own projects
    if project['creator_id'] != session['user_id']:
        conn.close()
        return jsonify({"error": "Forbidden: You can only delete your own projects"}), 403
        
    conn.execute('DELETE FROM Projects WHERE project_id = ?', (project_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Project deleted successfully!"}), 200


# 2. APPLICATION HANDLER
@app.route('/api/apply', methods=['POST'])
@login_required
def apply_project():
    data = request.get_json()
    project_id = data.get('project_id')
    
    if not project_id:
        return jsonify({"error": "project_id is required"}), 400
        
    conn = get_db_connection()
    try:
        # Logs the application into the database queue with a default 'Pending' status
        conn.execute(
            'INSERT INTO Applications (project_id, applicant_id, status) VALUES (?, ?, ?)',
            (project_id, session['user_id'], 'Pending')
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Database error or application already exists"}), 400
        
    conn.close()
    return jsonify({"message": "Application submitted successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True)