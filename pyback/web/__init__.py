from flask import Blueprint

bp = Blueprint('web', __name__)

from pyback.web import routes_web, routes_api
