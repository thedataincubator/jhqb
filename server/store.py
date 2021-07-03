from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
import uuid

def with_question(func):
    @wraps(func)
    def decorated(self, qid, *args, **kw):
        try:
            q = self._questions[qid]
        except KeyError:
            return False
        func(self, q, *args, **kw)
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
    def __init__(self):
        self._questions = dict()

    def add_question(self, text, creator):
        q = Question(text, creator)
        self._questions[q.id] = q
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
