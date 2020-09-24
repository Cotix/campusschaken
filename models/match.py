import enum
from config import db


class Match(db.Model):
    class Result(enum.Enum):
        DRAW = 0
        WHITE = 1
        BLACK = 2

        @staticmethod
        def from_string(text):
            text = text.upper()
            return Match.Result[text]

        def to_score(self):
            if self is self.WHITE:
                return '1 - 0'
            elif self is self.BLACK:
                return '0 - 1'
            else:
                return '½-½'

    id = db.Column(db.Integer, primary_key=True)

    white_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    white = db.relationship('Person', foreign_keys=[white_id])
    rating_white = db.Column(db.Float)
    black_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    black = db.relationship('Person', foreign_keys=[black_id])
    rating_black = db.Column(db.Float)
    result = db.Column(db.Enum(Result))
    date = db.Column(db.DateTime, default=db.func.current_timestamp())



