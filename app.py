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

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#Database format creation
subjects = [
    {"id": 1, "name": "Math", "chapters": [
        {"id": 1, "name": "Algebra", "quizzes": [{"id": 1, "name": "Quiz 1"}, {"id": 2, "name": "Quiz 2"}]},
        {"id": 2, "name": "Geometry", "quizzes": [{"id": 3, "name": "Quiz 1"}]}
    ]},
    {"id": 2, "name": "Science", "chapters": [
        {"id": 3, "name": "Physics", "quizzes": [{"id": 4, "name": "Quiz 1"}]}
    ]}
]





# Admin Dashboard
@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html', subjects=subjects)




# User Dashboard
@app.route('/')
def user_dashboard():
    return render_template('index.html', subjects=subjects)




# Quiz Attempt
@app.route('/quiz/<int:quiz_id>')
def attempt_quiz(quiz_id):
    return render_template('quiz.html', quiz_id=quiz_id)





    

# Sample data storage (replace with database in next phase)
scores = []

# Submit Quiz Route (handles score calculation and storage)
@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    quiz_id = request.form.get('quiz_id')
    score = 0

    # Sample scoring logic (replace with real question check logic later)
    if request.form.get('q1') == '4':
        score += 1

    # Store the score
    scores.append({"quiz_id": quiz_id, "score": score})
    return redirect(url_for('view_results'))

# Display past scores for users
@app.route('/results')
def view_results():
    return render_template('results.html', scores=scores)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)


# Admin search (search subjects or quizzes)
@app.route('/admin/search', methods=['GET'])
def admin_search():
    query = request.args.get('query', '').lower()
    results = []

    for subject in subjects:
        if query in subject['name'].lower():
            results.append(f"Subject: {subject['name']}")

        for chapter in subject['chapters']:
            for quiz in chapter['quizzes']:
                if query in quiz['name'].lower():
                    results.append(f"Quiz: {quiz['name']}")

    return render_template('admin_search.html', results=results)

# User search (search subjects or quizzes)
@app.route('/search', methods=['GET'])
def user_search():
    query = request.args.get('query', '').lower()
    results = []

    for subject in subjects:
        if query in subject['name'].lower():
            results.append(f"Subject: {subject['name']}")

        for chapter in subject['chapters']:
            for quiz in chapter['quizzes']:
                if query in quiz['name'].lower():
                    results.append(f"Quiz: {quiz['name']}")

    return render_template('search.html', results=results)
