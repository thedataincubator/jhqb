from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class Question:
    text: str
    creator: str
    votes: set[str] = field(default_factory=set)
    created: datetime = field(default_factory=datetime.now)
    closed: bool = False
    id: str = field(default_factory=lambda: uuid.uuid4().hex)


class QuestionsStore:
    def __init__(self):
        self._questions = dict()

    def add_question(self, text, creator):
        q = Question(text, creator)
        self._questions[q.id] = q

    def get_questions(self):
        return list(self._questions.values())

    def add_vote(self, qid, voter):
        q = self._questions[qid]
        q.votes.add(voter)

    def remove_vote(self, qid, voter):
        q = self._questions[qid]
        q.votes.remove(voter)
