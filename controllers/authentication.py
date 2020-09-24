from flask_login import login_user
from sqlalchemy import or_
from werkzeug.utils import redirect

from config import app, request, login_manager, db
from models.person import Person
from util import html


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return html.ok('login', {})

    username = request.values.get('username', '')
    password = request.values.get('password', '')

    user = Person.query.filter(Person.username == username).first()
    if user and user.check_password(password):
        login_user(user, remember=True)
        return redirect(request.values.get('next', '/'))

    return html.ok('login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return html.ok('register', {})

    email = request.values.get('email', '')
    username = request.values.get('username', '')
    password = request.values.get('password', '')
    first_name = request.values.get('first_name', '')
    last_name = request.values.get('last_name', '')

    user = Person.query.filter(or_(Person.username == username, Person.email == email)).first()

    if user:
        return html.ok('register', {'error': 'Gebruiker bestaat al!'})

    person = Person(username=username, email=email, first_name=first_name, last_name=last_name)
    person.set_password(password)
    db.session.add(person)
    db.session.commit()

    login_user(person, remember=True)

    return redirect(request.values.get('next', '/'))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)
