from flask import Flask, request

from store import QuestionsStore

app = Flask(__name__)
questions_store = QuestionsStore()

@app.route('/')
def index():
    return "Hello"

@app.route('/questions', methods=['GET'])
def questions():
    return questions_store.get_questions_json()

@app.route('/question', methods=['POST'])
def question():
    qid = request.data.get('qid')
    user = request.data.get('user')
    if not qid or not user:
        return "Error", 400
    questions_store.add_vote(qid, user)
    return "OK"

if __name__ == '__main__':
    questions_store.add_question("What?", "me")
    questions_store.add_question("Huh?", "you")
    app.run(port=8000, debug=True)
