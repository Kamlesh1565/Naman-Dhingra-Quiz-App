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

#setting up the app
# Milestone 2: Authentication and Role Management
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return "Welcome to Quiz Master!" 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('quiz_master.db')
        c = conn.cursor()
        c.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user'] = user[1]
            session['role'] = user[3]
            if user[3] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            return "Invalid credentials!"
    return render_template('login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') == 'admin':
        return "Welcome to Admin Dashboard!"
    return redirect(url_for('login'))

@app.route('/user_dashboard')
def user_dashboard():
    if session.get('role') == 'user':
        return "Welcome to User Dashboard!"
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


#ADMIN
@app.route('/admin/subjects')
def admin_subjects():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Subject")
    subjects = c.fetchall()
    conn.close()
    return render_template('admin_subjects.html', subjects=subjects)

#Add a subject
@app.route('/admin/subjects/add', methods=['GET', 'POST'])
def add_subject():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        conn = sqlite3.connect('quiz_master.db')
        c = conn.cursor()
        c.execute("INSERT INTO Subject (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_subjects'))
    return render_template('add_subject.html')

#Edit a subject
@app.route('/admin/subjects/edit/<int:id>', methods=['GET', 'POST'])
def edit_subject(id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    if request.method == 'POST':
        new_name = request.form['name']
        c.execute("UPDATE Subject SET name = ? WHERE id = ?", (new_name, id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_subjects'))
    c.execute("SELECT * FROM Subject WHERE id = ?", (id,))
    subject = c.fetchone()
    conn.close()
    return render_template('edit_subject.html', subject=subject)

#Delete a subject
@app.route('/admin/subjects/delete/<int:id>')
def delete_subject(id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    c.execute("DELETE FROM Subject WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_subjects'))

