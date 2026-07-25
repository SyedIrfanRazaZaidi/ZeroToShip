import sqlite3

# This creates the app.sqlite3 file and runs your Phase 1 SQL commands
connection = sqlite3.connect('app.sqlite3')
with open('db_setup.sql') as f:
    connection.executescript(f.read())
connection.close()
print("Database successfully initialized!")