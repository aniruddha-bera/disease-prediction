from flask import Flask, render_template, request, redirect, session
import sqlite3
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load dataset
df = pd.read_csv('dataset/Diseases_Symptoms.csv')

# Extract unique symptoms
all_symptoms = set()
for symptoms in df['Symptoms']:
    for s in str(symptoms).split(','):
        all_symptoms.add(s.strip().lower())
sorted_symptoms = sorted(all_symptoms)

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ---------- ROUTES ----------
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect('/main')
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup_user():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect('/')
    except sqlite3.IntegrityError:
        return "Username already exists. Try a different one."

@app.route('/main')
def main_page():
    if 'username' not in session:
        return redirect('/')
    return render_template('main.html', symptoms=sorted_symptoms)

@app.route('/predict', methods=['POST'])
def predict():
    selected_symptoms = [s.strip().lower() for s in request.form.getlist('symptoms')]

    predicted_disease = None
    treatment = None

    for _, row in df.iterrows():
        disease_symptoms = [s.strip().lower() for s in str(row['Symptoms']).split(',')]
        match_count = len(set(selected_symptoms) & set(disease_symptoms))
        if match_count >= 1:
            predicted_disease = row['Name']
            treatment = row['Treatments']
            break

    return render_template('main.html',
                           symptoms=sorted_symptoms,
                           prediction=predicted_disease,
                           treatment=treatment)

# ---------- RUN ----------
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
