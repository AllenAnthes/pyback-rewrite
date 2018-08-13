import logging
from os import environ, path

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore

from pyback.log_manager import setup_logging

app = Flask(__name__, template_folder="../templates", static_folder="../static")
setup_logging(logging.DEBUG)
logger = logging.getLogger()

# Load the default configuration
app.config.from_object('config.default')

# Load the file specified by the FLASK_ENV environment variable
# Variables defined here will override those in the default configuration
logger.debug(app.config)
try:
    if 'FLASK_ENV' in environ:
        app.config.from_object(f"config.{environ['FLASK_ENV']}")
    else:
        app.config.from_object(f"config.development")
except Exception as ex:
    logger.exception(ex)

logger.debug(app.config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = 'pbkdf2'
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_REGISTER_URL'] = '/signup'
app.secret_key = 'mega-secret'

UPLOAD_FOLDER = path.join('static', 'imageStore')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap(app)

from .routes import slack_routes, web_routes
from pyback.database import models, web_models

user_datastore = SQLAlchemyUserDatastore(db, web_models.WebUser, web_models.Role)
security = Security(app, user_datastore)

# # Create a user to test with
# from flask_security.utils import hash_password
# @app.before_first_request
# def create_user():
#     db.create_all()
#     user_datastore.create_user(email='abanthes@gmail.com', password=hash_password('fastpass'))
#     db.session.commit()
