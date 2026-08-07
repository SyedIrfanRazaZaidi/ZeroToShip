# CIS Hub: Peer Project Collaboration Platform 🚀

**Developer:** Syed Irfan Raza 
**Institution:** NED University of Engineering & Technology  
**Track:** Intermediate Track - ZeroToShip Summer Activity 2026  

## 📖 Project Overview
The CIS Hub (Peer Project Collaboration Platform) is a full-stack digital workspace designed to eliminate departmental silos on university campuses. It connects students who have innovative project ideas with peers who possess the specific technical skills needed to build them. This platform democratizes access to student talent, allowing users to effortlessly search for roles, apply for projects, and assemble cross-functional teams for real-world development.

## 🏗️ Development Phases
This project was developed incrementally through a 5-phase structured approach:

* **Phase 1: Database Architecture:** Designed and implemented a relational database using SQLite3, establishing secure tables for Users, Projects, and Applications with proper foreign key relationships.
* **Phase 2: Secure Authentication:** Built the backend registration and login systems utilizing Flask sessions and Werkzeug cryptography to ensure all user passwords are securely hashed and salted.
* **Phase 3: Core API Development:** Engineered RESTful API routes in Python/Flask to handle backend logic, including project creation, application processing, and a dynamic query system for skill-based filtering.
* **Phase 4: Frontend Integration:** Developed a responsive UI using Tailwind CSS and connected it to the backend APIs using Vanilla JavaScript and the Fetch API, bringing the Discovery Marketplace to life.
* **Phase 5: Polish & Dashboard:** Implemented the Creator Dashboard for project managers to accept/deny applicants, upgraded the UI with modern modals and toast notifications, and added professional typography (Inter).

## 🛠️ Technology Stack
* **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript (Fetch API)
* **Backend:** Python, Flask RESTful API
* **Database & Security:** SQLite3, Werkzeug Security, Flask Sessions
* **Styling:** Custom UI Modals, Toast Notifications, and Inter typography

## ✨ Core Features
1. **Secure Authentication:** Complete user registration and login system with encrypted passwords and session state management.
2. **Discovery Marketplace:** A dynamic grid where project creators can publish open roles with required skill tags.
3. **Real-Time Skill Filtering:** A search engine that instantly filters marketplace projects based on specific tech stack keywords (e.g., Python, React, UI/UX).
4. **Application System:** One-click applications that securely send peer requests directly to the project creator.
5. **Creator Dashboard:** A dedicated management panel where project visionaries can review, approve, or reject incoming talent applications.

---

## 🚀 How to Run Locally

### Prerequisites
* Python 3.x installed
* A virtual environment set up (`venv`)

### Installation & Execution Commands

**1. Clone the repository and open your terminal in the project folder.**

**2. Activate your virtual environment:**
```bash
.\venv\Scripts\activate
```

**3. Install the required backend libraries:**
```bash
pip install Flask werkzeug
```

**4. Initialize the database:** 
*(This creates `app.sqlite3` and injects professional seed data)*
```bash
py init_db.py
```

**5. Start the Flask development server:**
```bash
py app.py
```

**6. View the Platform:**
Open your web browser and navigate to: **`http://127.0.0.1:5000`**

### 🧪 Testing the Platform
* **Login as Admin:** Use `admin@cis.edu.pk` with the password `admin123` to access the pre-seeded admin account and view the dashboard.
* **Test the Flow:** Click "Register" to create a new user profile, then test the "Add Project" and "Apply for Role" workflows.