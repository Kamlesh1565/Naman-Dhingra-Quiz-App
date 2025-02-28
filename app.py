from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS Subject (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS Chapter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER,
            name TEXT NOT NULL,
            FOREIGN KEY (subject_id) REFERENCES Subject(id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS Quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_id INTEGER,
            title TEXT NOT NULL,
            duration INTEGER,
            FOREIGN KEY (chapter_id) REFERENCES Chapter(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
#Creating a router
#Home Page
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Subject')
    subjects = c.fetchall()
    conn.close()
    return render_template('index.html', subjects=subjects)

#ADMIN
@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Fetch subjects, chapters, and quizzes
    c.execute('SELECT * FROM Subject')
    subjects = c.fetchall()
    
    chapters = {}
    quizzes = {}
    for subject in subjects:
        c.execute('SELECT * FROM Chapter WHERE subject_id = ?', (subject[0],))
        chapters[subject[0]] = c.fetchall()
        for chapter in chapters[subject[0]]:
            c.execute('SELECT * FROM Quiz WHERE chapter_id = ?', (chapter[0],))
            quizzes[chapter[0]] = c.fetchall()
    
    conn.close()
    return render_template('admin.html', subjects=subjects, chapters=chapters, quizzes=quizzes)

# Add Subject
@app.route('/add_subject', methods=['POST'])
def add_subject():
    name = request.form['name']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO Subject (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

# Add Chapter
@app.route('/add_chapter/<int:subject_id>', methods=['POST'])
def add_chapter(subject_id):
    name = request.form['name']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO Chapter (subject_id, name) VALUES (?, ?)', (subject_id, name))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

# Add Quiz
@app.route('/add_quiz/<int:chapter_id>', methods=['POST'])
def add_quiz(chapter_id):
    title = request.form['title']
    duration = request.form['duration']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO Quiz (chapter_id, title, duration) VALUES (?, ?, ?)', (chapter_id, title, duration))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
