from flask_login import current_user, login_required
from werkzeug.utils import redirect

from config import *
from services.match import MatchService
from util import html
from models import Person, Match


def _render_matches(matches, endpoint, args={}):
    page = int(request.values.get('page', 1))
    pagination = matches.paginate(page, per_page=25)
    data = {
        'matches': pagination.items,
        'pages': pagination,
        'endpoint': endpoint,
        'args': args
    }
    return html.ok('matches', data)


@app.route('/matches/', methods=['GET', 'POST'])
def matches():
    return _render_matches(Match.query.order_by(Match.date.desc()), 'matches')


@app.route('/matches/<player_id>', methods=['GET', 'POST'])
def matches_player(player_id):
    player = Person.query.get(int(player_id))
    return _render_matches(player.matches.order_by(Match.date.desc()), 'matches_player', args={'player_id': player_id})


@app.route('/matches/add', methods=['GET', 'POST'])
@login_required
def matches_add():
    if request.method == 'GET':
        players = Person.query.filter(Person.id != current_user.id).all()
        return html.ok('add_match', {'players': players})

    opponent_id = request.values.get('opponent')
    player_color = request.values.get('color')
    winner_color = request.values.get('winner')

    if opponent_id is None or player_color is None or winner_color is None:
        players = Person.query.filter(Person.id != current_user.id).all()
        return html.ok('add_match', {'players': players})

    opponent = Person.query.get(int(opponent_id))
    if player_color == 'white':
        white, black = current_user, opponent
    else:
        white, black = opponent, current_user

    match_service = MatchService(white, black)
    match_service.finish_match(Match.Result.from_string(winner_color))
    return redirect('/')