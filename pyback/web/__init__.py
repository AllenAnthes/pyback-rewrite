from flask import Blueprint

bp = Blueprint('web', __name__)

from pyback.web import web_routes, api_routes
