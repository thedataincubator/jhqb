from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime
import json
import uuid

@dataclass
class Question:
    text: str
    creator: str
    votes: set[str] = field(default_factory=set)
    created: datetime = field(default_factory=datetime.now)
    closed: bool = False
    id: str = field(default_factory=lambda: uuid.uuid4().hex)


class QuestionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return tuple(obj)
        if is_dataclass(obj):
            return asdict(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class QuestionsStore:
    def __init__(self):
        self._questions = dict()

    def add_question(self, text, creator):
        q = Question(text, creator)
        self._questions[q.id] = q

    def get_questions(self):
        return self._questions.values()

    def get_questions_json(self):
        return json.dumps([asdict(q) for q in self.get_questions()], cls=QuestionEncoder)

    def add_vote(self, qid, voter):
        q = self._questions[qid]
        q.votes.add(voter)

    def remove_vote(self, qid, voter):
        q = self._questions[qid]
        q.votes.remove(voter)
