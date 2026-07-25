# Peer Project Collaboration Platform - Phase 1

**Developer:** Syed Irfan Raza
**Track:** Intermediate Track - ZeroToShip Summer Activity 2026
**Domain:** Database Management System 

## Overview
This repository contains the foundational relational database schemas for the Peer Project Collaboration Platform. The project serves as a digital workspace directory connecting students across campus for engineering and computing projects based on specific technical skill requirements.

## Database Architecture
The backend is designed using SQLite with three core tables:

1. **Users Table:** Stores user profiles, department information, and technical skills (stored as a comma-separated array).
2. **Projects Table:** Stores project postings, descriptions, required skill tags, and tracks open/closed status. Linked to the Users table via a `creator_id` foreign key.
3. **Applications Table:** A bridge table linking applicants (Users) to specific Projects, tracking the application status (Pending, Approved, Rejected).

## Repository Structure
- `db_setup.sql`: Contains the complete SQL data definition language (DDL) for creating the tables and constraints.
- `.gitignore`: Configured for Python/Flask environments and SQLite database exclusions.
- `models/`: Directory established for upcoming Phase 2 ORM models.
## Phase 2: Endpoint Architectures & Security

In Phase 2, the static database was integrated with a dynamic Python Flask backend. The core focus of this phase was establishing secure authentication and route authorization.

**Key Features Implemented:**
*   **Authentication Engine:** Built `/register` and `/login` routes.
*   **Password Cryptography:** Implemented `werkzeug.security` to hash all user passwords before database insertion, preventing plaintext credential storage.
*   **Data Integrity Guards:** Created a custom `@login_required` decorator and implemented session-based verification on the `/project/<id>/edit` route to ensure only the original creator of a project can modify it.