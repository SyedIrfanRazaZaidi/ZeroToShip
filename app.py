from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps

app = Flask(__name__)
# Secret key is required to safely encrypt login cookies
app.secret_key = 'super_secret_cis_key_2026' 

def get_db_connection():
    conn = sqlite3.connect('app.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------------------
# DATA INTEGRITY GUARD (Security Check)
# -----------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized. Please log in."}), 401
        return f(*args, **kwargs)
    return decorated_function

# -----------------------------------------
# AUTHENTICATION ROUTES
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

    # SECURITY: Encrypt the password before saving it
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

    # SECURITY: Compare the typed password with the stored hash
    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['user_id']
        return jsonify({"message": "Login successful!"}), 200
    
    return jsonify({"error": "Invalid email or password"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200

# -----------------------------------------
# SECURE PROJECT ROUTE
# -----------------------------------------
@app.route('/project/<int:project_id>/edit', methods=['PUT'])
@login_required # This enforces the data integrity guard
def edit_project(project_id):
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM Projects WHERE project_id = ?', (project_id,)).fetchone()

    if not project:
        conn.close()
        return jsonify({"error": "Project not found"}), 404

    # DATA INTEGRITY GUARD: Ensure the logged-in user actually owns this project
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

if __name__ == '__main__':
    app.run(debug=True)