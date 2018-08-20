from os import path

from flask import jsonify, send_file

from pyback.web import bp
from pyback.web.handlers import get_messages, delete, get_logs_dict


@bp.route('/api/logs')
def api_logs():
    logs = get_logs_dict()
    data = jsonify({'data': logs})
    return data


@bp.route('/api/botMessages')
def api_messages():
    messages = get_messages()
    return jsonify({'data': messages})


@bp.route('/api/delete/<ts>/<channel>')
def delete_message(ts, channel):
    response = delete(ts, channel)
    return jsonify(response)



@bp.route('/favicon.ico')
def send_favicon():
    """
    Gets rid of an annoying error where flask-admin keeps trying to get the favicon
    """
    favicon = path.join('static', 'img', 'favicon.ico')
    return send_file(favicon)
