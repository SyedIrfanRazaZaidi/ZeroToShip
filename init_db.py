import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    conn = sqlite3.connect('app.sqlite3')
    cursor = conn.cursor()

    # Phase 1: Database Architecture - Reset tables
    cursor.executescript('''
        DROP TABLE IF EXISTS Applications;
        DROP TABLE IF EXISTS Projects;
        DROP TABLE IF EXISTS Users;
    ''')

    # Create Core Tables
    cursor.executescript('''
        CREATE TABLE Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            department TEXT NOT NULL,
            skills TEXT NOT NULL
        );

        CREATE TABLE Projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            required_skills TEXT NOT NULL,
            creator_id INTEGER NOT NULL,
            status TEXT DEFAULT 'Open',
            FOREIGN KEY(creator_id) REFERENCES Users(user_id)
        );

        CREATE TABLE Applications (
            application_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            applicant_id INTEGER NOT NULL,
            status TEXT DEFAULT 'Pending Review',
            FOREIGN KEY(project_id) REFERENCES Projects(project_id),
            FOREIGN KEY(applicant_id) REFERENCES Users(user_id)
        );
    ''')

    # Seed Professional Data
    cursor.execute(
        'INSERT INTO Users (name, email, password_hash, department, skills) VALUES (?, ?, ?, ?, ?)',
        ('Syed Ghufran Raza', 'admin@cis.edu.pk', generate_password_hash('admin123'), 'Computer Science', 'Cybersecurity, Python, Nmap')
    )
    admin_id = cursor.lastrowid

    cursor.execute(
        'INSERT INTO Projects (title, description, required_skills, creator_id) VALUES (?, ?, ?, ?)',
        ('ARMOR Asset Management System', 'Developing a unified platform for digital asset management, risk assessment, and compliance inspection based on NIST RMF guidelines. Need a frontend UI developer to build the dashboard.', 'UI/UX, HTML, Tailwind', admin_id)
    )

    conn.commit()
    conn.close()
    print("Database initialized successfully with professional seed data!")

if __name__ == '__main__':
    init_db()