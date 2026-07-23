-- 1. Users Table
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    department TEXT NOT NULL,
    skills TEXT 
);

-- 2. Projects Table
CREATE TABLE Projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    creator_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    required_skills TEXT, 
    status TEXT CHECK(status IN ('Open', 'Closed')) DEFAULT 'Open',
    FOREIGN KEY (creator_id) REFERENCES Users(user_id)
);

-- 3. Applications Table
CREATE TABLE Applications (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    applicant_id INTEGER NOT NULL,
    status TEXT CHECK(status IN ('Pending', 'Approved', 'Rejected')) DEFAULT 'Pending',
    FOREIGN KEY (project_id) REFERENCES Projects(project_id),
    FOREIGN KEY (applicant_id) REFERENCES Users(user_id)
);