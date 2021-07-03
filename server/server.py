from flask import Flask, json, request
from functools import wraps

from store import QuestionsStore

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return tuple(obj)
        return super().default(obj)

Flask.json_encoder = SetEncoder

app = Flask(__name__)
questions_store = QuestionsStore()

def authenticated(func):
    """This will hook into the JH auth, returning an error if not logged in."""
    @wraps(func)
    def decorated(*args, **kw):
        return func({'name': 'me@example.com', 'admin': False}, *args, **kw)
    return decorated

@app.route('/')
def index():
    return "Hello"

@app.route('/questions', methods=['GET'])
@authenticated
def questions(user):
    return json.jsonify(questions_store.get_questions())

@app.route('/question', methods=['POST'])
@authenticated
def question(user):
    text = request.get_json().get('question')
    if not text:
        return "Error", 400
    q = questions_store.add_question(text, user['name'])
    return q.id

@app.route('/vote', methods=['POST'])
@authenticated
def vote(user):
    qid = request.form.get('qid')
    if not qid:
        return "Error", 400
    questions_store.add_vote(qid, user['name'])
    return "OK"

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

if __name__ == '__main__':
    questions_store.add_question("What?", "me")
    questions_store.add_question("Huh?", "you")
    app.run(port=8000, debug=True)
