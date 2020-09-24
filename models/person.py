from sqlalchemy import or_

from config import db, login_manager
import bcrypt
from .match import Match


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    _password = db.Column(db.Text)
    _roles = db.Column(db.Text, default='')
    email = db.Column(db.Text)
    username = db.Column(db.Text)
    rating = db.Column(db.Float, default=1200)

    def set_password(self, password):
        self._password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14)).decode('utf-8')

    def check_password(self, password):
        hash = self._password
        return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))

    @property
    def matches(self):
        return Match.query.filter(or_(Match.black_id == self.id, Match.white_id == self.id))

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __str__(self):
        return f'{self.username}'

    def __repr__(self):
        return str(self)


@login_manager.user_loader
def load_user(user_id):
    return Person.query.get(user_id)
