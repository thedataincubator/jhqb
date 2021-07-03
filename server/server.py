from flask import Flask, json, request

from store import QuestionsStore

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return tuple(obj)
        return super().default(obj)

Flask.json_encoder = SetEncoder

app = Flask(__name__)
questions_store = QuestionsStore()

@app.route('/')
def index():
    return "Hello"

@app.route('/questions', methods=['GET'])
def questions():
    return json.jsonify(questions_store.get_questions())

@app.route('/question', methods=['POST'])
def question():
    qid = request.data.get('qid')
    user = request.data.get('user')
    if not qid or not user:
        return "Error", 400
    questions_store.add_vote(qid, user)
    return "OK"

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    questions_store.add_question("What?", "me")
    questions_store.add_question("Huh?", "you")
    app.run(port=8000, debug=True)
