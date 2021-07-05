from flask import Flask, json, render_template, request
from functools import wraps
from jupyterhub.services.auth import HubAuth
import os

from store import QuestionsStore

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return tuple(obj)
        return super().default(obj)

Flask.json_encoder = SetEncoder

prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX', '/')
auth = HubAuth(api_token=os.environ['JUPYTERHUB_API_TOKEN'],
               api_url=os.environ['JUPYTERHUB_API_URL'],
               cache_max_age=60)

app = Flask(__name__,
            template_folder='../client/templates',
            static_folder='../client/public', static_url_path=prefix)
questions_store = QuestionsStore()

def route(path, *args, **kw):
    return app.route(prefix + path, *args, **kw)

def authenticated(func):
    """This will hook into the JH auth, returning an error if not logged in."""
    @wraps(func)
    def decorated(*args, **kw):
        cookie = request.cookies.get(auth.cookie_name)
        if cookie:
            user = auth.user_for_cookie(cookie)
            if user:
                return func(user, *args, **kw)
        return "Permission Denied", 403
    return decorated

@route('')
@authenticated
def index(user):
    return render_template('index.html', name=user['name'],
                           admin=user['admin'], prefix=prefix)

@route('questions', methods=['GET'])
@authenticated
def questions(user):
    return json.jsonify(questions_store.get_questions())

@route('question', methods=['POST'])
@authenticated
def question(user):
    text = request.get_json().get('question')
    if not text:
        return "Error", 400
    q = questions_store.add_question(text, user['name'])
    return q.id

@route('vote/<qid>/+', methods=['POST'])
@authenticated
def vote_p(user, qid):
    if questions_store.add_vote(qid, user['name']):
        return "OK"
    return "Error", 500

@route('vote/<qid>/-', methods=['POST'])
@authenticated
def vote_m(user, qid):
    if questions_store.remove_vote(qid, user['name']):
        return "OK"
    return "Error", 500

@route('close/<qid>', methods=['POST'])
@authenticated
def close(user, qid):
    q = questions_store.get_question(qid)
    if q and (q.creator == user['name'] or user['admin']):
        questions_store.close(qid)
        return "OK"
    return "Permission Denied", 403

@route('open/<qid>', methods=['POST'])
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
