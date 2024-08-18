
from flask import Flask, render_template, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

db = mysql.connector.connect(
  host=os.getenv("mysqlhostname"),
  user="mysqlusername",
  password="mysqlpassword",
  database="mysqldbname"
)

@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT MAX(score) as max_score FROM scores")
    result = cursor.fetchone()
    highest_score = result['max_score'] if result['max_score'] else 0
    return render_template('page1.html', best_score=highest_score)

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    score = calculate_score(request.form)

    cursor = db.cursor()
    cursor.execute("INSERT INTO scores (username, score) VALUES (%s, %s)", (username, score))
    db.commit()

    return jsonify({'score': score})

def calculate_score(data):

    # Define the correct answers
    correct_answers = {
        'question1': 'c',
        'question2': 'b',
        'question3': 'b',
    }

    # Initialize the score
    score = 0
    total_questions = len(correct_answers)

    # Check the answers
    for question, correct_answer in correct_answers.items():
        if data.get(question) == correct_answer:
            score += 1

    # Calculate the score as a percentage
    score_percentage = (score / total_questions) * 100

    return score_percentage

if __name__ == '__main__':
    app.run(debug=True)