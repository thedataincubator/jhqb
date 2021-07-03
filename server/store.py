from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import uuid

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

    def add_vote(self, qid, voter):
        try:
            q = self._questions[qid]
        except KeyError:
            return False
        q.votes.add(voter)
        return True

    def remove_vote(self, qid, voter):
        try:
            q = self._questions[qid]
        except KeyError:
            return False
        q.votes.remove(voter)
        return True
