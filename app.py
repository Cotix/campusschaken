from config import *
from controllers import *
from models import *
from util.filter import *
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sqlalchemy import text

import sys

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
