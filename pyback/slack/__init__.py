from flask import Blueprint

bp = Blueprint('slack', __name__)

from pyback.slack import routes, handler_router


