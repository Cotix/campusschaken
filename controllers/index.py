from config import *
from util import html
from models import Person

@app.route('/', methods=['GET'])
def index():
    players = Person.query.order_by(Person.rating.desc()).all()
    return html.ok('index', {'players': players})