#Quiz App

import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()
#Database Connected
# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS User (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT CHECK(role IN ('admin', 'user')) NOT NULL
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS Subject (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS Chapter (
                id INTEGER PRIMARY KEY,
                subject_id INTEGER,
                name TEXT NOT NULL,
                FOREIGN KEY(subject_id) REFERENCES Subject(id)
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS Quiz (
                id INTEGER PRIMARY KEY,
                chapter_id INTEGER,
                title TEXT NOT NULL,
                duration INTEGER,
                FOREIGN KEY(chapter_id) REFERENCES Chapter(id)
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS Question (
                id INTEGER PRIMARY KEY,
                quiz_id INTEGER,
                question_text TEXT NOT NULL,
                correct_option TEXT NOT NULL,
                FOREIGN KEY(quiz_id) REFERENCES Quiz(id)
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS Score (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                quiz_id INTEGER,
                score INTEGER,
                FOREIGN KEY(user_id) REFERENCES User(id),
                FOREIGN KEY(quiz_id) REFERENCES Quiz(id)
            )''')

conn.commit()
conn.close()

print("Database schema created successfully.")

