from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_admin import Admin
from decouple import config
from flask import Flask

from lib.flask_airtable_client import AirtableClient
from lib.flask_slack_client import SlackClient
from pyback.logging import setup_logging

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
# sentry = Sentry(app)
security = Security()
admin = Admin(name='Pyback', template_mode='bootstrap3')
slack_client = SlackClient()
airtable_client = AirtableClient()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config.default')

    if test_config is None:
        load_dotenv()
        app.config.from_object(f"config.{config('FLASK_ENV', default='development')}")
    else:
        app.config.update(test_config)

    logger = app.logger
    logger.setLevel(10)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    channels = {
        'community': app.config['COMMUNITY_CHANNEL'],
        'mentors': app.config['MENTORS_INTERNAL_CHANNEL']
    }
    other_keys = {'app_token': app.config['APP_TOKEN']}

    slack_client.init_app(app, app.config['TOKEN'], channels, other_keys)
    airtable_client.init_app(app, app.config['AIRTABLE_BASE_KEY'], app.config['AIRTABLE_API_KEY'])

    from pyback.errors import bp as errors_bp
    from pyback.slack import bp as slack_bp
    from pyback.web import bp as web_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(slack_bp)
    app.register_blueprint(web_bp)

    from pyback.database import models

    user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
    security.init_app(app, user_datastore)
    admin.init_app(app)

    from pyback.database import model_views

    return app
