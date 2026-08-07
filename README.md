# Peer Project Collaboration Platform - Final Build 🚀

**Developer:** Syed Irfan Raza  
**Track:** Intermediate Track - ZeroToShip Summer Activity 2026  
**Domain:** Database Management System  

## 📖 Project Overview
The Peer Project Collaboration Platform is a fully integrated digital workspace designed to connect university students across departments. It operates as a full-stack web application featuring secure user authentication, a live marketplace to discover open roles based on required skills, and a creator dashboard to manage incoming applications.

## 🛠️ Technology Stack
* **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript (Fetch API)
* **Backend:** Python, Flask REST API
* **Database & Auth:** SQLite3, Werkzeug Cryptography, Flask Sessions

## 🚀 How to Run Locally
1. Clone the repository and navigate into the folder.
2. Activate your virtual environment: `.\venv\Scripts\activate` (Windows).
3. Install dependencies: `pip install Flask werkzeug`.
4. Run the database initialization: `py init_db.py`.
5. Start the backend server: `py app.py`.
6. Open your browser and navigate to `http://127.0.0.1:5000` to interact with the live application.

## 🧪 Testing the Application (End-to-End)
* **Register/Login:** Users must be registered directly in the DB or via a tool like Postman. Use the "Quick Login" button in the UI navbar to establish an active browser session.
* **Skill Filtering:** Type "Python" or "React" into the Discovery Marketplace search bar to execute dynamic `GET` database filtering in real-time.
* **Applying:** Click "Apply Now" on any card to fire a `POST` request to the database queue. 
* **Managing:** Navigate to "My Dashboard" to execute an authenticated `GET` pull of live applications and test the Accept/Deny `PUT` hooks.