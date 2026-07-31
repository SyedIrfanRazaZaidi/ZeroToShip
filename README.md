# Peer Project Collaboration Platform

**Developer:** Syed Irfan Raza  
**Track:** Intermediate Track - ZeroToShip Summer Activity 2026  
**Domain:** Database Management System  

---

## 📖 Overview
The **Peer Project Collaboration Platform** is a centralized digital workspace designed to connect university students across engineering and computing departments. It acts as a talent-matching ecosystem where creators can post project ideas, specify required technical skills, and allow peers to instantly apply, solving the campus collaboration gap.

## 🛠️ Technology Stack
* **Frontend UI:** HTML5, Tailwind CSS (Utility-first styling)
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

### Phase 4: Static User Interface (UI)
Developed the frontend presentation layer to establish the platform's visual architecture and user experience.
* **Discovery Marketplace:** Built a responsive CSS Grid layout (`index.html`) featuring project cards with titles, descriptions, and colored skill tag badges.
* **Project Manager Dashboard:** Designed a dedicated creator view (`dashboard.html`) equipped with applicant tracking lists and actionable accept/deny interface assets.

---

## 📂 Repository Structure
```text
.
├── app.py             # Main Flask backend engine, security guards, and API routes
├── init_db.py         # Python script to initialize the SQLite database
├── db_setup.sql       # SQL Data Definition Language (DDL) for tables
├── index.html         # Frontend Marketplace UI (Tailwind CSS)
├── dashboard.html     # Frontend Creator Dashboard UI (Tailwind CSS)
├── README.md          # Project documentation
└── .gitignore         # Configured for Python/Flask environments