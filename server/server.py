from flask import Flask, json, render_template, request
from functools import wraps

from store import QuestionsStore

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return tuple(obj)
        return super().default(obj)

Flask.json_encoder = SetEncoder

app = Flask(__name__,
            template_folder='../client/templates',
            static_folder='../client/public', static_url_path='/')
questions_store = QuestionsStore()

def authenticated(func):
    """This will hook into the JH auth, returning an error if not logged in."""
    @wraps(func)
    def decorated(*args, **kw):
        return func({'name': 'me@example.com', 'admin': False}, *args, **kw)
    return decorated

@app.route('/')
@authenticated
def index(user):
    return render_template('index.html', name=user['name'], admin=user['admin'])

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

@app.route('/vote/<qid>/+', methods=['POST'])
@authenticated
def vote_p(user, qid):
    if questions_store.add_vote(qid, user['name']):
        return "OK"
    return "Error", 500

@app.route('/vote/<qid>/-', methods=['POST'])
@authenticated
def vote_m(user, qid):
    if questions_store.remove_vote(qid, user['name']):
        return "OK"
    return "Error", 500

@app.route('/close/<qid>', methods=['POST'])
@authenticated
def close(user, qid):
    q = questions_store.get_question(qid)
    if q and (q.creator == user['name'] or user['admin']):
        questions_store.close(qid)
        return "OK"
    return "Permission Denied", 403

@app.route('/open/<qid>', methods=['POST'])
@authenticated
def open(user, qid):
    q = questions_store.get_question(qid)
    if q and (q.creator == user['name'] or user['admin']):
        questions_store.open(qid)
        return "OK"
    return "Permission Denied", 403

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

if __name__ == '__main__':
    questions_store.add_question("What?", "me")
    questions_store.add_question("Huh?", "you")
    app.run(port=8000, debug=True)
