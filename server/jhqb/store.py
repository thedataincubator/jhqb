from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
from pathlib import Path
import pickle
import uuid

QUESTION_LIMIT = 2048

def with_question(func):
    @wraps(func)
    def decorated(self, qid, *args, **kw):
        try:
            q = self._questions[qid]
        except KeyError:
            return False
        func(self, q, *args, **kw)
        self._dump(q)
        return True
    return decorated


@dataclass
class Question:
    text: str
    creator: str
    votes: set[str] = field(default_factory=set)
    created: datetime = field(default_factory=datetime.utcnow)
    closed: bool = False
    id: str = field(default_factory=lambda: uuid.uuid4().hex)


class QuestionsStore:
    def __init__(self, store_path):
        self._questions = dict()
        self.path = Path(store_path) / 'jhqb_store'
        self.path.mkdir(exist_ok=True)
        for fn in self.path.iterdir():
            with open(fn, 'rb') as f:
                q = pickle.load(f)
                self._questions[q.id] = q

    def _dump(self, q):
        with open(self.path / q.id, 'wb') as f:
            pickle.dump(q, f)

    def add_question(self, text, creator):
        q = Question(text[:QUESTION_LIMIT], creator)
        self._questions[q.id] = q
        self._dump(q)
        return q

    def get_questions(self):
        return list(self._questions.values())

    def get_question(self, qid):
        return self._questions.get(qid)

    @with_question
    def add_vote(self, q, voter):
        q.votes.add(voter)

    @with_question
    def remove_vote(self, q, voter):
        q.votes.discard(voter)

    @with_question
    def close(self, q):
        q.closed = True

    @with_question
    def open(self, q):
        q.closed = False
