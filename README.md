# Peer Project Collaboration Platform

**Developer:** Syed Irfan Raza  
**Track:** Intermediate Track - ZeroToShip Summer Activity 2026  
**Domain:** Database Management System  

---

## 📖 Overview
The **Peer Project Collaboration Platform** is a centralized digital workspace designed to connect university students across engineering and computing departments. It acts as a talent-matching ecosystem where creators can post project ideas, specify required technical skills, and allow peers to instantly apply, solving the campus collaboration gap.

## 🛠️ Technology Stack
* **Backend Engine:** Python, Flask, RESTful API
* **Database:** SQLite3
* **Security:** Werkzeug (Password Cryptography), Flask Sessions

---

## 🚀 Project Progression

### Phase 1: Database Architecture
Established the foundational relational database schemas using SQLite.
* **Users Table:** Stores user profiles, department information, and technical skills.
* **Projects Table:** Stores project postings, descriptions, required skill tags, and tracks open/closed status. 
* **Applications Table:** A bridge table linking applicants (Users) to specific Projects.

### Phase 2: Endpoint Architectures & Security
Integrated the static database with a dynamic backend, focusing on secure authentication and route authorization.
* **Authentication Engine:** Built functional `/register`, `/login`, and `/logout` endpoints.
* **Password Cryptography:** Implemented `werkzeug.security` to hash all user passwords before database insertion.
* **Data Integrity Guards:** Created a custom `@login_required` decorator ensuring only the original creator of a project has the authority to edit or modify it.

### Phase 3: RESTful API Routing & Data Filtering
Developed the headless API routing points to enable seamless frontend-backend communication.
* **CRUD API Handlers:** Engineered HTTP endpoints (`POST`, `GET`, `DELETE`) for the `/api/projects` route to create, read, and manage project postings.
* **Skill Search Routing:** Built parameterized filtering capabilities (e.g., `GET /api/projects?skill=Flask`) to scan the database and instantly return tailored project matches.
* **Application Queues:** Created the `/api/apply` handler that safely logs student application entries directly into the database's bridge table.

---

## 📂 Repository Structure
```text
.
├── app.py             # Main Flask backend engine, security guards, and API routes
├── init_db.py         # Python script to initialize the SQLite database
├── db_setup.sql       # SQL Data Definition Language (DDL) for tables
├── README.md          # Project documentation
└── .gitignore         # Configured for Python/Flask environments