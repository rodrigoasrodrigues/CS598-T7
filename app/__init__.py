from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app.models import tables
from app.controllers import default
from app.controllers import add_dataset
from app.controllers import explore
from app.controllers import error_handler


app.register_error_handler(404, error_handler.page_not_found)
app.register_error_handler(500, error_handler.internal_error)
