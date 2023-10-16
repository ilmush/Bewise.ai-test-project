import os
from datetime import datetime

import psycopg2
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://quiz_user:pass@database/quiz_db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text_question = db.Column(db.String(80), unique=True)
    text_answer = db.Column(db.String(80))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, text_question, text_answer, created_at):
        self.text_question = text_question
        self.text_answer = text_answer
        self.created_at = created_at

    def __repr__(self):
        return f"<Question {self.text_question}>"


@app.route('/questions', methods=['POST', 'GET'])
def request_questions():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_question = Question(text_question=data['text_question'],
                                    text_answer=data['text_answer'],
                                    created_at=data['created_at'])
            db.session.add(new_question)
            db.session.commit()
            return {"message": f"question {new_question.text_question} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        obj = db.session.query(Question).order_by(Question.id.desc()).first()
        if obj:
            results = {
                "text_question": obj.text_question,
                "text_answer": obj.text_answer,
                "created_at": obj.created_at
            }

            return {"question": results}
        return "No objects"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)
