from flask import Flask, render_template, request, redirect, session
import sqlite3
import pandas as pd

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

# Database initialization (optional for login system)
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

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        return redirect('/main')
    return render_template('login.html')

@app.route('/main')
def main_page():
    return render_template('main.html', symptoms=sorted_symptoms)

@app.route('/predict', methods=['POST'])
def predict():
    selected_symptoms = [s.strip().lower() for s in request.form.getlist('symptoms')]

    predicted_disease = None
    treatment = None

    for _, row in df.iterrows():
        disease_symptoms = [s.strip().lower() for s in str(row['Symptoms']).split(',')]
        match_count = len(set(selected_symptoms) & set(disease_symptoms))
        if match_count >= 1:  # Match at least 2 symptoms
            predicted_disease = row['Name']
            treatment = row['Treatments']
            break

    return render_template('main.html',
                           symptoms=sorted_symptoms,
                           prediction=predicted_disease,
                           treatment=treatment)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
