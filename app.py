from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("myslquri")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Scores model
class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.route('/')
def index():
    highest_score = db.session.query(db.func.max(Score.score)).scalar()
    highest_score = highest_score if highest_score is not None else 0
    return render_template('page1.html', best_score=highest_score)

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    score = calculate_score(request.form)

    new_score = Score(username=username, score=int(score))
    db.session.add(new_score)
    db.session.commit()

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
