from os import path

from flask import jsonify, send_file
from flask_login import login_required

from pyback.web import bp
from pyback.web.log_handlers import get_logs_dict
from pyback.web.bot_message_handlers import get_messages, delete


@bp.route('/api/logs')
@login_required
def api_logs():
    logs = get_logs_dict()
    data = jsonify({'data': logs})
    return data


@bp.route('/api/botMessages')
@login_required
def api_messages():
    messages = get_messages()
    return jsonify({'data': messages})


@bp.route('/api/delete/<ts>/<channel>')
@login_required
def delete_message(ts: str, channel: str):
    response = delete(ts, channel)
    return jsonify(response)


@bp.route('/favicon.ico')
def send_favicon():
    """
    Gets rid of an annoying error where flask-admin keeps trying to get the favicon
    """
    favicon = path.join('static', 'img', 'favicon.ico')
    return send_file(favicon)
