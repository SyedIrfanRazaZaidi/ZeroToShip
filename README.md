# Peer Project Collaboration Platform

**Developer:** Syed Irfan Raza  
**Track:** Intermediate Track - ZeroToShip Summer Activity 2026  
**Domain:** Database Management System  

---

## 📖 Overview
The **Peer Project Collaboration Platform** is a centralized digital workspace designed to connect university students across engineering and computing departments. It acts as a talent-matching ecosystem where creators can post project ideas, specify required technical skills, and allow peers to instantly apply, solving the campus collaboration gap.

## 🛠️ Technology Stack
* **Backend Engine:** Python, Flask
* **Database:** SQLite3
* **Security:** Werkzeug (Password Cryptography), Flask Sessions

---

## 🚀 Project Progression

### Phase 1: Database Architecture
Established the foundational relational database schemas using SQLite.
* **Users Table:** Stores user profiles, department information, and technical skills (comma-separated arrays).
* **Projects Table:** Stores project postings, descriptions, required skill tags, and tracks open/closed status. Linked to the Users table via a `creator_id` foreign key.
* **Applications Table:** A bridge table linking applicants (Users) to specific Projects, tracking the application status (Pending, Approved, Rejected).

### Phase 2: Endpoint Architectures & Security
Integrated the static database with a dynamic Python Flask backend, focusing on secure authentication and route authorization.
* **Authentication Engine:** Built functional `/register`, `/login`, and `/logout` API endpoints.
* **Password Cryptography:** Implemented `werkzeug.security` to hash all user passwords before database insertion, completely preventing plaintext credential storage.
* **Data Integrity Guards:** Created a custom `@login_required` decorator and implemented strict session-based verification. Ensures only the original creator of a project has the authority to edit or modify it via the `/project/<id>/edit` route.

---

## 📂 Repository Structure
```text
.
├── app.py             # Main Flask backend server and API routes
├── init_db.py         # Python script to initialize the SQLite database
├── db_setup.sql       # SQL Data Definition Language (DDL) for tables
├── README.md          # Project documentation
└── .gitignore         # Configured for Python/Flask environments