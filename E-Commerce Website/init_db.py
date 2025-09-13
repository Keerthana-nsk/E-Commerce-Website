import sqlite3

# Load SQL schema from schema.sql file
with open('schema.sql', 'r') as f:
    schema = f.read()

# Create the database
conn = sqlite3.connect('database.db')
conn.executescript(schema)  # This creates the users and products tables
conn.commit()
conn.close()

print("Database initialized successfully.")
