from models import Match, Person
from config import db

class MatchService:
    K = 32

    def __init__(self, white: Person, black: Person):
        self.white = white
        self.black = black

    def finish_match(self, match_result: Match.Result):
        match = Match(white=self.white, black=self.black, result=match_result,
                      rating_black=self.black.rating, rating_white=self.white.rating)
        db.session.add(match)
        Ew, Eb = self.expected_value()

        if match_result == Match.Result.WHITE:
            Sw, Sb = 1, 0
        elif match_result == Match.Result.BLACK:
            Sw, Sb = 0, 1
        else:
            Sw, Sb = 0.5, 0.5

        self.white.rating += self.K * (Sw - Ew)
        self.black.rating += self.K * (Sb - Eb)

        db.session.commit()
        return match

    def expected_value(self):
        Rw, Rb = self.white.rating, self.black.rating
        Ew = 1.0/(1 + 10**((Rb-Rw)/400))
        return Ew, 1-Ew