from os import environ, path

from flask import Flask, logging
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore

from pyback.log_manager import setup_logging

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
security = Security()

setup_logging()
app = Flask(__name__)
logger = logging.create_logger(app)
logger.setLevel('DEBUG')

# Load the default configuration
app.config.from_object('config.default')

# Load the file specified by the FLASK_ENV environment variable
# Variables defined here will override those in the default configuration
app.config.from_object(f"config.{environ.get('FLASK_ENV', 'development')}")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = 'pbkdf2'
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_REGISTER_URL'] = '/signup'
app.secret_key = 'mega-secret'

db.init_app(app)
migrate.init_app(app, db)
bootstrap.init_app(app)

from .routes import slack_routes, web_view_routes, web_api_routes
from pyback.database import models, web_models

user_datastore = SQLAlchemyUserDatastore(db, web_models.WebUser, web_models.Role)
security.init_app(app, user_datastore)

# # Create a user to test with
# from flask_security.utils import hash_password
# @app.before_first_request
# def create_user():
#     db.create_all()
#     user_datastore.create_user(email='Will', password=hash_password('loserface'))
#     db.session.commit()
