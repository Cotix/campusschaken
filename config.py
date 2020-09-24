import os

from flask_login import LoginManager
from werkzeug.routing import BaseConverter
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__, template_folder='views')
app.debug = os.getenv('APP_DEBUG').lower() == 'true'
app.secret_key = os.getenv('APP_SECRET')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')

db = SQLAlchemy(app)
login_manager = LoginManager(app=app)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter
