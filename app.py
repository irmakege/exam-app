from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Define the correct answers
correct_answers = {
    'question1': 'c',  
    'question2': 'b', 
    'question3': 'b',  
}

@app.route('/')
def quiz():
    return render_template('page1.html')

@app.route('/submit', methods=['POST'])
def submit_exam():
    data = request.form

    # Initialize the score
    score = 0
    total_questions = len(correct_answers)

    # Check the answers
    for question, correct_answer in correct_answers.items():
        if data.get(question) == correct_answer:
            score += 1

    # Calculate the score as a percentage
    score_percentage = (score / total_questions) * 100

    return jsonify({'score': score_percentage})

if __name__ == '__main__':
    app.run(debug=True)